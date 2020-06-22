from django.shortcuts import render, redirect

# Create your views here.
from supportapp.forms import ProblemForm


def new_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        obj = form.save()
        obj.user = request.user
        obj.save()

        return redirect('main:main')
    else:
        form = ProblemForm()

    return render(request, 'supportapp/newproblem.html', {'form': form})