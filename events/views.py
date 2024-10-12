from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required

@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)  # Only show user's events
    return render(request, 'events/event_list.html', {'events': events})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'events/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('event_list')  # Redirect to event list after login
        return render(request, 'events/login.html', {'form': form})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)  # Create the event instance but don't save to DB yet
            event.user = request.user  # Set the user to the currently logged-in user
            event.save()  # Now save the event
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)  # Ensure user owns the event
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
