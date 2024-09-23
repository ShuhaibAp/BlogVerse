from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views import View
from django.views.generic import TemplateView,DetailView,ListView,CreateView,UpdateView,View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from .models import *
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Homepage
class HomePage(LoginRequiredMixin,TemplateView):
    template_name="HomePage.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_blogs"]=Blog.objects.all().order_by('-date')[:6]

        context["tech_blogs"]=Blog.objects.filter(category='Technology').order_by('-date')[:2]
        context["side_tech_blogs"]=Blog.objects.filter(category='Technology').order_by('-date')[2:5]
        context["end_tech_blogs"]=Blog.objects.filter(category='Technology').order_by('-date')[5:9]

        context["main_anime_blogs"]=Blog.objects.filter(category='Anime').order_by('-date')[:2]
        context["side_anime_blogs"]=Blog.objects.filter(category='Anime').order_by('-date')[2:5]
        context["end_anime_blogs"]=Blog.objects.filter(category='Anime').order_by('-date')[5:9]

        context["story_blogs"]=Blog.objects.filter(category='Story').order_by('-date')[:9]

        context["vert_sports_blogs"]=Blog.objects.filter(category='Sports').order_by('-date')[:1]
        context["horiz_sports_blogs"]=Blog.objects.filter(category='Sports').order_by('-date')[1:2]
        context["two_sports_blogs"]=Blog.objects.filter(category='Sports').order_by('-date')[2:4]
        return context
#search 
def blog_search(request):
    query=request.GET.get('search-value')
    blogs=Blog.objects.all()
    if query:
        blogs=blogs.filter( Q(title__icontains=query) | Q(category__icontains=query) | Q(profile__user__username__icontains=query))
    return render(request, 'blog_search.html', {'blogs': blogs, 'query': query})

# Profile Views
class NewProfile(View):
    def get(self,request):
        form=ProfileForm()
        return render(request,"Profile_add.html",{"form":form})
    def post(self,request):
        form_data=ProfileForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            profile=form_data.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('home')
        messages.error(request,"Please provide valid inputs!!")
        return render(request,"AddProfile.html",{"form":form_data})

class ProfileView(LoginRequiredMixin,DetailView):
    template_name="profile_view.html"
    context_object_name="profile"
    
    def get_object(self):
        user=get_object_or_404(User, username=self.kwargs.get('user'))
        return get_object_or_404(Profile, user=user)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        profile=self.get_object()
        # Fetch user blogs
        user_blogs=Blog.objects.filter(profile=profile)
        # Pagination setup
        paginator=Paginator(user_blogs, 5)# Show 5 blogs per page
        page=self.request.GET.get('page')
        
        try:
            blogs_paginated=paginator.page(page)
        except PageNotAnInteger:
            blogs_paginated=paginator.page(1)# If page is not an integer,show the first page
        except EmptyPage:
            blogs_paginated=paginator.page(paginator.num_pages)# If page is out of range, show last page
        context['user_blogs']=blogs_paginated
        return context
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

def FollowProfile(request, profile_id):
    profile=get_object_or_404(Profile, id=profile_id)
    if request.user.profile in profile.followers.all():
        profile.followers.remove(request.user.profile)
    else:
        profile.followers.add(request.user.profile)
    return redirect('pview', user=profile.user.username)

