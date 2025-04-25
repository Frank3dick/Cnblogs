import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from categories import models
from text_app import models as text_models
# Create your views here.
def create_categories(request):
    # if request.method == "GET":
    #     models.Category.objects.create(name="总类")
    #     models.Category.objects.create(name="科技")
    #     models.Category.objects.create(name="生活")
    #     models.Category.objects.create(name="体育")
    #     models.Category.objects.create(name="新闻")
    #     models.Category.objects.create(name="政治")
    #     return HttpResponse("create data success")
    pass

def dif_categories(request):
    statues = {'data':True}
    if request.method == "GET":
        # nid 为前端传回来的 categories表的id
        categories = models.Category.objects.all()
        return render(request, 'different_categories.html', {'categories': categories, 'photo':'/text_app/header_ex/', 'statues':statues})

def into_dif_group(request, nid):
    statues = {'data':True, 'photo':True}
    if request.method == "GET":
        text_list = []
        obj = text_models.Article.objects.filter(category_id=nid).all()
        for i in obj:
            data = {}
            data['id'] = i.id
            data['title'] = i.title
            data['summary'] = i.summary
            data['user_id'] = i.author_id.id # 注意 你的 def __str__ return self.name 则直接获取外键列虽然储存的是id，但返回值是return后的实例属性
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
            data['filename'] = file_name
            text_list.append(data)
        return render(request, 'own_text.html', {'text_list':text_list, 'photo':'/text_app/header_ex/', 'statues':statues})