# Create your views here.
from django.contrib.humanize.templatetags.humanize import naturaltime

__author__ = 'ushubham27'

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from forms import UserForm, UserProfileForm
from aakashuser.models import *
from django.contrib.auth.models import User
from django.core.validators import validate_email
from taggit.models import Tag
from django.db.models.signals import post_delete
import re
from django.contrib.auth.decorators import login_required
# INDEX PAGE VIEW
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
IMAGE_PATH = os.path.join(BASE_DIR, 'media/static/images/profile_image')


def handler404(request):
    return render(request, '404.html')


def change(request):
    pass_word = request.POST.get('reset1')
    print pass_word
    user = request.user.username
    user = User.objects.get(username=user)
    user.set_password(pass_word)
    user.save()
    user = UserProfile.objects.get(user=user)
    user.online_status= False
    user.save()
    active_user = request.user
    context_dict = {
        'user': active_user,
    }
    context = RequestContext(request)
    return render_to_response("index.html", context_dict, context)


def index(request):
    context = RequestContext(request)
    active_user = ""
    if request.user:
        active_user = request.user
    context_dict = {
        'user': active_user,
    }
    return render_to_response("index.html", context_dict, context)


def search(request):
    search_query = request.POST.get('q')
    resultset = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))

    if resultset:
        context_dict = {
            'posts': resultset
        }

    else:
        err_msg = "No results found.."

        context_dict = {
            'error_msg': err_msg
        }
    return render_to_response("search.html", context_dict, context_instance=RequestContext(request))


