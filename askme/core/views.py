from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect(
            'profile',  # a view name
            username=request.user.username)
    return render(request, 'core/home.html')
