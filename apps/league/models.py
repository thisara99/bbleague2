from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=255)
    coach = models.OneToOneField('Coach', on_delete=models.CASCADE)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    height = models.IntegerField()

    def get_average_score(self):
        # Calculate average score for the player
        total_score = PlayerScore.objects.filter(player=self).aggregate(total_score=models.Sum('score'))['total_score']
        total_games = PlayerScore.objects.filter(player=self).count()
        if total_games > 0:
            return total_score / total_games
        return 0.0


class Game(models.Model):
    ROUND_CHOICES = [
        (16, 'Round of 16'),
        (8, 'Quarter-finals'),
        (4, 'Semi-finals'),
        (2, 'Finals'),
    ]

    team1 = models.ForeignKey(Team, related_name='team1_games', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_games', on_delete=models.CASCADE)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, related_name='won_games', on_delete=models.CASCADE, null=True, blank=True)
    round = models.IntegerField(choices=ROUND_CHOICES)
    players = models.ManyToManyField(Player, through='PlayerScore')

    def update_scores(self):
        team1_players = self.players.filter(team=self.team1)
        team2_players = self.players.filter(team=self.team2)
        self.team1_score = sum(ps.score for ps in PlayerScore.objects.filter(game=self, player__in=team1_players))
        self.team2_score = sum(ps.score for ps in PlayerScore.objects.filter(game=self, player__in=team2_players))
        if self.team1_score > self.team2_score:
            self.winner = self.team1
        elif self.team2_score > self.team1_score:
            self.winner = self.team2
        else:
            self.winner = None  # In case of a tie
        self.save()

class PlayerScore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.game.update_scores()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.game.update_scores()