def validateEmail(email):
    if len(email) > 6:
        # if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) is not None:
        if re.match(r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b', email) is not None:
            return 1
    return 0


def register(request):
    context = RequestContext(request)
    temp_dict = {}

    if request.POST:
        postform = UserForm(data=request.POST)

        if postform.is_valid():
            pwd = request.POST['password']
            rpwd = request.POST['password1']
            username = request.POST['username']
            email = request.POST['email']

            print username

            if pwd == rpwd and validateEmail(email):
                temp_user = postform.save(commit=True)
                new_user = User.objects.get(username=request.POST['username'])
                new_user.set_password(pwd)
                new_user.save()

                # CREATE

                up = UserProfile.objects.create(user=new_user)
                up.save()

            else:
                er1 = ""
                er2 = ""

                if not validateEmail(email):
                    er2 = "Enter a valid email address. "

                if pwd != rpwd:
                    er1 = "Passwords don't match."

                temp_dict = {
                    'er1': er1,
                    'er2': er2
                }

        else:
            er3 = "Password should be of min_length 6"
            print er3
            temp_dict = {
                'er3': er3
            }
            print postform.errors
    else:
        postform = UserForm()

    context_dict = {
        'postform': postform,
    }
    context_dict.update(temp_dict)

    return render_to_response("user_profile/register.html", context_dict, context)

#PASSWORD RESET


def reset(request):
    try:
        data = request.POST['forgot']
        print data
        user = User.objects.get(email=data)

        password = User.objects.make_random_password()
        print password
        user.set_password(password)

        check = UserProfile.objects.get(user=user)
        check.online_status = True
        user.save()
        check.save()

        subject = "RESET PASSWORD"
        message = "Your Password is 123"
        my_email = "aakashkumariitb@gmail.com"

        print message
        return render_to_response('index.html', RequestContext(request))

    except ObjectDoesNotExist:
        msg = "Email-id does not exist."
        message_dict = {
            'login_error': msg
        }
        return render_to_response('user_profile/login.html', message_dict, RequestContext(request))


# LOGIN VIEW

def login_x(request):
    session_id = ""
    if request.method == 'POST':
        try:
            m = User.objects.get(username=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['id'] = m.email_id
                session_id = request.session['id']

                login_dict = {
                    'm': m,
                    'session_id': session_id,
                }
                return render_to_response('index.html', login_dict)
        except User.DoesNotExist:
            return HttpResponse("Your username and password pair didn't match.")
    else:
        c = {}
        c.update(csrf(request))
        context = RequestContext(request)
        return render_to_response("user_profile/login.html", c, context)


def logout_x(request):
    try:
        del request.session['id']
        msg = "You have been succesfully logged out."
        print msg
    except KeyError:
        msg = "KeyError : Unable to Logout "
        print msg

    logout_msg = {
        'msg': msg
    }

    return HttpResponseRedirect('/index/', logout_msg)


def login_new(request):
   # t = loader.get_template('registration/login.html') - not needed
    context = RequestContext(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['id'] = user.email
                session_id = request.session['id']
                login_error = ""
                login_dict = {
                    'user': user,
                    'session_id': session_id,
                    'login_error': login_error,
                }
                check = UserProfile.objects.get(user=user)
                if check.online_status:
                    response = render_to_response('user_profile/change.html', login_dict,context)
                    return response
                else:
                    response = render_to_response('index.html', login_dict, context)
                    return response
               
#               response.set_cookie('logged_in', user.email)
            else:
                login_error = "You are not an active user."
                login_dict = {
                    'login_error': login_error
                }
                return render_to_response('user_profile/login.html', login_dict, context)
        else:
            login_error = "User authentication failed."
            login_dict = {
                'login_error': login_error
            }
            return render_to_response('user_profile/login.html', login_dict, context)
    else:
        # URL was accessed directly
        c = {}
        c.update(csrf(request))
        context = RequestContext(request)
        return render_to_response('user_profile/login.html', c, context)


def logout_new(request):
    logout(request)
    response = HttpResponseRedirect('/index/')
    # response.delete_cookie('logged_in')
    print "You have been logged out successfully."
    return response


def view_tags(request):
    context = RequestContext(request)
    tags = Tag.objects.all()
    for i in tags:
        i.count = len(Post.objects.filter(tags=i))
    context_dict = {'tags': tags}
    return render_to_response('forum/../templates/questions/tags.html', context_dict, context)


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

@login_required
def profile(request):
    if request.method == "POST":
        if request.user.is_authenticated():
	    try:
                u = User.objects.get(username=request.user.username)
            except User.DoesNotExist:
                u = None
            print u
            up = UserProfile.objects.get_or_create(user=u)[0]
            print up
            user_profile_form = UserProfileForm(data=request.POST)
            user_profile_form.user = u
            if user_profile_form.is_valid():
                print "valid form"
                if 'avatar' in request.FILES:
                    up.location = request.POST['location']
                    # up.avatar=request.FILES['avatar'],
                    up.user_skills = request.POST['skills']
                    up.save()
                    image = request.FILES['avatar']
                    print image.content_type
                    print image.size
                    from django.core.files.images import *
                    if image.content_type in ["image/png"] and (image.size / 1024) <= 1024:
                        image_dim = get_image_dimensions(image)
                        print image_dim[0]<=500
                        print image_dim[1]<=500
                    else:
                        return render_to_response('user_profile/after_profile_update.html',
                                                  {"message":
                                                      "png file required"},
                                                  RequestContext(request))
                    if image.content_type in ["image/png"] and (image.size / 1024) <= 1024:
		      if image_dim[0]<=500 and image_dim[1]<=500:
                        up.avatar.save(image.name, image)
		      else:
                        return render_to_response('user_profile/after_profile_update.html',
                                                  {"message":
                                                      "Your pictures resolution should not be more than 500*500"},
                                                  RequestContext(request))
		    else:
		      return render_to_response('user_profile/after_profile_update.html',
                                                  {"message":
                                                      "file type is invalid or size exceeds 1 MB."},
                                                  RequestContext(request))
                else:
                    up.location = request.POST['location']
                    up.user_skills = request.POST['skills']
                    up_avatar = up.avatar
                    up.avatar = up_avatar
                    up.save()
                return render_to_response(
                    'user_profile/after_profile_update.html',
                    {"message": "Your profile has been updated"},
                    RequestContext(request))
            else:
                print "the form submitted was invalid"
                print user_profile_form.errors
                # this handles the ValidationError raised in forms.py
                return render_to_response('user_profile/after_profile_update.html',
                                          {
                                              "message": "please enter valid data.The location and skills field are required. Profile photo is optional"},
                                          RequestContext(request))
        else:
            # the user has to login to post and is displayed the login to post
            # message if he does so without logging in
            return HttpResponse("login to post")
    # displaying the form for the first time.

    else:
        user_profile_form = UserProfileForm()
        return render_to_response(
            'user_profile/update_profile.html',
            {'user_profile_form': user_profile_form},
            RequestContext(request))
        # else:
        # userprofile exists so display and give an option to update
        # resize the avatar while submitting the form
@login_required
def view_profile(request):
    u = User.objects.get(username=request.user.username)
    # if UserProfile already exists for the user then display the profile
    up = UserProfile.objects.get(user=u)
    related_post = Post.objects.filter(creator=up)

    try:
        up = UserProfile.objects.get(user=u)
    except UserProfile.DoesNotExist:
        up = None
        return render_to_response('user_profile/after_profile_update.html',
                                  {"message":
                                      "You have not yet updated your profile"},
                                  RequestContext(request))

    if up.avatar:
        context_dict = {
            'up': up,
            'posts': related_post,
            'location': up.location,
            'avatar': up.avatar,
            'user_skills': up.user_skills
        }
    else:
        context_dict = {
            'up': up,
            'posts': related_post,
            'location': up.location,
            'avatar': "static/images/profile_image/s1.PNG ",
            'user_skills': up.user_skills
        }

    return render_to_response('user_profile/profile_page.html', context_dict, RequestContext(request))


@login_required
def view_related_answers(request):
    u = User.objects.get(username=request.user.username)
    # if UserProfile already exists for the user then display the profile
    up = UserProfile.objects.get(user=u)
    related_replies = Reply.objects.filter(user=up)

    try:
        up = UserProfile.objects.get(user=u)
    except UserProfile.DoesNotExist:
        up = None
        return render_to_response('user_profile/after_profile_update.html',
                                  {"message":
                                      "You have not yet updated your profile"},
                                  RequestContext(request))
    if up.avatar:
        context_dict = {
            'replies': related_replies,
            'avatar': up.avatar,
            'up': up,
            'user': u
        }
    else:
        context_dict = {
            'replies': related_replies,
            'up': up,
            'avatar': "static/images/profile_image/s1.PNG ",
            'user': u
        }
    return render_to_response('user_profile/profile_page_ans.html', context_dict, RequestContext(request))




