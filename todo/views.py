from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def signUpUser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentToDos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm, 'error': 'This username already exists'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm, 'error': 'Passwords did not match'})


@login_required()
def logOutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')


def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form': AuthenticationForm, 'error': "Username and password do not match"})
        else:
            login(request, user)
            return redirect('currentToDos')


@login_required()
def createTodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newToDo = form.save(commit=False)
            newToDo.user = request.user
            newToDo.save()
            return redirect('currentToDos')
        except ValueError:
            return render(request, 'todo/createTodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required()
def currentToDos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currentToDos.html', {'todos': todos})


@login_required()
def viewTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewTodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentToDos')
        except ValueError:
            return render(request, 'todo/viewTodo.html', {'todo': todo, 'form': form, 'error': "Back data"})


@login_required()
def viewCompleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentToDos')


@login_required()
def deleteTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currentToDos')


@login_required()
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')
    return render(request, 'todo/completedTodos.html', {'todos': todos})
