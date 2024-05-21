from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreboardView, TeamDetailView, TeamListView, PlayerDetailView, TopPlayersView

# router = DefaultRouter()
# router.register(r'teams', TeamViewSet)
# router.register(r'games', GameViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
    path('player/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    path('topplayers/', TopPlayersView.as_view(), name='top-players'),
]
