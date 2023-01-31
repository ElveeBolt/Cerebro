from .models import Statistics
from django.core.exceptions import ObjectDoesNotExist


def get_statistic(request):
    try:
        statistic = Statistics.objects.latest('date')
    except ObjectDoesNotExist:
        statistic = None

    return {'sidebar_statistic': statistic}
