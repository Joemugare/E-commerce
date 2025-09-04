from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')  # Use the namespace
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Profile view
def profile(request):
    return render(request, 'users/profile.html')

# Dashboard view
def dashboard(request):
    return render(request, 'users/dashboard.html')
