from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path,include
from . import views

router = routers.DefaultRouter()

router.register('bank',views.TransactionBankToWaletViewSet , basename='transactionbanktowalet')
router.register('walet',views.TransactionWaletToWaletViewSet , basename='transactionwalettowalet')


schema_view = get_schema_view(
    openapi.Info(
        title="Transaction API",
        default_version="v1",
        description="API documentation for bank and wallet transactions",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]