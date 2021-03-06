from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from models import User, Travel, Join
import bcrypt
from datetime import date
import datetime

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('user'))

def index(request):
    travels = Travel.objects.filter(past = True)
    for x in travels:
        if x.end < datetime.date.today():
            x.past = False
            x.save()
    return render(request, 'travel/index.html')

def login(request):
    travels = False
    joins = False
    context = {'joins':joins, 'travels': travels}
    return render(request, 'travel/login.html', context)

def main(request):
    if 'user' in request.session:
        user = User.objects.get(id = request.session['user'])
        start = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).order_by('start')[:6]
        latest = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).order_by('-created_at')[:6]
        popular = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')[:6]
        travels = Travel.objects.filter(user_id = request.session['user'], past = True).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        user = User.objects.all()
        start = Travel.objects.filter(past = True).order_by('start')[:6]
        latest = Travel.objects.filter(past = True).order_by('start')[:6]
        popular = Travel.objects.filter(past = True).values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')[:6]
        travels = False
        joins = False

    context = {'start':start, 'latest':latest, 'popular':popular, 'user':user, 'joins':joins, 'travels': travels}
    return render(request, 'travel/main.html', context)

def display(request, search):
    if 'user' in request.session:
        user = User.objects.get(id = request.session['user'])
        if search == 'latest':
            display = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).order_by('-created_at')
        elif search == 'soon':
            display = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).order_by('start')
        elif search == 'popular':
            display = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')
        else:
            return redirect(reverse('main'))
        travels = Travel.objects.filter(user_id = request.session['user'], past = True).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        user = User.objects.all()
        if search == 'latest':
            display = Travel.objects.filter(past = True).order_by('-created_at')
        elif search == 'soon':
            display = Travel.objects.filter(past = True).order_by('start')
        elif search == 'popular':
            display = Travel.objects.filter(past = True).values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')
        else:
            return redirect(reverse('main'))
        travels = False
        joins = False
    result = search
    context = {'display':display, 'result':result, 'user':user, 'joins':joins, 'travels': travels}
    return render(request, 'travel/display.html', context)

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', None)
        if request.GET.get('by', None) == 'username':
            result = Travel.objects.filter(user_id__username__contains = search_query)
            print result
        elif request.GET.get('by', None) == 'destination':
            result = Travel.objects.filter(destination__contains = search_query)
            print result
        elif request.GET.get('by', None) == 'plan':
            result = Travel.objects.filter(plan__contains = search_query)
            print result
        else:
            result = False
        context = {'result':result}
        return render(request, 'travel/search.html', context)
    return render(request, 'travel/main.html', context)

def user(request):
    if 'user' in request.session:
        user = User.objects.get(id = request.session['user'])
        travels = Travel.objects.filter(user_id = request.session['user'], past = True)
        past = Travel.objects.filter(user_id = request.session['user'], past = False)
        joins = Join.objects.filter(user_id = request.session['user'])
        other = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).exclude(past = False).order_by('start')
        context = {'travels':travels,'past':past, 'user':user, 'other':other, 'joins': joins}
        return render(request, 'travel/user.html', context)
    return redirect(reverse('main'))

def travel(request, travel_id):
    travel = Travel.objects.get(id = travel_id)
    joined = Join.objects.filter(travel_id = travel_id)
    if 'user' in request.session:
        travels = Travel.objects.filter(user_id = request.session['user'], past = True).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        travels = False
        joins = False
    context = {'travel':travel, 'joined':joined, 'travels':travels, 'joins':joins}
    return render(request, 'travel/travel.html', context)

def add(request):
    if request.method == 'GET':
        today = date.today()
        format_time = today.strftime('%Y-%m-%d')
        user = User.objects.get(id = request.session['user'])
        if 'user' in request.session:
            travels = Travel.objects.filter(user_id = request.session['user'], past = True).order_by('-start')[:2]
            joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
        else:
            travels = False
            joins = False
        context = {'user':user, 'time':format_time, 'travels': travels, 'joins': joins}
        return render(request, 'travel/add.html', context)

    elif request.method == 'POST':
        result = Travel.manager.validateAddTravel(request)
        if result[0] == False:
            errors = result[1]
            print_messages(request, errors)
            return redirect(reverse('add'))
        creator = User.objects.get(id = request.session['user'])
        if 'image' in request.FILES:
            # No idea what this is...
            # request.FILES['image'].name = creator.username + "_" + request.POST['destination'][:8]
            Travel.objects.create(travel_image = request.FILES['image'], user_id = creator, destination=request.POST['destination'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'])
        else:
            Travel.objects.create(user_id = creator, destination=request.POST['destination'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'])
        return redirect(reverse('user'))

def register_process(request):
    result = User.manager.validateReg(request)
    resultPass = User.manager.validateRegPass(request)
    if result[0] == False or resultPass[0] == False:
        errors = result[1]+resultPass[1]
        print_messages(request, errors)
        return redirect(reverse('login'))
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.manager.create(username=request.POST['username'], pw_hash=pw_hash)
    return log_user_in(request, user)

def login_process(request):
    result = User.manager.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('login'))
    return log_user_in(request, result[1])

def logout(request):
    user = User.manager.get(id=request.session['user']) # ??? Why this line ???
    request.session.pop('user')
    return redirect(reverse('main'))


def join(request, travel_id):
    user = User.objects.get(id = request.session['user'])
    travel = Travel.objects.get(id = travel_id)
    join = Join.objects.create(travel_id = travel, user_id = user)
    return redirect(reverse('user'))


# when adding a travel and making a mistake information you typed in gets rubbed out
# html get a form page so everything doesn't repeat on every page
# do a seperate thing for travels and joins they repeat on every page -----> tried, same amount of space
