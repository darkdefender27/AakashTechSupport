# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from aakashuser.models import Post, Reply
from taggit.models import Tag
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def all_questions_view(request, url):
    context = RequestContext(request)
    context_dict = {}

    if url == 'latest':
        posts = Post.objects.all().order_by("-post_date")
        context_dict = {
            'posts': posts,
        }

    elif url == 'frequent':
        pass

    elif url == 'active':
        pass

    elif url == 'unanswered':
        posts = Post.objects.all()
        replies = Reply.objects.all()
        files = []

        for p in posts:
            a = 0
            for r in replies:
                if r.title.title == p.title:
                    a = 1
            if a == 0:
                files.append(p)
            context_dict = {
                'posts': files,
            }

    elif url == '':
        posts = Post.objects.all()
        context_dict = {
            'posts': posts,
        }

    return render_to_response('questions/all_questions.html', context_dict, context)
    
def qview(request, id):
    context = RequestContext(request)

    posts = Post.objects.get(pk=id)
    replies = Reply.objects.filter(title=posts)
   
    context_dict = {
        'posts': posts,
        'replies': replies,
    }
    return render_to_response("questions/allqueries_link.html", context_dict, context)



def view_tags(request):
    context = RequestContext(request)
    tags = Tag.objects.all()

    for i in tags:
        i.count = len(Post.objects.filter(tags=i))

    context_dict = {
        'tags': tags
    }

    return render_to_response('forum/tags.html', context_dict, context)


def search_tags(request):
    """
        @AJAX SEARCHING
        @author = d27
    """

    search_dict = {}

    if request.method == 'POST':
        search_text = request.POST['search_text']
        searched_tags = Tag.objects.filter(name__contains=search_text)
        search_dict = {
            'searched_tags': searched_tags
        }
    else:
        search_text = "No query provided."
        print search_text

    render_to_response('search.html', search_dict)


def linktag(request, qid):
    context = RequestContext(request)

    new_tag = Tag.objects.get(pk=qid)
    posts_date = Post.objects.filter(tags=new_tag).order_by('-post_date')
    posts_views = Post.objects.filter(tags=new_tag).order_by('-post_views')
    #post = Post.objects.get(tags=new_tag)


    context_dict = {
        'mytag': new_tag,
        'posts_views': posts_views,
        'posts_date': posts_date,
        #'post': post,
    }

    return render_to_response('questions/tagged_questions.html', context_dict, context)


def tag_search(request):
    context = RequestContext(request)
    mytag = request.POST.get('search_text')
    mytag = mytag.upper()
    try:
        new_tag = Tag.objects.get(name=mytag)
        posts = Post.objects.filter(tags=new_tag).order_by('-post_date')
        posts1 = Post.objects.filter(tags=new_tag).order_by('-post_views')
        context_dict = {
            'posts': posts,
            'mytag': new_tag,
            'posts1': posts1
        }
    except Tag.DoesNotExist:
        context_dict = {}
    return render_to_response('questions/all_questions.html', context_dict, context)
