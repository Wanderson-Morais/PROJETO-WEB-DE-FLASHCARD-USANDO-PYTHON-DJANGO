
# E AQUI ONDE O BANCO DE DADOS SE LIGA COM O FRONT#
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth ##autenticaçao do django##



def cadastro(request): ##o tratamento dos dados do cadastro html, daqui os dados vao para o banco de dados##
 if request.method == 'GET':
    return render(request, 'cadastro.html')
 else:
     username = request.POST.get('username')
     senha = request.POST.get('senha')
     confirmar_senha = request.POST.get('confirmar_senha')
 
     if not senha == confirmar_senha: ##verificar se a senha é igual##
        messages.add_message(request, constants.ERROR, 'Senha e confirmar senha  estao diferentes')
        return redirect('/usuarios/cadastro')
 
     user = User.objects.filter(username=username) ##verificar se o nome do usuario ja exste##
     if user.exists():
        messages.add_message(request, constants.ERROR, 'usuario ja existe')
        return redirect('/usuarios/cadastro')
 
     try: ##quando algum tipo de exeçao acontecer##
        user = User.objects.create_user(
        username=username,
        password=confirmar_senha,
        )

        return redirect('/usuarios/logar')
     except:
        messages.add_message(request, constants.ERROR, 'erro interno do servidor')
        return redirect('/usuarios/cadastro')


def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
     username = request.POST.get('username')
     senha = request.POST.get('senha')
     
     user = auth.authenticate(request, username=username, password=senha)##verificar se o usuario tem cadastro##
 
    if user:
        auth.login(request, user)
        messages.add_message(request, constants.SUCCESS, 'Logado!')
        return redirect('/flashcard/novo_flashcard/')
   
    else:
       messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
       return redirect('/usuarios/logar')


def logout(request):
 auth.logout(request)
 return redirect('/usuarios/login')
