from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render(request, "atbatvis/index.html")

def test(request):
    player = Player.objects.get(id='mauej001')

    plays = player.play.select_related("game").all()
    # for play in plays:
    #     games.get(play.game, []).append(play)
    # print(games)
    context = {"player": player, "plays": plays}
    return render(request, "atbatvis/test.html", context)