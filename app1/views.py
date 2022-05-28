from app1.models import Company
from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
from django.http.response import HttpResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
import json
from django.http import JsonResponse
import smtplib
import random
import email.message
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

# Create your views here.


#********************************** COMPANY ******************************************

def Login(request):
    if request.POST:
        em = request.POST['email']
        pa = request.POST['pass']

        try: 
            var = Company.objects.get(company_email = em)
            if var.company_pass == pa:
                request.session['company_data'] = var.id
                return redirect('DashBoard')
            else:
                 return HttpResponse("<a href=""><h1>You have entered Wrong Password</h1></a>")
        except:
            return HttpResponse("<a href=""><h1>You have entered Wrong Email ID</h1></a>")
    return render(request,'company/login/login.html')

def Register(request):
    if request.POST:
        nm = request.POST['name']
        em = request.POST['email']
        pass1 = request.POST['pass']
        pass2 = request.POST['re_pass']
        img1 = request.FILES.get('image')
        try:
            var = Company.objects.get(company_email = em)
            return HttpResponse("<h1><a href=''>Email Id already registered...</h1>")
        except:
            if pass1==pass2:
                obj=Company()

                obj.company_name=nm
                obj.company_email=em
                obj.company_pass=pass2
                if img1 != None:
                    obj.profile = img1
                obj.save()
                return redirect('Login')
            else:
                return HttpResponse("<h1><a href=''>Wrong Password</h1>")
    return render(request,'company/login/register.html')

def ComForgotPass(request):
    if request.POST:
        em1=request.POST['email']
        print(em1)
        try:
            valid=Company.objects.get(company_email = em1)
            print(valid) 

            sender_email='dgwork45@gmail.com'
            sender_pass='Darshak123     '
            reciv_email=em1

            server = smtplib.SMTP('smtp.gmail.com',587)

            #--------------OTP--------------
            nos=[1,2,3,4,5,6,7,8,9,0]
            otp=""

            for i in range(4):
                otp+=str(random.choice(nos))
                print(otp)
            print(otp)

            mes1=f'''
            This is your OTP
            {otp}


            Don't Share with Others....
            '''

            msg=email.message.Message()
            msg['Subject']="OTP From this site"
            msg['From']=sender_email
            msg['To']=reciv_email
            password=sender_pass
            msg.add_header('Content-Type','text/html')
            msg.set_payload(mes1)

            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())

            request.session['otp']=otp

            request.session['new_user'] =valid.id

            return redirect('OTP_check')
        except:
            return HttpResponse('<a href=""> You have entered wrong email Id...</a>')
    return render(request,'company/Login/forgot.html')

def OTP_check(request):
    if 'otp' in request.session.keys():
        print("NEW OTP CHECK")
        if request.POST:
            ot1=request.POST['ot1']
            print(ot1)

            otp=request.session['otp']
            print(otp)

            if ot1==otp:
                del request.session['otp']
                print("You are ready for create new pssword")
                return redirect('NewPassword')
            else:
                del request.session['otp']
                return redirect('Login')

        return render(request,'company/Login/OTP.html')
    else:
        return redirect('Login')

def NewPassword(request):
    if 'new_user' in request.session.keys():
        if request.POST:
            p1=request. POST['pass1']
            p2=request. POST['pass2']
            print(p1,p2)
            if p1==p2:  
                obj = Company.objects.get(id=int(request.session['new_user']))
                obj.company_pass=p2
                obj.save()
                del request.session['new_user']
                return redirect('Login')
            else:
                return HttpResponse("<a href="">Both Password are not same</a>")
        return render(request,'company/Login/NewPass.html')

    else:
        return redirect('Login')

def DashBoard(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        return render(request,'company/dashboard/index.html', {'users' : User})
    else:
        return redirect('Login')

def ProfileManage(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))

        if request.POST:
            nm = request.POST['nm1']
            em = request.POST['em1']
            pass1 = request.POST['pass1']
            con = request.POST['con1']
            add1 = request.POST['add1']
            img1 = request.FILES.get('img1')

            User.company_name = nm
            User.company_email = em
            User.company_cno = con 
            User.company_add = add1
            User.company_pass = pass1
            if img1 != None:
                User.profile = img1
            User.save()


        return render(request,'company/dashboard/profile.html', {'users' : User})
    else:
        return redirect('Login')

