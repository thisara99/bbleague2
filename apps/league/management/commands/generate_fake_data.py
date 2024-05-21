from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth.models import User
from apps.league.models import Team, Coach, Player, Game, PlayerScore
from itertools import combinations

class Command(BaseCommand):
    help = 'Generate fake data for the league application'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create users
        users = []
        for _ in range(176):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password='password123'
            )
            users.append(user)

        # Create coaches
        coaches = []
        for i in range(16):
            coach = Coach.objects.create(user=users[i])
            coaches.append(coach)

        # Create teams and assign coaches
        teams = []
        for i in range(16):
            team = Team.objects.create(name=faker.company(), coach=coaches[i])
            teams.append(team)

        # Assign players to teams
        player_users = users[16:]
        for i in range(16):
            team_players = player_users[i*10:(i+1)*10]
            for player_user in team_players:
                Player.objects.create(
                    user=player_user,
                    team=teams[i],
                    height=random.randint(160, 210),
                    #average_score=random.uniform(5, 25)
                )

        # Create games for Round of 16 (120 games)
        round_16_games = list(combinations(teams, 2))
        for team1, team2 in round_16_games:
            game = Game.objects.create(
                team1=team1,
                team2=team2,
                round=16
            )

            # Select 5 random players from each team
            team1_players = random.sample(list(Player.objects.filter(team=team1)), 5)
            team2_players = random.sample(list(Player.objects.filter(team=team2)), 5)

            # Assign random scores to players
            for player in team1_players:
                score = random.randint(0, 50)
                PlayerScore.objects.create(game=game, player=player, score=score)

            for player in team2_players:
                score = random.randint(0, 50)
                PlayerScore.objects.create(game=game, player=player, score=score)

        self.stdout.write(self.style.SUCCESS('Successfully generated all fake data'))
