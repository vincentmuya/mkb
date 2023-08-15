from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_list_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewClientForm, FeedbackInquiryForm, NewUserForm
from django.http import HttpResponseRedirect
from .models import Client, Profile, LoanHistory, User
from django.db.models import Sum
from datetime import date, timedelta, datetime
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma


# Create your views here.

@login_required(login_url='/accounts/login')
def index(request):
    loans_by_user = Client.objects.filter(lender_id=request.user)
    total_by_user = sum(client.loan_balance for client in loans_by_user)
    unpaid_clients = Client.objects.filter(lender_id=request.user, is_loan_paid=False)
    paid_clients = Client.objects.filter(lender_id=request.user, is_loan_paid=True)
    total_paid_balance = sum(client.loan_balance for client in paid_clients)
    profit_by_user = sum(client.loan_penalty for client in paid_clients)
    total_unpaid_balance = sum(client.loan_balance for client in unpaid_clients)
    loans_number_by_user = Client.objects.filter(lender_id=request.user).count
    unpaid_loans_by_user = Client.objects.filter(lender_id=request.user, is_loan_paid=False).count
    paid_loans_by_user = Client.objects.filter(lender_id=request.user, is_loan_paid=True).count
    total_loan_amount = current_month_loans_amount(request)
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

    return render(request, "index.html",{'feedback_form': feedback_form, 'total_unpaid_balance':intcomma(total_unpaid_balance), 'total_by_user':intcomma(total_by_user), 'unpaid_loans_by_user':unpaid_loans_by_user, 'paid_loans_by_user':paid_loans_by_user, 'loans_number_by_user':loans_number_by_user, 'total_loan_amount':intcomma(total_loan_amount), 'total_paid_balance':intcomma(total_paid_balance), 'profit_by_user':intcomma(profit_by_user)})

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
    # Format the loan_balance and loan_amount fields with commas
    for clients in client:
        clients.loan_balance = intcomma(clients.loan_balance)
        clients.loan_amount = intcomma(clients.loan_amount)
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

    return render(request, 'client.html', {"client": client, "total":intcomma(total), 'feedback_form': feedback_form})


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
    # Format the loan_balance and loan_amount fields with commas
    for client in all_clients:
        client.loan_balance = intcomma(client.loan_balance)
        client.loan_amount = intcomma(client.loan_amount)
        client.loan_penalty = intcomma(client.loan_penalty)

    for clients in history:
        clients.loan_balance = intcomma(clients.loan_balance)
        clients.loan_amount = intcomma(clients.loan_amount)
        clients.loan_penalty = intcomma(clients.loan_penalty)

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


def current_month_loans_amount(request):
    # Get the current date
    today = datetime.now()

    # Filter loans for the current month
    loans_this_month = Client.objects.filter(loan_collection_date__month=today.month, loan_collection_date__year=today.year)

    # Calculate the sum of loan amounts
    total_loan_amount_monthly = loans_this_month.aggregate(Sum('loan_balance'))['loan_balance__sum']

    if total_loan_amount_monthly is None:
        total_loan_amount_monthly = 0

    return total_loan_amount_monthly


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


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'registration/register.html', {'form': form})
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
    # Format the loan_balance and loan_amount fields with commas
    for client in lender_list:
        client.loan_balance = intcomma(client.loan_balance)
        client.loan_amount = intcomma(client.loan_amount)
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

    return render(request, "profile.html", {"user_profile": user_profile, "lender_list":lender_list, "total_unpaid_balance":intcomma(total_unpaid_balance), 'feedback_form': feedback_form})

def registered_users(request):
    users_in_db = User.objects.all()

    user_stats = []

    for user in users_in_db:
        loans_given = Client.objects.filter(lender=user)
        total_loans_given = sum(client.loan_balance for client in loans_given)
        paid_loans = loans_given.filter(is_loan_paid=True)
        profit_by_user = sum(client.loan_penalty for client in paid_loans)
        paid_loans = sum(client.loan_balance for client in paid_loans)
        unpaid_loans = loans_given.filter(is_loan_paid=False)
        unpaid_loans = sum(client.loan_balance for client in unpaid_loans)

        user_stat = {
            'user': user,
            'total_loans_given': intcomma(total_loans_given),
            'total_paid_loans': intcomma(paid_loans),
            'total_unpaid_loans': intcomma(unpaid_loans),
            'profit_by_user':intcomma(profit_by_user),
            'user_id': user.id,  # Add the user's ID to the dictionary
        }
        user_stats.append(user_stat)
    return render(request, "users.html", {"users_in_db": users_in_db, 'user_stats':user_stats})


def user_detail(request, id):
    user_info = get_object_or_404(User, id=id)

    return render(request, 'user_detail.html', {'user_info':user_info})

def search_results(request):
    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Client.search_by_id_number(search_term)
        message = f"{search_term}"
    # Format the loan_balance and loan_amount fields with commas
    for client in searched_ref:
        client.loan_balance = intcomma(client.loan_balance)
        client.loan_amount = intcomma(client.loan_amount)
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