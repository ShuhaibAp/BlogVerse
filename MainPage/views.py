from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView,DetailView,ListView,CreateView,UpdateView,View
from .forms import *
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.

class HomePage(TemplateView):
    template_name="HomePage.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_blogs"] = Blog.objects.all().order_by('-date')[:6]

        context["tech_blogs"] = Blog.objects.filter(category='Technology').order_by('-date')[:2]
        context["side_tech_blogs"] = Blog.objects.filter(category='Technology').order_by('-date')[2:5]
        context["end_tech_blogs"] = Blog.objects.filter(category='Technology').order_by('-date')[5:9]

        context["main_anime_blogs"] = Blog.objects.filter(category='Anime').order_by('-date')[:2]
        context["side_anime_blogs"] = Blog.objects.filter(category='Anime').order_by('-date')[2:5]
        context["end_anime_blogs"] = Blog.objects.filter(category='Anime').order_by('-date')[5:9]

        context["story_blogs"] = Blog.objects.filter(category='Story').order_by('-date')[:9]

        context["vert_sports_blogs"] = Blog.objects.filter(category='Sports').order_by('-date')[:1]
        context["horiz_sports_blogs"] = Blog.objects.filter(category='Sports').order_by('-date')[1:2]
        context["two_sports_blogs"] = Blog.objects.filter(category='Sports').order_by('-date')[2:4]
        return context

class NewProfile(View):
    def get(self,request):
        form=ProfileForm()
        return render(request,"Profile_add.html",{"form":form})
    def post(self,request):
        form_data=ProfileForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            profile=form_data.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
        messages.error(request,"Please provide valid inputs!!")
        return render(request,"AddProfile.html",{"form":form_data})

class NewBlog(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "Blog_add.html", {"form": form})
    
    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to create a blog.")
            return redirect('log')
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            profiles = Profile.objects.filter(user=request.user)
            if profiles.exists():
                blog.profile = profiles.first()
            else:
                messages.error(request, "Profile does not exist. Please create a profile first.")
                return render(request, "AddBlog.html", {"form": form})
            blog.save()
            return redirect('home')
        messages.error(request, "Please provide valid inputs.")
        return render(request, "AddBlog.html", {"form": form})


class BlogList(ListView):
    template_name = "blog_list.html"
    context_object_name = 'blogs'
    def get_queryset(self):
        category = self.kwargs.get('cat')
        return Blog.objects.filter(category=category)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.kwargs.get('cat')
        return context

class ProfileView(DetailView):
    template_name="profile_view.html"
    context_object_name="profile"
    def get_object(self):
        user=get_object_or_404(User, username=self.kwargs.get('user'))
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        profile=self.get_object()
        context['user_blogs']=Blog.objects.filter(profile=profile)
        return context

class UpdateProfile(UpdateView):
    template_name="profile_update.html"
    form_class=ProfileForm
    queryset=Profile.objects.all()
    pk_url_kwarg='user'

    def get_object(self):
        user=get_object_or_404(User, username=self.kwargs['user'])
        return get_object_or_404(Profile, user=user)

    def get_success_url(self):
        return reverse_lazy('pview', kwargs={'user': self.kwargs['user']})

def DeleteProfile(request, user):
    user=get_object_or_404(User, username=user)
    profile=get_object_or_404(Profile, user=user)
    profile.delete()
    return redirect('padd')

class BlogDetail(DetailView):
    model = Blog
    template_name = "blog_details.html"
    context_object_name = "blog_det"
    pk_url_kwarg = 'id'

    def get_object(self):
        return get_object_or_404(Blog, id=self.kwargs['id'])