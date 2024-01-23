from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from clothapp.models import cloth_product,AddCart,Order,Contact,customer_details
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.
def index(request):
    userid=request.user.id
    #print("id of logged in user :",userid)
    #print("Result:",request.user.is_authenticated)
    context={}
    p=cloth_product.objects.filter(is_active=True)
    context['products']=p
    print(p)
    return render(request,"index.html",context)
    

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname)
        context={}
        if uname=="" or uemail=="" or upass=="" or ucpass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"register.html",context)
        elif upass!=ucpass:
            context['errmsg']="Password did not match"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,first_name=uname)
                u.set_password(upass)
                u.save()
                context['success']="User Registered Successfully"
                return render(request,"login.html",context)
                #return HttpResponse("Data Fetched")
            except Exception:
                context['errmsg']="Username already exists! Try Login."
                return render(request,"register.html",context)
    else:
        return render(request,"register.html")

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"login.html",context)
            #print(uname)
            #print(upass)
            #return HttpResponse("Data Fetched")
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="Invalid Username/Password"
                return render(request,"login.html",context)        
    else:
        return render(request,"login.html")

def ulogout(request):
    logout(request)
    return redirect('/index')


def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=cloth_product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,"products.html",context)

def occafilter(request,ov):
    q1=Q(is_active=True)
    q2=Q(occa=ov)
    p=cloth_product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,"products.html",context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=cloth_product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,"products.html",context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=cloth_product.objects.filter(q1 & q2 & q3) 
    context={}
    context['products']=p
    return render(request,"products.html",context)

def products(request):
    return render(request,"products.html")

def productdetails(request,pid):
    context={}
    p=cloth_product.objects.filter(id=pid)
    context['products']=p
    print(p)
    return render(request,"productdetails.html",context)

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        #print(uname)
        context={}
        if name=="" or email=="" or message=="":
            context['errmsg']="Feilds cannot be empty"
            return render(request,"contact.html",context)
        else:
            try:
                a=Contact.objects.create(name=name,email=email,message=message)
                a.save()
                context['success']="FeedBack Submitted Successfully"
                return render(request,"contact.html",context)
                #return HttpResponse("Data Fetched")
            except Exception:
                return render(request,"contact.html",context)
    else:
        return render(request,"contact.html")

def addcart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        p=cloth_product.objects.filter(id=pid)
        print(p)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=AddCart.objects.filter(q1 & q2)
        print(c)
        context={}
        n=len(c)
        if n==1:
            context['errmsg']="Product already exists in Cart"
            context['products']=p
            return render(request,'productdetails.html',context)
        else:
            c=AddCart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added to Cart!"
            context['products']=p
            return render(request,'productdetails.html',context)
    else:
        return redirect('/login')  

def cart(request):
    c=AddCart.objects.filter(uid=request.user.id)
    print(c)
    context={}
    context['data']=c
    
    s=0
    for x in c:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(c)
    context['items']=np
    return render(request,"cart.html",context)

def remove(request):
    c=AddCart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def updatequantity(request,qv,cid):
    c=AddCart.objects.filter(id=cid)
    print(c[0])
    print(c[0].quantity)  
    if qv=='1':
        t=c[0].quantity+1
        c.update(quantity=t)
    else:
        t=c[0].quantity-1
        c.update(quantity=t)
    return redirect('/cart')

def placeorder(request):
    userid=request.user.id
    c=AddCart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.quantity
    print(s)
    context['total']=s
    np=len(orders)
    context['items']=np
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price * x.quantity
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_YvjZinDbG3pKzW", "3ahukKWs5YofrX6HW2Y8cCi9"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
    #return HttpResponse("In Payment Page")
    return render(request,'payment.html',context)

def sendusermail(request):
    send_mail(
    "Beauty Fashion Store Order Placed Successfully",
    "Order Completed !! Thanks for Ordering.",
    "tejashriprakashshinde25702@gmail.com",
    ["tejashripshinde002@gmail.com"],
    fail_silently=False,
    )
    context={}
    context['emailsend']="Email Send Successfully"
    p=cloth_product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'index.html',context)

def customerservices(request):
    return render(request,'customer_services.html')


def user_profile(request):
    c=User.objects.filter(username=request.user.username)
    context={}
    context['data']=c
    p=customer_details.objects.filter(uname=request.user.username)
    context['data1']=p
    return render(request,'profile.html',context)

def update_profile(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mobile=request.POST['mobile']
        address=request.POST['address']
        context={}
        c=User.objects.filter(username=request.user.username)
        context['data']=c
        p=customer_details.objects.filter(uname=request.user.username)
        context['data1']=p
        m=User.objects.filter(id=uid)
        m.update(username=uname,first_name=firstname,last_name=lastname)   
        m=customer_details.objects.filter(uname=request.user.username)
        m.create(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address) 
        m.update(uname=uname,firstname=firstname,lastname=lastname,mobile=mobile,address=address) 
        context['success']='Profile updated successfully,'
        return render(request,'profile.html',context)  
    else:
        return redirect('/profile')

def orderhome(request):
    userid=request.user.id
    c=AddCart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,uid=x.uid,pid=x.pid,quantity=x.quantity)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    return render(request,'display_orders.html',context)

def password(request):
    context={}
    c=User.objects.filter(username=request.user.username)
    # t=User.objects.get(id=request.user.id)
    # o=t.password
    
    context['data']=c
    return render(request,'change_password.html',context) 

def changepassword(request,uid):
    if request.method == 'POST':
        uname=request.POST['uname']
        passw=request.POST['passw']
        newpass=request.POST['newpass']
        confirmpass=request.POST['confrimpass']
        upass1=make_password(confirmpass)
        context={}
        c=User.objects.filter(username=request.user.username)
        u=authenticate(username=uname,password=passw)

        if passw=="" or newpass=="" or confirmpass=="" :
            context['data']=c
            context['errmsg']="Fields can not be empty"
            return render(request ,'change_password.html',context)

        elif newpass!=confirmpass:
            context['data']=c
            context['errmsg']="Password is not matching "
            return render(request ,'change_password.html',context)
        else:
            u=authenticate(username=uname,password=passw)
            if u is not None:
                m=User.objects.filter(id=uid)
                m.update(password=upass1)
                context['data']=c
                context['success']='Password updated successfully,'
                return render(request ,'change_password.html',context)   
    else:
        return redirect('/changepassword') 