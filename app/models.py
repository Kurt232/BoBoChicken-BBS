from django.db import models

# Create your models here.
class User(models.Model):
    uid=models.AutoField(primary_key=True)
    uname=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    email=models.CharField(max_length=40)
    created_time=models.CharField(max_length=20)
    num_followed=models.IntegerField(default=0)
    num_follow=models.IntegerField(default=0)
    follow=models.ManyToManyField('self',related_name="followed")
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
    title=models.CharField(max_length=50)
    created_time=models.CharField(max_length=20)
    content=models.CharField(max_length=100)
    num_reply=models.IntegerField(default=0)
    num_respond=models.IntegerField(default=0)
    num_star=models.IntegerField(default=0)
    
"""
    uid=
    title=
    created_time=
    content=
    num_reply=
    num_respond=
    num_star=
"""
class Respond(models.Model):
    rid=models.AutoField(primary_key=True)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    bid=models.ForeignKey(Bbs,on_delete=models.CASCADE)
    responded_rid=models.ForeignKey('Respond',on_delete=models.CASCADE)
    content=models.CharField(max_length=300)
    responded_time=models.CharField(max_length=20)





