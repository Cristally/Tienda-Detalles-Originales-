from django.shortcuts import render

# Create your views here.
def VistaBase(request):
    return render(request, 'base.html')