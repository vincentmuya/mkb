from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, NewPropertyForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponseRedirect
from .models import Property
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    buildings = Property.objects.all()

    return render(request, "index.html", {'buildings': buildings})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = NewUserForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


@login_required(login_url='/accounts/login')
def new_property(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            building = form.save(commit=False)
            building.owner = current_user
            building.save()
            return HttpResponseRedirect('/')
    else:
        form = NewPropertyForm()
    return render(request, 'new_property.html', {"form": form})


def property_detail(request, id, slug):
    prop_det = get_object_or_404(Property, id=id, slug=slug)

    return render(request, 'property_detail.html', {"prop_det": prop_det})
