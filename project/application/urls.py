from django.urls import path
from . import views

urlpatterns=[
    path('friend/', views.friends),
    path('adminlogin/', views.adminlogin),
    path('',views.registerpage),
    path('adminpage/<str:username>', views.adminpage),
    path('transedit/<int:id>', views.transedit),
    path('credit/<str:username>', views.credit),
    path('friendlogin/', views.friendlogin),
    path('debit/<str:username>',views.debit),
    path('catadd/',views.categoryadd),
    path('friendpage/<str:username>',views.friendpage),
    path('friendaccept/<int:id>', views.friendaccept),
    path('frienddelete/<int:id>', views.frienddelete),
    path('filter/', views.filter),
    path('trancdelete/<int:id>', views.transcdelete),

]