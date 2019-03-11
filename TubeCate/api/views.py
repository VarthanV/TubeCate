from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.core.exceptions import SuspiciousOperation
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Tube.models import Clan,Link
from django.shortcuts import get_object_or_404
class LoginView(APIView):
    permission_classes=(AllowAny,)

    def post(self,request):
        user=authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if not user:
            raise SuspiciousOperation
        else:    
            token,dummy=Token.objects.get_or_create(user=user) 
            return Response({'token':token.key,'username':user.username,'email':user.email})

class RegisterView(APIView):
    def post(self,request):
        if User.objects.filter(username=request.POST.get('username')).exists() or User.objects.filter(email=request.POST.get('email')).exists():
            raise SuspiciousOperation
        user=User()
        user.username=request.POST.get('username')
        user.email=request.POST.get('email')
        user.set_password(request.POST.get('password'))
        user.save()
        
        return Response() 
class ClanCreateView(APIView):
    permission_classes=(IsAuthenticated,)  
    authentication_classes=(TokenAuthentication,)
    def post(self,request):
        if Clan.objects.filter(name=request.POST.get('name')).exists():
            raise SuspiciousOperation
        clan=Clan() 
        clan.name=request.POST.get('name')
        clan.description=request.POST.get('description')
        clan.url=request.POST.get('url')
        clan.tag=request.POST.get('tag')
        clan.leader=request.user 
        clan.save()
        return Response({'pk':clan.pk})
class LinkCreateView(APIView):
    permission_classes=(IsAuthenticated,) 
    authentication_classes=(TokenAuthentication,) 
    def post(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk)
        if  not(clan.leader==request.user):
            raise SuspiciousOperation
        else:
            link=Link()
            link.title=request.POST.get('title')
            link.description=request.POST.get('description')
            link.link=request.POST.get('link')
            link.clan=Clan.objects.get(pk=request.POST.get('pk'))
            link.save() 
        return Response() 

class HomeView(APIView):
    def get(self,request):
        return Response(
    {'clan':[
        {
         'name':clan.name,
         'description':clan.description,
         'url':clan.url,
         'tag':clan.tag,
         'leader':clan.leader.username, 

        }
     for clan in Clan.objects.all()]}
    )               
             



   



