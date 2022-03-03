from re import search
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.db.models import Q
from .forms import postForm
from .models import membership #membership 모델

# Create your views here.
def car(request):
    memberships = membership.objects.all() #전부 가져오기
    context = {'membership_list' : memberships}
    return render(request, 'client/client_1.html', context)

def car2(request):
    memberships = membership.objects.all() #membership 데이터 가져오기
    m = request.GET.get('car') #m에 url "?car="형식에서 뒤에 있는 값 가져오기
    if m:
        memberships = memberships.filter(userCar__icontains=m) #폼 값 = userCar과 동일한 값 가져오기
    return render(request, 'client/client_2.html', {'post_list': memberships, 'm':m, })

def order1(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_3.html', context)

def order2(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_4.html', context)   

def order3(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_5.html', context)      
def manage_login(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_login.html', context)
def manage_menu(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu.html', context)

def manage_menuadd(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu_add.html', context)

# database 도전

def db(request):
    memberships = membership.objects.all() #전부 가져오기
    context = {'membership_list' : memberships}
    return render(request, 'client/client_db.html', context)

class SearchFromView(FormView):
    form_class = postForm
    template_name = 'client/client_db_2.html'

    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word']
        post_list = membership.objects.filter( Q(userCar__icontains = schWord)).distinct()

        context={}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list
        return render(self.request, self.template_name, context)