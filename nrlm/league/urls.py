from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from nrlm.league import views

schema_view = get_schema_view(title='NRLM Schema')

router = DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'identities', views.IdentityViewSet)
router.register(r'games', views.GameViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
]
