# goats_app/urls.py
from django.urls import path
from .views import (
    UserListCreateView,
    SellerSellingToAgentView,
    AgentMergeSplitView,
    SellerCreateGoatView,
    AgentSellingToBuyerView,
    GoatListCreateView,
    LoadListCreateView,
    SalesListCreateView,
    AgentGoatListView,
    BuyerGoatListView,
    Login,
    Logoutview,
    GoatListForAgentView
)

urlpatterns = [ 
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('goats/', GoatListCreateView.as_view(), name='goat-list-create'),
    path('goatsforagent/', GoatListForAgentView.as_view(), name='goat-list-for-agent'),
    path('loads/', LoadListCreateView.as_view(), name='load-list-create'),
    path('sales/', SalesListCreateView.as_view(), name='sales-list-create'),
    path('seller-create-goat/', SellerCreateGoatView.as_view(), name='seller-create-goat'),
    path('seller-selling-to-agent/', SellerSellingToAgentView.as_view(), name='seller-selling-to-agent'),
    path('agent-merge-split/<int:pk>/', AgentMergeSplitView.as_view(), name='agent-merge-split'),
    path('agent-selling-to-buyer/', AgentSellingToBuyerView.as_view(), name='agent-selling-to-buyer'),
    path('goats/', GoatListCreateView.as_view(), name='goat-list-create'),
    path('loads/', LoadListCreateView.as_view(), name='load-list-create'),
    path('sales/', SalesListCreateView.as_view(), name='sales-list-create'),
    path('agent-goats/<int:agent_id>/', AgentGoatListView.as_view(), name='agent-goat-list'),
    path('buyer-goats/<int:buyer_id>/', BuyerGoatListView.as_view(), name='buyer-goats-list'),
    path('login/', Login.as_view(), name='user-login'),
    path('logout/', Logoutview.as_view(), name='user-logout'),
]
