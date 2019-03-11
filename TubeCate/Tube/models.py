from django.db import models

from django.contrib.auth.models import User
class Clan(models.Model):
    leader=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    Link=models.URLField(null=True,blank=True)
    members=models.ManyToManyField(User,related_name='members_set')
    likes=models.ManyToManyField(User,related_name='likes_set')
    url=models.URLField()
    tag=models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.name
    

class Notifications(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    liked=models.BooleanField(default=False)
    joined=models.BooleanField(default=False)
    followed=models.BooleanField(default=False)
    clan=models.ForeignKey(Clan,on_delete=models.CASCADE)
    new_announcement=models.BooleanField(default=False)
    date=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receivers_set',null=True)
   
class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    clan=models.ForeignKey(Clan,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
class Link(models.Model):
    clan=models.ForeignKey(Clan,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.TextField()
    link=models.URLField()
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    img=models.ImageField(default='default.jpg',upload_to='profile_pic')
    followers=models.ManyToManyField(User,related_name='followers_set',symmetrical=False)
User.profile=property(lambda u:Profile.objects.get_or_create(user=u)[0])









