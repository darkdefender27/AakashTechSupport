#from PIL import Image as PImage


from aakashuser.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from ac.forms import SubmitTicketForm
import json
from django.shortcuts import render
from django import forms
from django.db.models import Max
from ac.forms import SubmitTicketForm
from ac.forms import SubmitTicketForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from datetime import *
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

@login_required
def submit_ticket(request):
    if request.method=="POST":
        print request.POST
	if request.user.email!=request.POST["user_id"]:
		return render_to_response('ac/email_not_valid.html',{"message":"Please enter a valid email id; the email id you used during registration!"},RequestContext(request))
        if request.user.is_authenticated() and request.user.email==request.POST["user_id"]:
	    user_tab_id=request.POST["tab_id"]
	    #if user_tab_id.length()==8:
		#TODO validate the tablet id here
	    if len(user_tab_id)!=8:
		return render_to_response('ac/email_not_valid.html',{"message":"the tablet id you entered is not valid.Please enter a valid tablet id"},RequestContext(request))	
	    user_details=request.user.email
            submit_ticket_form=SubmitTicketForm(request.POST,user_details=user_details)           
            category=Category.objects.get(category=request.POST["topic_id"])
            cat_id=category.id
            submit_ticket_form.topic_id=cat_id
            print cat_id
            
            if submit_ticket_form.is_valid():
                #submit_ticket_form.cleaned_data['ticket_id'] = ticket_id_new
                submit_ticket_form.save()
                ticket_id=1
                if Ticket.objects.all()==[]:
                    ticket_id=1
                else:
                    ticket_id=int(Ticket.objects.all().aggregate(Max('ticket_id'))['ticket_id__max'])
                print "success"
                return render_to_response(
                    'ac/after_submit.html',
                    {'ticket_id': ticket_id},
                    RequestContext(request))
            else:
		#the form does not validate when user enters a tablet_id that is not present in the database
		return render_to_response('ac/email_not_valid.html',{"message":"the tablet id you entered is not valid.Please enter a valid tablet id"},RequestContext(request))
        else:
            return HttpResponse("login to post")
    else:#displaying the form for the first time. i think instance variable should be passed here.
	user_details=request.user.email
        submit_ticket_form=SubmitTicketForm(user_details=user_details)
    return render_to_response(
    'ac/submit_ticket.html',
    {'submit_ticket_form': submit_ticket_form,'user':request.user},
    RequestContext(request))

@staff_member_required
def main(request):
    """Main listing."""
    tickets = Ticket.objects.all()
    return render_to_response("ac/d.html",dict(tickets=tickets), RequestContext(request))

@staff_member_required
def display(request, id):     
     """Displaying the details of the corresponding tickets"""
     threads= Ticket.objects.get(pk=id)
     response = Threads.objects.filter(ticketreply=id)
     count    =  Threads.objects.filter(ticketreply=id).count()
     count_open = Ticket.objects.filter(status=0).count()
     count_close= Ticket.objects.filter(status=1).count() 

   
     if response.exists():
      context_dict = {
        'threads': threads,
        'response': response,
        'count'   : count,
        'count_open':count_open,
        'count_close':count_close,
      }
     else:
        context_dict={
            'threads':threads,
            'count_open':count_open,
            'count_close':count_close,
        }
    
     return render_to_response("ac/second.html", context_dict ,RequestContext(request))
@staff_member_required    
def search(request):
 if request.method == "POST":
   Search= request.POST.get('search')
   """Searching for ticket-id"""
   tickets=Ticket.objects.filter(Q(ticket_id__icontains=Search) | Q(user_id__icontains=Search))
   if tickets.exists():
       #importticket=Ticket.objects.get(pk=Search)
       return render_to_response("ac/search.html",dict(tickets=tickets),RequestContext(request))
   else:
       """Searching for Topic-id"""
       tickets=Category.objects.filter(category__icontains=Search)
       if tickets.exists():
         #tickets=Ticket.objects.get(pk=tickets)
         tickets=Ticket.objects.filter(topic_id=tickets)
         return render_to_response("ac/search.html",dict(tickets=tickets),RequestContext(request))
       else:
         tickets = Ticket.objects.all()
         return render_to_response("ac/d.html",dict(tickets=tickets),RequestContext(request))
       
       
@staff_member_required       
def graph(request):
	data={}
	category_names=[]#a list
	category=Category.objects.all()
	for c in category:
		category_names.append(c.category)
	#we now have a list of  category
	#now count no of tickets in each category
	count={}#a dictionary
	category=Category.objects.all()
	ticket=Ticket.objects.all()
	for c in category:
		count[c.category]=0
		#like count['android']		
		for t in ticket:
			ticket_for_a_cat=Ticket.objects.filter(topic_id=c)
		count[c.category]=ticket_for_a_cat.count()
	print category_names
	print count	
	#{ label: "Series1",  data: 10},
	#	//	{ label: "Series2",  data: 30},
	#	//	{ label: "Series3",  data: 90},
	#	//	{ label: "Series4",  data: 70},
	#	//	{ label: "Series5",  data: 80},
	#	//	{ label: "Series6",  data: 110}
	tickets=Ticket.objects.all()
	t_open=0
	t_closed=0
	for t in tickets:
		status=t.status
		if status==0:
			t_open=t_open+1
		if status==1:
			t_closed=t_closed+1
	status_dict={'open':t_open,'closed':t_closed}
	return render_to_response("ac/graphs.html",{'count':count,'category_names':category_names,'status_dict':status_dict},RequestContext(request))

