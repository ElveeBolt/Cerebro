from .models import Statistics

def get_statistic(request):
     statistic = Statistics.objects.latest('date')
     return {'sidebar_statistic': statistic}
