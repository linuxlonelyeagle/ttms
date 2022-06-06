import datetime
import time
from urllib.request import Request

from django.shortcuts import render, redirect
from movie.models import *


def film_management(request):
    if request.method == 'GET':
        classify = Classify.objects.values('name')
        films = Films.objects.values('id', 'name', 'classify', 'discription', 'classify', 'movie_runtime',
                                     'onlien_time', 'value', 'actor', 'director')
        context = {'classify': classify, 'films': films}
        return render(request, 'controller/home.html', context=context)
    elif request.method == 'POST':
        ID = request.POST.getlist('id')[0]
        film = Films.objects.get(id=ID)
        film.delete()
        return redirect('/movie/film_management')


def film_create(request):
    if request.method == 'GET':
        classify = Classify.objects.values('name')
        context = {'classify': classify}
        return render(request, 'controller/film_create.html', context=context)
    elif request.method == 'POST':
        image = request.FILES.get('photo')
        film_name = request.POST.get('电影名')
        actor = request.POST.get('演员')
        movie_runtime = request.POST.get('时长')
        onlien_time = request.POST.get('上映时间')
        classify = request.POST.getlist('分类')
        director = request.POST.get('导演')
        discription = request.POST.get('描述')
        value = request.POST.get('价格')
        str_sum = ''
        print(type(image))
        for i in classify:
            str_sum += i
        Films.objects.create(name=film_name, actor=actor, director=director, discription=discription,
                             movie_runtime=movie_runtime, onlien_time=onlien_time, classify=str_sum,
                             value=value, image=image)
        return redirect('/movie/film_management')


def studio_management(request):
    if request.method == 'GET':
        studios = Studio.objects.values('width', 'length', 'id', 'name', 'num')
        context = {'studios': studios}
        return render(request, 'controller/studio.html', context=context)


def studio_create(request):
    if request.method == 'GET':
        return render(request, 'controller/studio_create.html')
    elif request.method == 'POST':
        length = request.POST.get('长度')
        width = request.POST.get('宽度')
        name = request.POST.get('名称')
        num = int(width) * int(length)
        Studio.objects.create(name=name, length=length, width=width, num=num)
        return redirect('/movie/studio_management')


def studio_fix(request):
    if request.method == 'GET':
        ID = request.GET.get('id')
        studio = Studio.objects.values('id', 'length', 'width', 'name', 'seats').get(id=ID)
        seats_str = studio['seats'].split(sep='/')
        for i in range(len(seats_str) - 1):
            temp = seats_str[i].split(sep=',')
            seats_str[i] = (int(temp[0]), int(temp[1]))
        length = range(1, studio['length'] + 1)
        width = range(1, studio['width'] + 1)
        context = {'id': studio['id'], 'length': length, 'width': width, 'name': studio['name'], 'seats': seats_str}
        return render(request, 'controller/studio_fix.html', context=context)
    elif request.method == 'POST':
        seats = request.POST.getlist('seat')
        ID = request.POST.get('id')
        seats_str = ''
        # 将无法选择的座位以 x,y/x,y/x,y的形式存成字符串
        for i in seats:
            seats_str += i + '/'
        studio = Studio.objects.get(id=ID)
        studio.num = studio.length * studio.width - len(seats)
        studio.seats = seats_str
        studio.save()
        return redirect('/movie/studio_management')


def controller_management(request):
    if request.method == 'GET':
        users = UserInfo.objects.values('id', 'username').filter(grade=1)
        context = {'users': users}
        return render(request, 'controller/controller.html', context=context)
    elif request.method == 'POST':
        ID = request.POST.getlist('id')[0]
        film = UserInfo.objects.get(id=ID)
        film.delete()
        return redirect('/movie/controller_management')


def controller_create(request):
    if request.method == 'GET':
        return render(request, 'controller/controller_create.html')
    elif request.method == 'POST':
        username = request.POST.get('用户名', '')
        password = request.POST.get('密码', '')
        UserInfo.objects.create_user(username=username, password=password, grade=1)
        return redirect('/movie/controller_management')


def session_management(request):
    if request.method == 'GET':
        session = Sessions.objects.all()
        context = {'session': session}
        return render(request, 'controller/session.html', context=context)
    if request.method == 'POST':
        ID = request.POST.get('id')
        session = Sessions.objects.get(id=ID)
        session.delete()
        return redirect('/movie/session_management')


def session_create(request):
    if request.method == 'GET':
        studios = Studio.objects.values('id', 'name')
        films = Films.objects.values('id', 'name')
        print(UserInfo.objects.values('date_joined')[0], type(UserInfo.objects.values('date_joined')[0]))
        t = time.localtime()
        context = {'studios': studios, 'films': films, 'year': range(t.tm_year, t.tm_year + 10), 'mon': range(1, 13),
                   'day': range(1, 32), 'hour': range(24), 'min': range(0, 60)}
        return render(request, 'controller/session_create.html', context=context)
    elif request.method == 'POST':
        studio = request.POST.get('演播厅')
        film = request.POST.get('电影')
        year = int(request.POST.get('年'))
        mon = int(request.POST.get('月'))
        day = int(request.POST.get('日'))
        hour = int(request.POST.get('时'))
        min = int(request.POST.get('分'))
        date = datetime.datetime(year, mon, day, hour, min)
        Sessions.objects.create(studio_id=studio, film_id=film, begin_time=date,
                                seats=Studio.objects.get(id=studio).seats)
        return redirect('/movie/session_management')


def order_management(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        context = {'orders': orders}
        return render(request, 'controller/order.html', context=context)
    elif request.method == 'POST':
        ID = request.POST.get('id')
        order = Order.objects.get(id=ID)
        order.delete()
        return redirect('/movie/user_order')
