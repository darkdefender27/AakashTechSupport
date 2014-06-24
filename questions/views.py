# Create your views here.
import datetime
from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from aakashuser.models import Post, Reply, UserProfile
from taggit.models import Tag
from django.core.context_processors import csrf

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
        posts = Post.objects.all().order_by("-post_views")
        context_dict = {
            'posts': posts,
        }

    elif url == 'votes':
        posts = Post.objects.all().order_by("-upvotes")
        context_dict = {
            'posts': posts,
        }

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
        c_dict = {
            'url': url
        }
        context_dict.update(c_dict)

    return render_to_response('questions/all_questions.html', context_dict, context)


def ask_question(request):
    context = RequestContext(request)
    if request.POST:
        title = request.POST['post_title']
        body = request.POST['post_text']
        post_date = datetime.datetime.now()
        upvotes = 0

        u = User.objects.get(username=request.user.username)
        print "Username : "
        print u.username

        some_user = UserProfile.objects.get(user=u)

        creator_id = some_user.id
#        post.creator.id = creator_id

        print creator_id

        post = Post.objects.create(title=title, body=body, post_date=post_date, upvotes=upvotes, creator=some_user)
        post.tags.all()
        post.tags.add(request.POST['post_tags'])#Adding tags to the object created.

        que_dict = {
            'posts': post,
            'user': request.user,
        }
        return render_to_response('questions/question_page.html', que_dict, context)

    else:
        if request.user.is_authenticated():
            user = request.user
            c = {'user': user}
            print user.username
        else:
            err_msg = "You need to login to post a question."
            c = {'err_msg': err_msg}

        c.update(csrf(request))
        return render_to_response('questions/ask_question.html', c)


def submit_reply(request, qid):
    context = RequestContext(request)
    context_dict = {}

    if request.POST:
        current_post = Post.objects.get(pk=qid)
        print current_post.creator
        print current_post.title

        reply_body = request.POST['post_answer']
        upvotes = 0

        u = User.objects.get(username=request.user.username)
        some_user = UserProfile.objects.get(user=u)

        reply = Reply.objects.create(title=current_post, body=reply_body, upvotes=upvotes, user=some_user)
        print reply.reply_date

        context_dict = {
            'user': request.user,
            'posts': current_post,
            'post_reply': reply,
        }

    else:
        return HttpResponse("Reply failed to process..")

    return render_to_response('questions/question_page.html', context_dict, context)


def link_question(request, qid):
    context = RequestContext(request)
    question = Post.objects.get(pk=qid)
    posts = Post.objects.get(pk=qid)
    replies = Reply.objects.filter(title=posts)

    context_dict = {
        'user': request.user,
        'posts': posts,
        'replies': replies,
    }

    return render_to_response('questions/question_page.html', context_dict, context)


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


