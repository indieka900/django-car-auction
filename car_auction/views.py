from django.shortcuts import render,redirect
from .models import CustomUser,Cars
from django.utils import timezone
import time
from .decorators import seller_required, buyer_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user')
        
        if email and password and user_type:
            # Create user
            user = CustomUser.objects.create_user(email, password)
            # Save additional user data like user type
            user.usertype = user_type
            user.save()
            # Redirect to login page or any other page
            return redirect('login')  # Change 'login' to your login URL name
        else:
            error_message = "All fields are required."
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user= CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'email does not exist!') 
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login succesful')
            # Redirect based on user role
            # print(f'Hello ---> {user.usertype}')
            if user.usertype == 'Buyer':
                return redirect('view_cars')
            elif user.usertype == 'Seller':
                return redirect('upload_car')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')

def home(request):
    context = {}
    return render(request, 'index.html', context)

def log_out(request):
    logout(request)
    return redirect('login')

@seller_required
def upload_car(request):
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = request.POST.get('year')
        condition = request.POST.get('condition')
        image = request.FILES.get('image')
        
        if make and model and year and condition and image:
            car = Cars(make=make, model=model, year=year, condition=condition, image=image)
            car.save()
            return redirect('index')  # Redirect to the homepage or any other page you want
        else:
            error_message = "All fields are required."
            return render(request, 'upload_car.html', {'error_message': error_message})

    return render(request, 'upload_car.html')

@login_required
def view_cars(request):
    cars = Cars.objects.all().order_by('?')
    for car in cars:
        end_time = car.created_at + timezone.timedelta(days=1)  # Assuming bidding ends 24 hours after the car is listed
        # remaining_time = max(0, end_time - time.time())
        # car.remaining_hours = int(remaining_time // 3600)
        # car.remaining_minutes = int((remaining_time % 3600) // 60)
        # car.remaining_seconds = int(remaining_time % 60)
        now_dt = timezone.now()
        # print(f'this are types endtime -> {type(car.created_at)} and now_dt -> {type(now_dt)}')
        remaining_time = int((end_time - now_dt).total_seconds())
        car.remaining_time = remaining_time

    return render(request, 'view_cars.html', {'cars': cars,'now': timezone.now(),})

# def view_car(request,id):
#     car = Cars.objects.get(pk=id)
#     return render(request, 'bids.html',{'car':car})
@buyer_required
def place_bid(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        bid_amount = request.POST['bid_amount']

        try:
            car = Cars.objects.get(id=car_id)
            current_highest_bid = car.highest_bid

            if bid_amount > current_highest_bid:
                car.bid_count += 1
                car.highest_bid = bid_amount
                car.save()
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(request, 'Sorry, your bid must be higher than the current highest bid.')
        except Cars.DoesNotExist:
            messages.error(request, 'Error: Car details not found.')

        return redirect('view_cars')
    else:
        car_id = request.GET.get('id')
        try:
            car = Cars.objects.get(id=car_id)
            return render(request, 'place_bid.html', {'car': car})
        except Cars.DoesNotExist:
            messages.error(request, 'Car not found.')
            return redirect('view_cars')
        
@buyer_required   
def view_car(request, car_id):
    if request.method == 'POST':
        # car_id = request.POST['car_id']
        bid_amount = int(request.POST['bid_amount'])

        try:
            car = Cars.objects.get(id=car_id)
            current_highest_bid = car.highest_bid

            if bid_amount > current_highest_bid:
                car.bid_count += 1
                car.highest_bid = bid_amount
                car.last_bid = request.user
                car.save()
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(request, 'Sorry, your bid must be higher than the current highest bid.')
        except Cars.DoesNotExist:
            messages.error(request, 'Error: Car details not found.')

        return redirect(f'/view_car/{car_id}/')
    else:
        try:
            car = Cars.objects.get(id=car_id)
            return render(request, 'bids.html', {'car': car})
        except Cars.DoesNotExist:
            messages.error(request, 'Car not found.')
            return redirect('view_cars')
# Create your views here.
