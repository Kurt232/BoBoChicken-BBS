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
            return JsonResponse({"code": 100, "data": info_user[0]}) #right
        else:
            return JsonResponse({"code": 200})# 密码错误或用户不存在

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
        return JsonResponse({"code":200})#不该出现
    elif req.method=='POST':
        account = data['account']
        uname = data['uname']
        account_temp = User.objects.filter(email = data['account'])
        password = data['password']
        # return ReturnJsonResponse(JsonResponse({"code": 200}))# 密码错误或用户不存在
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

# 发帖post 拿post get pass test
# 默认按时间 pass test
respone_way = ['-bid', '-num_reply', '-num_star', '-num_seen', '-num_like'] 
@csrf_exempt
#path('post', views.post, name="post"), POST
def post(req):
    if req.method == "GET":
        page = int(req.GET.get('page'))
        pageSize = int(req.GET.get('pageSize'))
        try:
            way = respone_way[int(req.GET.get('way'))]
        except IndexError and KeyError:
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
        response['code'] = 100
        return JsonResponse(response)
    elif req.method == "POST":
        data = json.loads(req.body)
        try:
            # print(req.session['uid']) <type: int>
            if req.session['uid'] == data['uid']:
            # if True:
                user = User.objects.get(uid = data["uid"])
                newbbs = Bbs.objects.create(uid=user,
                                    title=data["title"],
                                    uname=user.uname,
                                    created_time=data["stamp"],
                                    content=data["content"],
                                    reply_time=data["stamp"],
                                    num_reply=0,
                                    num_seen=0,
                                    num_star=0,
                                    num_like=0)     
                user.post.add(newbbs)
                return JsonResponse({'code':100}) # 成功
            else:
                return JsonResponse({"code": 300}) # 身份问题
        except KeyError:
            return JsonResponse({"code": 302}) # 


## 拿写评论
@csrf_exempt
@transaction.atomic
#path('reply', views.reply, name="reply")
def reply(req):
    if req.method == "GET": # 拿评论 pass test
        try:
            bid = req.GET.get('bid')
            responds = Respond.objects.filter(bid=bid)
            response = {}
            response['totol'] = responds.count()
            response['list'] = json.loads(serializers.serialize("json", responds))
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({"code": 301}) # 报错
    elif req.method == "POST": # 写评论 pass test
        data = json.loads(req.body)
        try:
            # print(req.session['uid']) <type: int>
            if req.session['uid'] == int(data['uid']):
            # if True:
                f = False
                while True:
                    try:
                        user = User.objects.get(uid=int(data["uid"]))
                        bbs = Bbs.objects.get(bid=int(data["bid"]))
                        reuser = User.objects.get(uid=int(data["rid"]))
                    except User.DoesNotExist and Bbs.DoesNotExist:
                        return JsonResponse({'code':400})
                    if not f :
                        res_t = Respond.objects.create(uid=user,
                                                        uname=user.uname,
                                                        rename=reuser.uname,
                                                        bid=bbs,
                                                        content=data['content'],
                                                        created_time=data['stamp'])
                        user.reply.add(res_t)
                        f = True
                    # 评论数 + 1 原子性
                    num_reply_t = bbs.num_reply
                    stamp = bbs.reply_time
                    try:
                        with transaction.atomic():
                            bbs.num_reply = num_reply_t + 1
                            bbs.reply_time = data['stamp']
                            bbs.save()
                            break
                    except DatabaseError:
                        bbs.num_reply = num_reply_t
                        bbs.reply_time = stamp
                return JsonResponse({"code": 100}) # 成功
            else:
                return JsonResponse({"code": 300}) # 身份问题
        except KeyError:
            return JsonResponse({'code': 301}) # 没有session 其他异常


