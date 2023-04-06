from django.shortcuts import render


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

