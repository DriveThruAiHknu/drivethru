from django.shortcuts import render

# Create your views here.
def car(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_1.html', context)

def car2(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_2.html', context)