from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 
from .models import *
from django.contrib.auth.decorators import login_required

from .models import User
x = ['']

class listing_form(forms.Form):
    title = forms.CharField(label="Title ")
    description = forms.CharField(label="Description ",widget=forms.Textarea())
    starting_bid = forms.IntegerField(label="Starting bid ")
    url = forms.URLField(label="Image URL",required=False)

@login_required(login_url='/login')
def index(request):
    something = Auctions.objects.all()
    return render(request, "auctions/index.html",{
        "active_listing":Auctions.objects.filter(state=False),
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def new_listing(request):
    if request.method == "POST" :
        form = listing_form(request.POST)
        if form.is_valid():

            user = request.user 
            c = request.POST.get("selected")
            print(c)
            k = categories.objects.filter(categories=c).first()
            print(k)
            
            m = Auctions.objects.create(title=form.cleaned_data["title"],description=form.cleaned_data["description"],creator=user,category=k,url=form.cleaned_data["url"])
            x = bids.objects.create(starting_bid=form.cleaned_data["starting_bid"],auction=m,current_bid=form.cleaned_data["starting_bid"])
            m.bid = x
            m.save()

            return HttpResponseRedirect(reverse('index'))
        else: 
            return render(request,"auctions/new_listing.html",{
                "listing_form":listing_form(),
                "message":"Please enter valid form data"
            })

    else:
        cat = categories.objects.all()
        return render(request,"auctions/new_listing.html",{
            "listing_form":listing_form(),
            "category":cat

        })

@login_required(login_url='/login')
def active_listing(request,number):
    if request.method == "POST":
        try:
            message = ''

            #updating the current bid 
            nbid = int(request.POST.get("bid"))
            user = request.user 
            product = Auctions.objects.get(id=number)
            print(product)
            product_bid = bids.objects.get(auction=product)
            print(nbid)
            print(product_bid.current_bid)
            print(product.bid)

            if nbid >= product_bid.starting_bid :
                if nbid > product_bid.current_bid:
                    product_bid.current_bid = nbid
                    product_bid.save()

                    product_bid.bidder=user
                    product_bid.save()

            else :
                message = "The bid you placed is not enough please place a bid higher than the current one "
        except:
            print("Failed to put current bid")
            pass 

        try :
            close = request.POST.get("close")
            n = Auctions.objects.get(id=close)
            n.state="True"
            n.save()

            m = bids.objects.get(auction=n)
            m.final_bid=m.current_bid
            m.save()

        except:
            pass 
        user = request.user 
        product = Auctions.objects.get(id=number)
        comment = request.POST.get("comment")
        if comment is not None:
            comments.objects.create(comment=comment,auction=product,user=user)


        return HttpResponseRedirect(reverse('active_listing',args=[number]))

    else :
        user = request.user 
        #close the auction button visibility 
        try:
            a = Auctions.objects.get(creator=user,id=number)
            close = "open"
        except:
            close=""

        try :
            q = Auctions.objects.get(id=number,state="True")
            stop="stop"
            bidder="Sorry, The auction has been closed"
        except:
            stop = ""
            bidder=""

        #final bidder message 
        try:
            user = request.user
            q = Auctions.objects.get(id=number,state="True")
            b = bids.objects.get(bidder=user,auction=q)
            stop="stop"
            bidder="Congratulation you've won the auction for this product !"

        except:
            pass
        product = Auctions.objects.get(id=number)
        temp = Auctions.objects.get(id=number)
        print(watchlist.objects.filter(user=request.user,listing=Auctions.objects.get(id=number)))
        return render(request,"auctions/product.html",{
            "product":Auctions.objects.get(id=number),
            "bids":bids.objects.get(auction=temp),
            "close":close,
            "bidder":bidder,
            "stop":stop,
            "watchlist":watchlist.objects.filter(user=request.user,listing=Auctions.objects.get(id=number)),
            "comment":comments.objects.filter(auction=product)
        })
        
@login_required(login_url='/login')
def Watchlist(request):
    if request.method == "POST":
        
        user = request.user 
        data = request.POST.get("node")
        remove = request.POST.get("remove")

        try:
            a = watchlist.objects.get(user=user)
            print(a.user)
        except:
            a = watchlist.objects.create(user=user)


        if data is not None :  
            a.listing.add(data)
            a.save()

        if remove is not None:
            b = Auctions.objects.get(id=remove)
            a.listing.remove(b)
            a.save()
            print(a)


        return HttpResponseRedirect(reverse('watchlist'))
    else :
        message=''
        temp = 0
        user = request.user
        if user is not None :
            try:
                temp = watchlist.objects.get(user=user) 

            except :
                watchlist.objects.create(user=user)
                message = "Watchlist empty"

        return render(request,"auctions/watchlist.html",{
            "active_listing": Auctions.objects.filter(listings=temp),
            "message":message
        })
@login_required(login_url='/login')
def category(request):
    if request.method == "POST":
        message=""
        s = None 
        cat = request.POST.get("category")
        print(cat)
        
        if cat is not None:
            try:
                r = categories.objects.get(categories=cat)
                message="This category already exists"
            except:    
                categories.objects.create(categories=cat)

        specific = request.POST.get("specific")
        if specific is not None:
            s = categories.objects.get(categories=specific)

        return render(request,"auctions/category.html",{
            "category":categories.objects.all(),
            "active_listing":Auctions.objects.filter(category=s),
            "message":message
        })

    else:
        return render(request,"auctions/category.html",{
            "category":categories.objects.all()
        })


    

