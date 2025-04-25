import json
import os

from importlib.metadata import files
from io import BytesIO
from struct import pack_into

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import User
from django.utils import timezone
from accounts import models
from django.forms import forms
from django.forms import fields
from django.forms import widgets
from django.utils.decorators import method_decorator
def test_redirect(request):
    if request.method == 'GET':
        return render(request, 'test_redirect.html')
# Create your views here.
def contrast(func):
    def wrapper(request, *args, **kwargs):
        cookie = request.COOKIES.get('username')
        print(cookie)
        print("================================================")
        if not cookie:
            return redirect('/accounts/login/')
        if not request.session.get('is_login'):
            return redirect('/accounts/login/')
        return func(request, *args, **kwargs)
    return wrapper
def login(request):
    statues = {'data':None, 'error':None, 'is_log':False, "redirect_url":None}
    if request.method == "GET":
        return render(request, 'login.html', {'check_code':'/accounts/check_code/'})
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        code = request.POST.get('code', None)
        print(username, password, email, code)
        try:
            username_db = User.objects.filter(username=username).first().username
            password_db = User.objects.filter(password=password).first().password
            email_db = User.objects.filter(email=email).first().email
            code_str = request.session.get('code')
            print(username_db, password_db, email_db, code_str)
            if username_db==username and password_db==password and email_db==email and code_str.upper()==code.upper():
                statues['is_log'] = True
                id_db = User.objects.filter(username=username, password=password).first()
                request.session['id'] = id_db.id
                request.session['password'] = password_db
                request.session['is_login'] = True
                statues['redirect_url'] = "http://127.0.0.1:8000/"
                rep = JsonResponse(statues)
                rep.set_cookie('username', username_db)
                if request.POST.get('check_member'):
                    request.session.set_expiry(60*60*24*7)
                return rep
            else:
                statues['error'] = 'ACCOUNT NOT FOUND'
                statues['is_log'] = False
                statues['redirect_url'] = '/accounts/login/'
                return JsonResponse(statues)
        except AttributeError:
            statues['error'] = 'ACCOUNT NOT FOUND'
            statues['is_log'] = False
            statues['redirect_url'] = '/accounts/login/'
            return JsonResponse(statues)
def check_code(request):
    if request.method == "GET":
        from work_photo import check_code
        stream = BytesIO()
        img, code = check_code.generate_captcha()
        img.save(stream, format='PNG')
        request.session['code'] = code
        return HttpResponse(stream.getvalue(), content_type='image/png')

class Fm(forms.Form):
    username = fields.CharField(error_messages={'required':'用户名不能为空'},)
    password = fields.CharField(error_messages={'required':"密码不能为空", 'min_length':"最短为6", "max_length":"最长为12"},
                                max_length=12, min_length=6,
                                widget=widgets.PasswordInput(),)
    email = fields.EmailField()
    def clean_password(self):
        password = self.cleaned_data['password']
        if password.isdigit():
            raise ValueError('密码不能全为数字', 'invalid')
        return password
def register(request):
    statues = {'data':None, 'error':None, 'message':None, "redirect_url":None}
    if request.method == "GET":
        statues['redirect_url'] = '/accounts/register/'
        fm = Fm()
        return render(request, 'register.html', {'fm':fm})
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        code = request.POST.get('code', None)
        if code.upper()==request.session.get('code').upper():
            dict_create = {
                'username': username,
                'password': password,
                'email': email,
            }
            new_user = User(**dict_create)
            new_user.save()
            new_id = new_user.id
            statues['redirect_url'] = '/accounts/login/'
            #==============创建头像文件===================
            os.makedirs(f"D:\\pycharm_project\\Cnblogs\\static\\photo\\{new_id}")
            return JsonResponse(statues)
        else:
            statues['error'] = 'ACCOUNT NOT FOUND'
            statues['redirect_url'] = '/accounts/register/'
            return JsonResponse(statues)
@contrast
def editor(request):
    statues = {'data':None, 'error':None, 'message':None, "redirect_url":None}
    if request.method == "GET":
        account_id = request.session.get('id')
        print(account_id)
        obj = models.User.objects.filter(id=account_id).first()
        dicts = {
            'username': obj.username,
            'password': obj.password,
            'email': obj.email,
        }
        fm = Fm(initial=dicts)
        return render(request, 'login_editor.html', {'fm':fm})
    if request.method == "POST":
        account_id = request.session.get('id')
        # 检查 account_id 是否有效
        if account_id is None:
            # 处理 account_id 为 None 的情况，例如重定向到登录页
            return redirect('/accounts/login')
        obj = Fm(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data['username']
            email = obj.cleaned_data['email']
            password = obj.cleaned_data['password']
            # 对密码进行哈希处理
            editor_dict = {
                'username': username,
                'email': email,
                'password': password,
                'update_time': timezone.now(),
            }
            # 更新数据库记录
            models.User.objects.filter(id=account_id).update(**editor_dict)
            statues['is_log'] = True
            statues['redirect_url'] = "http://127.0.0.1:8000/"
            return JsonResponse(statues)
# 文件名一定不能是 带中文的!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def change_head(request):
    statues = {'data':None, 'error':None, 'message':None, 'user_id':None, 'redirect_url':None}
    if request.method == "GET":
        return redirect('/accounts/editor/')
    if request.method == "POST":
        print("===================================")
        print(request.FILES)
        head = request.FILES.get('file')
        print(head)
        print("===================================")
        try:
            statues['user_id'] = request.session.get('id', None)
        except:
            print('mei  id///////////////////////////////')
            statues['redirect_url'] = '/accounts/login/'
            return JsonResponse(statues)
        statues['redirect_url'] = '/accounts/login/'
        static_path = r"D:\pycharm_project\Cnblogs\static\photo"
        os.makedirs(static_path+f'\\{statues['user_id']}', exist_ok=True)
        load_path = os.path.join(static_path+f'\\{statues['user_id']}', head.name)

        with open(load_path, 'wb') as f:
            for chunk in head.chunks():
                f.write(chunk)
        files = []
        for entry in os.scandir(static_path+f'\\{statues['user_id']}'):
            if entry.is_file():
                files.append(entry)
        if files:
            files.sort(key=lambda x: os.path.getmtime(x.path), reverse=True)
            true_path = files[0].path
            file_name = os.path.basename(true_path)
            statues['data'] = file_name
        rep = JsonResponse(statues)
        rep.set_cookie('head', statues['data'])
        print(statues['data'])
        return rep