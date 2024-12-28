from datetime import timezone
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from slugify import slugify
from .models import Customer, Order, Box, TimeSlot, Master, Service


# Create your views here.
def index(request):
    template_name = 'service/index.html'

    services = Service.objects.select_related(
        'master'
    ).filter(
        is_shown=True,
        master__is_shown=True
    )

    context = {
        'services': services
    }
    return render(request, template_name, context)


def service_detail(request, service_slug):
    template_name = 'service/service_detail.html'

    service = get_object_or_404(
        Service.objects.select_related(
            'master'
        ),
        is_shown=True,
        master__is_shown=True,
        slug=service_slug,
    )

    context = {
        'service': service
    }

    return render(request, template_name, context)


def master_detail(request, master_slug):
    template_name = 'service/master_detail.html'

    master = get_object_or_404(Master, slug=master_slug)

    context = {
        'master': master
    }

    return render(request, template_name, context)


def order_list(request):
    template_name = 'service/order_list.html'

    order_list = Order.objects.select_related(
        'service',
        'master'
    ).filter(
        'service__is_shown' is True,
        'master__is_shown' is True,
        'start_time' == timezone.now()
    )

    context = {
        'order_list': order_list
    }

    return render(request, template_name, context)


def order_detail(request, order_id):
    template_name = 'service/order_detail.html'

    order = get_object_or_404(
        Order.objects.select_related(
            'service',
            'box'
        ),
        order_id
    )

    customer = get_object_or_404(Customer, order=order)

    total_price = order.service.price * customer.discount / 100

    context = {
        'order': order,
        'customer': customer,
        'total_price': total_price
    }

    return render(request, template_name, context)
