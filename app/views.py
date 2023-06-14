from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewClientForm
from django.http import HttpResponseRedirect
from .models import Client, Profile
from django.db.models import Sum


# Create your views here.


def index(request):

    return render(request, "index.html")


@login_required(login_url='/accounts/login')
def new_client(request):
    if request.method == 'POST':
        form = NewClientForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return HttpResponseRedirect('/')
    else:
        form = NewClientForm()
    return render(request, 'new_client.html', {'form': form})


@login_required(login_url='/accounts/login')
def client_list(request):
    client = Client.objects.all()
    total = Client.objects.aggregate(s=Sum("loan_balance"))["s"]
    return render(request, 'client.html', {"client": client, "total":total})


@login_required(login_url='/accounts/login')
def update_client(request, pk):
    instance = get_object_or_404(Client, pk=pk)
    form = NewClientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    return render(request, 'update_client.html', {'form': form})


def client_detail(request, id, slug, ):
    client = get_object_or_404(Client, id=id, slug=slug)
    return render(request, 'client_detail.html', {'client': client})


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


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


@login_required(login_url='/accounts/login')
def profile(request, username):
    user_profile = Profile.objects.filter(user_id=request.user.id)
    lender_list = Client.objects.filter(lender_id=request.user).order_by('loan_collection_date')[::-1]
    total = Client.objects.aggregate(s=Sum("loan_balance"))["s"]
    client = Client.objects.all()



    return render(request, "profile.html", {"user_profile": user_profile, "lender_list":lender_list, "total":total})

def search_results(request):
    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Client.search_by_id_number(search_term)
        message = f"{search_term}"
        return render(request, "search.html", {"message": message, "name": searched_ref,})