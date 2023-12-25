from django.shortcuts import render
from .models import counter
from django.http import response
# Create your views here.

def countm1(request):
    try: 
        m1 = counter.objects.get(name="m1")
    except counter.DoesNotExist: 
        m1 = None 
    if m1 is None: 
        m1 = counter(name="m1")
        m1.amount += 1
        m1.save()
        return response.HttpResponse("Create m1 and increment its value") 
    else: 
        m1.amount += 1 
        m1.save() 
        return response.HttpResponse("get m1 and increment its value") 


def countm2(request):
    try: 
        m2 = counter.objects.get(name="m2")
    except counter.DoesNotExist: 
        m2 = None 
    if m2 is None: 
        m2 = counter(name="m2")
        m2.amount += 1
        m2.save() 
        return response.HttpResponse("create m2 and increment its value ")
    else: 
        m2.amount += 1 
        m2.save() 
        return response.HttpResponse("get m2 and increment its value") 


