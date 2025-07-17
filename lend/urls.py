# listings/urls.py

from django.urls import path
from .views import listing_list_create, get_borrow_listings, get_lend_listings,create_match,user_matches,rate_user

urlpatterns = [
    path('listings/', listing_list_create, name='listings'),
    path('listings/borrow/', get_borrow_listings, name='get-borrow-listings'),
    path('listings/lend/', get_lend_listings, name='get-lend-listings'),

    path('matches/', create_match,name="create-match"),
    path('my-matches/', user_matches,name="usermatches"),

    path('rate/', rate_user,name="rate"),

]
