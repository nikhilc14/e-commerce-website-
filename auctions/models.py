from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class categories(models.Model):
    categories = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return f"{self.categories}"

class Auctions(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.ForeignKey('bids', on_delete=models.CASCADE,null=True)
    url = models.URLField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    state = models.BooleanField(default=False)
    category=models.ForeignKey(categories, on_delete=models.CASCADE,null=True,blank=True)
    

    def __str__(self):
        return f"{self.title}"

class bids(models.Model):
    auction = models.ForeignKey(Auctions,on_delete=models.CASCADE,blank=True,null=True,related_name="bidders")
    current_bid = models.IntegerField(blank=True,null=True)
    starting_bid = models.IntegerField()
    final_bid = models.IntegerField(blank=True,null=True)
    bidder= models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.current_bid}"



class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1,null=True)
    comment = models.TextField()
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE,default=1,null=True)

    def __str__(self):
        return f"{self.comment}"

class watchlist(models.Model):
    user = models.ForeignKey(User,blank=True,on_delete=models.CASCADE)
    listing = models.ManyToManyField(Auctions,blank=True,related_name="listings")



    

    






