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
                    file_up.file_data=files
                    file_up.save()
                    file_up=UploadFiles.objects.filter(reg_id=user_reg)
                    success_message='Your File is Uploaded Successful.'
                    return render(request,'Dashboard/file_upload.html',{'success_message':success_message,'file_up':file_up})


        else:
           return render(request,'Analsis_HomePage.html')


def RemoveUpload_File(request,pk):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
           
        else:
            return render(request,'Analsis_HomePage.html')
        
        user_reg=RegisterUser.objects.get(id=uid)
        
        file_up=UploadFiles.objects.get(id=pk)
        file_name=file_up.file_Name
        file_up.delete()
        delete_msg=file_name + ' File Deleted.'
        
        
        file_up=UploadFiles.objects.filter(reg_id=user_reg)
        file_up_count=UploadFiles.objects.filter(reg_id=user_reg).count()
        return render(request,'Dashboard/dashboard.html',{'user_reg':user_reg,'file_up':file_up,'file_up_count':file_up_count,'delete_msg':delete_msg})
       
        
    else:
        return render(request,'Analsis_HomePage.html')


   
def Analysis(request,pk):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
           
        else:
            return render(request,'Analsis_HomePage.html')
        
        user_reg=RegisterUser.objects.get(id=uid)
        
        file_up=UploadFiles.objects.get(id=pk)
        excel_contents = file_up.read_excel()
        
   
        return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents})

    else:
        return render(request,'Analsis_HomePage.html')


   
def Analysis_search(request,pk):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
           
        else:
            return render(request,'Analsis_HomePage.html')
        
        user_reg=RegisterUser.objects.get(id=uid)
        
        file_up=UploadFiles.objects.get(id=pk)
        excel_contents = file_up.read_excel()
        file_path = file_up.file_data.path
        df = pd.read_excel(file_path)

        if request.method =='POST':
            col=request.POST['colname']
            val=request.POST['serch_value']

            #checking the column is selected or not
            if col == '0':
                msg='Please select column  head'
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'msg':msg})
           
            elif val == '0':
                # Select the column based on its name
                excel_contents = df[col].tolist()

                content={'col':col,'val':request.POST['serch_value']}
                return render(request,'Dashboard/Analysis_column.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'content':content})
            
            else:
        
                excel_contents = df.loc[df[col].astype(str).str.contains(val, case=False)]

                content={'col':col,'val':request.POST['serch_value']}
         
   
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'content':content})

    else:
        return render(request,'Analsis_HomePage.html')
    


def Analysis_rangesearch(request,pk):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
           
        else:
            return render(request,'Analsis_HomePage.html')
        
        user_reg=RegisterUser.objects.get(id=uid)
        
        file_up=UploadFiles.objects.get(id=pk)
        excel_contents = file_up.read_excel()
        file_path = file_up.file_data.path
        df = pd.read_excel(file_path)

        if request.method =='POST':
            col=request.POST['colnamerange']
            if col == '0':
                msg='Please select column  head'
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'msg':msg})
            else:
                startval=request.POST['start_val']
                endval=request.POST['end_val']
                excel_contents = df.loc[(df[col] >= int(startval)) & (df[col] <= int(endval))]
        
            

                content={'col':col,'val':'Start value:'+ startval +'  '+'End value:'+ endval}
         
   
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'content':content})

    else:
        return render(request,'Analsis_HomePage.html')
    


def Analysis_datesearch(request,pk):
    if 'uid' in request.session:
        if request.session.has_key('uid'):
            uid = request.session['uid']
           
        else:
            return render(request,'Analsis_HomePage.html')
        
        user_reg=RegisterUser.objects.get(id=uid)
        
        file_up=UploadFiles.objects.get(id=pk)
        excel_contents = file_up.read_excel()
        file_path = file_up.file_data.path
        df = pd.read_excel(file_path)

        if request.method =='POST':
            col=request.POST['datecol']
            if col == '0':
                msg='Please select column  head'
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'msg':msg})

            else:
                startval=request.POST['start_dt']
                endval=request.POST['end_dt']
                stardat = pd.to_datetime(startval)
                enddat = pd.to_datetime(endval)
                # Convert the column values to pandas datetime objects
                df[col] = pd.to_datetime(df[col])
                excel_contents = df.loc[(df[col] >= stardat) & (df[col] <= enddat)]
        
            

                content={'col':col,'val':'Start value:'+ startval +'  '+'End value:'+ endval}
         
   
                return render(request,'Dashboard/Analysis.html',{'user_reg':user_reg,'file_up':file_up,'excel_contents':excel_contents,'content':content})

    else:
        return render(request,'Analsis_HomePage.html')
    
    


