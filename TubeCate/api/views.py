from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import SuspiciousOperation
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Tube.models import Clan, Link,DeviceId
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
import datetime
import pytz
import json
from Tube.models import Notifications
from oauth2client.service_account import ServiceAccountCredentials
import threading
import requests
def get_token():
        SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('api/key.json',SCOPES)
        access_token_info = credentials.get_access_token()
        return access_token_info.access_token
def like_notification(sender,receiver,name):
    d=DeviceId.objects.get(user=receiver)
    device_id=d.device_id

    headers={
        "Content-Type":'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    body={
        "message":{
        "token" : str(device_id),
        "notification" : {
        "body" : f"",
        "title" : "{name} was liked by {sender.username}",
        },
          "android": {
            "notification": {
                "sound": "default"
            }
        },

        }
    }
    response = requests.post('https://fcm.googleapis.com/v1/projects/tubecate-dzhz1/messages:send',
    json=body,
    headers=headers
    
    )
    print(response)
    print(device_id)
def join_notification(sender,receiver,name):
    device_id=receiver.profile.device_id
    headers={
        "Content-Type":'application/json',
        'Authorization': f'Bearer {get_token()}'
    }
    body={
        "message":{
        "token" : str(device_id),
        "notification" : {
        "body" : f"",
        "title" : "{name} was liked by {sender.username}",
        },
          "android": {
            "notification": {
                "sound": "default"
            }
        },

        }
    }
    response = requests.post('https://fcm.googleapis.com/v1/projects/tubecate-dzhz1/messages:send',
    json=body,
    headers=headers
    
    )
    print(response)

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if not user:
            raise SuspiciousOperation
        else:
            login(request, user)
            
            user.save()
            d=DeviceId()
            d.user=user
            d.device_id=request.POST.get('deviceid')
            print(d.device_id)
            d.save()
            token, dummy = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username, 'email': user.email, 'pk': user.pk})


class RegisterView(APIView):
    def post(self, request):
        if User.objects.filter(username=request.POST.get('username')).exists() or User.objects.filter(email=request.POST.get('email')).exists():
            raise SuspiciousOperation
        user = User()
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()

        return Response()


class ClanCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        if Clan.objects.filter(name=request.POST.get('name')).exists():
            raise SuspiciousOperation
        clan = Clan()
        clan.name = request.POST.get('name')
        clan.description = request.POST.get('description')
        clan.url = request.POST.get('url')
        clan.tag = request.POST.get('tag')
        clan.leader = request.user
        clan.save()
        for follower in request.user.followers.all():
            notif=Notifications(clan=True,sender=request.user,receiver=follower)
            notif.save()
        return Response({'pk': clan.pk})


class LinkCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, pk):
        clan = get_object_or_404(Clan, pk=pk)
        if not(clan.leader == request.user):
            raise SuspiciousOperation
        else:
            link = Link()
            link.title = request.POST.get('title')
            link.description = request.POST.get('description')
            link.link = request.POST.get('link')
            link.clan = Clan.objects.get(pk=request.POST.get('pk'))
            link.save()
        return Response()


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        tz = pytz.timezone('Asia/Kolkata')
        return Response(
            {'clan': [
                {
                    'pk': clan.pk,
                    'name': clan.name,
                    'description': clan.description,
                    'url': clan.url,
                    'tag': clan.tag,
                    'leader': clan.leader.username,
                    'likes_count': clan.likes.count(),
                    'members_count': clan.members.count(),
                    'link_count': clan.link_set.count(),
                    'date_posted': clan.date_posted.astimezone(tz).strftime('%c'),
                    'liked': request.user in clan.likes.all(),
                    'member': request.user in clan.members.all(),


                }
                for clan in Clan.objects.all().order_by('-date_posted')]}
        )


