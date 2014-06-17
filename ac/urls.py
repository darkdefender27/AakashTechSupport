from django.conf.urls  import patterns , include , url


urlpatterns = patterns( '',
             
     url(r'^$', 'ac.views.main', name='Main'),
     url(r'^back', 'ac.views.main'),
     url(r'^display/(\d+)/$', "ac.views.display"),
     url(r'^search/$', "ac.views.search"),
     url(r'^graphs', "ac.views.graph"),
     url(r'^reply/(\d+)/$',"ac.views.reply"),
     url(r'^submit_ticket/', 'ac.views.submit_ticket', name='submit ticket'),
     url(r'^ticket_stats/', 'ac.views.ticket_status_graph', name='ticket stats'),
     url(r'^ticket_traffic/', 'ac.views.ticket_traffic_graph', name='ticket traffic'),	
     url(r'^open/', 'ac.views.open', name='open'),	
     url(r'^close/', 'ac.views.close', name='close'),
     url(r'^view_tickets/', 'ac.views.view_tickets', name='view tickets'),	
		
)
