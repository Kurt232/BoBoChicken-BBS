from django.http import HttpResponse
#导入,可以使此次请求忽略csrf校验
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import mail as ML
import json
from .models import *
import datetime

# 分页请求
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# atomic
from django.db import transaction, DatabaseError
#登录 pass test
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
    if req.method == 'GET': # 不应该存在GET 方法
        return JsonResponse({})
    elif req.method == 'POST':
        account_temp = User.objects.filter(email = data['account'], pwd = data['password'])
        if account_temp.exists():
            info_user = list(account_temp.values())
            assert len(info_user) == 1
            try:
                del req.session['uid']
            except KeyError:
                pass
            req.session['uid'] = info_user[0]['uid']
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
            response = JsonResponse({"code":100,
                                 "account":account,
                                 "uname":uname,
                                "password":password,
                                "randomnum":randomnum})
            response["Access-Control-Allow-Origin"] = "*"
            return response

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
            response = JsonResponse({"code":200,
                                "account":account,
                                "uname":uname,
                                'password':password})
            response["Access-Control-Allow-Origin"] = "*"
            return response
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
            response = JsonResponse({"code":100,
                                "account":account,
                                "uname":uname,
                                'password':password,
                                'randomnum':randomnum})
            response["Access-Control-Allow-Origin"] = "*"
            return response
        elif not checknum==randomnum:
            #验证码错误
            response = JsonResponse({"code":200,
                                "account":account,
                                "uname":uname,
                                'password':password,
                                'randomnum':randomnum})
            response["Access-Control-Allow-Origin"] = "*"
            return response
        response = JsonResponse({"code":200,
                            "account":account,
                            "uname":uname,
                            'password':password,
                            'randomnum':randomnum})
        response["Access-Control-Allow-Origin"] = "*"
        return response

# 发帖post 拿post get  pass test
# 默认按时间 pass test
respone_way = ['bid', 'num_reply', 'num_star']
@csrf_exempt
#path('post', views.post, name="post"), POST
def post(req):
    if req.method == "GET":
        page = req.GET.get('page')
        pageSize = int(req.GET.get('pageSize'))
        try:
            way = respone_way[int(req.GET.get('way'))]
        except KeyError:
            way = respone_way[0]
        # print(way)
        response = {}
        bbs_list = Bbs.objects.all().only('bid').order_by(way)
        # bbs_list = Bbs.objects.all().only('bid')
        paginator = Paginator(bbs_list, pageSize)
        response['total'] = paginator.count
        try:
            bbss = paginator.page(page)
        except PageNotAnInteger:
            bbss = paginator.page(1)
        except EmptyPage:
            bbss = paginator.page(paginator.num_pages)
        response['list'] = json.loads(serializers.serialize("json", bbss))
        return JsonResponse(response)
    elif req.method == "POST":
        data = json.loads(req.body)
        try:
            # print(req.session['uid']) <type: int>
            if req.session['uid'] == data['uid']:
                # print(1)
                user = User.objects.get(uid = data["uid"])
                Bbs.objects.create(uid=user,
                                   title=data["title"],
                                   created_time=data["stamp"],
                                   content=data["content"],
                                   reply_time=data["stamp"],
                                   num_reply=0,
                                   num_respond=0,
                                   num_star=0)
                return JsonResponse({"code": 100}) # 成功
            else:
                return JsonResponse({"code": 300}) # 身份问题
        except KeyError:
            return JsonResponse({'code': 301}) # 没有session 其他异常
            

# # 拿帖1
# # path('post/id?<int:post_id>', views.get_post, name="get_post"), GET
# @csrf_exempt
# def get_post(req, post_id):
#     if req.method == 'GET':
#         bbs = list(Bbs.objects.filter(bid = post_id).values())
#         assert len(bbs) == 1 # uid唯一
#         return JsonResponse(bbs[0])
#     else:
#         return JsonResponse({"code":200})


