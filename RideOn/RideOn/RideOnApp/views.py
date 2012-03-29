from RideOnApp.models import Driver, Rider, RideRequest, User
from django.core import serializers
from django.http import HttpResponse
from functools import wraps
# Create your views here.

def requireParams(*params):
    def decorator(func):
        def check(request):
            for r in params:
                if r not in request.REQUEST:
                    return HttpResponse("1", "application/json")
            return func(request)
        return wraps(func)(check)
    return decorator

@requireParams("name", "email")
def addUser(request):
    u = User(name = request.REQUEST["name"], email = request.REQUEST["email"])
    u.save()
    return HttpResponse("0", "application/json")

def getUsers(request):
    if "id" in request.REQUEST:
        data = User.objects.filter(id = request.REQUEST["id"])
    else:
        data = User.objects.all()
    data = serializers.serialize("json", data, ensure_ascii=False)
    return HttpResponse(data, "application/json")
    
def getDrivers(request):
    data = serializers.serialize("json", Driver.objects.all(), ensure_ascii=False)
    return HttpResponse(data, "application/json")

@requireParams("source", "destination", "user")
def addDriver(request):
    try:
        u = User.objects.get(id=request.REQUEST["user"])
    except User.DoesNotExist:
        return HttpResponse("2", "application/json")
    
    try:
        Driver.objects.get(user=u)
    except Driver.DoesNotExist:
        try:
            Rider.objects.get(user=u)
        except Rider.DoesNotExist:
            d = Driver(source=request.REQUEST["source"], destination=request.REQUEST["destination"], user=u)
            d.save()
            return HttpResponse("0", "application/json")
    return HttpResponse("3", "application/json")

@requireParams("user")
def removeDriver(request):
    try:
        u = User.objects.get(id = request.REQUEST["user"])
    except User.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    try:
        d = Driver.objects.get(user=u)
    except Driver.DoesNotExist:
        return HttpResponse("2.2", "application/json")
    d.delete()
    return HttpResponse("0", "application/json")

def getRiders(request):
    data = serializers.serialize("json", Rider.objects.all(), ensure_ascii=False)
    return HttpResponse(data, "application/json")

@requireParams("source", "destination", "user")
def addRider(request):
    try:
        u = User.objects.get(id=request.REQUEST["user"])
    except User.DoesNotExist:
        return HttpResponse("2", "application/json")
    try:
        Rider.objects.get(user=u)
    except Rider.DoesNotExist:
        try:
            Driver.objects.get(user=u)
        except Driver.DoesNotExist:
            r = Rider(source=request.REQUEST["source"], destination=request.REQUEST["destination"], user=u)     
            r.save()
            return HttpResponse("0", "application/json")
    return HttpResponse("3", "application/json")

@requireParams("user")
def removeRider(request):
    required = ("user")
    if required not in request.REQUEST:
        return HttpResponse("1", "application/json")
    try:
        u = User.objects.get(id = request.REQUEST["user"])
    except User.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    try:
        r = Rider.objects.get(user=u)
    except Rider.DoesNotExist:
        return HttpResponse("2.2", "application/json")
    r.delete()
    return HttpResponse("0", "application/json")

def getRideRequests(request):
    if "user" in request.REQUEST:
        u = User.objects.get(id=request.REQUEST["user"])
        data = RideRequest.objects.filter(driver__user=u)
        if not data:
            data = RideRequest.objects.filter(rider__user=u)
    else:
        data  = RideRequest.objects.all()
    data = serializers.serialize("json", data, ensure_ascii=False)
    return HttpResponse(data, "application/json")

@requireParams("rider", "driver")
def addRideRequest(request):
    try:
        d = Driver.objects.get(id=request.REQUEST["driver"])
        r = Rider.objects.get(id=request.REQUEST["rider"]) 
    except Driver.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    except Rider.DoesNotExist:
        return HttpResponse("2.2", "application/json")
    try:
        RideRequest.objects.get(driver = d, rider = r)
    except RideRequest.DoesNotExist:
        rr = RideRequest(rider = r,driver = d)
        rr.save()
        return HttpResponse("0", "application/json")
    return HttpResponse("3", "application/json")

@requireParams("id")
def removeRideRequest(request):
    try:
        rr = RideRequest.objects.get(id = request.REQUEST["id"])
    except RideRequest.DoesNotExist:
        return HttpResponse("2", "application/json")
    rr.delete()
    return HttpResponse("0", "application/json")

@requireParams("id", "accept")
def acceptRideRequest(request):
    try:
        rr = RideRequest.objects.get(id = request.REQUEST["id"])
    except RideRequest.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    rr.accepted = request.REQUEST["accept"]
    rr.save()
    return HttpResponse("0", "application/json")

@requireParams("id", "type")
def enterRide(request):
    try:
        ride = RideRequest.objects.get(id=request.REQUEST["id"])
    except RideRequest.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    
    if ride.entered:
        return HttpResponse("3", "application/json")
    if request.REQUEST["type"] == "driver":
        ride.d_ack = True
    elif request.REQUEST["type"] == "rider":
        ride.r_ack = True
    else:
        return HttpResponse("2.2", "application/json")
    
    if ride.d_ack == ride.r_ack == True:
        ride.entered = True
        ride.d_ack = ride.r_ack = False
    
    ride.save()
    return HttpResponse("0", "application/json")

@requireParams("id", "type")
def exitRide(request):
    try:
        ride = RideRequest.objects.get(id=request.REQUEST["id"])
    except RideRequest.DoesNotExist:
        return HttpResponse("2.1", "application/json")
    
    if not ride.entered:
        return HttpResponse("3", "application/json")
    if request.REQUEST["type"] == "driver":
        ride.d_ack = True
    elif request.REQUEST["type"] == "rider":
        ride.r_ack = True
    else:
        return HttpResponse("2.2", "application/json")
    
    if ride.d_ack == ride.r_ack == True:
        ride.exited = True
        ride.d_ack = ride.r_ack = False
    ride.save()
    return HttpResponse("0", "application/json")