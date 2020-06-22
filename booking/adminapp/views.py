import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
#     DeleteView

from mainapp.models import Hotel, Room, RoomGallery, HotelFacility
from geopy.geocoders import Nominatim
from adminapp.forms import HotelForm, RoomForm, HotelFacilityForm
from adminapp import utils

from mainapp.models import Facility


@login_required(login_url='/auth/login/')
def main(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)
    days = [datetime.date.today() + datetime.timedelta(days=dayR) for dayR in range(14)]
    now = datetime.datetime.now()

    # get hotel data
    hotel_data = []
    for hotel in hotels:
        hotel_data.append({"name": hotel.name,
                           "rooms": [{"id": room.id,
                                      "name": room.name,
                                      "price": room.price} for room in
                                     Room.objects.filter(hotel=hotel, is_active=True)]})

    rooms = [room for hotel in Hotel.objects.filter(user=request.user, is_active=True) for room in
             Room.objects.filter(hotel=hotel, is_active=True)]

    context = {'hotels': hotels, 'days': days, 'rooms': rooms,
               'now': f'{now.hour}:{now.minute}', 'hotel_data': hotel_data}

    return render(request, 'adminapp/main.html', context)


# function that checks the hotel's address
def ajax_check_address(request):
    # if address is valid and function returned coordinates -> address passed check
    # else coordinates list is empty
    address = request.GET.get('address', None)

    geolocator = Nominatim(user_agent="check_address")
    location = geolocator.geocode(address)
    if location:
        coordinates = [location.latitude, location.longitude]
        message = ''
    else:
        coordinates = []
        message = 'Invalid address'

    return JsonResponse({'coordinates': coordinates, 'address': location.address,
                         'message': message})


# function that creates room in hotel
@login_required(login_url='/auth/login/')
def create_room(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)

    if request.method == 'POST':
        # get data
        hotel = request.POST['hotel']
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        adults = request.POST['adults']
        kids = request.POST['kids']
        infants = request.POST['infants']
        images = request.POST.get('image_count', 0)

        # try:
        # get hotel
        hotel = Hotel.objects.get(name=hotel, is_active=True)
        # try to find a room with the same name
        rooms = Room.objects.filter(hotel=hotel, name=name, is_active=True)

        if rooms:
            try:
                # get the last room's name
                # and get the count number ex. 'Room 1' (result - '1')
                existing_room_count_number = int(rooms.reverse()[0].name.split(' ')[-1])
                # increase it
                existing_room_count_number += 1
                # change room name to not duplicate room's name
                name = f'{name} {existing_room_count_number}'
            except ValueError:
                name = f'{name} 1'

        # create room
        room = Room.objects.create(hotel=hotel, name=name,
                                   price=int(price), description=description,
                                   adult=int(adults), kids=int(kids),
                                   infants=int(infants),
                                   is_active=True)

        count = 1
        for image in range(1, int(images) + 1):
            image_file = request.FILES.get(f'image-{image}')
            if image_file:
                if count == 1:
                    RoomGallery.objects.create(room=room, image=image_file, is_avatar=True)
                    count += 1
                else:
                    RoomGallery.objects.create(room=room, image=image_file)

        return HttpResponseRedirect(reverse('management:main'))

        # except Exception as err:
        # print(err)

    context = {'hotels': hotels}
    return render(request, 'adminapp/create_room.html', context)


# page of editing hotel details
@login_required(login_url='/auth/login/')
def edit_room(request, hotel_id, room_id):
    # if there is such room
    hotel = get_object_or_404(Hotel, pk=hotel_id, user=request.user, is_active=True)
    room = get_object_or_404(Room, pk=room_id, hotel=hotel, is_active=True)

    form = RoomForm(request.POST or None, request.FILES or None, instance=room)

    if request.method == 'POST':
        # saving images

        images = request.POST.get('image_count', 0)
        if images:
            for image in range(1, int(images) + 1):
                image_file = request.FILES.get(f'image-{image}')
                if image_file:
                    RoomGallery.objects.create(room=room, image=image_file)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            messages.success(request, "You successfully updated the room")

            context = {'form': form}

            return HttpResponseRedirect(reverse('management:rooms'))

        else:
            messages.warning(request, "The room was not updated successfully.")

    images = RoomGallery.objects.filter(room=room, room__hotel=hotel)
    context = {'form': form, 'hotel_id': hotel_id, 'room_id': room_id, 'room': room, 'images': images}
    return render(request, 'adminapp/edit_room.html', context)


def ajax_delete_image(request):
    try:
        room = request.GET.get('room', None)
        hotel = request.GET.get('hotel', None)
        image = request.GET.get('image', None)
        RoomGallery.objects.get(room__pk=room, room__hotel__pk=hotel,
                                image__contains=image.replace('/media/', '')).delete()
        return JsonResponse({'code': 200})
    except Exception as err:
        return JsonResponse({'code': 500})