# Blog Views
class NewBlog(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to create a blog.")
            return redirect('log')
        if not Profile.objects.filter(user=request.user).exists():
            return redirect('padd')
        form=BlogForm()
        return render(request, "Blog_add.html", {"form": form})
    
    def post(self, request):
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            profiles=Profile.objects.filter(user=request.user)
            if profiles.exists():
                blog.profile=profiles.first()
            else:
                messages.error(request, "Profile does not exist. Please create a profile first.")
                return render(request, "AddBlog.html", {"form": form})
            blog.save()
            return redirect('home')
        messages.error(request, "Please provide valid inputs.")
        return render(request, "AddBlog.html", {"form": form})

def BlogDelete(request,*args,**kwargs):
    bid=kwargs.get('id')
    Blog.objects.get(id=bid).delete()
    return redirect('home')

class BlogList(ListView):
    template_name="blog_list.html"
    context_object_name='blogs'
    paginate_by=6
    def get_queryset(self):
        category=self.kwargs.get('cat')
        return Blog.objects.filter(category=category)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['selected_category']=self.kwargs.get('cat')
        return context

class BlogDetail(DetailView):
    model=Blog
    template_name="blog_details.html"
    context_object_name="blog_det"
    pk_url_kwarg='id'

    def get_object(self):
        return get_object_or_404(Blog, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blog=self.get_object()
        #taking the reviews from table and passing to 'review' context.
        reviews=Review.objects.filter(blog=blog)
        rcount=reviews.count()
        context['review']=reviews.order_by('-date')[:5]
        context['total_reviews']=rcount
        context['review_form']=ReviewForm()
        context['relProducts']=Blog.objects.filter(category=blog.category).exclude(id=blog.id).order_by('-date')[:4]
        return context
    
def AddReview(request, *args, **kwargs):
    blog_id=kwargs.get('id')
    blog=Blog.objects.get(id=blog_id)
    try:
        profile=get_object_or_404(Profile, user=request.user)
    except Profile.DoesNotExist:
        return redirect('padd')
    if request.method=='POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.profile=profile
            review.blog=blog
            review.save()
            return redirect('bdet', id=blog.id)
    return redirect('bdet', id=blog.id)

class ReviewList(ListView):
    template_name="reviews_list.html"
    context_object_name="allrevs"

    def get_blog(self):
        return get_object_or_404(Blog, id=self.kwargs['id'])

    def get_queryset(self):
        blog = self.get_blog()
        return Review.objects.filter(blog=blog)

def ReviewEdit(request, review_id):
    review=get_object_or_404(Review, id=review_id)
    blog=review.blog.id
    # Ensure only the owner of the review can edit it
    if review.profile.user!=request.user:
        return HttpResponseForbidden()
    # Get 'next' parameter from the request to redirect back to the correct page
    next_url=request.GET.get('next') or request.POST.get('next') or reverse('bdet', kwargs={'id': blog})
    if request.method=='POST':
        form = ReviewForm(data=request.POST, instance=review)
        if form.is_valid():
            form.save()
            # Redirect to the 'next' URL or fallback to the 'allrev' view
            return redirect(next_url)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews_edit.html', {'form': form, 'next': next_url})

def ReviewDelete(request,review_id):
    review=get_object_or_404(Review, id=review_id)
    review.delete()
    next_url=request.GET.get('next') or request.POST.get('next') or reverse('bdet', kwargs={'id': blog})
    return redirect(next_url)

class BlogUpdate(UpdateView):
    template_name="blog_update.html"
    form_class=BlogForm
    pk_url_kwarg='id'
    queryset=Blog.objects.all()
    def get_success_url(self):
        return reverse('bdet', kwargs={'id': self.object.id})

def BlogLikes(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('bdet', id=blog_id)

class LikedList(ListView):
    template_name="Liked_list.html"
    context_object_name="likelist"
    def get_queryset(self):
        user_id = self.kwargs.get('id')
        return Blog.objects.filter(likes=user_id)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user_id=self.kwargs.get('id')
        like_blogs=Blog.objects.filter(likes=user_id)
        paginator=Paginator(like_blogs, 5)# Show 5 blogs per page
        page=self.request.GET.get('page')
        
        try:
            blogs_paginated=paginator.page(page)
        except PageNotAnInteger:
            blogs_paginated=paginator.page(1)# If page is not an integer,show the first page
        except EmptyPage:
            blogs_paginated=paginator.page(paginator.num_pages)# If page is out of range, show last page
        context['likelist']=blogs_paginated
        context['page_obj']=blogs_paginated
        return context

def BlogBookmark(request, blog_id):
    blog=get_object_or_404(Blog, id=blog_id)
    if request.user in blog.bookmarks.all():
        blog.bookmarks.remove(request.user)
    else:
        blog.bookmarks.add(request.user)
    return redirect('bdet',id=blog_id)

class BookmarkList(ListView):
    template_name="bookmark_list.html"
    context_object_name="booklist"
    def get_queryset(self):
        user_id=self.kwargs.get('id')
        return Blog.objects.filter(bookmarks=user_id)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user_id=self.kwargs.get('id')
        book_blogs=Blog.objects.filter(bookmarks=user_id)
        paginator=Paginator(book_blogs, 5)# Show 5 blogs per page
        page=self.request.GET.get('page')
        
        try:
            blogs_paginated=paginator.page(page)
        except PageNotAnInteger:
            blogs_paginated=paginator.page(1)# If page is not an integer,show the first page
        except EmptyPage:
            blogs_paginated=paginator.page(paginator.num_pages)# If page is out of range, show last page
        # context['booklist']=blogs_paginated
        context['page_obj']=blogs_paginated
        return context    

class AboutView(TemplateView):
    template_name="about.html"

class ContactView(TemplateView):
    template_name="contact.html"
