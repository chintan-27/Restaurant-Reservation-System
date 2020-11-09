import math, random
import uuid
from django.shortcuts import render,redirect
from .forms import SignUpForm, ReviewForm, SignUpHotel, PhotosForm
from .models import Restaurant, RestaurantTables, Reservation, Review, User, Location, RestaurantPhotos, CustomerPhotos
import datetime
from django.contrib.auth.decorators import login_required
from django import template
register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

# Create your views here.
def IndexView(request):
    restaurants = Restaurant.objects.all()[:10]
    a = {'restaurants':restaurants}
    restaurantphotos = RestaurantPhotos.objects.filter(ptype = "NORMAL")
    c = {'restaurantphotos':restaurantphotos}
    locations = Location.objects.all()
    b = {'locations':locations}
    response = {**a,**b,**c}
    return render(request,'index.html',response)

def FilterIndex(request,type,filter):
    restaurantphotos = RestaurantPhotos.objects.filter(ptype = "NORMAL")
    c = {'restaurantphotos':restaurantphotos}
    locations = Location.objects.all()
    b = {'locations':locations}
    if(type == "location"):
        location = Location.objects.get(location=filter)
        restaurants = Restaurant.objects.filter(location = location)[:10]
        a = {'restaurants':restaurants}
    else:
        if(filter == "food"):
            restaurants = Restaurant.objects.all().order_by('-ratingbyfood')[:10]
            a = {'restaurants':restaurants}
        elif(filter == "staff"):
            restaurants = Restaurant.objects.all().order_by('-ratingbystaff')[:10]
            a = {'restaurants':restaurants}
        elif(filter == "location"):
            restaurants =Restaurant.objects.all().order_by('-ratingbylocation')[:10]
            a = {'restaurants':restaurants}
        elif(filter == "hygiene"):
            restaurants = Restaurant.objects.all().order_by('-ratingbyhygiene')[:10]
            a = {'restaurants':restaurants}
    response={**a,**b,**c}
    return render(request,'index.html',response)


def registerView(request):
    form=SignUpForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect('login_url')
        else:
            return render(request,'registration/register.html',{'form': form})
    else:
        return render(request,'registration/register.html',{'form': form})


def registerHotelView(request):
    form=SignUpHotel(request.POST)
    if request.method=="POST":
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            username = form.cleaned_data['username']
            location = form.cleaned_data['location']
            m = Location.objects.get(location = location)
            password = form.cleaned_data['password1']
            restaurant_name = form.cleaned_data['restaurant_name']
            description = form.cleaned_data['description']
            city = form.cleaned_data['city']
            ratingbystaff = form.cleaned_data['ratingbystaff']
            ratingbyfood = form.cleaned_data['ratingbyfood']
            ratingbylocation = form.cleaned_data['ratingbylocation']
            ratingbyhygiene = form.cleaned_data['ratingbyhygiene']
            ab = User(username = username, email=email,phone=phone,first_name=first_name,last_name=last_name,usertype="restaurant")
            ab.save()
            bc = Restaurant(restaurant_name=restaurant_name,location=m,username = ab,restaurant_id = uuid.uuid1(),description=description,city=city,ratingbyfood=ratingbyfood,ratingbystaff=ratingbystaff,ratingbylocation=ratingbylocation,ratingbyhygiene=ratingbyhygiene)
            bc.save()
            return redirect('login_url')
        else:
            return render(request,'registerhotel.html',{'form': form})
    else:
        return render(request,'registerhotel.html',{'form': form})

@login_required
def SearchView(request):
    if request.user.is_authenticated:
        return render(request, 'search.html',)
    else:
        return redirect('login_url')

