from django.shortcuts import render,redirect,get_object_or_404
from .models import Room
from .forms import BetForm
from .logic import Game


def home(request):
    rooms = Room.objects.all()
    return render(request, 'bj/home.html', {'rooms' : rooms})

def create_room(request):
    room = Room.objects.create()
    return redirect('bj:lobby', room_id = room.id)

def lobby(request, room_id):
    room = Room.objects.get(id = room_id)
    if request.method == 'POST':
        form = BetForm(request.POST, room=room)
        if form.is_valid():
            bet = form.cleaned_data['bet']
            game = Game()
            game.room = room.id
            game.bet = bet
            game.player_hand = [game.draw() for _ in range(2)]
            game.dealer_hand = [game.draw() for _ in range(2)]
            request.session['game_data'] = game.to_dict()
            room.chip -= bet
            room.save()
            return redirect('bj:start_game',room_id = room.id)
            
    else:
        form = BetForm(room=room)
    return render(request, 'bj/lobby.html', {'room' : room,'form' : form})

def start_game(request, room_id):
    room = Room.objects.get(id=room_id)
    game_data = request.session.get('game_data')

    if game_data:
        game = Game.from_dict(game_data)
    else:
        game = Game()

    game.player_sum = game.hand_sum(game.player_hand)
    game.dealer_sum = game.hand_sum(game.dealer_hand)
    request.session['game_data'] = game.to_dict()

    context = {
        'player_hand' : game.player_hand,
        'dealer_hand' : game.dealer_hand,
        'cards' : game.cards,
        'bet' : game.bet,
        'player_sum' : game.player_sum,
        'dealer_sum' : game.dealer_sum,
        'room' : room
    }
    return render(request, 'bj/start_game.html', context)


def hit(request):
    game_data = request.session.get('game_data')
    game = Game.from_dict(game_data)
    game.player_hand.append(game.draw())
    game.player_sum = game.hand_sum(game.player_hand)
    request.session['game_data'] = game.to_dict()

    if game.bust_check(game.player_sum): #Trueがバーストしている状態
        return redirect('bj:result', room_id = game.room)
    else:
        context = {
            'player_hand' : game.player_hand,
            'dealer_hand' : game.dealer_hand,
            'cards' : game.cards,
            'bet' : game.bet,
            'player_sum' : game.player_sum,
            'dealer_sum' : game.dealer_sum,
        }
        return redirect('bj:start_game',room_id = game.room)

def result(request, room_id):
    room = Room.objects.get(id=room_id)
    game_data = request.session.get('game_data')
    game = Game.from_dict(game_data)
    game.player_sum = game.hand_sum(game.player_hand)
    game.dealer_sum = game.hand_sum(game.dealer_hand)
    while game.dealer_sum < 17:
        game.dealer_hand.append(game.draw())
        game.dealer_sum = game.hand_sum(game.dealer_hand)
        
    print(game.dealer_sum)
    result = game.judge(room)

    context = {
        'room' : room,
        'result' : result,
        'player_hand' : game.player_hand,
        'dealer_hand' : game.dealer_hand,
        'dealer_sum' : game.dealer_sum,
        'player_sum' : game.player_sum,
        'bet' : int(game.bet),
        'isChip' : int(game.isChip)
            }
    return render(request, 'bj/result.html', context)

def room_delete(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    return redirect('bj:home')