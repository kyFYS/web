from django.shortcuts import render,HttpResponse, redirect
from app01.form.account import RegisterModelForm, SendSmsForm,LoginSMSForm,LoginForm
import random
from utils.Tencent.sms import send_sms_single
from django.http import JsonResponse
from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from utils.image_code import check_code
from io import BytesIO
from django.db.models import Q

def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request,'register.html', {'form': form})
    print(request.POST)
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    # 只是校验手机号：不能为空、格式是否正确
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})



def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm
        return render(request , 'login_sms.html', {'form': form})
    print(request.POST)
    form = LoginSMSForm(data=request.POST)
    if form.is_valid():
        return JsonResponse({"status": True, 'data': "/index/"})
    return JsonResponse({"status": False, 'error': form.errors})


def login(request):
    """ 用户名和密码登录 """
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        #  (手机=username and pwd=pwd) or (邮箱=username and pwd=pwd)

        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()
        if user_object:
            # 登录成功为止1
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.flush()
    return redirect('index')