@login_required
def SelectRestaurant(request,day,start_time,end_time,persons):
    if request.user.is_authenticated:
        availability = []
        restaurants = Restaurant.objects.all()
        restaurantphotos = RestaurantPhotos.objects.filter(ptype = "NORMAL")
        j= {'restaurantphotos':restaurantphotos}
        a,b,c,d,e = {'start_time':start_time},{'end_time':end_time},{'persons':persons},{'restaurants':restaurants},{'day':day}
        if(day == "TODAY"):
            date = datetime.date.today()
        elif(day == "TOMORROW"):
            date = datetime.date.today() +  datetime.timedelta(1)
        else:
            date = datetime.date.today() +  datetime.timedelta(2)
        start = datetime.datetime.strptime(start_time+':00','%H:%M:%S').time()
        end = datetime.datetime.strptime(end_time+':00','%H:%M:%S').time()
        for restaurant in restaurants:
            tables = RestaurantTables.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id)
            reservations = Reservation.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id).filter(date=date)
            totaltable = []
            totaltable.append(restaurant.restaurant_name)
            for i in tables:
                totaltable.append(i.tablefor)
                totaltable.append(i.nooftables)
            for i in reservations:
                tables_for = []
                no_of_tables = []
                if((i.start_time<=start and i.end_time>start and i.end_time<=end) or (i.start_time>=start and i.end_time<=end) or (i.start_time>=start and i.start_time<end and i.end_time>=start)):
                    for r in i.tablesfor:
                        tables_for.append(int(r))
                    for r in i.nooftables:
                        no_of_tables.append(int(r))
                    for n in range(len(tables_for)):
                        index = 0
                        for z in range(len(totaltable)):
                            if(tables_for[n] == totaltable[z]):
                                index = z
                        totaltable[index+1] = totaltable[index+1] - no_of_tables[n]
            total_available = 0
            for n in range(1,len(totaltable)):
                if(n%2 == 0):
                    total_available = total_available + (totaltable[n]*totaltable[n-1])
            if(total_available > int(persons)):
                totaltable.append("Available")
            else:
                totaltable.append("Unavailable")
            availability.append(totaltable)
        f = {'availability':availability}
        response = {**a,**b,**c,**d,**e,**f,**j}
        return render(request,'search.html',response)
    else:
        return redirect('login_url')

def options(no_of_tables,persons):
    options = []
    index = 0
    for i in no_of_tables:
        sum = 0
        option = []
        sum = sum + i
        if(sum < persons):
            for j in no_of_tables:
                sum = i + j
                if(sum < persons):
                    for k in no_of_tables:
                        sum = i + j + k
                        if(sum < persons):
                            for l in no_of_tables:
                                sum = i + j + k + l
                                if(sum>=persons):
                                    option = []
                                    option.append(i)
                                    option.append(j)
                                    option.append(k)
                                    option.append(l)
                                    options.append(option)
                                    continue

                        else:
                            option = []
                            option.append(i)
                            option.append(j)
                            option.append(k)
                            options.append(option)
                            continue

                else:
                    option = []
                    option.append(i)
                    option.append(j)
                    options.append(option)
                    continue
        else:
            option = []
            option.append(i)
            options.append(option)
            continue
    return options

