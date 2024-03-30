from django.urls import path
from car_auction.views import (
    home,login_view,upload_car,
    register_view,view_cars,place_bid,
    view_car,log_out
)

urlpatterns = [
    path('', home, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='logout'),
    path('upload_car/', upload_car, name='upload_car'),
    path('register/', register_view, name='register'),
    path('view_cars/', view_cars, name='view_cars'),
    path('view_car/<int:car_id>/', view_car, name='view_car'),
    path('place_bid/', place_bid, name='place_bid'),
]