@staff_member_required    
def ticket_status_graph(request):
	data={}
	category_names=[]#a list
	category=Category.objects.all()
	for c in category:
		category_names.append(c.category)
	#we now have a list of  category
	#now count no of tickets in each category
	count={}#a dictionary
	category=Category.objects.all()
	ticket=Ticket.objects.all()
	for c in category:
		count[c.category]=0
		#like count['android']		
		for t in ticket:
			ticket_for_a_cat=Ticket.objects.filter(topic_id=c)
		count[c.category]=ticket_for_a_cat.count()
	print category_names
	print count	
	#{ label: "Series1",  data: 10},
	#	//	{ label: "Series2",  data: 30},
	#	//	{ label: "Series3",  data: 90},
	#	//	{ label: "Series4",  data: 70},
	#	//	{ label: "Series5",  data: 80},
	#	//	{ label: "Series6",  data: 110}
	tickets=Ticket.objects.all()
	t_open=0
	t_closed=0
	for t in tickets:
		status=t.status
		if status==0:
			t_open=t_open+1
		if status==1:
			t_closed=t_closed+1
	status_dict={'open':t_open,'closed':t_closed}
	return render_to_response("ac/graphs_tickets.html",{'count':count,'category_names':category_names,'status_dict':status_dict},RequestContext(request))
    
@staff_member_required
def ticket_traffic_graph(request):
	year=date.today().year
	#ticket in a particular month
	ticket_dict={}
	for i in range(1,13):
		tickets_in_i=Ticket.objects.filter(created_date_time__year=year, 
                      created_date_time__month=i)
		tickets_in_i_count=tickets_in_i.count()
		ticket_dict[i]=tickets_in_i_count
	print ticket_dict
	return render_to_response("ac/ticket_traffic.html",{'ticket_dict':ticket_dict},RequestContext(request))
	

@staff_member_required
def reply(request, id):
  if request.method == 'POST':
    Reply= request.POST.get('response')
    ticket=Ticket.objects.get(pk=id)
   
    response = Threads.objects.create(ticketreply=ticket, reply=Reply,count=1)
    response.save()
   
    check=request.POST.get('reply_ticket_status')
    print check
    if check== 'Open':
        s=ticket.objects.get(pk=id)
        s.status=0
        s.save()
   
 
    threads = Ticket.objects.get(pk=id)
    response = Threads.objects.filter(ticketreply=id)
    count    =  Threads.objects.filter(ticketreply=id).count()
    count_open = Ticket.objects.filter(status=0).count()
    count_close= Ticket.objects.filter(status=1).count()
   

   
  
    context_dict = {
        'threads': threads,
        'response': response,
        'count'   :  count,
        'count_open':count_open,
        'count_close':count_close,
    }
   
   
   
   
    return render_to_response("ac/second.html",context_dict, RequestContext(request))

@staff_member_required
def open(request):
     tickets = Ticket.objects.filter(status=0)
     return render_to_response("ac/d.html",dict(tickets=tickets), RequestContext(request))

@staff_member_required
def close(request):
     tickets = Ticket.objects.filter(status=1)
     return render_to_response("ac/d.html",dict(tickets=tickets), RequestContext(request))

@login_required
def view_tickets(request):
	email=request.user.email
	tickets=Ticket.objects.filter(user_id=email)
	if not tickets:	
		return render_to_response("ac/email_not_valid.html",{"message":"No tickets to display"}, context_instance=RequestContext(request))
	else:
		tickets_dict=[]
		print tickets
		for t in tickets:
			t_dic={}
			if t.status==0:
				status="open"
			if t.status==1:
				status="closed"
			t_dic["status"]=status
			t_dic["tablet id"]=t.tab_id
			t_dic["message"]=t.message
			t_dic["created date and time"]=t.created_date_time
			t_dic["ticket id"]=t.ticket_id
			if t.topic_priority==0:
				p="low"
			if t.topic_priority==1:
				p="normal"
			if t.topic_priority==2:
				p="high"
			t_dic["priority"]=p
		
			#reply_dict={}
			replies=Threads.objects.filter(ticketreply=t.ticket_id)
			if not replies:
				reply_str="No replies yet"
			else:
				reply_str=""
			print replies
			for reply in replies:
				print reply.reply
				print reply.created
				reply_str=reply_str+"Reply on "+reply.created.strftime('%Y-%m-%d')+" : "+reply.reply+" ;"
			print reply_str
			t_dic["Replies"]=reply_str
			tickets_dict.append(t_dic)
		print tickets_dict

		return render_to_response("ac/view_tickets.html",{"tickets_dict":tickets_dict}, context_instance=RequestContext(request))
		           

    
 
        
