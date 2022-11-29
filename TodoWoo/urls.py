"""TodoWoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signUpUser, name="signupuser"),
    path('logout/', views.logOutUser, name="logOutUser"),
    path('login/', views.loginUser, name="loginUser"),

    # Todos
    path('current/', views.currentToDos, name='currentToDos'),
    path('', views.home, name='home'),
    path('createTodo', views.createTodo, name='createTodo'),
    path('todo/<int:todo_pk>', views.viewTodo, name='viewTodo'),
    path('todo/<int:todo_pk>/complete', views.viewCompleteTodo, name='viewCompleteTodo'),
    path('todo/<int:todo_pk>/delete', views.deleteTodo, name='deleteTodo'),
    path('completed/', views.completedTodos, name='completedTodos'),

    # API
    path('api/', include('api.urls')),
]
