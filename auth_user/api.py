from rest_framework.routers import DefaultRouter

from .views import SkillsViewSet

routers = DefaultRouter()

routers.register(f'skills', SkillsViewSet, basename='skills')
# routers.register(f'category', CategoryViewset, basename='category')


urlpatterns = routers.urls
