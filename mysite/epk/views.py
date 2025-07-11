from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def main(request):
    return render(request, 'epk/main.html')

def customerWaitingList(request):
    data = {
        "customer1": {"name": "Customer 1", "status": "Customer 1 is waiting"},
        "customer2" : {"name": "Customer 2", "status": "Customer 2 is waiting"},
        };
    return JsonResponse(data)

def customerWorkingList(request):
    data = {
        "customer3": {"name": "Customer 3", "status": "You are working on Customer 3"},
        "customer4" : {"name": "Customer 4", "status": "You are working on Customer 4"},
        };
    return JsonResponse(data)