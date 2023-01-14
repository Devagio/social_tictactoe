from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Results, Profile
from .forms import RoomForm, UserForm, ProfileForm
from .logic import check


def login_page(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f'User "{username}" does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'The password entered for user "{username}" is incorrect.')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        messages.error(request, 'Please logout first.')
        return redirect('home')

    page = 'register'
    form = UserCreationForm()
    form2 = ProfileForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form2 = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            user = form.save()
            login(request, user)
            obj = form2.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration (either username taken, weak password, unmatching password confirmation, etc.). Please try again.')

    context = {'page':page, 'form':form, 'form2':form2}
    return render(request, 'base/login_register.html', context)


def home(request):
    rooms = Room.objects.all()
    profiles = Profile.objects.all()
    all_room_count = rooms.count()
    results = Results.objects.all()

    q = request.GET.get('q')
    if q != None:
        rooms = rooms.filter(best_of=q)
        results = results.filter(room__best_of=q)
        
    r = request.GET.get('r')
    if r != None:
        print(r)
        rooms = rooms.filter(Q(name__icontains=r))
        results = results.filter(Q(room__name__icontains=r))
        
    lengths = [[i, 0] for i in range(1,7)]
    room_count = rooms.count()
    for i in range(len(lengths)):
        lengths[i][1] = Room.objects.all().filter(best_of=lengths[i][0]).count()
    context = {'user':None, 'rooms':rooms, 'lengths':lengths, 'room_count':room_count, 'results':results, 'all_room_count':all_room_count, 'profiles':profiles}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    profiles = Profile.objects.all()

    if request.user.is_authenticated:
        room.viewers.add(request.user)
    else:
        room.anon_viewers += 1
        room.save()
    
    viewers = room.viewers.all()

    if request.method == 'POST':
        if 'body' in request.POST:
            Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body')
            )
            return redirect('room', pk=room.id)
        
        elif 'challenge' in request.POST:
            if room.challenger == None:
                room.challenger = request.user
                room.save()
            else:
                messages.error(f'The {room.name} challenge has already been accepted. You can only view this match, or challenge someone else.')
            return redirect('room', pk=room.id)

        else:
            temp = [f'X{i}' for i in range(9)] + [f'O{i}' for i in range(9)]
            for name in temp:
                if name in request.POST:
                    i = int(name[1])
                    room.board_state = room.board_state[:i] + name[0] + room.board_state[i+1:]
                    room.save()
                    return redirect('room', pk=room.id)

    winner = check(room.board_state)
    
    if winner == 'X':
        room.host_score += 2
        room.save()
    elif winner == 'O':
        room.challenger_score += 2
        room.save()
    elif winner == 'D':
        room.host_score += 1
        room.challenger_score += 1
        room.save()
    if winner != None:
        room.board_state = '.........'
        room.save()

    if not room.done:
        if room.challenger_score > room.best_of:
            room.overall = room.challenger
            room.done = True
            room.save()
            challenger_profile = profiles.get(user=room.challenger)
            challenger_profile.wins = challenger_profile.wins + 1
            challenger_profile.save()
            host_profile = profiles.get(user=room.host)
            host_profile.losses = host_profile.losses + 1
            host_profile.save()
            Results.objects.create(room=room)
        if room.host_score > room.best_of:
            room.overall = room.host
            room.done = True
            room.save()
            challenger_profile = profiles.get(user=room.challenger)
            challenger_profile.losses = challenger_profile.losses + 1
            challenger_profile.save()
            host_profile = profiles.get(user=room.host)
            host_profile.wins = host_profile.wins + 1
            host_profile.save()
            Results.objects.create(room=room)
        if room.host_score == room.challenger_score == room.best_of:
            room.done = True
            room.save()
            challenger_profile = profiles.get(user=room.challenger)
            challenger_profile.draws = challenger_profile.draws + 1
            challenger_profile.save()
            host_profile = profiles.get(user=room.host)
            host_profile.draws = host_profile.draws + 1
            host_profile.save()
            Results.objects.create(room=room)
        
    
    turn = int(room.host_score/2 + room.challenger_score/2 + room.board_state.count('.')) % 2
    context = {'user':None, 'room':room, 'room_messages':room_messages, 'viewers':viewers, 'turn':turn, 'profiles':profiles}
    #if room.done: context['results'] = Results.objects.get(room=room)
    return render(request, 'base/room.html', context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.all()
    rooms = rooms.filter(Q(host=user) | Q(challenger=user))
    all_room_count = rooms.count()
    results = Results.objects.filter(Q(room__host=user) | Q(room__challenger=user))
    profiles = Profile.objects.all()

    lengths = [[i, 0] for i in range(1,7)]
    room_count = rooms.count()
    for i in range(len(lengths)):
        lengths[i][1] = rooms.filter(best_of=lengths[i][0]).count()

    q = request.GET.get('q')
    if q != None:
        rooms = rooms.filter(best_of=q)
        results = results.filter(room__best_of=q)

    r = request.GET.get('r')
    if r != None:
        rooms = rooms.filter(Q(name__icontains=r))
        results = results.filter(Q(room__name__icontains=r))

    context = {'user':user, 'rooms':rooms, 'results':results, 'lengths':lengths, 'room_count':room_count, 'all_room_count':all_room_count, 'profiles':profiles}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.host = request.user
            obj.save()
            return redirect('home')
    users = User.objects.all()
    profiles = Profile.objects.all()

    context = {'form': form, 'users':users, 'create':True, 'profiles':profiles}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room', pk=room.id)
    users = User.objects.all()
    profiles = Profile.objects.all()

    context = {'form': form, 'users':users, 'create':False, 'profiles':profiles}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    profiles = Profile.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'obj':room, 'profiles':profiles})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)
    profiles = Profile.objects.all()
    form = UserForm(instance=user)
    form2 = ProfileForm(instance=profile_obj)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        form2 = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'An error occurred during registration (either username taken, weak password, unmatching password confirmation, etc.). Please try again.')


    return render(request, 'base/update_user.html', {'form':form, 'form2':form2, 'profiles':profiles})


def topics_page(request):
    rooms = Room.objects.all()
    all_room_count = rooms.count()
    profiles = Profile.objects.all()
        
    lengths = [[i, 0] for i in range(1,7)]
    for i in range(len(lengths)):
        lengths[i][1] = Room.objects.all().filter(best_of=lengths[i][0]).count()
    context = {'lengths':lengths, 'all_room_count':all_room_count, 'profiles':profiles}
    return render(request, 'base/topics.html', context)


def activities_page(request):
    results = Results.objects.all()
    profiles = Profile.objects.all()
    context = {'results':results, 'profiles':profiles}
    return render(request, 'base/activities.html', context)