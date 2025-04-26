import os

from django.contrib.auth import logout
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random
from text_app import models as text_models
from categories import models as categories_models
from accounts import models as accounts_models
from comments import models as comments_models
from accounts.views import contrast
from django.utils.safestring import mark_safe
from text_app.html_filter.filter import XSSFilter
# Create your views here.
def contrast_head(func):
    statues = {'data': [], 'is_login': False, 'error': None, 'head': None, 'id':None}
    def wrapper(request, *args, **kwargs):
        cookie = request.COOKIES.get('username')
        if not cookie:
            statues['is_login'] = False
            # print('================not cookie=======================')
            new_args = args + (statues, )
            result = func(request, *new_args, **kwargs)
            return result
        else:
            statues['is_login'] = True
            # print('================sure cookie=======================')

            user_id = request.session.get('id')
            statues['id'] = user_id
            static_path = r"D:\pycharm_project\Cnblogs\static\photo"
            files = []
            for entry in os.scandir(static_path + f'\\{user_id}'):
                if entry.is_file():
                    files.append(entry)
            if files:
                files.sort(key=lambda x: os.path.getmtime(x.path), reverse=True)
                true_path = files[0].path
                file_name = os.path.basename(true_path)
                if statues['data']:
                    statues['data'].clear()
                    statues['data'].append(file_name)
                else:
                    statues['data'].append(file_name)

                new_args = args + (statues,)
                result = func(request, *new_args, **kwargs)
                return result
            else:
                statues['data'].append('1.jpg')
                new_args = args + (statues,)
                result = func(request, *new_args, **kwargs)
                return result
    return wrapper
# def decorator(func):
#     def wrapper(*args):
#         extra_param = "额外参数"
#         # 将额外参数添加到原有的参数中
#         new_args = args + (extra_param,)
#         result = func(*new_args)
#         return result
#     return wrapper
#
#
# @decorator
# def example_function(a, b, extra):
#     print(f"接收到参数: a={a}, b={b}, extra={extra}")
#     return a + b
#
#
# result = example_function(1, 2)
# print(result)

# including  detail \ home : exhibit all content for all_users \
@contrast_head
def home(request, extra):
    if request.method == "GET":
        text_list = []
        obj = text_models.Article.objects.all()
        # user = accounts_models.User.objects
        # obj = text_models.Article.objects.select_related(f'{user}').all()
        for i in obj:
            data = {}
            data['id'] = i.id
            data['title'] = i.title
            data['summary'] = i.summary
            data['user_id'] = i.author_id.id  # 注意 你的 def __str__ return self.name 则直接获取外键列虽然储存的是id，但返回值是return后的实例属性
            ###################
            static_path = r"D:\pycharm_project\Cnblogs\static\photo"
            files = []
            for entry in os.scandir(static_path + f'\\{data['user_id']}'):
                if entry.is_file():
                    files.append(entry)
            if files:
                files.sort(key=lambda x: os.path.getmtime(x.path), reverse=True)
                true_path = files[0].path
            else:
                true_path = r"D:\pycharm_project\Cnblogs\static\photo\1.jpg"
            file_name = true_path
            ########################
            data['filename'] = file_name
            text_list.append(data)
        random.shuffle(text_list)
        # print(text_list)
        return render(request, 'home.html', {'statues': extra, 'photo':'/text_app/header_ex/', 'text_list': text_list})
def header_ex(request):
    # print('======================photo=================')
    user_id = request.session.get('id')
    # print(user_id)
    static_path = r"D:\pycharm_project\Cnblogs\static\photo"
    files = []
    for entry in os.scandir(static_path + f'\\{user_id}'):
        if entry.is_file():
            files.append(entry)
    if files:
        files.sort(key=lambda x: os.path.getmtime(x.path), reverse=True)
        true_path = files[0].path
    else:
        true_path = r"D:\pycharm_project\Cnblogs\static\photo\1.jpg"
    with open(true_path, 'rb') as f:
        result = f.read()
    # print('获取到图片')
    return HttpResponse(result, content_type="image/jpeg")
