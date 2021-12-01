from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from .models import Resturants,Tables,Reservation
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from .decorators import *
from .backends import *
# Create your views here.

#homepage
def homepage(request):
    all_location = Resturants.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Resturants.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            # for each_reservation in Reservation.objects.all():
            #     if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
            #         pass
            #     elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
            #         pass
            #     else:
            #         rr.append(each_reservation.room.id)
                
            room = Tables.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(request,"Sorry No Rooms Are Available on this time period")
            data = {'rooms':room,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)

#about
def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))

#user sign up
def user_sign_up(request):
    if request.method =="POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if Account.objects.all().get(username=username):
                messages.warning(request,"Username Not Available")
                return redirect('userloginpage')
        except:
            pass
            
        account = Account()
        account.fname = first_name
        account.lname = last_name
        account.username = username
        account.email = email
        account.password = password1
        account.is_staff = False
        account.save()


        user = authenticate(username=username, password=password1)
        messages.success(request,"Registration Successfull")
        login(request, user)
        return redirect("userloginpage")
    return render(request= 'homepage')
#staff sign up
def staff_sign_up(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("staffpanel")
    if request.method =="POST":
        user_name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if Account.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = Account.objects.create_user(username=user_name, email= email, password=password1)
        new_user.is_superuser=False
        new_user.is_staff=True
        new_user.save()
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')
#user login and signup page
@unauthenticated_user
def user_log_sign_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect("viewApp")


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            messages.success(request,"successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.error(request,"Incorrect username or Password")
            return redirect('userloginpage')

    response = render(request,'user/userlogsign.html')
    return HttpResponse(response)

def Guestreservation(request):
    if request.method == "POST":
        Name = request.POST['Name']

        phone = request.POST['phone']
        email = request.POST['email']
        partysize = int(request.POST['party'])
        arrival = request.POST['arrival']

        #payment
        card_no= request.POST['card_no']
        expiration = request.POST['expiration'] 
        cvc_no = request.POST['cvc']
        if partysize > 6:
            reservation_fee =+ 5

        applicant_data = Reservation(
            Client_name=Name, phone=phone, email=email, partysize= partysize, 
            arrival=arrival,card_no=card_no,expiration=expiration, cvc_no=cvc_no, reservation_fee=reservation_fee
        )
        applicant_data.save()
        print("it worked")
        return HttpResponse ("Data Saved Good Job")
    else:
        return render(request, 'user')
    return render(request, 'Guest.html' )

@login_required(login_url='/user')
def userReservation(request):

    if request.method == 'POST':

        Name = request.POST['Name']
        phone = request.POST['phone']
        email = request.POST['email']
        partysize = int(request.POST['party'])
        arrival = request.POST['arrival']

        #payment
        card_no= request.POST['card_no']
        expiration = request.POST['expiration'] 
        cvc_no = request.POST['cvc']
        if partysize > 6:
            reservation_fee =+ 5

        applicant_data = Reservation(
            Client_name=Name, phone=phone, email=email, partysize= partysize, 
            arrival=arrival,card_no=card_no,expiration=expiration, cvc_no=cvc_no, reservation_fee=reservation_fee
        )
        applicant_data.save()
        print("it worked")
        return HttpResponse ("Data Saved Good Job")
    else:
        return render(request, 'user')

#logout for admin and user 
def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')

#staff login and signup page
def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        
        if user.is_staff:
            login(request,user)
            return redirect('staffpanel')
        
        else:
            messages.success(request,"Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request,'staff/stafflogsign.html')
    return HttpResponse(response)

#staff panel page
@login_required(login_url='/staff')
def panel(request):
    
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    
    rooms = Tables.objects.all()
    total_rooms = len(rooms)
    available_rooms = len(Tables.objects.all().filter(status='1'))
    unavailable_rooms = len(Tables.objects.all().filter(status='2'))
    reserved = len(Reservation.objects.all())

    hotel = Resturants.objects.values_list('location','id').distinct().order_by()

    response = render(request,'staff/panel.html',{'location':hotel,'reserved':reserved,'rooms':rooms,'total_rooms':total_rooms,'available':available_rooms,'unavailable':unavailable_rooms})
    return HttpResponse(response)

#for editing room information
@login_required(login_url='/staff')
def edit_room(request):
    if request.user.is_staff == False:   
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_room = Tables.objects.all().get(id= int(request.POST['roomid']))
        hotel = Resturants.objects.all().get(id=int(request.POST['hotel']))
        old_room.room_type  = request.POST['roomtype']
        old_room.capacity   =int(request.POST['capacity'])
        old_room.price      = int(request.POST['price'])
        old_room.size       = int(request.POST['size'])
        old_room.hotel      = hotel
        old_room.status     = request.POST['status']
        old_room.room_number=int(request.POST['roomnumber'])

        old_room.save()
        messages.success(request,"Room Details Updated Successfully")
        return redirect('staffpanel')
    else:
    
        room_id = request.GET['roomid']
        room = Tables.objects.all().get(id=room_id)
        response = render(request,'staff/editroom.html',{'room':room})
        return HttpResponse(response)

@login_required(login_url='/staff')
def deleteTable(request):
    if request.user.is_staff == False:   
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)


#for adding room
@login_required(login_url='/staff')
def add_new_room(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        total_rooms = len(Tables.objects.all())
        new_room = Tables()
        hotel = Resturants.objects.all().get(id = int(request.POST['hotel']))
        print(f"id={hotel.id}")
        print(f"name={hotel.name}")


        new_room.roomnumber = total_rooms + 1
        new_room.room_type  = request.POST['roomtype']
        new_room.capacity   = int(request.POST['capacity'])
        new_room.size       = int(request.POST['size'])
        new_room.capacity   = int(request.POST['capacity'])
        new_room.hotel      = hotel
        new_room.status     = request.POST['status']
        new_room.price      = request.POST['price']

        new_room.save()
        messages.success(request,"New Room Added Successfully")
    
    return redirect('staffpanel')

#booking room page
@login_required(login_url='/user')
def book_room_page(request):
    room = Tables.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'user/bookroom.html',{'room':room}))

#For booking the room
@login_required(login_url='/user')
def book_room(request):
    
    if request.method =="POST":

        room_id = request.POST['room_id']
        
        room = Tables.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room = room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Tables.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = Account.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')

def handler404(request):
    return render(request, '404.html', status=404)

@login_required(login_url='/staff')   
def view_room(request):
    room_id = request.GET['roomid']
    room = Tables.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request,'staff/viewroom.html',{'room':room,'reservations':reservation}))

@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = Account.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'user/mybookings.html',{'bookings':bookings}))

@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        owner = request.POST['new_owner']
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        hotels = Tables.objects.all().filter(location = location , state = state)
        if hotels:
            messages.warning(request,"Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_hotel = Resturants()
            new_hotel.owner = owner
            new_hotel.location = location
            new_hotel.state = state
            new_hotel.country = country
            new_hotel.save()
            messages.success(request,"New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")
    
#for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
   
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'staff/allbookings.html',{'bookings':bookings}))
    


        