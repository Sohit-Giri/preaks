from django.shortcuts import render, redirect
from .forms import ForumForm

def index(request):
    if request.method == 'POST':
        form = ForumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', {'form': form, 'success': True})
        else:
            return render(request, 'index.html', {'form': form, 'success': False})
    else:
        form = ForumForm()
    return render(request, 'index.html', {'form': form})