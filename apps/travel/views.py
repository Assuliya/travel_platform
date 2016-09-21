from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from models import User, Travel, Join
import bcrypt
from datetime import date

def index(request):
    return render(request, 'travel/index.html')

def login(request):
    travels = False
    joins = False
    context = {'joins':joins, 'travels': travels}
    return render(request, 'travel/login.html', context)

def main(request):
    if 'user' in request.session:
        user = User.objects.get(id = request.session['user'])
        start = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).order_by('start')[:6]
        latest = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).order_by('-created_at')[:6]
        popular = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')[:6]
        travels = Travel.objects.filter(user_id = request.session['user']).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        user = User.objects.all()
        start = Travel.objects.order_by('start')[:6]
        latest = Travel.objects.order_by('start')[:6]
        popular = Travel.objects.values('id','destination','plan','start','end','travel_image','join_travel__user_id_id','user_id_id').annotate(count=Count('join_travel__user_id_id')).order_by('-count')[:6]
        travels = False
        joins = False

    context = {'start':start, 'latest':latest, 'popular':popular, 'user':user, 'joins':joins, 'travels': travels}
    return render(request, 'travel/main.html', context)

def user(request):
    if 'user' in request.session:
        user = User.objects.get(id = request.session['user'])
        travels = Travel.objects.filter(user_id = request.session['user'])
        joins = Join.objects.filter(user_id = request.session['user'])
        other = Travel.objects.exclude(join_travel__user_id_id = request.session['user']).order_by('start')
        context = {'travels':travels, 'user':user, 'other':other, 'joins': joins}
        return render(request, 'travel/user.html', context)
    return redirect(reverse('main'))

def travel(request, travel_id):
    travel = Travel.objects.get(id = travel_id)
    joined = Join.objects.filter(travel_id = travel_id)
    if 'user' in request.session:
        travels = Travel.objects.filter(user_id = request.session['user']).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        travels = False
        joins = False
    context = {'travel':travel, 'joined':joined, 'travels':travels, 'joins':joins}
    return render(request, 'travel/travel.html', context)

def add(request):
    today = date.today()
    format_time = today.strftime('%Y-%m-%d')
    if 'user' in request.session:
        travels = Travel.objects.filter(user_id = request.session['user']).order_by('-start')[:2]
        joins = Join.objects.filter(user_id = request.session['user']).order_by('-travel_id__start')[:2]
    else:
        travels = False
        joins = False
    context = {'time':format_time, 'travels': travels, 'joins': joins}
    return render(request, 'travel/add.html', context)

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

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def log_user_in(request, user):
    request.session['user'] = user.id
    return redirect(reverse('user'))

def logout(request):
    user = User.manager.get(id=request.session['user'])
    request.session.pop('user')
    return redirect(reverse('main'))

def add_travel(request):
    errors = []
    print request.POST['end']
    if len(request.POST['destination']) < 1:
        errors.append('Destination can not be empty')
    if len(request.POST['plan']) < 1:
        errors.append('Description can not be empty')
    if len(request.POST['start']) < 1:
        errors.append('Travel Date From can not be empty')
    if len(request.POST['end']) < 1:
        errors.append('Travel Date To can not be empty')
    if request.POST['end'] < request.POST['start']:
        errors.append('Travel Date To can not be earlier than Travel Date From')
    if len(errors) > 0:
        print errors
        print_messages(request, errors)
        return redirect(reverse('add'))

    creator = User.objects.get(id = request.session['user'])

    if 'image' in request.FILES:
        # request.FILES['image'].name = creator.username + "_" + request.POST['destination'][:8]
        Travel.objects.create(travel_image = request.FILES['image'], user_id = creator, destination=request.POST['destination'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'])
    else:
        Travel.objects.create(user_id = creator, destination=request.POST['destination'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'])

    return redirect(reverse('user'))

def join(request, travel_id):
    user = User.objects.get(id = request.session['user'])
    travel = Travel.objects.get(id = travel_id)
    join = Join.objects.create(travel_id = travel, user_id = user)
    return redirect(reverse('user'))
