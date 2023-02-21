from api import api


def ping_elasticsearch(request):
    status = api.ping_elasticsearch()
    return {'ping_elasticsearch': status}


def tasks_elasticsearch(request):
    status = api.check_indexation_tasks()
    return {'tasks_elasticsearch': status}