# 点收藏 star pass test
@csrf_exempt
@transaction.atomic
#path('post/star', views.star, name="star_post") GET 点收藏
#path('post/star', views.star, name="star_post") POST 取消收藏
def star(req):
    if req.method == 'GET':
        try:
            uid = int(req.GET.get('uid'))
            bid = int(req.GET.get('bid'))
            try:
                if req.session['uid'] == uid:
                # if True:
                    while True:
                        try:
                            user = User.objects.get(uid=uid)
                            bbs = Bbs.objects.get(bid=bid)
                        except User.DoesNotExist and Bbs.DoesNotExist: #不存在user 
                            return JsonResponse({'code':400}) # 请忽略
                        num = bbs.num_star
                        try:
                            Star.objects.get(uid=user, bid=bbs)
                            return JsonResponse({'code':200}) # 已点收藏
                        except Star.DoesNotExist:
                            try:
                                with transaction.atomic():
                                    bbs.num_star = num + 1
                                    bbs.save()
                                    Star.objects.create(uid=user, bid=bbs)
                                    break
                            except DatabaseError:
                                bbs.num_star = num
                    return JsonResponse({'code':100})
            except KeyError:
                return JsonResponse({'code':301})
        except KeyError:
            return JsonResponse({'code':302})
    elif req.method == 'POST':
        data = json.loads(req.body)
        try:
            uid_t = int(req.session['uid'])
            bid = int(data['bid'])
            uid = int(data['uid'])
            if uid == uid_t:
            # if True:
                while True:
                    try:
                        bbs = Bbs.objects.get(bid=bid)
                        user = User.objects.get(uid=uid)
                    except Bbs.DoesNotExist and User.DoesNotExist:
                        return JsonResponse({'code':400})
                    num = bbs.num_star
                    try:
                        star = Star.objects.get(uid=user, bid=bbs)
                        try:
                            with transaction.atomic():
                                bbs.num_star = num - 1
                                bbs.save()
                                star.delete()
                                break
                        except DatabaseError:
                            bbs.num_star = num
                    except Star.DoesNotExist:
                        return JsonResponse({'code':200}) # 已经取消
                return JsonResponse({'code':100})
            else:
                return JsonResponse({'code': 302})
        except Exception:
            return JsonResponse({'code': 302}) # 没有对应值 异常


# 点赞 like pass test
@csrf_exempt
@transaction.atomic
#path('post/like', views.like, name="like_post") GET 点收藏
#path('post/like', views.like, name="like_post") POST 取消收藏
def like(req):
    if req.method == 'GET':
        try:
            uid = int(req.GET.get('uid'))
            bid = int(req.GET.get('bid'))
            try:
                #print(req.session['uid'])
                if req.session['uid'] == uid:
                # if True:
                    while True:
                        try:
                            user = User.objects.get(uid=uid)
                            bbs = Bbs.objects.get(bid=bid)
                        except User.DoesNotExist and Bbs.DoesNotExist: #不存在user 
                            return JsonResponse({'code':400}) # 请忽略
                        num = bbs.num_like
                        try:
                            Like.objects.get(uid=user, bid=bbs)
                            return JsonResponse({'code':200}) # 已点收藏
                        except Like.DoesNotExist:
                            try:
                                with transaction.atomic():
                                    bbs.num_like = num + 1
                                    bbs.save()
                                    Like.objects.create(uid=user,
                                                        bid=bbs)
                                    break
                            except DatabaseError:
                                bbs.num_like = num
                    return JsonResponse({'code':100})
            except KeyError:
                return JsonResponse({'code':301})
        except KeyError:
            return JsonResponse({'code':302})
    elif req.method == 'POST':
        data = json.loads(req.body)
        try:
            uid_t = int(req.session['uid'])
            bid = int(data['bid'])
            uid = int(data['uid'])
            if uid == uid_t:
            # if True:
                while True:
                    try:
                        bbs = Bbs.objects.get(bid=bid)
                        user = User.objects.get(uid=uid)
                    except Bbs.DoesNotExist and User.DoesNotExist:
                        return JsonResponse({'code':400})
                    num = bbs.num_like
                    try:
                        like = Like.objects.get(uid=user, bid=bbs)
                        try:
                            with transaction.atomic():
                                bbs.num_like = num - 1
                                bbs.save()
                                like.delete()
                                break
                        except DatabaseError:
                            bbs.num_like = num
                    except Like.DoesNotExist:
                        return JsonResponse({'code':200}) # 已经取消
                return JsonResponse({'code':100})
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


