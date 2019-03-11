from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic import View,DeleteView,ListView
from .forms import *
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

class HomeView(View):
    template_name="Tube/home.html"
    def get( self,request):
        clan=Clan.objects.all()
        return render(request,self.template_name,{'clans':clan})
class ClanCreateView(LoginRequiredMixin,View):
    template_name="Tube/clan_create.html"
    def get(self,request):
        form=ClanCreationForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=ClanCreationForm(request.POST)
        if form.is_valid():
            clan=Clan()
            url=form.cleaned_data.get('url')
            url=url.replace('watch?v','embed/')
            url=url.replace("=","")
            clan.leader=request.user
            clan.name=form.cleaned_data.get('name')
            clan.url=url
            clan.description=form.cleaned_data.get('description')
            clan.tag=form.cleaned_data.get('tag')
            clan.save()
            

            
            return redirect('link-create',pk=clan.pk)
        return render(request,self.template_name,{'form':form})    
class ClanEditView(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name="Tube/clan_create.html"
    def test_func(self):
        clan=get_object_or_404(Clan,pk=self.kwargs['pk'])
        return clan.leader.pk==self.request.user.pk
    def get(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk)
        form=ClanCreationForm(
            initial={
                'name':clan.name,
                'description':clan.description,
                
                'tag':clan.tag,
                'url':clan.url

            },
            instance=clan
        )
        return render(request,self.template_name,{'form':form,'edit':True,'pk':clan.pk})
    def post(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk)
        form=ClanCreationForm(request.POST,instance=clan)

        
        if form.is_valid():
            clan=Clan()
            clan.leader=request.user
            clan.name=form.cleaned_data.get('name')
            clan.description=form.cleaned_data.get('description')
            clan.tag=form.cleaned_data.get('tag')
            
            clan.url=form.cleaned_data.get('url')
            clan.save()
           
            return redirect('detail-view',pk=clan.pk)
            
        return render(request,self.template_name,{'form':form,'edit':True,'pk':clan.pk})
        
class ClanDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
     template_name="Tube/clan_delete.html"
     def test_func(self):
         clan=get_object_or_404(Clan,pk=self.kwargs.get('pk'))
         return self.request.user.pk==clan.leader.pk

     model=Clan
     context_object_name='clan'
     success_url=reverse_lazy('home')
class LinkCreateView(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name="Tube/link_create.html"
    def test_func(self):
        clan=get_object_or_404(Clan,pk=self.kwargs['pk'])
        return self.request.user.pk==clan.leader.pk
    def get(self,request,pk):
       
        form=LinkCreationForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk)
        
        form=LinkCreationForm(request.POST)
        if form.is_valid():
            link=Link()
            link.title=form.cleaned_data.get('title')
            link.link=form.cleaned_data.get('link')
            link.description=form.cleaned_data.get('description')
            link.clan=clan
            link.save()
            return redirect('detail-view',pk=clan.pk)
          
           
        return render(request,self.template_name,{'form':form})

class LinkEditView(LoginRequiredMixin,UserPassesTestMixin,View):
        template_name="Tube/link_create.html"
        def test_func(self):
            link=get_object_or_404(Link,pk=self.kwargs['pk'])
            return self.request.user==link.clan.leader
        def get(self,request,pk):
            link=get_object_or_404(Link,pk=pk)
            form=LinkCreationForm(
                initial={
                    'title':link.title,
                    'description':link.description,
                    'link':link.link
                }
            )
            return render(request,self.template_name,{'form':form,'edit':True,'pk':link.clan.pk}) 
        
        def  post(self,request,pk):
            link=get_object_or_404(Link,pk=pk)
            form=LinkCreationForm(request.POST)
            if form.is_valid():
                link.title=form.cleaned_data.get('title')
                link.link=form.cleaned_data.get('link')  
                link.description=form.cleaned_data.get('description')
                link.save()
                return redirect('detail-view',pk=link.clan.pk)
            return render(request,self.template_name,{'form':form,'edit':True,'pk':link.clan.pk})    
                    
        
    
          
class LinkDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    template_name="Tube/link_delete.html"
    def test_func(self):
        link=get_object_or_404(Link,pk=self.kwargs['pk'])
        return self.request.user.pk==link.clan.leader.pk
    def get(self,request,pk):
        link=get_object_or_404(Link,pk=pk)
        return render(request,self.template_name,{'link':link,'pk':link.clan.pk})
    def post(self,request,pk):
        link=get_object_or_404(Link,pk=pk)
        pk=link.clan.pk
        link.delete()
        return render(request,self.template_name,{'link':link,'pk':link.clan.pk})    
class ProfileView(View):
    template_name="Tube/profile.html"
    def get(self,request,pk):
        re_user=get_object_or_404(User,pk=pk)
        tab=request.GET.get('tab')
        if(tab =='clans'):
            return render(request,self.template_name,{'re_user':re_user,'clans':re_user.clan_set.all(),'clan_view':True})
        elif(tab == 'liked'):
                return render(request,self.template_name,{'re_user': re_user,'clans':re_user.likes_set.all(),'like_view':True})
        elif(tab=='followers'):
                return render(request,self.template_name,{'re_user':re_user,'followers':re_user.profile.followers.all(),'followers_view':True}) 
        elif(tab=='following'):
                return render(request,self.template_name,{'re_user':re_user,'following':re_user.followers_set.all(),'following_view':True})  
         
        else:
            return render(request,self.template_name,{'re_user':re_user,'clans':re_user.clan_set.all,'view':True}) 
class ClanDetailView(View):
      template_name="Tube/clan_detail.html"
      def get(self,request,pk):
          clan=get_object_or_404(Clan,pk=pk)
          tab=request.GET.get('tab')
          if(tab =='clandata'):
              return render(request,self.template_name,{'clanview':True,'clan':clan})
          elif(tab=='members'):
              return render(request,self.template_name,{'clan':clan,'memberview':True}) 
          elif(tab=='comments'):
              return render(request,self.template_name,{'clan':clan,'commentview':True,'comments':clan.comment_set.all(),'form':CommentForm()})    
          else:  
               return render(request,self.template_name,{'clan':clan})   
        
             
          

class NotificationView(LoginRequiredMixin,ListView):
    template_name="Tube/notifs.html"
    context_object_name='notifs'
    def  get_queryset(self):
        return self.request.user.receivers_set.all()

class  CategoryView(LoginRequiredMixin,View):
        template_name = 'Tube/category.html'

        def get(self,request):
            if request.GET.get('tag') == None:
                return HttpResponseRedirect('/clan/category/?tag')
            clans = Clan.objects.filter(tag__istartswith=request.GET.get('tag'))
            if clans is None:
                return render(request,self.template_name,{'clans':None})    
            return render(request,self.template_name,{'clans':clans})
        
class SearchView(LoginRequiredMixin,View): 
      template_name = 'Tube/search.html'

      def get(self, request):
         clans = Clan.objects.annotate(search=SearchVector('name','description')).filter(search=request.GET.get('q'))
         return render(request,self.template_name,{'clans':clans})
    
class RegisterView(View):
     template_name="Tube/register.html"     
     def get(self,request):
         form=RegisterForm()
         return render(request,self.template_name,{'form':form})
     def post(self,request):
         form=RegisterForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('login')
         return render(request,self.template_name,{'form':form})        
''' Ajax Stuffs'''
@csrf_exempt
def join(request):
    
    if request.method == "POST":
        clan=get_object_or_404(Clan,pk=json.loads(request.body).get('pk'))
        if request.user in clan.members.all():
            clan.members.remove(request.user)
            return JsonResponse({"member":False})
        else:
                clan.members.add(request.user)
                notifs=Notifications(sender=request.user,receiver=clan.leader,joined=True,clan=clan)
                notifs.save()

                return JsonResponse({'member':True,'name':clan.name})    
@csrf_exempt
def remove(request):
    if request.method=='POST':
        
        clan=get_object_or_404(Clan,pk=json.loads(request.body).get('pk'))
        print(request.user.clan.member)
       
        clan.members.remove(request.user.clan.member)
    
        return JsonResponse({'removed':True})      
@csrf_exempt
def follow(request):
    if request.method == 'POST' :
       re_user=get_object_or_404(User,pk=json.loads(request.body).get('pk'))
    if request.user in re_user.followers.all():
           re_user.followers.remove(request.user)
           return JsonResponse({'followed':False})
    else:
          re_user.followers.add(request.user)
          notifs=Notifications(sender=request.user,receiver=re_user,followed=True)
          notifs.save()
          return JsonResponse({'followed':True})   
@csrf_exempt
def like(request):
    if request.method == 'POST':
        clan=get_object_or_404(Clan,pk=json.loads(request.body).get('pk'))
        if request.user in clan.likes.all():
            clan.likes.remove(request.user)
            return JsonResponse({'liked':False})
        else:
            clan.likes.add(request.user)
            notif=Notifications(sender=request.user,receiver=clan.leader,liked=True)
            notif.save()
            return JsonResponse({'liked': True})    
       
@csrf_exempt
def remove_notif(request):
    notif = get_object_or_404(Notifications,pk=json.loads(request.body).get('pk'))
    if notif.receiver != request.user:
        return JsonResponse({'removed':'Invalid'})
    notif.delete()
    return JsonResponse({'removed':True})   
@csrf_exempt
def remove_all(request):
    request.user.receivers_set.all().delete()
    return JsonResponse({'removed':True})
class CommentView(LoginRequiredMixin,View):
    template_name='Tube/clan_detail.html'
    def get(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk)
        form=CommentForm()
        return render(request,self.template_name,{'form':form,'clan':clan})
    def post(self,request,pk):
        clan=get_object_or_404(Clan,pk=pk) 
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=Comment()
            comment.title=form.cleaned_data.get('title')
            comment.content=form.cleaned_data.get('content')
            comment.clan=clan
            comment.author=request.user
            comment.save()
        return render(request,self.template_name,{'form':form,'clan':clan})    




        


    