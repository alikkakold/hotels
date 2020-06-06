from django.shortcuts import render

# Create your views here.

def new_problem(request):
    return render(request, 'supportapp/newproblem.html')