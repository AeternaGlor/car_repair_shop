from datetime import timezone
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Customer, Order, Box, TimeSlot, Master, Service
from . import utils


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

    orders = Order.objects.select_related(
        'service',
        'box',
        'customer'
    ).filter(
        start_time__gte=timezone.now()
    )

    context = {
        'orders': orders
    }

    return render(request, template_name, context)


def order_detail(request, order_id):
    template_name = 'service/order_detail.html'

    order = get_object_or_404(
        Order.objects.select_related(
            'service',
            'customer',
            'box'
        ),
        id=order_id
    )

    final_price = order.service.price * (100 - order.customer.discount) / 100
    final_price = int(final_price)

    ruble_word_form = utils.PluralRubleForm(final_price)

    start_time = order.start_time.strftime('%d/%m/%Y')
    print(start_time)

    context = {
        'order': order,
        'start_time': start_time,
        'final_price': final_price,
        'ruble_word_form': ruble_word_form
    }

    return render(request, template_name, context)
