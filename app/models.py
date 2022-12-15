from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.AutoField(primary_key=True)
    uname=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    email=models.CharField(max_length=40)
    created_time=models.CharField(max_length=50)
    num_followed=models.IntegerField(default=0)
    num_follow=models.IntegerField(default=0) # 其实不需要这个值，我们可以直接User.follow.all().count() 因为原子操作始终是性能瓶颈
    post=models.ManyToManyField('Bbs',related_name="posted")
    reply=models.ManyToManyField('Respond',related_name="replied")
"""
    uname=
    pwd=
    email=
    created_time=
    num_followed=
    num_follow=
    follow=
    post=
    reply=
"""
class Bbs(models.Model):
    bid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    uname=models.CharField(max_length=20)
    title=models.CharField(max_length=100)
    created_time=models.CharField(max_length=50)
    reply_time=models.CharField(max_length=50)
    content=models.CharField(max_length=400)
    num_reply=models.IntegerField(default=0)
    num_seen=models.IntegerField(default=0)
    num_star=models.IntegerField(default=0)
    num_like=models.IntegerField(default=0)
"""
    uid=
    title=标题
    created_time=创建时间
    content=内容
    num_reply=回复人数
    num_seen=浏览数
    num_star=被喜欢数
"""
class Respond(models.Model):
    rid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    uname=models.CharField(max_length=20)
    rename=models.CharField(max_length=20)
    bid=models.ForeignKey(Bbs,on_delete=models.CASCADE)
    content=models.CharField(max_length=300)
    created_time=models.CharField(max_length=50)
"""
    rid=
    uid=
    bid=
    responded_rid=
    content=
    created_time=
"""

class Follow(models.Model):
    fid=models.AutoField(primary_key=True)
    from_uid=models.ForeignKey(User,related_name='fuid', on_delete=models.CASCADE)
    to_uid=models.ForeignKey(User,related_name='tuid', on_delete=models.SET_NULL, blank = True,null=True)

class Like(models.Model):
    lid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(User, on_delete=models.CASCADE)
    bid=models.ForeignKey(Bbs,on_delete=models.CASCADE)

class Star(models.Model):
    sid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(User, on_delete=models.CASCADE)
    bid=models.ForeignKey(Bbs,on_delete=models.CASCADE)