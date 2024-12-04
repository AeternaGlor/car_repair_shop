from django.shortcuts import render  # type: ignore[import-untyped]


# Create your views here.
def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')