def removeDuplicates(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res

def OccurenceList(test_list):
    res = []
    temp_list = removeDuplicates(test_list)
    for i in temp_list:
        res.append(test_list.count(i))
    return res

def SelectTables(request,restaurant_id,day,start_time,end_time,persons):
    if(request.user.is_authenticated):
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        review = Review.objects.filter(restaurant_name = restaurant)
        w = {'reviews':review}
        a = {'restaurant':restaurant}
        b,c,d,e = {'start_time':start_time},{'end_time':end_time},{'persons':persons},{'day':day}
        tables = RestaurantTables.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id)
        if(day == "TODAY"):
            date = datetime.date.today()
        elif(day == "TOMORROW"):
            date = datetime.date.today() +  datetime.timedelta(1)
        else:
            date = datetime.date.today() +  datetime.timedelta(2)
        start = datetime.datetime.strptime(start_time+':00','%H:%M:%S').time()
        end = datetime.datetime.strptime(end_time+':00','%H:%M:%S').time()
        reservations = Reservation.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id).filter(date=date)
        totaltable = []
        totaltable.append(restaurant.restaurant_name)
        for i in tables:
            totaltable.append(i.tablefor)
            totaltable.append(i.nooftables)
        for i in reservations:
            tables_for = []
            no_of_tables = []
            if((i.start_time<=start and i.end_time>start and i.end_time<=end) or (i.start_time>=start and i.end_time<=end) or (i.start_time>=start and i.start_time<end and i.end_time>=start)):
                for r in i.tablesfor:
                    tables_for.append(int(r))
                for r in i.nooftables:
                    no_of_tables.append(int(r))
                for n in range(len(tables_for)):
                    index = 0
                    for z in range(len(totaltable)):
                        if(tables_for[n] == totaltable[z]):
                            index = z
                    totaltable[index+1] = totaltable[index+1] - no_of_tables[n]
        # options = []
        no_of_tables = []
        availabletables = []
        for i in range(1,len(totaltable)):
            if(i%2 == 0):
                availabletables.append(totaltable[i])
            else:
                no_of_tables.append(totaltable[i])
        # print(type(no_of_tables))
        tableoptions = options(no_of_tables, int(persons))
        notavailable = []
        for i in tableoptions:
            for j in i:
                if(availabletables[no_of_tables.index(j)] < 0):
                    notavailable.append(i)
                    break
        for i in notavailable:
            tableoptions.remove(i)
        recommended = []
        notrecommended = []
        for i in tableoptions:
            i.sort()
        tableoptions = removeDuplicates(tableoptions)
        bestoptions = []
        one,two,three,four = [],[],[],[]
        for i in tableoptions:
            min1,min2,min3,min4 = 999,999,999,999
            if(len(i) == 1):
                if(sum(i) < min1):
                    min1 = sum(i)
                    one = i
            elif(len(i) == 2):
                if(sum(i) < min2):
                    min2 = sum(i)
                    two = i
            elif(len(i) == 3):
                if(sum(i) < min3):
                    min3 = sum(i)
                    three = i
            elif(len(i) == 4):
                if(sum(i) < min4):
                    min4 = sum(i)
                    four = i
        bestoptions.append(one)
        bestoptions.append(two)
        bestoptions.append(three)
        bestoptions.append(four)
        res = []
        for i in bestoptions:
            if(i != []):
                res.append(i)
        bestoptions = res
        f = {'bestoptions':bestoptions}
        restaurantphotos = RestaurantPhotos.objects.filter(restaurant_name = restaurant)
        j= {'restaurantphotos':restaurantphotos}
        response = {**a,**b,**c,**d,**e,**f,**j,**w}
        return render(request,'tables.html',response)
    else:
        return redirect('login_url')


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
@login_required
def ConfirmReservation(request,restaurant_id,day,start_time,end_time,persons,tables):
    if(request.user.is_authenticated):
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        date = datetime.date.today()
        if(day == "TODAY"):
            date = datetime.date.today()
        elif(day == "TOMORROW"):
            date = datetime.date.today() +  datetime.timedelta(1)
        else:
            date = datetime.date.today() +  datetime.timedelta(2)
        start = datetime.datetime.strptime(start_time+':00','%H:%M:%S').time()
        end = datetime.datetime.strptime(end_time+':00','%H:%M:%S').time()
        combination = []
        for i in tables:
            combination.append(int(i))
        a = removeDuplicates(combination)
        b = OccurenceList(combination)
        a = map(str,a)
        b = map(str,b)

        tablesfor = "".join(a)
        nooftables = "".join(b)

        reservation = Reservation(reservation_id = uuid.uuid1(),restaurant_id = restaurant, username = request.user, date = date, start_time = start, end_time = end, tablesfor = tablesfor, nooftables = nooftables,otp = generateOTP(), done = False)
        reservation.save()

        return redirect("home")
    else:
        return redirect('login_url')

@login_required
def CheckOtp(request,reservation_id,otp):
    reservation = Reservation.objects.get(reservation_id=reservation_id)
    if(reservation.otp == int(otp)):
        reservation.done = True
        reservation.save()
        print(reservation.done)
        return redirect('Dashboard')
    else:
        return redirect('Dashboard')

@login_required
def Dashboard(request):
    if(request.user.is_authenticated):
        user = request.user
        if(user.usertype == "restaurant"):
            restaurant = Restaurant.objects.get(username = user)
            reservations = Reservation.objects.filter(restaurant_id = restaurant).order_by('date')
            a = {'reservations' : reservations}
            return render(request,'hoteldashboard.html',a)
        else:
            reservations = Reservation.objects.filter(username = user).order_by('date')
            a = {'reservations' : reservations}
            return render(request,'dashboard.html',a)
    else:
        return redirect('login_url')

@login_required
def ReviewView(request, restaurant_id):
    if(request.user.is_authenticated):
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        review = Review.objects.filter(restaurant_name = restaurant)
        form = ReviewForm(request.POST)
        if(request.method == "POST"):
            if(form.is_valid()):
                review_title = form.cleaned_data['review_title']
                review = form.cleaned_data['review']
                ratingbystaff  = form.cleaned_data['ratingbystaff']
                ratingbyfood = form.cleaned_data['ratingbyfood']
                ratingbylocation = form.cleaned_data['ratingbylocation']
                ratingbyhygiene = form.cleaned_data['ratingbyhygiene']
                sumfood = 0
                sumstaff = 0
                sumlocation = 0
                sumhygiene = 0
                for i in review:
                    sumfood = sumfood + ratingbyfood
                    sumstaff = sumstaff + ratingbystaff
                    sumlocation = sumlocation + ratingbylocation
                    sumhygiene = sumhygiene + ratingbyhygiene
                restaurant.ratingbyfood = sumfood/(len(review)+1)
                restaurant.ratingbystaff = sumstaff/(len(review)+1)
                restaurant.ratingbylocation = sumlocation/(len(review)+1)
                restaurant.ratingbyhygiene = sumhygiene/(len(review)+1)
                restaurant.save()
                a = Review(review_id=uuid.uuid1(),restaurant_name = restaurant, username = request.user,review_title=review_title,review=review,ratingbystaff=ratingbystaff,ratingbyfood=ratingbyfood,ratingbylocation=ratingbylocation,ratingbyhygiene=ratingbyhygiene)
                a.save()
                return redirect('Dashboard')
            return render(request,'review.html',{'form':form})
        return render(request,'review.html',{'form':form})
    else:
        return redirect('login_url')


