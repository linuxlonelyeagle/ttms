import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from user.models import UserInfo
from movie.models import *
from django.shortcuts import render, redirect


def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('用户名', '')
        password = request.POST.get('密码', '')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            request.session['id'] = user.id
            if user.grade == 1:
                return redirect('/movie/film_management')
            else:
                return redirect('/user/home')
        else:
            return render(request, 'user/login.html', context={'tip': '密码错误或用户名不存在'})


def user_register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('用户名', '')
        password = request.POST.get('密码', '')
        UserInfo.objects.create_user(username=username, password=password)
        return redirect('/user/login')


def home(request):
    if request.method == 'GET':
        ID = request.GET.get('id')
        if ID is None:
            classify = Classify.objects.values('name')
            films = Films.objects.all()
            return render(request, 'user/home.html', {'films': films, 'classify': classify})
        else:
            film = Films.objects.get(id=ID)
            session = Sessions.objects.filter(film_id=ID)
            if len(session) == 0:
                return render(request, 'user/film.html', {'film': film, 'tip': '暂无场次'})
            else:
                return render(request, 'user/film.html', {'film': film, 'tip': '欢迎选座'})


def buy(request):
    if request.method == 'GET':
        ID = request.GET.get('id')
        print(ID)
        session = Sessions.objects.get(id=ID)
        width = range(1, session.studio.width + 1)
        length = range(1, session.studio.length + 1)
        seats_str = session.seats.split(sep='/')
        for i in range(len(seats_str) - 1):
            temp = seats_str[i].split(sep=',')
            seats_str[i] = (int(temp[0]), int(temp[1]))
        return render(request, 'user/buy.html',
                      {'session': session, 'width': width, 'length': length, 'seats': seats_str})
    elif request.method == 'POST':
        user_id = request.session.get('id')
        print('user', user_id)
        ID = request.POST.get('id')
        session = Sessions.objects.get(id=ID)
        seats_str = session.seats
        seats_list = seats_str.split(sep='/')
        seats_buy = request.POST.getlist('seat')
        seats_buy_str = ''
        print(seats_list)
        for i in seats_buy:
            print(i)
            if i in seats_list:
                return HttpResponse('抱歉，该座位以售出')
            seats_buy_str += (i + '/')
        session.seats = seats_str + seats_buy_str
        session.save()
        value = len(seats_buy) * session.film.value
        Order.objects.create(seats=seats_buy_str, value=value)
        return HttpResponse('ok')


def choice_session(request):
    if request.method == 'GET':
        ID = request.GET.get('id')
        session = Sessions.objects.filter(film_id=ID)
        context = {'session': session}
        return render(request, 'user/session.html', context)
