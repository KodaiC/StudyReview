from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r"ratings", RatingViewSet)
router.register(r"tags", TagViewSet)
router.register(r"users", UserViewSet)
