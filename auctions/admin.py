from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Auctions)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(watchlist)
admin.site.register(User)
admin.site.register(categories)