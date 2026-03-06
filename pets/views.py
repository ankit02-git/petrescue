from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Pet
from .models import Pet, Favorite
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse



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
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered. Please login.")
            return redirect('register')

        user = User.objects.create_user(
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")

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

    favorite_ids = Favorite.objects.filter(user=request.user)\
                     .values_list('pet_id', flat=True)

    return render(request,'all_requests.html',{
        'pets':pets,
        'favorite_ids':favorite_ids
    })


@login_required
def add_request(request):
    if request.method == "POST":
        pet_type = request.POST.get('pet_type')
        breed = request.POST.get('breed')
        color = request.POST.get('color')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contact_info = request.POST.get('contact_info')
        description = request.POST.get('description')
        incident_datetime = request.POST.get('incident_datetime')
        image = request.FILES.get('image')

        # Basic validation
        if not latitude or not longitude:
            messages.error(request, "Please select location on the map.")
            return redirect('add_request')

        Pet.objects.create(
            user=request.user,
            pet_type=pet_type,
            breed=breed,
            color=color,
            latitude=float(latitude),
            longitude=float(longitude),
            contact_info=contact_info,
            description=description,
            incident_datetime=incident_datetime,
            image=image,
        )

        messages.success(request, "Pet request submitted successfully!")
        return redirect('my_requests')

    return render(request, 'add_request.html')




@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, id=pk)

    is_favorite = Favorite.objects.filter(
        user=request.user,
        pet=pet
    ).exists()

    return render(request, 'pet_detail.html', {
        'pet': pet,
        'is_favorite': is_favorite
    })


@login_required
def add_to_favorites(request, pk):
    pet = get_object_or_404(Pet, id=pk)
    Favorite.objects.get_or_create(user=request.user, pet=pet)
    return redirect('favorites')


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})

import requests

@login_required
def add_request(request):
    if request.method == "POST":
        pet_type = request.POST.get('pet_type')
        breed = request.POST.get('breed')
        color = request.POST.get('color')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        contact_info = request.POST.get('contact_info')
        description = request.POST.get('description')
        incident_datetime = request.POST.get('incident_datetime')
        image = request.FILES.get('image')

        location_name = "Unknown Location"

        if latitude and longitude:
            try:
                url = "https://nominatim.openstreetmap.org/reverse"

                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "format": "json"
                }

                # ✅ ADD IT HERE
                headers = {
                    "User-Agent": "petrescue-app"
                }

                # ✅ Pass headers here
                response = requests.get(url, params=params, headers=headers)

                data = response.json()

                address = data.get("address", {})

                city = address.get("city") or \
                       address.get("town") or \
                       address.get("village") or \
                       address.get("county")

                state = address.get("state")
                country = address.get("country")

                location_name = ", ".join(filter(None, [city, state, country]))

            except Exception as e:
                print("Reverse geocoding error:", e)

        Pet.objects.create(
            user=request.user,
            pet_type=pet_type,
            breed=breed,
            color=color,
            latitude=latitude,
            longitude=longitude,
            location=location_name,
            contact_info=contact_info,
            description=description,
            incident_datetime=incident_datetime,
            image=image,
        )

        return redirect('my_requests')

    return render(request, 'add_request.html')



@login_required
def my_requests(request):
    pets = Pet.objects.filter(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)\
                                 .values_list('pet_id', flat=True)

    return render(request, 'my_requests.html', {
        'pets': pets,
        'favorites': list(favorites)   # VERY IMPORTANT
    })

from .models import Pet, Favorite
from django.db.models import Q

def all_pets(request):
    search = request.GET.get('search', '')
    location = request.GET.get('location', '')

    pets = Pet.objects.all()

    if search:
        pets = pets.filter(
            Q(pet_type__icontains=search) |
            Q(breed__icontains=search)
        )

    if location:
        pets = pets.filter(location__icontains=location)

    favorite_ids = []

    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('pet_id', flat=True)

    return render(request, 'all_pets.html', {
        'pets': pets,
        'favorite_ids': favorite_ids,
        'search': search,
        'location': location
    })


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Pet, Favorite

@login_required
def toggle_favorite(request, pet_id):

    pet = Pet.objects.get(id=pet_id)

    favorite = Favorite.objects.filter(user=request.user, pet=pet).first()

    if favorite:
        favorite.delete()
        return JsonResponse({"status": "removed"})

    Favorite.objects.create(user=request.user, pet=pet)
    return JsonResponse({"status": "added"})