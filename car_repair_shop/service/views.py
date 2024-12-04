from django.shortcuts import render  # type: ignore[import-untyped]
from django.http import Http404


services = [
    {
        'id': 0,
        'name': 'Техническое обслуживание',
        'master': 'Иванов И.А.',
        'date': '16.10.2022',
        'text': '''Замена масла и масляного фильтра.
                   Проверка и замена воздушного, топливного и салонного
                   фильтров. Проверка состояния свечей зажигания и их
                   замена при необходимости. Проверка уровня и состояния всех
                   жидкостей (тормозная жидкость, антифриз, жидкость
                   гидроусилителя руля и т.д.).''',
    },
    {
        'id': 1,
        'name': 'Диагностика',
        'master': 'Степанов В.А.',
        'date': '16.10.2022',
        'text': '''Компьютерная диагностика для выявления неисправностей
                   в электронных системах автомобиля.Проверка состояния
                   двигателя, трансмиссии, подвески и других ключевых систем.
                   ''',
    },
    {
        'id': 2,
        'name': 'Ремонт двигателя',
        'master': 'Василенко В.И.',
        'date': '16.10.2022',
        'text': '''Ремонт и замена компонентов двигателя, таких как поршни,
                   кольца, клапаны и т.д. Ремонт или замена головки блока
                   цилиндров. Ремонт или замена турбокомпрессора.''',
    },
    {
        'id': 3,
        'name': 'Ремонт трансмиссии',
        'master': 'Сурвилов А.О.',
        'date': '16.10.2022',
        'text': '''Ремонт и замена компонентов коробки передач
                   (механической или автоматической). Ремонт сцепления.
                   Ремонт или замена карданного вала и других элементов
                   трансмиссии.''',
    },
    {
        'id': 4,
        'name': 'Ремонт тормозной системы',
        'master': 'Павлов А.А.',
        'date': '16.10.2022',
        'text': '''Замена тормозных колодок и дисков.
                   Проверка и замена тормозных шлангов и трубок.
                   Ремонт и замена главного тормозного цилиндра и
                   других компонентов тормозной системы.''',
    },
]

new_services = {service['id']: service for service in services}


# Create your views here.
def index(request):
    template_name = 'service/index.html'
    context = {
        'posts': posts.__reversed__()
    }
    return render(request, template_name, context)


def service_detail(request, post_id):
    template_name = 'service/service_detail.html'

    if str(post_id) not in new_posts.keys():
        # raise ValueError(f'Нет поста с таким иднтифакатором: {post_id}')
        raise Http404(f'Нет поста с таким идeнтифакатором: {post_id}')
    post = new_posts[str(post_id)]

    context = {
        'post': post
    }

    return render(request, template_name, context)


def master_detail(request, category_slug):
    template_name = 'service/master_detail.html'
    context = {
        'category_slug': category_slug
    }
    return render(request, template_name, context)
