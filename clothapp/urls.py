from django.urls import path
from clothapp import views
from clothshop import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index',views.index),
    path('register',views.register),
    path('login',views.ulogin),
    path('logout',views.ulogout),
    path('catfilter/<cv>',views.catfilter),
    path('occafilter/<ov>',views.occafilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('products',views.products),
    path('productdetails/<pid>',views.productdetails),
    path('about',views.about),
    path('contact',views.contact),
    path('addcart/<pid>',views.addcart),
    path('cart',views.cart),
    path('remove/<cid>',views.remove),
    path('updatequantity/<qv>/<cid>',views.updatequantity),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),
    path('customerservices',views.customerservices),
    path('profile',views.user_profile),
    path('updateprofile/<uid>',views.update_profile),
    path('orderhome',views.orderhome),
    path('changepassword/<uid>',views.changepassword),
    path('changepassword',views.password),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
