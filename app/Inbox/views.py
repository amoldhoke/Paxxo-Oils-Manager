from django.shortcuts import render
# My import
from django.contrib.auth.decorators import login_required  # Login required to access private pages
from django.views.decorators.cache import cache_control  # Destroy the section after logout
from Inbox.models import Customer  # From models.py
from Inbox.forms import CustomerForm, EmailForm  # From forms.py
from django.contrib import messages  # Return messages
from django.http import HttpResponseRedirect  # Redirect the pages
from django.core.paginator import Paginator  # Pagination
from django.db.models import Q  # Global search
from datetime import datetime  # Used (in the example) to get msg received today
from django.core.mail import EmailMessage # Send message
from django.contrib.auth import logout  # Used to get auto logout

# ================================ FRONTEND ===============================|
# Create your views here.
# Function to home page (frontend)
def home(request):
    return render(request, "home.html")

# Function to send a message
def send_message(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Message send successfully !")
            return HttpResponseRedirect('/')
        else:
            return render(request, 'home.html', {'form':form})
    else:
        form = CustomerForm()
        return render(request, 'home.html', {'form':form})

# =============================== BACKEND =================================|
# Function to inbox page (backend)
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | 
            Q(email__icontains=q) | Q(subject__icontains=q) | 
            Q(status__icontains=q) | Q(message__icontains=q)
        ).order_by('-created_at')
    else:
        all_customer_list = Customer.objects.all().order_by('-created_at')
    
    paginator = Paginator(all_customer_list, 10)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)

    # ------------------------------ Message ------------------------------|
    # 1) Total
    total = Customer.objects.all().count()
    # 2) Read
    read = Customer.objects.filter(status='Read')
    # 3) Unread
    pending = Customer.objects.filter(status='Pending')
    # 4) Today
    base = datetime.now().date()
    today = Customer.objects.filter(created_at__gt = base)

    context = {
        'customers':all_customer,
        'total': total,
        'read': read,
        'pending': pending,
        'today': today,
    }

    return render(request, "inbox.html", context)

# Function to delete the message
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, customer_id):
    customer =Customer.objects.get(id = customer_id)
    customer.delete()
    messages.success(request, "Message successfully delete !")
    return HttpResponseRedirect('/inbox')

# Funtion to view the message individually
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer(request, customer_id):
    customer = Customer.objects.get(id = customer_id)
    if customer != None:
        return render(request, 'customer.html', {'customer': customer})

# Function to mark the message as read
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_message(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id = request.POST.get('id'))
        if customer != None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, "Message marked as READ !")
            return HttpResponseRedirect('/inbox')

# Function to reply the messages
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        company = "PAXXO OIL"

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            cc = form.cleaned_data['cc']
            files = request.FILES.getlist("attach")

            mail = EmailMessage(subject, message, company, [email], [cc])
            for f in files:
                mail.attach(f.name, f.read(), f.content_type)
            mail.send()

            messages.success(request, 'Reply sent successfully !')
            return HttpResponseRedirect('/inbox')

    else:
        form = EmailForm()
        return render(request, {'form':form})

# Auto Logout Function
def AutoLogoutUser(request):
    logout(request)
    request.user = None
    messages.info(request, ".")  # I put dot because the argument cannot be empty
    return HttpResponseRedirect('/')

# ========================== ERRORS ==============================|
def E_500(request):
    return render(request, '500.html')

def E_404(request, exception):
    return render(request, '404.html', status=404)