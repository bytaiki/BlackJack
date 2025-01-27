from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, GameResult
from .forms import BetForm
from .logic import Card, Game
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    users = CustomUser.objects.all().order_by('-chip')[:3]
    all_users = CustomUser.objects.all().order_by('-chip')
    #リクエストしたユーザーの、インデックス番号で順位を取る
    rank = 0
    for user in all_users:
        rank += 1
        if request.user.id == user.id:
            break

    return render(request, 'bj/home.html', {'users': users,'rank':rank})

@login_required
def lobby(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    game_results = GameResult.objects.filter(user=user).order_by('-played_date')[:5]
    for game_result in game_results:
        game_result.p_hand_img = game_result.p_hand_img.split(',')
        game_result.d_hand_img = game_result.d_hand_img.split(',')
    if request.method == 'POST':
        form = BetForm(request.POST, user=user)
        if form.is_valid():
            bet = form.cleaned_data['bet']
            game = Game()
            game.user = user.id
            game.bet = bet
            game.player_hand = [game.draw() for _ in range(2)]
            game.dealer_hand = [game.draw() for _ in range(2)]
            request.session['game_data'] = game.to_dict()
            user.chip -= bet
            user.save()
            return redirect('bj:start_game', user_id=user.id)
    else:
        form = BetForm(user=user)
    return render(request, 'bj/lobby.html', {'user': user, 'form': form, 'game_results': game_results})

@login_required
def start_game(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
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

    game_results = GameResult.objects.filter(user=user).order_by('-played_date')[:5]
    for game_result in game_results:
        game_result.p_hand_img = game_result.p_hand_img.split(',')
        game_result.d_hand_img = game_result.d_hand_img.split(',')

    context = {
        'player_hand': game.player_hand,
        'dealer_handOne': game.dealer_hand[0].split(),
        'player_hand_img': player_hand_img,
        'player_hand_img_list': player_hand_img,
        'dealer_hand_img': dealer_hand_img,
        'cards': game.cards,
        'bet': game.bet,
        'player_sum': game.player_sum,
        'dealer_sum': game.dealer_sum,
        'user': user,
        'game_results': game_results,
    }
    return render(request, 'bj/start_game.html', context)

@login_required
def hit(request):
    game_data = request.session.get('game_data')
    game = Game.from_dict(game_data)
    game.player_hand.append(game.draw())
    game.player_sum = game.hand_sum(game.player_hand)
    request.session['game_data'] = game.to_dict()

    if game.bust_check(game.player_sum):
        return redirect('bj:result', user_id=game.user)

    return redirect('bj:start_game', user_id=game.user)

@login_required
def result(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    game_data = request.session.get('game_data')
    game = Game.from_dict(game_data)
    game.player_sum = game.hand_sum(game.player_hand)
    game.dealer_sum = game.hand_sum(game.dealer_hand)
    while game.dealer_sum < 17:
        game.dealer_hand.append(game.draw())
        game.dealer_sum = game.hand_sum(game.dealer_hand)

    player_hand_img = [Card.card_img(card) for card in game.player_hand]
    dealer_hand_img = [Card.card_img(card) for card in game.dealer_hand]

    result = game.judge(user)

    GameResult.objects.create(
        user=user,
        result=result,
        bet_result=game.isBet,
        p_hand_sum=game.player_sum,
        d_hand_sum=game.dealer_sum,
        p_hand_img=",".join(player_hand_img),
        d_hand_img=",".join(dealer_hand_img)
    )

    context = {
        'user': user,
        'result': result,
        'player_hand': game.player_hand,
        'dealer_hand': game.dealer_hand,
        'player_hand_img': player_hand_img,
        'dealer_hand_img': dealer_hand_img,
        'dealer_sum': game.dealer_sum,
        'player_sum': game.player_sum,
        'bet': int(game.bet),
        'getChip': game.isBet,
        'player_sum': game.player_sum,
        'dealer_sum': game.dealer_sum,
    }
    return render(request, 'bj/result.html', context)