# follow pass test
@csrf_exempt
@transaction.atomic
#path('follow', views.follow, name="follow") GET follow
#path('follow', views.follow, name="unfollow") POST unfollow
def follow(req):
    if req.method == 'GET':
        try:
            uid = int(req.GET.get('uid'))
            fid = int(req.GET.get('fid'))
            try:
                if req.session['uid'] == uid:
                # if True:
                    while True:
                        try:
                            user = User.objects.get(uid=uid)
                            fuser = User.objects.get(uid=fid)
                        except User.DoesNotExist: #不存在user 
                            return JsonResponse({'code':400}) # 请忽略
                        num1 = user.num_follow
                        num2 = fuser.num_followed
                        try:
                            Follow.objects.get(from_uid=user, to_uid=fuser)
                            return JsonResponse({'code':200}) # 已经follow
                        except Follow.DoesNotExist:
                            try:
                                with transaction.atomic():
                                    user.num_follow = num1 + 1
                                    fuser.num_followed = num2 + 1
                                    user.save()
                                    fuser.save()
                                    Follow.objects.create(from_uid=user,
                                                        to_uid=fuser)
                                    break
                            except DatabaseError:
                                user.num_follow = num1
                                fuser.num_followed = num2
                    return JsonResponse({'code':100})
            except KeyError:
                return JsonResponse({'code':301})
        except KeyError:
            return JsonResponse({'code':302})
    elif req.method == 'POST':
        data = json.loads(req.body)
        try:
            uid_t = int(req.session['uid'])
            fid = int(data['fid'])
            uid = int(data['uid'])
            if uid == uid_t:
            # if True:
                while True:
                    try:
                        user = User.objects.get(uid=uid)
                        fuser = User.objects.get(uid=fid)
                    except User.DoesNotExist: #不存在user 
                        return JsonResponse({'code':400}) # 请忽略
                    num1 = user.num_follow
                    num2 = fuser.num_followed
                    try:
                        follow = Follow.objects.get(from_uid=user, to_uid=fuser)
                        try:
                            with transaction.atomic():
                                user.num_follow = num1 - 1
                                fuser.num_followed = num2 - 1
                                user.save()
                                fuser.save()
                                follow.delete()
                                break
                        except DatabaseError:
                            user.num_follow = num1
                            fuser.num_followed = num2
                    except Follow.DoesNotExist:
                        return JsonResponse({'code':200}) # 已经unfollow
                return JsonResponse({'code':100})
            else:
                return JsonResponse({'code': 302})    
        except Exception:
            return JsonResponse({'code': 302}) # 没有对应值 异常

# 浏览 seen pass test
@csrf_exempt
@transaction.atomic
def seen(req):
    if req.method == 'GET':
        try:
            bid = int(req.GET.get('bid'))
        except KeyError:
            return JsonResponse({'code':400})
        while True:
            try:
                bbs = Bbs.objects.get(bid=bid)
            except Bbs.DoesNotExist:
                return JsonResponse({'code':400})
            num = bbs.num_seen
            try:
                with transaction.atomic():
                    bbs.num_seen = num + 1
                    bbs.save()
                    break
            except DatabaseError:
                bbs.num_seen = num
        response ={}
        response['code'] = 100
        response['liked'] = False
        response['stared'] = False
        try:
            uid = req.session['uid']
            try:
                user = User.objects.get(uid=uid)
                try:
                    user.like.get(bid=bid)
                    response['liked'] = True
                except Bbs.DoesNotExist:
                    pass
                try:
                    user.star.get(bid=bid)
                    response['stared'] = True
                except Bbs.DoesNotExist:
                    pass
            except User.DoesNotExist:
                pass
        except KeyError:
            pass
        return JsonResponse(response)

