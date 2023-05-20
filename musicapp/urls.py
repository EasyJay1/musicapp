from django.urls import path
from .import views
from .views import contact




urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('contact/', views.contact, name='contact'),

    # ... other URL patterns ...
    path('contact', contact, name='contact'),



    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("add_to_cart", views.add_to_cart, name= "add"),
    path("confirm_payment/<str:pk>", views.confirm_payment, name="add"),
    path('emptysample.html', views.emptysample_view, name='emptysample'),

    path('artist.html/', views.artist_view, name='artist'),

]


