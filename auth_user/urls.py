from django.urls import path
from .api import urlpatterns as api_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
    TokenObtainSlidingView, TokenRefreshSlidingView
)
from .views import (
    SingUpView, UserListView,
    UserDeleteView, UserBlockView,
    UserRetrieveUpdateView, SpecializationListCreateView,
    SpecializationDeleteView,

    BlacklistRefreshView
)

urlpatterns = [
    path('user/signup/', SingUpView.as_view(), name='sign_up'),
    path('user/userlist/', UserListView.as_view(), name='user_list'),
    path('user/userdelete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/userblock/', UserBlockView.as_view(), name='user_block'),
    path('user/userretrieveupdate/<int:pk>/', UserRetrieveUpdateView.as_view(), name='user_retrieve_update'),
    # path('api/logout/', BlacklistRefreshView.as_view(), name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('specialization/listcreate', SpecializationListCreateView.as_view(), name='specialization_list_create'),
    path('specialization/delete/<int:pk>/', SpecializationDeleteView.as_view(), name='specialization_delete'),
]

urlpatterns += api_urls