# page of editing room details
@login_required(login_url='/auth/login/')
def edit_hotel(request, pk):
    # if there is such hotel
    hotel = get_object_or_404(Hotel, pk=pk, user=request.user, is_active=True)
    facilities = HotelFacility.objects.all().filter(hotel_id=pk)
    facility_names = []
    facility_icons = []
    for name in range(len(facilities)):
        facility_names.append(facilities[name].get_name())
        facility_icons.append(facilities[name].get_icon())
    ficility_dict = dict(zip(facility_names, facility_icons))

    form = HotelForm(request.POST or None, request.FILES or None, instance=hotel)
    form_facility = HotelFacilityForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            messages.success(request, "You successfully updated the post")
            return HttpResponseRedirect(reverse('management:hotels'))

        else:
            messages.warning(request, "The form was not updated successfully.")

    context = {
        'form': form,
        'pk': pk,
        'form_comforts': form_facility,
        'ficility_dict': ficility_dict,
    }

    return render(request, 'adminapp/edit_hotel.html', context)


def ajax_get_rooms(request):
    hotel = get_object_or_404(Hotel, id=request.GET['hotel'])
    return JsonResponse(
        {'rooms': [{'pk': room.pk, 'name': room.name} for room in Room.objects.filter(hotel=hotel, is_active=True)]})


# page of hotel details
@login_required(login_url='/auth/login/')
def hotels(request):
    hotels_ = Hotel.objects.filter(user=request.user, is_active=True)

    content = {'hotels': hotels_}
    return render(request, 'adminapp/hotels.html', content)


# page of room details
@login_required(login_url='/auth/login/')
def rooms(request):
    hotels = Hotel.objects.filter(user=request.user, is_active=True)
    rooms_ = []

    for hotel in hotels:
        rooms_ += Room.objects.filter(hotel=hotel, is_active=True)

    content = {'rooms': rooms_}
    return render(request, 'adminapp/rooms.html', content)


@login_required(login_url='/auth/login')
def delete_room(request, id):
    room = get_object_or_404(Room, id=id, hotel__user=request.user, is_active=True)
    room.is_active = False
    room.save()

    return HttpResponseRedirect(reverse('management:rooms'))


@login_required(login_url='/auth/login')
def delete_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id, user=request.user, is_active=True)
    hotel.is_active = False
    hotel.save()

    return HttpResponseRedirect(reverse('management:hotels'))


# function which creates hotel
@login_required(login_url='/auth/login/')
def create_hotel(request):
    facilities = Facility.objects.all()
    if request.method == 'POST':
        hotel_name = request.POST['name']
        description = request.POST['description']
        stars = request.POST['stars']
        banner = request.FILES['banner']
        location = request.POST['location']
        phone = request.POST['number']

        location = utils.get_address(location)
        hotel = Hotel.objects.create(user=request.user,
                                     name=hotel_name,
                                     description=description,
                                     stars=stars,
                                     banner=banner,
                                     location=location,
                                     phone_number=phone,
                                     is_active=True)

        # adding hotel facilities
        for facility in facilities:
            if (facility.name in request.POST) and request.POST.get(facility.name):
                HotelFacility.objects.create(hotel=hotel, facility=facility)

        return HttpResponseRedirect(reverse('management:main'))

    return render(request, 'adminapp/create_hotel.html', {'facilities': facilities})


"""
---------------Возможный вариант отображения отелей:---------------------------

class HotelList(ListView):
    model = Hotel

    def get_queryset(self):
        return Hotel.objects.filter(user=self.request.user)


class HotelItemsCrete(CreateView):
    model = Hotel
    fields = []
    success_url = reverse_lazy('adminapp:main')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        hotel_form_set = inlineformset_factory(Hotel, HotelFacility,
                                               form=HotelFacilityForm, extra=1)

        if self.request.POST:
            formset = hotel_form_set(self.request.POST, self.request.FILES)
        else:
            formset = hotel_form_set()
        data['hotelfacility'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        hotelfacility = context['hotelfacility']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if hotelfacility.is_valid():
                hotelfacility.instance = self.object
                hotelfacility.save()

        return super().form_valid(form)


class HotelRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'оттель/просмотр'
        return context


class HotelItemsUpdate(UpdateView):
    model = Hotel
    fields = []
    success_url = reverse_lazy('adminapp:main')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        hotel_form_set = inlineformset_factory(Hotel, HotelFacility,
                                               form=HotelFacilityForm, extra=1)

        if self.request.POST:
            data['hotelfacility'] = hotel_form_set(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = hotel_form_set(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['facility'] = form.instance.facility.name
            data['hotelfacility'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        hotelfacility = context['hotelfacility']

        with transaction.atomic():
            self.object = form.save()
            if hotelfacility.is_valid():
                hotelfacility.instance = self.object
                hotelfacility.save()

        return super().form_valid(form)


class HotelDelete(DeleteView):
    model = Hotel
    success_url = reverse_lazy('adminapp:main')
"""
