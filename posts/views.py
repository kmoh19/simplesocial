from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404,HttpResponse
from django.views import generic
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib import messages


from django.contrib.auth import get_user_model
# Create your views here.


User=get_user_model()


class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    select_related=('user','group')# allows you to select the user and the group the post is related to
    
    
class UserPosts(generic.ListView):
    model = models.Post
    template_name ='posts/user_post_list.html'
    
    def get_queryset(self):
        
        try:
            self.post_user=User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    
    def get_context_data(self, **kwargs):
        
        context =super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context
        
class PostDetail(SelectRelatedMixin,generic.DetailView):
    model =models.Post
    select_related=('user','group')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
    
    
    
class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    
    fields =['message','custom_viz','D3_version','js_file_1','js_file_2','data_file','group']
    model = models.Post
    
    def form_valid(self,form):
        self.object =form.save(commit=False)
        self.object.user= self.request.user
        self.object.save()
        return super().form_valid(form)
    
    
# class CreateVizPost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
#     
#     fields =['message','custom_viz','group']
#     model = models.Post
#     
#     def form_valid(self,form): #form validation and setting user to active user
#         self.object =form.save(commit=False)
#         self.object.user= self.request.user
#         self.object.save()
#         return super().form_valid(form)
    
    
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    
    model = models.Post
    select_related =('user','group')
    success_url = reverse_lazy('posts:all')
    
    def get_queryset(self):
        queryset =super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
    
    
    
class UpdatePost(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    model =models.Post
    fields =('message','custom_viz','D3_version','data_file','js_file_1','js_file_2','group')
    select_related =('user','group')
   
    
    def get(self, request, *args, **kwargs):
        upd_obj=generic.UpdateView.get(self, request, *args, **kwargs)
        if request.user.id==upd_obj.context_data['post'].user.id:
            return generic.UpdateView.get(self, request, *args, **kwargs)#generic.UpdateView is same as calling super()
        else:
            return HttpResponse('<h1>no way Jose!</h1>')