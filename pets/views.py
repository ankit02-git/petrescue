from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Pet

User = get_user_model()


def home(request):
    rescued_count = Pet.objects.filter(status='rescued').count()
    adopted_count = Pet.objects.filter(status='adopted').count()
    lost_count = Pet.objects.filter(status='lost').count()
    happy_users = User.objects.count()

    context = {
        'rescued_count': rescued_count,
        'adopted_count': adopted_count,
        'lost_count': lost_count,
        'happy_users': happy_users,
    }

    return render(request, 'home.html', context)


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists. Please choose another.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered. Please login.")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def my_requests(request):
    pets = Pet.objects.filter(user=request.user)
    return render(request, 'my_requests.html', {'pets': pets})


@login_required
def all_pets(request):
    pets = Pet.objects.all()
    return render(request, 'all_pets.html', {'pets': pets})


@login_required
def add_request(request):
    if request.method == "POST":
        pet_type = request.POST.get('pet_type')
        breed = request.POST.get('breed')
        color = request.POST.get('color')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contact_info = request.POST.get('contact_info')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Pet.objects.create(
            user=request.user,
            pet_type=pet_type,
            breed=breed,
            color=color,
            location=location,
            latitude=latitude,
            longitude=longitude,
            contact_info=contact_info,
            description=description,
            image=image
        )

        return redirect('my_requests')

    return render(request, 'add_request.html')