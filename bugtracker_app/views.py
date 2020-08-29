from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from bugtracker_app.models import MyUser, Ticket
from bugtracker_app.forms import LoginForm, AddTicketForm


@login_required
def index(request):
    my_tickets = Ticket.objects.all()
    return render(request, "index.html", {"tickets": my_tickets})


@login_required
def add_ticket(request):
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title = data.get("title"),
                description = data.get("description"),
                ticket_author = request.user,
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddTicketForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def edit_ticket_view(request, ticket_id):
    ticket_instance = Ticket.objects.filter(id=ticket_id).first()
    form = AddTicketForm(instance=ticket_instance)
    if request.method == "POST":
        form = AddTicketForm(request.POST, instance=ticket_instance)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))
    return render(request, "generic_form.html", {"form": form})


@login_required
def user_detail_view(request, user_id):
    my_ticket = Ticket.objects.filter(ticket_author=user_id)
    my_user = Ticket.objects.filter(id=user_id).first()
    return render(request, "user_detail.html", {"my_user": my_user, "user_ticket": my_ticket})


@login_required
def ticket_detail_view(request, ticket_id):
    my_ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"my_ticket": my_ticket})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("homepage"))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))