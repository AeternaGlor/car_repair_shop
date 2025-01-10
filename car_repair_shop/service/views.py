from datetime import timezone
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Customer, Order, Box, TimeSlot, Master, Service
from . import utils
from . import forms


# Create your views here.
def index(request):
    template_name = 'service/index.html'

    services = Service.objects.select_related(
        'master'
    ).filter(
        is_shown=True,
        master__is_shown=True
    )

    paginator = Paginator(services, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, template_name, context)


def service_detail(request, service_slug):
    template_name = 'service/service_detail.html'

    service = get_object_or_404(
        Service,
        slug=service_slug,
    )

    master = service.master

    context = {
        'service': service,
        'master': master
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

    orders = utils.filter_orders(
        Order.objects.select_related(
            'service',
            'box',
            'customer'
        )
    )

    for order in orders:
        order.start_time = order.start_time.strftime('%d/%m/%Y')

    paginator = Paginator(orders, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
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

    order.start_time = order.start_time.strftime('%d/%m/%Y')

    context = {
        'order': order,
        'final_price': final_price,
        'ruble_word_form': ruble_word_form
    }

    return render(request, template_name, context)


def CreateOrder(request):

    form = forms.CreateOrderForm()

    context = {
        'form': form
    }

    return render(request, 'service/order_create.html', context)
