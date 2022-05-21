from django.urls import path
from .views import ProjectListView, ProjectUpdateDeleteView, ProjectRetrieveView, ProjectCreateView

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('updatedelete/<int:pk>', ProjectUpdateDeleteView.as_view(), name='project_update_delete'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectRetrieveView.as_view(), name='project_retrieve'),
]
