from django.http import HttpResponse
from django.shortcuts import render
#导入,可以使此次请求忽略csrf校验
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import mail as ML
import json
from .models import *
import datetime

#登录
@csrf_exempt# 所有的view 都需要 这个注解防止被攻击
def login(req):
    '''
    req: json
    req: {
        account: str,
        password: str
    }
    '''
    data = json.loads(req.body)
    if req.method == 'GET':
        return JsonResponse({})
    elif req.method == 'POST':
        account_temp = User.objects.filter(email = data['account'], pwd = data['password'])
        if account_temp.exists():
            info_user = list(account_temp.values())
            assert len(info_user) == 1
            return JsonResponse({"code": 100, "data": info_user[0]}) # right
            # return JsonResponse({"code": 100}, safe = False) # 可以传入任何一个可以转成json的data
        else:
            return JsonResponse({"code": 200}) # 密码错误或用户不存在

#验证码发送前
@csrf_exempt
def register(req):
    """
        req: json
    req: {
        account: str,
        password: str,
        checknum: str
    }
    """
    
    data = json.loads(req.body)
    print(data)
    if req.method=='GET':
        return JsonResponse({})
    elif req.method=='POST':
        account = data['account']
        uname = data['uname']
        account_temp = User.objects.filter(email = data['account'])
        password = data['password']
        
        # 邮箱用户已存在
        if account_temp.exists():
            return JsonResponse({"code":200,
                                "account":account,
                                "uname":uname,
                                'password':password})
        else:
            randomnum = ML.postmailnum(account)
            return JsonResponse({"code":100,
                                 "account":account,
                                 "uname":uname,
                                "password":password,
                                "randomnum":randomnum})

#验证码发送后
@csrf_exempt
def register_check(req):
    """
        req: json
    req: {
        account: str,
        password: str
        checknum: str
    }
    """
    data = json.loads(req.body)
    if req.method=='GET':
        return JsonResponse({})
    elif req.method=='POST':
        account = data['account']
        uname = data['uname']
        password = data['password']
        checknum = data['checknum']
        randomnum = data['randomnum']
        account_temp = User.objects.filter(email = data['account'])
         # 邮箱用户已存在
        if account_temp.exists():
            return JsonResponse({"code":200,
                                "account":account,
                                "uname":uname,
                                'password':password})
        elif checknum == randomnum:
            User.objects.create(email=data['account'],
                               uname=data['uname'],
                               pwd=data['password'],
                               created_time=datetime.date.today().isoformat(),
                               num_followed=0,
                               num_follow=0)
            # User.follow.set()
            # User.post.set()
            # User.reply.set()
            return JsonResponse({"code":100,
                                "account":account,
                                "uname":uname,
                                'password':password,
                                'randomnum':randomnum})
        elif not checknum==randomnum:
            #验证码错误
            return JsonResponse({"code":200,
                                "account":account,
                                "uname":uname,
                                'password':password,
                                'randomnum':randomnum})
        return JsonResponse({"code":200,
                            "account":account,
                            "uname":uname,
                            'password':password,
                            'randomnum':randomnum})

# 发帖
@csrf_exempt
#path('post', views.dump_post, name="dump_post"), POST
def dump_post(req):
    if req.method == "GET":
        return JsonResponse({"code": 200}) #TODO 查询
    elif req.method == "POST":
        data = json.loads(req.body)
        # stamp = datetime.date.today().isoformat() # 带时间戳的格式 但是感觉前端给比较好，这样和前端时间一致
        
        Bbs.objects.create(uid=data["uid"],
                            title=data["title"],
                            created_time=data["stamp"],
                            content=data["content"],
                            num_respond=0,
                            num_star=0)
        return JsonResponse({"code": 100})

# 拿帖1
# path('post/id?<int:post_id>', views.get_post, name="get_post"), GET
@csrf_exempt
def get_post(req, post_id):
    if req.method == 'GET':
        bbs = list(Bbs.objects.filter(bid = post_id).values())
        assert len(bbs) == 1 # uid唯一
        return JsonResponse(bbs[0])
    else:
        return JsonResponse({"code":200})

# 拿用户
#浏览贴
@csrf_exempt
def browsepost(req):
    if req.method == "POST":
        Posts = Bbs.objects.filter().order_by("num_reply")[0:10]
        print(Posts)
        return JsonResponse({"code": 100})
    if req.method == "GET":
        Posts = Bbs.objects.filter().order_by("num_reply")
        posts_list = []
        for i in Posts:
            posts_list.append(i)
            if posts_list.__len__()>=10: break
        print(posts_list)
        return JsonResponse({"code": 100})
    
#登出
@csrf_exempt
def logout(req):
    if req.method == "GET":
        return JsonResponse({})
    elif req.method == "POST":
        data = json.loads(req.body)
        a=User.objects.all()
        for i in a:
            print(i)
        return JsonResponse({"code": 100})




        