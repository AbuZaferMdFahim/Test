# urls.py
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import signup,login_view ,TeamCreateView,ProfileCreateAPIView,ProfileUpdateDeleteAPIView
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSet

router = DefaultRouter()
router.register(r'managers', ManagerViewSet, basename='manager')

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login_view'),
    path('profile/create/', ProfileCreateAPIView.as_view(), name='profile-create'),
    path('profile_update/', ProfileUpdateDeleteAPIView.as_view(), name='profile-update-delete'),
    path('teamCreate/', TeamCreateView.as_view(), name='team-create'),
    path('', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)