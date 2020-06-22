import json
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.template import RequestContext, engines, Context
from django.template.loader import render_to_string

import mainapp
from constructor_app import utils
from constructor_app.models import Template, Order
from mainapp.models import Hotel, HotelFacility, Room, RoomGallery

from constructor_app.models import WebSite


@login_required(login_url='/auth/login/')
def main(request):
    templates = Template.objects.all()
    hotel_id = request.GET['hotel_id']

    return render(request, 'constructor_app/main.html', {'templates': templates, 'hotel_id': hotel_id})


@login_required(login_url='/auth/login/')
def about_template(request, id):
    # get template
    template = get_object_or_404(Template, id=id)

    hotel_id = request.GET.get('hotel_id', 0)

    return render(request, 'constructor_app/detail.html', {'template': template, 'hotel_id': hotel_id})


@login_required(login_url='/auth/login/')
def orders_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'constructor_app/orders.html', {'orders': orders})


@login_required(login_url='/auth/login/')
def pack_project(request):
    if request.GET.get('hotel_id', 0) and request.GET.get('template_id', 0):
        # get template
        template = get_object_or_404(Template, id=request.GET.get('template_id'))

        # create order for user
        hotel = get_object_or_404(Hotel, id=request.GET['hotel_id'])
        order = Order.objects.create(user=request.user, hotel=hotel, template=template)

        prj_path = f'{settings.BASE_DIR}/media/preparing_projects/{order.id}'  # new project path
        template_path = f'{settings.BASE_DIR}/{order.template.path}'

        # create project folder
        os.mkdir(prj_path)
        utils.copytree(template_path, prj_path)

        # copying projects to zip archive
        if order.status == Order.FORMING:
            django_engine = engines['django']
            template = django_engine.from_string(open(prj_path + '/index.html', 'r').read())

            context = {'hotel': hotel, 'domain': settings.DOMAIN_NAME,
                       'facilities': HotelFacility.objects.filter(hotel=hotel),
                       'rooms': [{'id': room.id, 'name': room.name, 'avatar': '', 'price': room.price} for room in
                                 Room.objects.filter(hotel=hotel, is_active=True)]}

            for room in context['rooms']:
                try:
                    room['avatar'] = RoomGallery.objects.get(room__id=room['id'], is_avatar=True)
                except mainapp.models.RoomGallery.DoesNotExist:
                    room['avatar'] = RoomGallery.objects.filter(room__id=room['id'])[0]

            data = template.render(context)

            # rewrite page index.html
            file = open(os.path.join(prj_path, 'index.html'), 'w')
            file.write(str(data))
            file.close()

            utils.zipdir(order.hotel.name + str(order.id), prj_path,
                         f'{settings.BASE_DIR}/media/ready_projects', order.id)

            order.status = Order.READY
            order.save()
        else:
            return redirect('main:404')

        return render(request, 'constructor_app/result.html',
                      {'order': order,
                       'path': f'{settings.DOMAIN_NAME}/media/ready_projects/{order.hotel.name}{order.id}.zip'})
