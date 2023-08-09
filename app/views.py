from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_list_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewClientForm, FeedbackInquiryForm
from django.http import HttpResponseRedirect
from .models import Client, Profile, LoanHistory
from django.db.models import Sum
from datetime import date, timedelta, datetime


# Create your views here.


def index(request):
    loans_by_user = Client.objects.filter(lender_id=request.user)
    total_by_user = sum(client.loan_balance for client in loans_by_user)
    unpaid_clients = Client.objects.filter(lender_id=request.user, is_loan_paid=False)
    total_unpaid_balance = sum(client.loan_balance for client in unpaid_clients)
    loans_number_by_user = Client.objects.filter(lender_id=request.user).count
    unpaid_loans_by_user = Client.objects.filter(lender_id=request.user, is_loan_paid=False).count
    paid_loans_by_user = Client.objects.filter(lender_id=request.user, is_loan_paid=True).count
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()

    return render(request, "index.html",{'feedback_form': feedback_form, 'total_unpaid_balance':total_unpaid_balance, 'total_by_user':total_by_user, 'unpaid_loans_by_user':unpaid_loans_by_user, 'paid_loans_by_user':paid_loans_by_user, 'loans_number_by_user':loans_number_by_user})

def calculate_loan_penalty(loan_amount, loan_interest):
    # Implement your logic to calculate the loan balance based on the loan amount, interest, and penalty
    return int(loan_amount * loan_interest /100)

def calculate_loan_balance(loan_amount, loan_interest):
    # Implement your logic to calculate the loan balance based on the loan amount, interest, and penalty
    return int(loan_amount * loan_interest /100 + loan_amount)

@login_required(login_url='/accounts/login')
def new_client(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            # Calculate loan interest based on the loan amount (Principal)
            loan_amount = form.cleaned_data['loan_amount']
            loan_interest = form.cleaned_data['loan_interest']
            # Calculate and loan balance
            loan_penalty = calculate_loan_penalty(loan_amount, loan_interest)
            loan_balance = calculate_loan_balance(loan_amount, loan_interest)
            # Assign the calculated values to the respective fields
            client.loan_interest = loan_interest
            client.loan_penalty = loan_penalty
            client.loan_balance = loan_balance
            client.lender = current_user
            client.save()
            return HttpResponseRedirect('/')
    else:
        form = NewClientForm()
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'new_client.html', {'form': form, 'feedback_form': feedback_form})


def update_loan_balance(request, client_id):
    # Get the client object from the database
    client = get_object_or_404(Client, id=client_id)
    # Calculate the number of weeks since the loan was taken
    week_passed = (date.today() - client.loan_collection_date).days // 7
    # Calculate the total penalty to be added based on the number of weeks
    total_penalty =  week_passed * client.loan_penalty
    # Add the total_penalty to the loan_balance
    client.loan_balance += total_penalty




@login_required(login_url='/accounts/login')
def client_list(request):
    client = Client.objects.filter(is_loan_paid=False)[::-1]
    total = sum(client_obj.loan_balance for client_obj in client)
    # Loop through each client and update their loan balance using the update_loan_balance function
    for clients in client:
        update_loan_balance(request, clients.id)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()

    return render(request, 'client.html', {"client": client, "total":total, 'feedback_form': feedback_form})


@login_required(login_url='/accounts/login')
def update_client(request, pk):
    instance = get_object_or_404(Client, pk=pk)
    form = NewClientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'update_client.html', {'form': form, 'feedback_form': feedback_form})


def client_detail(request, id, slug, ):
    client = get_object_or_404(Client, id=id, slug=slug)
    history = LoanHistory.objects.filter(id_number=client.id_number)  # Get loan history for the client's id_number
    all_clients = Client.objects.filter(id_number=client.id_number)   # Get all clients with the same id_number

    # Prepare the list of id_numbers present in LoanHistory and all Clients with the same id_number
    history_ids = list(history.values_list('id_number', flat=True))
    clients_with_loan = list(all_clients.values_list('id_number', flat=True))

    # Check if all loans are paid for the client's id_number
    all_loans_paid = client.is_loan_paid and all(client.is_loan_paid for client in all_clients)

    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'client_detail.html', {'client': client, 'history':history, 'feedback_form': feedback_form, 'history_ids': history_ids, 'clients_with_loan': clients_with_loan, 'all_loans_paid': all_loans_paid})

def loan_paid(request,  id_number):
    client = get_list_or_404(Client, id_number=id_number)
    if len(client) > 1:
        # If multiple clients found, choose the first one and save it
        client = client[0]
    else:
        # If only one client found, use that client for loan payment
        client = client[0]

    # Mark the loan as paid and save
    client.is_loan_paid = True
    client.save()

    # Create a loan history entry
    LoanHistory.objects.create(client=client)

    return HttpResponse("Loan Paid Successfully!")

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
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
    return render(request, 'registration/login.html', {'form': form, 'feedback_form': feedback_form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


@login_required(login_url='/accounts/login')
def profile(request, username):
    user_profile = Profile.objects.filter(user_id=request.user.id)[::-1]
    lender_list = Client.objects.filter(lender_id=request.user).order_by('loan_collection_date')[::-1]
    unpaid_clients = Client.objects.filter(lender_id=request.user, is_loan_paid=False)
    total_unpaid_balance = sum(client.loan_balance for client in unpaid_clients)
    client = Client.objects.all()
    # Loop through each client and update their loan balance using the update_loan_balance function
    for clients in lender_list:
        update_loan_balance(request, clients.id)
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()

    return render(request, "profile.html", {"user_profile": user_profile, "lender_list":lender_list, "total_unpaid_balance":total_unpaid_balance, 'feedback_form': feedback_form})

def search_results(request):
    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Client.search_by_id_number(search_term)
        message = f"{search_term}"
    if request.method == 'POST':
        feedback_form = FeedbackInquiryForm(request.POST)
        if feedback_form.is_valid():
            sender = feedback_form.cleaned_data['email']
            subject = "You have a new Question or Inquiry from {}".format(sender)
            message_content = "Message: {}".format(feedback_form.cleaned_data['message_content'])
            message = "The Question or Inquiry is {}".format(message_content)

            return HttpResponseRedirect('/')
    else:
        feedback_form = FeedbackInquiryForm()
        return render(request, "search.html", {"message": message, "name": searched_ref, 'feedback_form': feedback_form})