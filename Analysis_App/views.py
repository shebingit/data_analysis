from django.shortcuts import render,redirect
from Analysis_App.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


# All the data analysis function for this site  listout here
# Home page load

def Analysis_HomePage(request):
    return render(request,'Analsis_HomePage.html')

def About(request):
    return render(request,'About.html')

def Contact(request):
    return render(request,'Contact.html')

def Signup_Page(request):
     return render(request,'SignUp.html')


def Signup_user(request):

    if request.method=='POST':

        if RegisterUser.objects.filter(email=request.POST['email'], pasword=request.POST['psw']).exists():
            error_msg='Email id or Password alredy exit.'
            return render(request,'SignUp.html',{'error_msg':error_msg})
        
        else:
            register=RegisterUser()
            register.name=request.POST['name']
            register.email=request.POST['email']
            register.pasword=request.POST['psw']
            register.save()
            success_msg='You can now Sign in.'
            return render(request,'SignUp.html',{'success_msg':success_msg})
    else:
        error_msg='Registeration Not Completed'
        return render(request,'SignUp.html',{'error_msg':error_msg})


def loging(request):
    
    if RegisterUser.objects.filter(email=request.POST['email'], pasword=request.POST['psw']).exists():
        user_reg=RegisterUser.objects.get(email=request.POST['email'], pasword=request.POST['psw'])
        request.session["uid"]=user_reg.id
        user_reg=RegisterUser.objects.get(id=user_reg.id)
        file_up=UploadFiles.objects.filter(reg_id=user_reg)
        file_up_count=UploadFiles.objects.filter(reg_id=user_reg).count()
        return render(request,'Dashboard/dashboard.html',{'user_reg':user_reg,'file_up':file_up,'file_up_count':file_up_count})

    else:
        error_msg='Email id or Password is Invalid.'
        return render(request,'Analsis_HomePage.html',{'error_msg':error_msg})
    
    

# Dashboard 
@csrf_exempt
def fileName_check(request):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
            user_reg=RegisterUser.objects.get(id=uid)

            if request.method == 'POST':

                file_name= request.POST.get('fileName')

                #checking the user input file name already exit or not
                if UploadFiles.objects.filter(file_Name=file_name).exists():
                    message='This File name already exit !  Please use another file name.'
                    return JsonResponse({'message': message})
                else:
                    return JsonResponse({'error': 'Invalid request method'})
   

def user_dashboard(request):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
        else:
            return redirect('/')
       
        user_reg=RegisterUser.objects.get(id=uid)
        file_up=UploadFiles.objects.filter(reg_id=user_reg)
        file_up_count=UploadFiles.objects.filter(reg_id=user_reg).count()
        return render(request,'Dashboard/dashboard.html',{'user_reg':user_reg,'file_up':file_up,'file_up_count':file_up_count})

def user_logout(request):
    if 'uid' in request.session:  
        request.session.flush()
        return render(request,'Analsis_HomePage.html')
    else:
       return render(request,'Analsis_HomePage.html')
   


def upload_files_page(request):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
        else:
            return render(request,'Analsis_HomePage.html')
        user_reg=RegisterUser.objects.get(id=uid)
        file_up=UploadFiles.objects.filter(reg_id=user_reg)
        return render(request,'Dashboard/file_upload.html',{'user_reg':user_reg,'file_up':file_up})

# Saveing uploaded File

def uploadfiles(request):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
            user_reg=RegisterUser.objects.get(id=uid)

            if request.method == 'POST':

                file_name=request.POST['fileName']
                files=request.FILES['files_data']
              

                #checking the user input file name already exit or not
                if UploadFiles.objects.filter(file_Name=file_name).exists():
                    message='This File name already exit !  Please use another file name.'
                    file_up=UploadFiles.objects.filter(reg_id=user_reg)
                    return render(request,'Dashboard/file_upload.html',{'message':message,'user_reg':user_reg,'file_up':file_up})
            
                else:
                    file_up=UploadFiles()
                    file_up.reg_id=user_reg
                    file_up.file_Name=file_name
                    fs = FileSystemStorage()
                    filename = fs.save(files.name, files)
                    file_up.file_data=fs.url(filename)
                    file_up.save()
                    file_up=UploadFiles.objects.filter(reg_id=user_reg)
                    success_message='Your File is Uploaded Successful.'
                    return render(request,'Dashboard/file_upload.html',{'success_message':success_message,'file_up':file_up})


        else:
           return render(request,'Analsis_HomePage.html')

   