# 用户信息
@csrf_exempt
def info(req):
    if req.method=='GET':
        try:
            uid = req.GET.get('uid')
        except IndexError:
            return JsonResponse({'code': 303})
        response = {}
        user = User.objects.get(uid=uid)
        response['messsage'] = {}
        response['messsage']['uname'] = user.uname
        response['messsage']['email'] = user.email
        response['statistics'] = {}
        response['statistics']['num_follow'] = user.num_follow
        response['statistics']['num_followed'] = user.num_followed
        response['statistics']['num_post'] = user.post.all().count()
        response['statistics']['num_like'] = Like.objects.filter(uid=user).count()
        response['statistics']['num_star'] = Star.objects.filter(uid=user).count()
        response['statistics']['num_reply'] = user.reply.all().count()
        response['code'] = 100
        return JsonResponse(response)

# 按uid拿post
@csrf_exempt
def get_post(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result = user.post.all().only('bid').order_by('pk')
            paginator = Paginator(result, pageSize)
            response = {}
            response['total'] = paginator.count
            try:
                bbss = paginator.page(page)
            except PageNotAnInteger:
                bbss = paginator.page(1)
            except EmptyPage:
                bbss = paginator.page(paginator.num_pages)
            response['list'] = json.loads(serializers.serialize("json", bbss))
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})
# 按uid拿like
@csrf_exempt
def get_like(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result =Like.objects.filter(uid=user).only('bid').order_by('pk')
            response = {}
            if result.count() > 0:
                bns=None
                for i in result:
                    ans = Bbs.objects.filter(bid=i.bid.bid)
                    if bns ==None: bns = ans
                    else: bns = bns.union(ans)
                paginator = Paginator(bns, pageSize)
                response['total'] = paginator.count
                try:
                    bbss = paginator.page(page)
                except PageNotAnInteger:
                    bbss = paginator.page(1)
                except EmptyPage:
                    bbss = paginator.page(paginator.num_pages)
                response['list'] = json.loads(serializers.serialize("json", bbss))
            else:
                response['total'] = 0
                response['list'] = []
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})
# 按uid拿star
@csrf_exempt
def get_star(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result = Star.objects.filter(uid=user).only('bid').order_by('pk')
            response = {}
            if result.count() > 0:
                bns=None
                for i in result:
                    ans = Bbs.objects.filter(bid=i.bid.bid)
                    if bns ==None: bns = ans
                    else: bns = bns.union(ans)
                paginator = Paginator(bns, pageSize)
                response['total'] = paginator.count
                try:
                    bbss = paginator.page(page)
                except PageNotAnInteger:
                    bbss = paginator.page(1)
                except EmptyPage:
                    bbss = paginator.page(paginator.num_pages)
                response['list'] = json.loads(serializers.serialize("json", bbss))
            else:
                response['total'] = 0
                response['list'] = []
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})
# 按uid拿reply
@csrf_exempt
def get_reply(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result = user.reply.all().only('bid').order_by('pk')
            paginator = Paginator(result, pageSize)
            response = {}
            response['total'] = paginator.count
            try:
                bbss = paginator.page(page)
            except PageNotAnInteger:
                bbss = paginator.page(1)
            except EmptyPage:
                bbss = paginator.page(paginator.num_pages)
            response['list'] = json.loads(serializers.serialize("json", bbss))
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})

# 按uid拿follow # 注意不能暴露密码
@csrf_exempt
def get_follow(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result = Follow.objects.filter(from_uid=user).order_by('pk')
            response = {}
            if result.count() > 0:
                bns=None
                for i in result:
                    ans = User.objects.filter(uid=i.to_uid.uid)
                    if bns ==None: bns = ans
                    else: bns = bns.union(ans)
                paginator = Paginator(bns, pageSize)
                response['total'] = paginator.count
                try:
                    bbss = paginator.page(page)
                except PageNotAnInteger:
                    bbss = paginator.page(1)
                except EmptyPage:
                    bbss = paginator.page(paginator.num_pages)
                print(type(bbss))
                response['list'] = json.loads(serializers.serialize("json", bbss))
            else:
                response['total'] = 0
                response['list'] = []
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})