@contrast_head
def create_articles(request, extra):
    if request.method == "GET":
        if not extra['is_login']:
            return redirect('/accounts/login/')
        categories = categories_models.Category.objects.all()
        # 模板继承---- 发表文章函数
        return render(request, 'create_articles.html', {'photo':'/text_app/header_ex/', 'categories':categories, 'statues': extra})
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary')
        author_id = request.session.get('id')
        obj_author_id = accounts_models.User.objects.get(id=author_id)
        category_id = request.POST.get('select_category')
        obj_category_id = categories_models.Category.objects.get(id=category_id)
        if not content or not title:
            return redirect("http://127.0.0.1:8000/")
        # 将content 进行 富文本编辑源码过滤 防止 xss攻击
        obj_content = XSSFilter()
        content = XSSFilter.process(obj_content, content)
        content = content.decode('utf-8')

        text_models.Article.objects.create(title=title, content=content, summary=summary, author_id=obj_author_id, category_id=obj_category_id)

        # from django.db import  transaction
        # 对于多表操作要保证 原子性， transaction.atomic()
        # with transaction.atomic():
        #     text_models.Article.objects.create(title=title, content=content, summary=summary, author_id=obj_author_id,
        #                                        category_id=obj_category_id)
        #     return redirect("http://127.0.0.1:8000/")

        return redirect("http://127.0.0.1:8000/")



def clean_login(request):
    if request.method == "GET":
        return HttpResponse('待完善')
@contrast
def own_articles(request):
    statues = {'data': True, 'photo':False}
    # 我的文章：      还是用home的方式list展览， 但可以按照create_time方式排序以时间顺序输出自己的文章
    if request.method == "GET":
        text_list = []
        obj = text_models.Article.objects.filter(author_id=request.session.get('id')).all()
        for i in obj:
            data = {}
            data['id'] = i.id
            data['title'] = i.title
            data['summary'] = i.summary
            data['user_id'] = request.session.get('id')  # 注意 你的 def __str__ return self.name 则直接获取外键列虽然储存的是id，但返回值是return后的实例属性
            text_list.append(data)
        return render(request, 'own_text.html', {'photo':'/text_app/header_ex/', 'text_list':text_list, 'statues': statues})

@contrast_head
def detail(request, nid, author_id, extra): #  后台通过url传递两个参数顺序传递， 最后一个传递的是装饰器中的额外函数
    if request.method == "GET":
        content = text_models.Article.objects.get(id=nid, author_id=author_id).content
        if int(author_id) == request.session.get('id'):
            alter_able = True
        else:
            alter_able = False
        # comments = comments_models.Comment.objects.filter(author_id=author_id).all()
        # 评论根据article_id列 来查询, 呈现 content列
        # print(nid)
        # print(content)
        # print(extra)
        # print(type(author_id), type(request.session.get('id')))
        # print(alter_able)
        comment_obj = comments_models.Comment.objects.filter(article_id=nid).order_by('-id').all()
        return render(request, 'detail.html', {'content':mark_safe(content),
                                               'photo':'/text_app/header_ex/',
                                               'statues':extra,
                                               'alter_able':alter_able,
                                               'articles_id': nid,
                                               'author_id': author_id,
                                               'comments':comment_obj,
                                               'count':122})

def delete_article(request, nid):
    if request.method == "GET":
        obj = text_models.Article.objects.get(id=nid)
        obj.delete()
        return JsonResponse({'status':{'error':'fault'}})

def alter_article(request, nid, author_id):
    statues = {'data': {}, 'error':None}
    if request.method == "GET":
        obj = text_models.Article.objects.get(id=nid, author_id=author_id)
        statues['data']['title']= obj.title
        statues['data']['content']= obj.content
        statues['data']['summary']= obj.summary
        statues['data']['category_id']= obj.category_id.id
        categories = categories_models.Category.objects.all()
        return render(request, 'alter_article.html', {'statues':statues, 'articles_id': nid, 'author_id': author_id, 'categories': categories})
