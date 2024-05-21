import numpy as np
from django.http import JsonResponse
from rest_framework import permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Team, Game, Player, Coach
from .serializers import GameSerializer, TeamSerializer, TeamDetailSerializer, PlayerDetailsSerializer


class ScoreboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        games = Game.objects.all().order_by('round')
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)


class TeamListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TeamDetailView(generics.RetrieveAPIView):
    # queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs.get('pk')
        try:
            user = self.request.user
            if user.is_superuser:
                return Team.objects.filter(id=team_id)
            coach = Coach.objects.get(user=user)

            team = Team.objects.get(coach=coach)
            if team.id == team_id:
                return Team.objects.filter(id=team_id)
            raise PermissionDenied("You do not have permission to view this team's details.")
        except:
            raise PermissionDenied("You do not have permission to view this team's details.")


class PlayerDetailView(RetrieveAPIView):
    serializer_class = PlayerDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        try:
            player_id = self.kwargs.get('pk')
            user = self.request.user
            if user.is_superuser:
                return Player.objects.filter(id=player_id)
            coach = Coach.objects.get(user=self.request.user)

            team = Team.objects.get(coach=coach)

            player = Player.objects.get(id=player_id)
            if team.id != player.team_id:
                raise PermissionDenied("You do not have permission to view this team's players.")

            return Player.objects.filter(id=player_id)

        except:
            raise PermissionDenied("You do not have permission to view this team's players.")


class TopPlayersView(generics.ListAPIView):
    serializer_class = PlayerDetailsSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            players = Player.objects.all()
        else:
            coach = Coach.objects.get(user=self.request.user)
            team = Team.objects.get(coach=coach)
            players = Player.objects.filter(team=team)

        # Calculate the average score dynamically and store in a list
        players_with_avg = [(player, player.get_average_score()) for player in players]

        # Calculate the 90th percentile score for the players
        average_scores = [avg for _, avg in players_with_avg]
        if not average_scores:
            return Player.objects.none()

        percentile_90 = np.percentile(average_scores, 90)
        self.percentile_90 = percentile_90  # Store percentile_90 in the instance variable

        # Filter players whose average score is in the 90th percentile
        top_players = [player for player, avg in players_with_avg if avg >= percentile_90]

        return top_players

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"players": serializer.data, "99P": self.percentile_90}, safe=False)
