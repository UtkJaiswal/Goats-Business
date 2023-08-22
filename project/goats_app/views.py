from rest_framework import generics
from .models import User, Goat, Load, Sales
from .serializers import UserSerializer, GoatSerializer, LoadSerializer, SalesSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .permissions import *
from knox.models import AuthToken


class UserListCreateView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        try:
            user = request.user
            if user:
                user_data = {
                    'email': user.email,
                    'name': user.name,
                    'type': user.type,
                }
                return Response(user_data)
        except AuthToken.DoesNotExist:
            pass
        return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GoatListCreateView(APIView):

    def get(self, request, format=None):
        # permission_classes = [IsAuthenticated]
        user = request.user
        if user.id and request.user.type == "Seller":
            goats = Goat.objects.all()
            serializer = GoatSerializer(goats, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def post(self, request, format=None):
        # permission_classes = [IsSellerUser]
        user = request.user
        if  user.id and request.user.type == "Seller":
            data = request.data.copy()
            data['seller_id'] = request.user.id  
            serializer = GoatSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GoatListForAgentView(APIView):

    def get(self, request, format=None):
        # permission_classes = [IsAgentUser]
        user = request.user
        if user.id and request.user.type == "Agent":
            goats = Goat.objects.all()
            serializer = GoatSerializer(goats, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    

class LoadListCreateView(APIView):
    
    # permission_classes = [IsAgentUser]
    
    def get(self, request, format=None):
        user = request.user
        if user.id and request.user.type == "Agent":
            loads = Load.objects.all()
            serializer = LoadSerializer(loads, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    
    def post(self, request, format=None):
        serializer = LoadSerializer(data=request.data)
        user = request.user
        if user.id and request.user.type == "Agent":
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class SalesListCreateView(APIView):
    
    # permission_classes = [IsAgentUser]
    
    def get(self, request, format=None):
        user = request.user
        if user.id and user.type == "Agent":
            sales_entries = Sales.objects.filter(agent=user.id)
            serializer = SalesSerializer(sales_entries, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        elif user.id and user.type == "Buyer":
            sales_entries = Sales.objects.filter(agent=user.id)
            serializer = SalesSerializer(sales_entries, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You do not have permission to access this data.'}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, format=None):
        user = request.user
        serializer = SalesSerializer(data=request.data)
        
        if user.id and user.type == "Agent":
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Unauthorized user"},status=status.HTTP_200_OK)
            


# class SellerCreateGoatView(generics.CreateAPIView):
#     queryset = Goat.objects.all()
#     serializer_class = GoatSerializer

#     def create(self, request, *args, **kwargs):
#         goats_data = request.data.get('goats', [])

#         # Add seller_id to each goat data
#         for goat_data in goats_data:
#             goat_data['seller_id'] = request.data.get('seller_id')

#         # Create the Goat objects and associate them with the Load (if needed)
#         goat_serializer = self.get_serializer(data=goats_data, many=True)
#         goat_serializer.is_valid(raise_exception=True)
#         goat_serializer.save()

#         return Response(goat_serializer.data, status=status.HTTP_201_CREATED)

# class AgentGoatListView(generics.ListAPIView):
#     serializer_class = GoatSerializer

#     def get_queryset(self):
#         agent_id = self.kwargs['agent_id']
#         # print("agent id ",agent_id)
#         try:
#             all_goats = Goat.objects.all()
#             queryset = []
#             for goat in all_goats:
#                 load = goat.load
#                 while load.master:
#                     load = load.master
#                 goat.agent = load.agent
#                 # print("goat agent id", goat.agent.id)
#                 if goat.agent.id == agent_id:
#                     queryset.append(goat)
#             return queryset
#         except User.DoesNotExist:
#             return Goat.objects.none()

class AgentGoatListView(APIView):
    
    serializer_class = GoatSerializer
    
    def get(self, request, format=None):
        try:
            user = request.user
            if user.id and user.type == "Agent":
                agent_id = user.id
                all_goats = Goat.objects.all()
                queryset = []
                for goat in all_goats:
                    load = goat.load
                    while load.master:
                        load = load.master
                    goat.agent = load.agent
                    if goat.agent.id == agent_id:
                        queryset.append(goat)
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"message:Unauthorized user"},status=status.HTTP_401_UNAUTHORIZED)
        except Goat.DoesNotExist:
            return Response({'detail': 'No goats found for the agent.'}, status=status.HTTP_404_NOT_FOUND)
        



class SellerSellingToAgentView(APIView):
    
    serializer_class = LoadSerializer
    
    def post(self, request, format=None):

        user = request.user
        if user.id and user.type == "Agent":

            seller_id = request.data.get('seller_id')
            agent_id = request.data.get('agent')
            paid_amount = request.data.get('paid_amount', 0)

            try:
                seller = User.objects.get(pk=seller_id)
                agent = User.objects.get(pk=agent_id)
                
                load_data = {
                    'seller_id': seller_id,
                    'agent': agent_id,
                    'paid_amount': paid_amount,
                    'due_amount': paid_amount,
                }
                load_serializer = self.serializer_class(data=load_data)
                load_serializer.is_valid(raise_exception=True)
                load = load_serializer.save()

                # Update the load of all the goats belonging to the seller to the newly created load
                Goat.objects.filter(seller_id=seller_id).update(load=load)

                return Response(load_serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'detail': 'Seller or agent not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message":"Unauthorized user"},status=status.HTTP_401_UNAUTHORIZED)


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

class Login(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)

        # print("gg",serializer.is_valid())
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}

        if serializer.is_valid():
            try:
                user_data = authenticate(email=serializer.validated_data['email'],
                                         password=serializer.validated_data['password'])

            except:
                # Response data
                result['status'] = 'NOK'
                result['valid'] = False
                result['result']['message'] = 'User not present'
                # Response data
                return Response(result, status=status.HTTP_204_NO_CONTENT)

            if user_data is not None:
                user_details = User.objects.all().filter(name=user_data).values('id', 'name', 'email','type')
                if user_data.is_active:
                    login(request, user_data)
                    data = super(Login, self).post(request)
                    data = data.data
                    # print(data)
                    # data['message'] = "Login successfully"
                    data['user_info'] = user_details

                # Response data
                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "Login successfully"
                result['result']['data'] = data
                # result['result']['data'] = data
                # Response data
                return Response(result, status=status.HTTP_200_OK)
            else:

                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Invalid Credentials'
                # Response data
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # Response data
        result['status'] = "NOK"
        result['valid'] = False
        result['result']['message'] = (
                    list(serializer.errors.keys())[0] + ' - ' + list(serializer.errors.values())[0][0]).capitalize()
        # Response data
        return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class Logoutview(LogoutView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        result = {}
        result['status'] = 'NOK'
        result['valid'] = False
        result['result'] = {"message": "Unauthorized access", "data": []}
        if request.user.is_authenticated:
            try:
                request._auth.delete()
            except:
                # Response data
                result['status'] = "NOK"
                result['valid'] = False
                result['result']['message'] = 'Error while logging out'
                # Response data
                return Response(result, status=status.HTTP_200_OK)
            # Response data
            result['status'] = "OK"
            result['valid'] = True
            result['result']['message'] = 'Logout successfully !'
            # Response data
            return Response(result, status=status.HTTP_200_OK)

