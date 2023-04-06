from django.views import *
from .import views
from django.urls import  path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[  
    
                path('',views.Analysis_HomePage,name='Analysis_HomePage'),
                path('About',views.About,name='About'),
                path('Contact',views.Contact,name='Contact'),


              
            ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)