# 按uid拿followed
@csrf_exempt
def get_followed(req):
    if req.method == "GET":
        try:
            page = int(req.GET.get('page'))
            pageSize = int(req.GET.get('pageSize'))
            uid = int(req.GET.get('uid'))
            user = User.objects.get(uid=uid)
            result = Follow.objects.filter(to_uid=user).order_by('pk')
            response = {}
            if result.count() > 0:
                bns=None
                for i in result:
                    ans = User.objects.filter(uid=i.from_uid.uid)
                    if bns ==None: bns = ans
                    else: bns = bns.union(ans)
                paginator = Paginator(bns, pageSize)
                response['total'] = paginator.count
                try:
                    bbss = paginator.page(page)
                except PageNotAnInteger:
                    bbss = paginator.page(1)
                except EmptyPage:
                    bbss = paginator.page(paginator.num_pages)
                response['list'] = json.loads(serializers.serialize("json", bbss))
            else:
                response['total'] = 0
                response['list'] = []
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})

#查询
@csrf_exempt
def search(req):
    if req.method == "POST":
        try:
            data = json.loads(req.body)
            pageSize = data['pageSize']
            page = data['page']
            searchtext = data["searchtext"]
            result = Bbs.objects.filter(title__contains=searchtext).only('bid').order_by('pk')
            paginator = Paginator(result, pageSize)
            response = {}
            response['total'] = paginator.count
            try:
                bbss = paginator.page(page)
            except PageNotAnInteger:
                bbss = paginator.page(1)
            except EmptyPage:
                bbss = paginator.page(paginator.num_pages)
            response['list'] = json.loads(serializers.serialize("json", bbss))
            response['code'] = 100
            return JsonResponse(response)
        except KeyError:
            return JsonResponse({'code':301})

#删帖
@csrf_exempt
@transaction.atomic
def deleteBbs(req):
    if req.method=='GET':
        return JsonResponse({'code':400})#不该存在
    elif req.method == "POST":
        data = json.loads(req.body)
        try:
            delete_bid = data["delete_bid"]
            result = Bbs.objects.filter(bid=delete_bid)
            Bbsuid = None
            if result.count()>0:
                for i in result: 
                    Bbsuid = i.uid.uid 
                    break
                if req.session['uid'] == data['uid'] and req.session['uid'] == Bbsuid:
                # if True:
                    maxnum = 10#最多试十次
                    while maxnum>0:
                        maxnum-=1
                        try:
                            with transaction.atomic():
                                result.delete()
                                break
                        except:
                            maxnum=0
                            break
                    if maxnum>0:  
                        return JsonResponse({'code':100})#删除成功
                    else:
                        return JsonResponse({'code':200})#删除失败
                else:
                        return JsonResponse({'code':201})#id不匹配
            else:
                return JsonResponse({'code':300})#回复不存在
        except KeyError:
            return JsonResponse({'code':301})
        
#删回复
@csrf_exempt
@transaction.atomic
def deleteRespond(req):
    data = json.loads(req.body)
    if req.method=='GET':
        return JsonResponse({'code':400})#不该存在
    if req.method == "POST":
        try:
            delete_rid = data["delete_rid"]
            result = Respond.objects.filter(rid=delete_rid)
            Responduid=None
            if result.count()>0:
                for i in result: 
                    Responduid = i.uid.uid 
                    break
                #会话uid=回复uid,绘画uid=前端传输uid
                if req.session['uid'] == data['uid'] and req.session['uid'] == Responduid:
                # if True:
                    maxnum = 10
                    while maxnum>0:
                        maxnum-=1
                        try:
                            with transaction.atomic():
                                result.delete()
                                break
                        except:
                            maxnum=0
                            break
                    if maxnum>0:  
                        return JsonResponse({'code':100})#删除成功
                    else:
                        return JsonResponse({'code':200})#删除失败
                else:
                        return JsonResponse({'code':201})#id不匹配
            else:
                return JsonResponse({'code':300})#回复不存在
        except KeyError:
            return JsonResponse({'code':301})

#删用户
@csrf_exempt
def deleteUser(req):
    if req.method=='GET':
        uid = int(req.GET.get('uid'))
        user = User.objects.get(uid=uid)
        try:
            user.delete()
            return JsonResponse({'code':100})
        except DatabaseError:
            return JsonResponse({'code':200})
        