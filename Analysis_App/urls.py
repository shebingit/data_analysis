from django.views import *
from .import views
from django.urls import  path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[  
    
                path('',views.Analysis_HomePage,name='Analysis_HomePage'),
                path('About',views.About,name='About'),
                path('Contact',views.Contact,name='Contact'),

                path('Account-Sinup',views.Signup_Page,name='Signup_Page'), # SingUp page load
                path('Signup-user',views.Signup_user,name='Signup_user'),
                path('loging',views.loging,name='loging'),


                #User Dasboard
                
                path('User-Dashboard',views.user_dashboard,name='user_dashboard'),
                path('User-Logout',views.user_logout,name='user_logout'),


                # File upload 
                path('Check-File',views.fileName_check,name='fileName_check'),
                path('Upload-File',views.upload_files_page,name='upload_files_page'),
                path('Upload-File-Save',views.uploadfiles,name='uploadfiles'),
                
                
                


              
            ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)