# #拿贴((还没写完) #这个是按热度拿 --DWJ
# @csrf_exempt
# def get_post(req):
#     data = json.loads(req.body)
#     if req.method == "POST":
#         Posts = Bbs.objects.filter().order_by("num_reply")[0:10]
#         print(Posts)
#         return JsonResponse({"code": 100})
#     if req.method == "GET":
#         Posts = Bbs.objects.filter().order_by("num_reply")[data.begin:data.begin+10]
#         print(Posts)
#         return JsonResponse({"code": 100})

## 拿写评论
@csrf_exempt
@transaction.atomic
#path('reply', views.reply, name="reply")
def reply(req):
    if req.method == "GET":
        try:
            bid = req.GET.get('bid')# TODO session 验证身份
            # 多表联合查询 语句谁来写一下#TODO
            
        except KeyError:
            return JsonResponse({"code": 301}) # 报错
    elif req.method == "POST":
        data = json.loads(req.body)
        try:
            # print(req.session['uid']) <type: int>
            if req.session['uid'] == data['uid']:
                # print(1) #TODO 问题 由于用户和bbs都是外键 所以保证是否还存在。。。。 需要吗？ 如果我们测的时候不删除应该就不会被发现
                user = User.objects.get(uid = int(data["uid"]))
                bbs = Bbs.objects.get(bid=int(data["bid"]))
                try:
                    res=int(data['rid'])
                except KeyError:
                    res=-1
                Respond.objects.create(uid=user,
                                    bid=bbs,
                                    responded_rid=res,
                                    content=data['content'],
                                    created_time=data['stamp'],
                                    num_star = 0)
                # 评论数 + 1 原子性
                num_respond_t = bbs.num_respond
                while True:
                    try:
                        with transaction.atomic():
                            bbs.num_respond += 1
                            bbs.save()
                            break
                    except DatabaseError:
                        bbs.num_respond = num_respond_t
                return JsonResponse({"code": 100}) # 成功
            else:
                return JsonResponse({"code": 300}) # 身份问题
        except KeyError:
            return JsonResponse({'code': 301}) # 没有session 其他异常


# 点赞 star 待测
@csrf_exempt
@transaction.atomic
#path('post/star', views.star, name="star_post") GET 点赞
#path('post/star', views.star, name="star_post") POST 取消赞
def star(req):
    if req.method == 'GET':
        try:
            uid = int(req.GET.get('uid'))
            bid = int(req.GET.get('bid'))
            try:
                if req.session['uid'] == uid:
                    event = Bbs.objects.get(bid=bid)
                    num = event.num_star
                    try:
                        user = User.objects.get(uid=uid)
                        bbs = Bbs.objects.get(bid=bid)
                        Star.objects.create(uid=user,
                                            bid=bbs)
                    except DatabaseError: #可能不存在user, bbs 
                        return JsonResponse({'code':400}) # 请忽略
                    while True:
                        try:
                            with transaction.atomic():
                                event.num_star = num + 1
                                event.save()
                                break
                        except DatabaseError:
                            event.num_star = num
                    return JsonResponse({'code':100})
            except KeyError:
                return JsonResponse({'code':301})
        except KeyError:
            return JsonResponse({'code':302})
    elif req.method == 'POST':
        data = json.loads(req.body)
        try:
            uid = req.session['uid']
            if uid == data['uid']:
                try:
                    star = Star.objects.get(sid=data['sid'])
                    if star.uid == uid:
                        while True:
                            try:
                                with transaction.atomic():
                                    bbs = Bbs.objects.get(bid=bid)
                                    num = bbs.num_star
                                    bbs.num_star = num - 1
                                    bbs.save()
                                    break
                            except Bbs.DoesNotExist:
                                break
                            except DatabaseError:
                                pass
                except Star.DoesNotExist:
                    pass
            else:
                return JsonResponse({'code': 302})    
        except Exception:
            return JsonResponse({'code': 302}) # 没有对应值 异常

# 登出 pass test
@csrf_exempt
def logout(req):
    if req.method == "GET":
        try:
            if req.session['uid'] == int(req.GET.get('uid')):
                del req.session['uid'] # 删掉会话代表登出
                return JsonResponse({"code": 100})
            else:
                return JsonResponse({'code': 300}) # 身份不对
        except Exception:
            return JsonResponse({'code': 301}) # 身份不对 异常



        