from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny

from .views.usuarioView import UsuarioViewSet
from .views.restauranteView import RestauranteViewSet
from .views.categoriaView import CategoriaViewSet
from .views.direccionView import DireccionViewSet
from .views.platoView import PlatoViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Zeppelin API",
        default_version='v1',
        description="Zeppelin functionality description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'restaurante', RestauranteViewSet,
                basename='restaurante')
router.register(r'usuario', UsuarioViewSet,
                basename='usuario')
router.register(r'categoria', CategoriaViewSet,
                basename='categoria')
router.register(r'direccion', DireccionViewSet,
                basename='direccion')
router.register(r'plato', PlatoViewSet,
                basename='plato')

urlpatterns = [
    path('', include(router.urls)),

    path('swagger',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
