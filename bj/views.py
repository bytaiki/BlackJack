from django.shortcuts import render,redirect,get_object_or_404
from .models import Room,GameResult
from .forms import BetForm
from .logic import Card,Game


def home(request):
    rooms = Room.objects.all()
    return render(request, 'bj/home.html', {'rooms' : rooms})

def create_room(request):
    room = Room.objects.create()
    return redirect('bj:lobby', room_id = room.id)

def lobby(request, room_id):
    room = Room.objects.get(id = room_id)
    game_results = GameResult.objects.filter(room=room).order_by('-played_date')[:5]
    for game_result in game_results:
        game_result.p_hand_img = game_result.p_hand_img.split(',')
        game_result.d_hand_img = game_result.d_hand_img.split(',')
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
    return render(request, 'bj/lobby.html', {'room' : room,'form' : form, 'game_results' : game_results})

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

    player_hand_img = [Card.card_img(card) for card in game.player_hand]
    dealer_hand_img = [Card.card_img(card) for card in game.dealer_hand]

    game_results = GameResult.objects.filter(room=room).order_by('-played_date')[:5]
    for game_result in game_results:
        game_result.p_hand_img = game_result.p_hand_img.split(',')
        game_result.d_hand_img = game_result.d_hand_img.split(',')

    
    context = {
        'player_hand' : game.player_hand,
        'dealer_handOne' : game.dealer_hand[0].split(),
        'player_hand_img' : player_hand_img,
        'player_hand_img_list' : player_hand_img,
        'dealer_hand_img' : dealer_hand_img,
        'cards' : game.cards,
        'bet' : game.bet,
        'player_sum' : game.player_sum,
        'dealer_sum' : game.dealer_sum,
        'room' : room,
        'game_results' : game_results,
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
        
    player_hand_img = [Card.card_img(card) for card in game.player_hand]
    dealer_hand_img = [Card.card_img(card) for card in game.dealer_hand]

    result = game.judge(room)

    GameResult.objects.create(
        room = room,
        result = result,
        bet_result = game.isBet,
        p_hand_sum = game.player_sum,
        d_hand_sum = game.dealer_sum,
        p_hand_img = ",".join(player_hand_img),
        d_hand_img = ",".join(dealer_hand_img)
    )

    context = {
        'room' : room,
        'result' : result,
        'player_hand' : game.player_hand,
        'dealer_hand' : game.dealer_hand,
        'player_hand_img' : player_hand_img,
        'dealer_hand_img' : dealer_hand_img,
        'dealer_sum' : game.dealer_sum,
        'player_sum' : game.player_sum,
        'bet' : int(game.bet),
        'getChip' : game.isBet,
        'player_sum' : game.player_sum,
        'dealer_sum' : game.dealer_sum,
            }
    return render(request, 'bj/result.html', context)

def room_delete(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    return redirect('bj:home')