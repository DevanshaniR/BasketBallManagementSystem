from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Role(models.Model):
    COACH = 'C'
    PLAYER = 'P'
    ADMIN = 'A'

    ROLE_TYPES = [
        (COACH, 'Coach'),
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]
    type = models.CharField(
        max_length=2,
        choices=ROLE_TYPES,
        default=PLAYER,
        verbose_name='type of role'
    )

    class Meta:
        db_table = 'role'

    def __str__(self):
        return str(self.type)


class UserRole(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'user_role'


class UserLoginDetails(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    login_time = models.DateTimeField(verbose_name='login date time', default=timezone.now)
    logout_time = models.DateTimeField(verbose_name='logout date time')

    def __str__(self):
        return str(self.login_time)

    class Meta:
        db_table = 'user_login_details'


class Team(models.Model):
    name = models.TextField(max_length=100)
    abbr = models.TextField(max_length=3)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'team'


class Game(models.Model):
    QF = 'QF'
    SF = 'SF'
    FI = 'FI'
    WI = 'WI'

    ROUNDS = [
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final'),
        (WI, 'Winner')
    ]

    host = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='host')
    guest = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='guest')
    host_score = models.IntegerField()
    guest_score = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
    date = models.DateField(verbose_name='game date', blank=True)
    round_number = models.CharField(
        max_length=2,
        choices=ROUNDS,
        default=QF,
        verbose_name='round type'
    )

    def __str__(self):
        return 'Game # %s' % self.id

    class Meta:
        db_table = 'game'


class TeamStat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    score = models.IntegerField()

    def __str__(self):
        return str(self.score)

    class Meta:
        db_table = 'TeamStat'


class Coach(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True)
    name = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return 'Name : %s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        db_table = 'coach'


class Player(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    height = models.IntegerField()
    name = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return 'Name : %s , Height : %s' % (self.user.first_name, self.height)

    class Meta:
        db_table = 'player'


class PlayerStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return str(self.score)

    class Meta:
        db_table = 'playerStat'
