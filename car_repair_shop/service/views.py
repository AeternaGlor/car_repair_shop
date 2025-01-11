from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Customer, Order, Box, TimeSlot, Master, Service
from . import utils
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms

User = get_user_model()


def index(request):
    template_name = 'service/index.html'

    services = Service.objects.select_related(
        'master'
    ).filter(
        is_shown=True,
        master__is_shown=True
    )

    paginator = Paginator(services, 5)
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


@login_required
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
        order.time_slot.start_time = order.time_slot.start_time.strftime(
            '%d/%m/%Y %H:%M')

    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, template_name, context)


@login_required
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

    final_price = utils.calculate_price(order)

    ruble_word_form = utils.PluralRubleForm(final_price)

    order.time_slot.start_time = order.time_slot.start_time.strftime(
        '%d/%m/%Y %H:%M')

    context = {
        'order': order,
        'final_price': final_price,
        'ruble_word_form': ruble_word_form
    }

    return render(request, template_name, context)


@login_required
def order_create(request, service_slug):

    template_name = 'service/order_create.html'

    service = get_object_or_404(Service, slug=service_slug)

    if request.method == 'POST':
        form = forms.CreateOrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.service = service
            order.save()

            order.service.master.slots.add(order.time_slot)
            order.box.slots.add(order.time_slot)

            order.cusotomer.discount = order.cusotomer.discount + 1

            return redirect('service:order_success', order_id=order.id)

    form = forms.CreateOrderForm(initial={'service': service})
    return render(request, template_name, {'form': form})


@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':

        order.service.master.slots.remove(order.time_slot)
        order.box.slots.remove(order.time_slot)

        order.delete()

        return redirect('service:order_list')

    return render(
        request,
        'service/order_delete.html',
        {'order': order}
    )


@login_required
def order_success(request, order_id):

    template_name = 'service/order_success.html'

    order = get_object_or_404(Order, id=order_id)

    final_price = utils.calculate_price(order)

    ruble_word_form = utils.PluralRubleForm(final_price)

    context = {
        'order': order,
        'final_price': final_price,
        'ruble_word_form': ruble_word_form
    }

    return render(request, template_name, context)


@login_required
def get_time_slots(request):
    box_id = request.GET.get('box_id')
    service_id = request.GET.get('service_id')

    print(service_id)
    service = get_object_or_404(Service, pk=service_id)
    print(service)
    master_id = service.master.id

    time_slots = TimeSlot.objects.exclude(
        boxes__id=box_id
    ).exclude(
        masters__id=master_id
    )

    time_slots_list = list(time_slots.values('id', 'start_time'))

    for time_slot in time_slots_list:
        time_slot['start_time'] = time_slot['start_time'].strftime('%d-%m-%Y %H:%M')

    return JsonResponse({'time_slots': time_slots_list})


def profile(request, username):

    template_name = 'service/profile.html'

    profile = get_object_or_404(User, username=username)

    context = {
        'profile': profile,
        # 'page_obj': page_obj
    }

    return render(request, template_name, context)


class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_superuser'
    )
    template_name = 'service/user.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_success_url(self):
        return reverse(
            'service:profile',
            kwargs={'username': self.object.username}
        )
    # def get_absolute_url(self):
    #     context = self.get_context_data()
    #     user = context['user']
    #     return reverse(
    #         'service:profile',
    #         kwargs={'username': user.username}
    #     )
    # success_url = reverse_lazy('service:index')
