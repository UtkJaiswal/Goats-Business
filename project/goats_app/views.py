# goats_app/views.py
from rest_framework import generics
from .models import User, Goat, Load, Sales
from .serializers import UserSerializer, GoatSerializer, LoadSerializer, SalesSerializer
from rest_framework import generics, status
from rest_framework.response import Response

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GoatListCreateView(generics.ListCreateAPIView):
    queryset = Goat.objects.all()
    serializer_class = GoatSerializer

class LoadListCreateView(generics.ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

class SalesListCreateView(generics.ListCreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer


class SellerCreateGoatView(generics.CreateAPIView):
    queryset = Goat.objects.all()
    serializer_class = GoatSerializer

    def create(self, request, *args, **kwargs):
        goats_data = request.data.get('goats', [])

        # Add seller_id to each goat data
        for goat_data in goats_data:
            goat_data['seller_id'] = request.data.get('seller_id')

        # Create the Goat objects and associate them with the Load (if needed)
        goat_serializer = self.get_serializer(data=goats_data, many=True)
        goat_serializer.is_valid(raise_exception=True)
        goat_serializer.save()

        return Response(goat_serializer.data, status=status.HTTP_201_CREATED)

class AgentGoatListView(generics.ListAPIView):
    serializer_class = GoatSerializer

    def get_queryset(self):
        agent_id = self.kwargs['agent_id']
        # print("agent id ",agent_id)
        try:
            all_goats = Goat.objects.all()
            queryset = []
            for goat in all_goats:
                load = goat.load
                while load.master:
                    load = load.master
                goat.agent = load.agent
                # print("goat agent id", goat.agent.id)
                if goat.agent.id == agent_id:
                    queryset.append(goat)
            return queryset
        except User.DoesNotExist:
            return Goat.objects.none()


# goats_app/views.py



class SellerSellingToAgentView(generics.CreateAPIView):
    serializer_class = LoadSerializer

    def create(self, request, *args, **kwargs):
        seller_id = request.data.get('seller_id')
        agent_id = request.data.get('agent')
        paid_amount = request.data.get('paid_amount', 0)

        seller = User.objects.get(pk=seller_id)
        agent = User.objects.get(pk=agent_id)

        # Create the Load object and set the agent field
        load_data = {
            'seller_id': seller_id,
            'agent': agent_id,  # Set the agent explicitly
            'paid_amount': paid_amount,
            'due_amount': paid_amount,
        }
        load_serializer = self.get_serializer(data=load_data)
        load_serializer.is_valid(raise_exception=True)
        load = load_serializer.save()

        # Update the load of all the goats belonging to the seller to the newly created load
        Goat.objects.filter(seller_id=seller_id).update(load=load)

        return Response(load_serializer.data, status=status.HTTP_201_CREATED)


class AgentMergeSplitView(generics.UpdateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        merge_data = request.data.get('merge', [])
        split_data = request.data.get('split', [])

        if merge_data:
            # Perform Merge
            to_agent_id = merge_data['to_agent_id']
            from_agent_ids = merge_data['from_agent_ids']

            to_agent = User.objects.get(pk=to_agent_id)
            from_agents = Load.objects.filter(agent__id__in=from_agent_ids)

            # Create a new load with the to_agent as the agent
            new_load = Load.objects.create(
                agent=to_agent,
                paid_amount=0,  # Set paid_amount to 0 for the new load
                due_amount=0,   # Set due_amount to 0 for the new load
            )

            # Get all goats from the original loads and associate them with the new load
            goats = Goat.objects.filter(load__in=[instance, *from_agents])
            goats.update(load=new_load)

            # Update the master field of the original loads to point to the new load
            Load.objects.filter(id__in=[instance.id, *from_agent_ids]).update(master=new_load)

        if split_data:
            # Perform Split
            from_agent_id = split_data['from_agent_id']
            to_agent_ids = split_data['to_agent_ids']

            from_agent = User.objects.get(pk=from_agent_id)
            to_agents = User.objects.filter(id__in=to_agent_ids)

            total_goats = Goat.objects.filter(load=instance, seller_id=from_agent_id).count()
            num_to_agents = to_agents.count()

            # Calculate the number of goats to be distributed to each target agent
            goats_per_agent, remainder = divmod(total_goats, num_to_agents)

            # Create new loads for each target agent and associate the goats
            new_loads = []
            for to_agent in to_agents:
                new_load = Load.objects.create(
                    agent=to_agent,
                    paid_amount=0,  # Set paid_amount to 0 for the new load
                    due_amount=0,   # Set due_amount to 0 for the new load
                )
                new_loads.append(new_load)

            # Associate the goats to the new loads
            goats = Goat.objects.filter(load=instance)
            for i, goat in enumerate(goats):
                new_load = new_loads[i % num_to_agents]
                goat.load = new_load
                goat.save()

            # Update the master field of the original load to point to one of the new loads
            Load.objects.filter(id=instance.id).update(master=new_loads[0].id)

        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)

    

class AgentSellingToBuyerView(generics.CreateAPIView):
    serializer_class = SalesSerializer

    def create(self, request, *args, **kwargs):
        agent_id = request.data.get('agent_id')
        goat_ids = request.data.get('goat_ids', [])
        buyer_id = request.data.get('buyer_id')
        amount_paid = request.data.get('amount_paid')

        agent = User.objects.get(pk=agent_id)
        buyer = User.objects.get(pk=buyer_id)

        # Check if all the goats belong to the agent
        agent_goats = Goat.objects.filter(load__agent=agent, id__in=goat_ids)
        if agent_goats.count() != len(goat_ids):
            return Response({"detail": "Some goats do not belong to the agent."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Sales instance
        sales_data = {
            'agent': agent_id,
            'buyer': buyer_id,
            'amount_paid': amount_paid,
        }
        sales_serializer = self.get_serializer(data=sales_data)
        sales_serializer.is_valid(raise_exception=True)
        sales = sales_serializer.save()

        # Update the sales_id and buyer_id for the selected goats
        Goat.objects.filter(id__in=goat_ids).update(sales=sales, buyer_id=buyer_id)

        return Response(sales_serializer.data, status=status.HTTP_201_CREATED)


class BuyerGoatListView(generics.ListAPIView):
    serializer_class = GoatSerializer

    def get_queryset(self):
        buyer_id = self.kwargs['buyer_id']
        try:
            return Goat.objects.filter(buyer_id=buyer_id)
        except Goat.DoesNotExist:
            return Goat.objects.none()
