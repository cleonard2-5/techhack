from django.shortcuts import render

# Create your views here.
def index(request, lobby_id):
    return render(request, 'lobby/index.html', {'lobby_id': lobby_id})

def game(request):
    return render(request, 'lobby/game.html')

def results(request):
    return render(request, 'lobby/results.html')