@login_required
def AddRestaurantPhotos(request,restaurant_id):
    form = PhotosForm(request.POST,request.FILES)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    if request.method == "POST":
        if form.is_valid():
            image = form.cleaned_data['form']
            a = RestaurantPhotos(restaurant_name = restaurant,photos=image)
            a.save()
            return redirect("dashboard")
    return render(request,'photos.html',{'form':form})

@login_required
def AddCustomerPhotos(request,restaurant_id):
    form = PhotosForm(request.POST,request.FILES)
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    if request.method == "POST":
        if form.is_valid():
            image = form.cleaned_data['form']
            a = CustomerPhotos(restaurant_name = restaurant,username=request.user,photos=image)
            a.save()
            return redirect("dashboard")
    return render(request,'photos.html',{'form':form})

def OneRestaurant(request,restaurant_id):
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    review = Review.objects.filter(restaurant_name = restaurant)
    w = {'reviews':review}
    restaurantphotos = RestaurantPhotos.objects.filter(restaurant_name = restaurant)
    j= {'restaurantphotos':restaurantphotos}
    a = {'restaurant':restaurant}
    response = {**a,**j,**w}
    return render(request,'oneres.html',response)

@login_required
def CheckAvailabilityOne(request,restaurant_id,day,start_time,end_time,persons):
    if(request.user.is_authenticated):

        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        a,b,c,d,e = {'start_time':start_time},{'end_time':end_time},{'persons':persons},{'restaurant':restaurant},{'day':day}
        if(day == "TODAY"):
            date = datetime.date.today()
        elif(day == "TOMORROW"):
            date = datetime.date.today() +  datetime.timedelta(1)
        else:
            date = datetime.date.today() +  datetime.timedelta(2)
        start = datetime.datetime.strptime(start_time+':00','%H:%M:%S').time()
        end = datetime.datetime.strptime(end_time+':00','%H:%M:%S').time()
        tables = RestaurantTables.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id)
        reservations = Reservation.objects.filter(restaurant_id__restaurant_id = restaurant.restaurant_id).filter(date=date)
        totaltable = []
        totaltable.append(restaurant.restaurant_name)
        for i in tables:
            totaltable.append(i.tablefor)
            totaltable.append(i.nooftables)
        for i in reservations:
            tables_for = []
            no_of_tables = []
            if((i.start_time<=start and i.end_time>start and i.end_time<=end) or (i.start_time>=start and i.end_time<=end) or (i.start_time>=start and i.start_time<end and i.end_time>=start)):
                for r in i.tablesfor:
                    tables_for.append(int(r))
                for r in i.nooftables:
                    no_of_tables.append(int(r))
                for n in range(len(tables_for)):
                    index = 0
                    for z in range(len(totaltable)):
                        if(tables_for[n] == totaltable[z]):
                            index = z
                    totaltable[index+1] = totaltable[index+1] - no_of_tables[n]
        total_available = 0
        for n in range(1,len(totaltable)):
            if(n%2 == 0):
                total_available = total_available + (totaltable[n]*totaltable[n-1])
        if(total_available > int(persons)):
            totaltable.append("Available")
        else:
            totaltable.append("Unavailable")
        availability = []
        availability.append(totaltable)
        f = {'availability':availability}
        restaurantphotos = RestaurantPhotos.objects.filter(restaurant_name = restaurant)
        j= {'restaurantphotos':restaurantphotos}
        review = Review.objects.filter(restaurant_name = restaurant)
        w = {'reviews':review}
        response = {**a,**b,**c,**d,**e,**f,**j,**w}
        return render(request,'oneres.html',response)
    else:
        return redirect('login_url')