def AddCustomer(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        if request.POST:
            nm=request.POST['nm1']
            em=request.POST['em1']
            con=request.POST['con1']

            obj = CompanyCustomer()
            obj.comp=User
            obj.cust_name=nm
            obj.cust_email=em
            obj.cust_con=con

            #--------------Password Creation--------------
            salfa = 'qwertyuioplkjhgfdsazxcvbnm'
            ualfa = salfa.upper()
            spic = '!@#$%^&*'
            num = '1234567890'
            data = salfa + ualfa + spic + num

            otp=""

            for i in range(8):
                otp+=str(random.choice(data))
                print(otp)
            print(otp)            

            obj.cust_pass = otp
            obj.save()

            try:
                sender_email='dgwork45@gmail.com'
                sender_pass='Darshak123'
                reciv_email=em

                server = smtplib.SMTP('smtp.gmail.com',587)

                mes1=f'''
                Hello, You are Now New Customer of this Company,

                Here is Your Login Details:
                
                email id : {em}
                password : {otp}
                link : http://127.0.0.1:8000/CustomerLogin
                '''

                msg=email.message.Message()
                msg['Subject']="New Customer Added"
                msg['From']=sender_email
                msg['To']=reciv_email
                password=sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(mes1)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                return redirect('ViewCustomer')
            except:
                return HttpResponse('<a href=""> You have entered wrong email Id...</a>') 
        return render(request,'company/dashboard/addCustomer.html', {'users' : User})
    else:
        return redirect('Login')

def ViewCustomer(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        custs = CompanyCustomer.objects.filter(comp = User)
        print(custs)
        return render(request,'company/dashboard/viewCustomer.html', {'users' : User,  'cust':custs})
    else:
        return redirect('Login')

def DeleteCustomer(request,id):
    if 'company_data' in request.session.keys():
        custs=CompanyCustomer.objects.get(id=id)
        print(custs)
        custs.delete()
        return redirect('ViewCustomer')
    else:
        return redirect('Login')

def AddProduct(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        if request.POST:
            nm = request.POST['nm1']
            pr = request.POST['pr1']
            qty = request.POST['qty1']
            img = request.FILES.get('img1') 

            var = CompanyProduct()
            var.comp = User
            var.pro_name = nm
            var.pro_price = pr
            var.pro_qty = qty
            var.pro_img = img
            var.save()

            return redirect('ViewProduct')

        return render(request,'company/dashboard/addProduct.html', {'users' : User})
    else:
        return redirect('Login')
    
def ViewProduct(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        prod = CompanyProduct.objects.filter(comp = User)
        return render(request,'company/dashboard/viewProduct.html',{'users':User, 'Prod':prod})
    else:
        return redirect('Login')

def DeleteProducts(request,id):
    if 'company_data' in request.session.keys():
        prod = CompanyProduct.objects.get(id = id)
        prod.delete()       
        return redirect('ViewProduct')
    else:
        return redirect('Login')

def UpdateProducts(request,id):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        prod = CompanyProduct.objects.get(id = id)
        if request.POST:
            nm = request.POST['name']
            pr = request.POST['price']
            q = request.POST['qty']
            img = request.FILES.get('img')

            prod.comp = User
            prod.pro_name = nm
            prod.pro_price = pr
            prod.pro_qty = q
            if img != None:
                prod.pro_img = img
            prod.save()
            return redirect('ViewProduct')
        return render(request,'company/dashboard/updateProduct.html',{'users':User, 'Prod':prod})
    else:
        return redirect('Login')

def ViewOrder(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        corder = CustomerOrder.objects.filter(comp = User, status = False)

        return render(request,'company/dashboard/viewOrder.html',{'users':User, 'Corder':corder})
    else:
        return redirect('Login')

def YesOrder(request,id):
    if 'company_data' in request.session.keys():
        corder = CustomerOrder.objects.get(id = id)
        corder.status = 'Yes'
        corder.save()
        return redirect('ViewOrder')
    else:
        return redirect('Login')

def NoOrder(request,id):
    if 'company_data' in request.session.keys():
        corder = CustomerOrder.objects.get(id = id)
        # prod = CompanyProduct.objects(id=corder.prod)
        corder.status = 'No'
        # prod.pro_qty += corder.qty
        corder.save()
        # prod.save()
        return redirect('ViewOrder')
    else:
        return redirect('Login')

def MlModule(request):
    if 'company_data' in request.session.keys():
        User = Company.objects.get(id = int(request.session['company_data']))
        if request.POST:
            return redirect("https://colab.research.google.com/drive/1MIwuUqTwSMOF83Gajng-Zp3ZRcJzOHVi?usp=sharing")
        return render(request,'company/dashboard/checkModule.html',{'users':User})
    else:
        return redirect('Login')

def logoutComp(request):
    if 'company_data' in request.session.keys():
        del request.session['company_data']
        return redirect('Login')
    else:
        return redirect('Login')


#********************************** CUSTOMER ******************************************

def CustomerLogin(request):
    if request.POST:
        em = request.POST['email']
        p = request.POST['pass']

        try:
            valid = CompanyCustomer.objects.get(cust_email = em, cust_pass = p)
            request.session['custom_user'] = valid.id
            return redirect(CustomerDash)
        except:
            return redirect('CustomerLogin')
    return render(request,'customer/login/login.html')

def CustomerDash(request):
    if 'custom_user' in request.session.keys():
        cust = CompanyCustomer.objects.get(id = int( request.session['custom_user'])) 
        prod = CompanyProduct.objects.filter(comp = cust.comp)
        return render(request,'customer/dash/index.html',{'Prod':prod})
    else:
        return redirect('CustomerLogin')

def Profile(request):
    if 'custom_user' in request.session.keys():
        cust = CompanyCustomer.objects.get(id = int( request.session['custom_user']))
        if request.POST:
            nm = request.POST['name']
            em = request.POST['email']
            p = request.POST['pass']
            cn = request.POST['cno']
            a1 = request.POST['add1']
            a2 = request.POST['add2']
            i = request.FILES.get('img')

            cust.cust_name = nm
            cust.cust_email = em
            cust.cust_pass = p
            cust.cust_cno = cn
            cust.cust_add1 = a1
            cust.cust_add2 = a2
            if i != None:
                cust.cust_profile = i
            cust.save()
        return render(request,'customer/dash/profile.html',{'Cust':cust})
    else:
        return redirect('CustomerLogin')

def OrderPlace(request,id):
    if 'custom_user' in request.session.keys():
        cust = CompanyCustomer.objects.get(id = int( request.session['custom_user'])) 
        prod = CompanyProduct.objects.get(id = id)
        if request.POST:
            q = request.POST['qty1']
            if prod.pro_qty >= int(q):
                prod.pro_qty -= int(q)
                obj = CustomerOrder()
                obj.comp = cust.comp
                obj.cust = cust
                obj.prod = prod
                obj.status = 'False'
                obj.qty = int(q)
                obj.tot_price = int(int(q) * int(prod.pro_price))
                obj.save()
                prod.save()
                return redirect('CustomerDash')
            else:
                return redirect('CustomerDash')
        return render(request,'customer/dash/orderPlace.html',{'Prod':prod})
    else:
        return redirect('CustomerLogin')

def AllOrder(request):
    if 'custom_user' in request.session.keys():
        cust = CompanyCustomer.objects.get(id = int( request.session['custom_user'])) 
        ord = CustomerOrder.objects.filter(cust = cust)

        return render(request,'customer/dash/allOrder.html',{'Ord':ord})
    else:
        return redirect('CustomerLogin')



def LogoutCustomer(request):
    if 'custom_user' in request.session.keys():
        del request.session['custom_user']
        return redirect('CustomerLogin')
    else:
        return redirect('CustomerLogin')
    