from django.shortcuts import render


def history(request):
    return render(request, 'history/user_history.html')

def all_history(requset):
    return render(requset, 'history/admin_history.html')
