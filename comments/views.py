import json
from django.shortcuts import render, redirect
from comments.models import Comment
from comments import models
from django.http import JsonResponse, HttpResponse


# Create your views here.

def submit_comments(request):
    status = {'data':None, 'error':'=================', 'redirect_url':None}
    if request.method == "POST":
        comments = request.POST.get("comments_contents")
        if not comments:
            status['redirect_url'] = request.path
            return JsonResponse(status)
        # 存储到models表格中, 并重定向刷新此页面
        article_id = request.POST.get("articles_id")
        up_id = request.session.get("id")
        # print('article id:', article_id)
        models.Comment.objects.create(content=comments,up_user_id_id=up_id, article_id_id=article_id)
        status['data'] = '提交成功'
        status['redirect_url'] = request.path
        # print('status:', status)
        # print(status)
        # print(comments)
        return JsonResponse(status)



def own_comments(request):
    if request.method == "GET":
        obj = models.Comment.objects.select_related("up_user_id").filter(up_user_id=request.session.get('id')).all()
        # print(obj)
        return render(request, 'own_comments.html', {'objs':obj})

