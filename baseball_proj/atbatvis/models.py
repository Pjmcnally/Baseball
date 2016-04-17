from django.db import models

# Create your models here.
class Player(models.Model):
    """ Model for player data """

    id = models.CharField(primary_key=True, max_length=20)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    debut = models.DateField(auto_now=False, auto_now_add=False)
    throws = models.CharField(max_length=1, blank=True)
    bats = models.CharField(max_length=1, blank=True)
    position = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return "{}, {}".format(
            self.l_name,
            self.f_name,
        )

    class Meta:
        ordering = ['l_name', 'f_name']


class Game(models.Model):
    """ Model for game data """

    id = models.CharField(primary_key=True, max_length=50)
    home_team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='home_team'
    )
    away_team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='away_team'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
        related_name='location',
        blank=True,
        null=True
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    players = models.ManyToManyField("player")

    def __str__(self):
        return "{a} @ {h} on {d}".format(
            a=self.away_team,
            h=self.home_team,
            d=self.date
        )

    class Meta:
        ordering = ['date', 'start_time']

class Location(models.Model):
    """ Model for location data """

    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    aka = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    start = models.DateField(auto_now=False, auto_now_add=False)
    end = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return "{}: {} in {}, {}".format(
            self.id,
            self.name,
            self.city,
            self.state
        )

    class Meta:
        ordering = ['id']

class Team(models.Model):
    """ Model for team data """ 

    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=7)
    
    def __str__(self):
        return "{}: {}".format(self.id, self.name)

    class Meta:
        ordering = ['id']

class Play(models.Model):
    """ Model for play data """

    inning = models.PositiveSmallIntegerField()
    bottom = models.BooleanField()
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        related_name='play'
    )
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        related_name='play'
    )
    count = models.CharField(max_length=5, blank=True)
    pitches = models.CharField(max_length=50, blank=True)
    play_full = models.CharField(max_length=100)
    play_short = models.CharField(max_length=5)

    def __str__(self):
        return "{f} {l}: {p} in the {b} of the {i}".format(
            f=self.player.f_name,
            l=self.player.l_name,
            p=self.play_short,
            b=((self.bottom and "bottom") or "top"),
            i=self.inning
        )

    class Meta:
        ordering = ['game', 'inning', "bottom"]
