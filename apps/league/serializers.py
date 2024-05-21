from django.db.models import Sum
from rest_framework import serializers

from .models import Team, Game, PlayerScore, Player, Coach


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class PlayerScoreSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.user.username')

    class Meta:
        model = PlayerScore
        fields = ['player', 'player_name', 'score']


class TeamPlayerScoresSerializer(serializers.ModelSerializer):
    player_scores = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['name', 'player_scores']

    def get_player_scores(self, team):
        game = self.context.get('game')
        player_scores = PlayerScore.objects.filter(game=game, player__team=team)
        return PlayerScoreSerializer(player_scores, many=True).data


class GameSerializer(serializers.ModelSerializer):
    team1_name = serializers.CharField(source='team1.name')
    team2_name = serializers.CharField(source='team2.name')
    team1_player_scores = serializers.SerializerMethodField()
    team2_player_scores = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id', 'team1', 'team1_name', 'team2', 'team2_name',
            'team1_score', 'team2_score', 'winner', 'round',
            'team1_player_scores', 'team2_player_scores'
        ]

    def get_team1_player_scores(self, game):
        serializer_context = {'game': game}
        return TeamPlayerScoresSerializer(game.team1, context=serializer_context).data['player_scores']

    def get_team2_player_scores(self, game):
        serializer_context = {'game': game}
        return TeamPlayerScoresSerializer(game.team2, context=serializer_context).data['player_scores']



class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')


    class Meta:
        model = Player
        fields = ['id', 'username']


class PlayerDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    total_scores = serializers.SerializerMethodField()
    total_games = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    team = TeamSerializer()

    class Meta:
        model = Player
        fields = ['id', 'username', 'total_scores', 'height', 'total_games', 'average_score', "team"]

    def get_total_scores(self, player):
        return PlayerScore.objects.filter(player=player).aggregate(total_score=Sum('score'))['total_score']

    def get_total_games(self, player):
        return PlayerScore.objects.filter(player=player).count()

    def get_average_score(self, player):
        total_scores = self.get_total_scores(player)
        total_games = self.get_total_games(player)
        if total_games > 0:
            return total_scores / total_games
        return 0

    def get_team(self, player):
        return player.team  # Return the entire team object

class CoachSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Coach
        fields = ['id', 'username']


class TeamDetailSerializer(serializers.ModelSerializer):
    coach = CoachSerializer()
    players = PlayerSerializer(source='player_set', many=True)
    average_team_score = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players','average_team_score']  # Add 'average_score' here

    def get_average_team_score(self, instance):
        team_id = instance.id
        total_score_team1 = Game.objects.filter(team1=team_id).aggregate(total_score=Sum('team1_score'))['total_score']
        total_score_team2 = Game.objects.filter(team2=team_id).aggregate(total_score=Sum('team2_score'))['total_score']

        # Check if total_score_team1 or total_score_team2 is None and handle accordingly
        total_score_team1 = total_score_team1 if total_score_team1 is not None else 0
        total_score_team2 = total_score_team2 if total_score_team2 is not None else 0

        total_score = total_score_team1 + total_score_team2

        total_games_team1 = Game.objects.filter(team1=team_id).count()
        total_games_team2 = Game.objects.filter(team2=team_id).count()
        total_games = total_games_team1 + total_games_team2

        if total_games > 0:
            return round(total_score / total_games, 2)
        return 0.0



