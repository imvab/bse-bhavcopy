from rest_framework import routers
from main.viewsets import StockViewSet
router = routers.DefaultRouter()
router.register(r'stock', StockViewSet)
