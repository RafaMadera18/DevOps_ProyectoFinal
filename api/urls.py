# urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from api import views
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r'vehiculos', views.VehiculoViewSet, basename='vehiculos')
router.register(r'choferes', views.ChoferViewSet, basename='choferes')
router.register(r'asignaciones', views.AsignacionViewSet, basename='asignaciones')
router.register(r'rutas', views.RutaViewSet, basename='rutas')
router.register(r'administradores', views.AdministradorViewSet, basename='administradores')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.RegisterAdminView.as_view(), name='register'),
    path('auth/login/', views.AdminTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)