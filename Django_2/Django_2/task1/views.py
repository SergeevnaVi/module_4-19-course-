from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegister
from .models import Buyer, Game


def platform(request):
    title = 'Игровая платформа'
    text = 'Главная страница'

    context = {
        'title': title,
        'text': text,
    }
    return render(request, 'platform.html', context)

def shop(request):
    title = 'Игровая платформа'
    text = 'Игры'
    products = Game.objects.all()
    text4 = 'Купить 💳'
    text5 = '🔙 Вернуться обратно'
    text6 = 'Добавить в корзину ✅'

    context = {
        'title': title,
        'text': text,
        'products': products,
        'text4': text4,
        'text5': text5,
        'text6': text6
    }
    return render(request, 'shop.html', context)

def cart(request):
    title = 'Игровая платформа'
    text = 'Корзина'
    products = Game.objects.all()
    text4 = 'Купить 💳'
    text5 = '🔙 Вернуться обратно'
    text6 = 'Удалить 🗑'
    text7 = 'Сделать заказ!'

    context = {
        'title': title,
        'text': text,
        'products': products,
        'text4': text4,
        'text5': text5,
        'text6': text6,
        'text7': text7
    }
    return render(request, 'cart.html', context)


def sign_up_by_django(request):
    info = {}

    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            repeat_password = request.POST.get('repeat_password')
            age = int(request.POST.get('age', 0))

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
            elif Buyer.objects.filter(name=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                Buyer.objects.create(name=username, age=age, balance=0)
                return HttpResponse(f'Приветствуем, {username}!')
        else:
            info['error'] = 'Некорректные данные'

        context = {
            'form': form,
            'info': info
        }
        return render(request, 'registration_page.html', context)

    else:
        form = UserRegister()
        context = {
            'form': form,
            'info': info
        }
        return render(request, 'registration_page.html', context)


def sign_up_by_html(request):
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age', 0))

        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif age < 18:
            info['error']  = 'Вы должны быть старше 18'
        elif Buyer.objects.filter(name=username).exists():
            info['error'] = 'Пользователь уже существует'
        else:
            Buyer.objects.create(name=username, age=age, balance=0)
            return HttpResponse(f'Приветствуем, {username}!')

    context = {
        'info': info
    }
    return render(request, 'registration_page.html', context)