class ClanDetailView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        clan = Clan.objects.get(pk=pk)
        links = clan.link_set.all()
        tz = pytz.timezone('Asia/Kolkata')

        return Response(

            {'is_leader': request.user == clan.leader,
                'pk': clan.pk,
                'name': clan.name,
                'description': clan.description,
                'url': clan.url,
                'tag': clan.tag,
                'leader': clan.leader.username,
                'likes_count': clan.likes.count(),
                'members_count': clan.members.count(),
                'link_count': clan.link_set.count(),
                'date_posted': clan.date_posted.astimezone(tz).strftime('%c'),
                'liked': request.user in clan.likes.all(),

                'member': request.user in clan.members.all(),
                'links': [
                    {
                        'title': link.title,
                        'description': link.description,
                        'link': link.link

                    }
                    for link in links],

                'comments': [
                    {
                        'title': comment.title,
                        'content': comment.content,
                        'author': comment.author.username,
                    }
                    for comment in clan.comment_set.all()],
                'members': [
                    {
                        'pk': member.pk,
                        'name': member.username
                    }
                    for member in clan.members.all()]})


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        clan = get_object_or_404(Clan, pk=json.loads(request.body)['pk'])
        if request.user in clan.likes.all():
            clan.likes.remove(request.user)
            
            return Response({'liked': False})
        else:
            clan.likes.add(request.user)
            notif=Notifications(sender=request.user,receiver=clan.leader,liked=True,clan=clan)
            notif.save()
            clan.save()
            like_notification(sender=request.user,receiver=clan.leader,name=clan.name)
            return Response({'liked': True})


class MemberView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, pk):

        clan = get_object_or_404(Clan, pk=pk)
        if request.user == clan.leader:
            raise SuspiciousOperation
        if request.user in clan.members.all():
            clan.members.remove(request.user)

            return Response({'member': False})
        else:
            clan.members.add(request.user)
            clan.save()
            notif=Notifications(sender=request.user,receiver=clan.leader,joined=True,clan=clan)
            notif.save()
            return Response({'member': True})


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return Response({
            'is_same': request.user == user,
            'name': user.username,
            'clan_count': user.clan_set.count(),
            'email': user.email,

            'clans': [
                {
                    'clan_pk': clan.pk,
                    'name': clan.name,
                    'member_count': clan.members.count(),
                    'leader': clan.leader.username,
                    'description': clan.description,
                    'url': clan.url,
                    'tag': clan.tag,



                }
                for clan in user.clan_set.all()],

            'followers': [
                {'name': follower.username,
                 'pk': follower.pk


                 }

                for follower in user.profile.followers.all()],

            'following': [
                {
                    'name': following.user.username,
                    'pk': following.pk

                }

                for following in user.followers_set.all()],

            'likes': [{
                'pk': clan.pk,
                'name': clan.name,
                'member_count': clan.members.count(),
                'leader': clan.leader.username,
                'leader_pk': clan.leader.pk,
                'description': clan.description,
                'tag': clan.tag,
                'date':clan.date_posted

            }



                for clan in user.likes_set.all().order_by('-date_posted')]})


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.user == user:
            raise SuspiciousOperation
        if request.user in user.profile.followers.all():
            user.profile.followers.remove(request.user)
            
            return Response({'followed': False})
        else:
            user.profile.followers.add(request.user)
            notif=Notifications(sender=request.user,receiver=user,followed=True)
            notif.save()
            return Response({'followed': True})


class TagSearchView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        tag = request.POST.get('tag')
        clan = Clan.objects.filter(tag=tag).order_by('-date_posted')
        if clan == None:
            raise SuspiciousOperation
        else:
            return Response([
                {
                    'name': clan.name,
                    'pk': clan.pk,
                    'description': clan.description,
                    'tag': clan.tag,
                    'leader': clan.leader.username,
                    'member_count': clan.members.count(),
                    'likes_count':clan.likes.count()


                }


                for clan in clan])
class SearchView(APIView):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,) 
    def post(self,request):
        clan=Clan.object.get(name=request.POST.get('name'))    
        return Response([
                {
                    'name': clan.name,
                    'pk': clan.pk,
                    'description': clan.description,
                    'tag': clan.tag,
                    'leader': clan.leader.username,
                    'member_count': clan.members.count(),
                    'likes_count':clan.likes.count()


                }


                for clan in clan])
class NotificationView(APIView):
    authentication_classes=(TokenAuthentication,) 
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        notif=Notifications.objects.all()
        for notif in notif:    

                if notif.liked:
                    return Response(
                        {
                            'pk':notif.clan.pk,
                            'message':f'{notif.sender.username} liked your Clan {notif.clan}',
                            'type':'clan'

                        }
                    )
                elif notif.followed:
                    return Response(
                        {
                        'pk':notif.sender.pk,
                        'message':f'{notif.sender.username} followed you' ,
                        'type':'user'

                        }
                )   
                elif notif .joined:
                    return Response(
                        {
                            'pk':notif.clan.pk,
                            'message':f'{notif.sender.username} joined your Clan {notif.clan}',
                            'type':'clan'
                        }
                    )
                else:
                    return Response({'null':True})    
class CommentCreateView(APIView):
    pass
