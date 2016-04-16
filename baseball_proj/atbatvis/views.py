from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render(request, "atbatvis/index.html")

def test(request):
    player = Player.objects.get(id='mauej001')
    # print(player)
    # plays = player.play.all()
    # for play in plays:
    #     print(play)
    context = {"player": player}
    return render(request, "atbatvis/test.html", context)