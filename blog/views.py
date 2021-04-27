from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm 
from django.core.mail import send_mail
# Create your views here.
class PostListView(ListView):
    queryset= Post.published.all()
    context_object_name= 'posts' #3 posts per opage
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
    status='published', publish__year=year,
    publish__month=month, publish__day=day)

    #list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create a comment object but dont save to thedatabase yet
            new_comment= comment_form.save(commit=False)
            #assign the current bpost to the comment.post
            new_comment.post=post

            new_comment.save()

    else:
        comment_form = CommentForm()        

    return render(request, 'blog/post/detail.html',{'post':post, 'comments': comments, 'new_comment': new_comment,'comment_form': comment_form})

def post_share(request, post_id):
     #retreive post by id
     post = get_object_or_404(Post,id=post_id, status='published')

     sent = False

     if request.method == 'POST':
         form = EmailPostForm(request.POST)
         if form.is_valid():
             cd = form.cleaned_data
             post_url = request.build_absolute_uri(post.get_absolute_url())
             subject = f"{cd['name']} recommends you read" f"{post}"
             message = f"Read {post.title} at {post_url}\n\n"f"{cd['name']}\'s comments: {cd['comments']}"

             send_mail(subject,message, 'petermbaik@gmail.com', [cd['to']]) 

             sent = True 

             

     else:
         form = EmailPostForm()
     return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})     

        

