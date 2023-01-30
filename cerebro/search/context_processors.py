from api import api


def ping_elasticsearch(request):
    status = api.ping_elasticsearch()
    return {'ping_elasticsearch': status}
