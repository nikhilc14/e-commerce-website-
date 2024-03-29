from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing",views.new_listing,name="new_listing"),
    path("active_listing/<int:number> ",views.active_listing,name="active_listing"),
    path("watchlist",views.Watchlist,name="watchlist"),
    path("category",views.category,name="category")
]
