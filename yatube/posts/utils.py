from django.conf import settings
from django.core.paginator import Paginator


def paginator_func(input_objects, request):
    paginator = Paginator(input_objects, settings.CONST_TEN)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
