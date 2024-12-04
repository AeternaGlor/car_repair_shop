from django.shortcuts import render  # type: ignore[import-untyped]
from django.http import Http404
from slugify import slugify


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

new_services = {service['name']: service for service in services}
for name, service in new_services.items():
    service['master_slug'] = slugify(service['master'])


# Create your views here.
def index(request):
    template_name = 'service/index.html'
    context = {
        'services': services.__reversed__()
    }
    return render(request, template_name, context)


def service_detail(request, service_name):
    template_name = 'service/service_detail.html'

    if str(service_name) not in new_services.keys():
        raise Http404(f'Нет услуги с таким названием: {service_name}')
    service = new_services[str(service_name)]

    context = {
        'service': service
    }

    return render(request, template_name, context)


def master_detail(request, master_slug):
    template_name = 'service/master_detail.html'
    context = {
        'master_slug': master_slug
    }
    return render(request, template_name, context)


if __name__ == "__main__":
    # new_services = {service['master_slug'] = slugify(service['master']) for name, service in new_services.items()}
    for name, service in new_services.items():
        service['master_slug'] = 'slaggggg'
    print(new_services['Ремонт тормозной системы'])