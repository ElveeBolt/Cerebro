from elasticsearch import Elasticsearch
from elasticsearch import exceptions
from django.conf import settings

client = Elasticsearch(settings.ELASTIC_SERVER,
                       ssl_assert_fingerprint=settings.ELASTIC_CERT_FINGERPRINT,
                       basic_auth=(settings.ELASTIC_USER['username'], settings.ELASTIC_USER['password']))


def ping_elasticsearch() -> bool:
    """
    Ping elasticsearch server

    :return: bool of ping
    """
    return client.ping(request_timeout=0.5)


def get_elasticsearch_tasks() -> dict or None:
    """
    Get all active tasks from elasticsearch server.

    :return: dict or None of tasks
    """
    try:
        tasks = client.cat.tasks(format='json', detailed=True)
    except exceptions.ConnectionTimeout:
        return

    return tasks


def check_indexation_tasks() -> bool:
    """
    Get all active tasks from elasticsearch server and check
    indexation task.

    :return: bool of indexation task
    """
    try:
        tasks = client.cat.tasks(format='json', detailed=True)
    except exceptions.ConnectionTimeout:
        return False

    for task in tasks:
        if 'indices:data/write/bulk' == task['action']:
            return True

    return False


def get_total_documents() -> int:
    """
    Get documents count of indexes

    :return: str of count
    """
    count = client.count(index="*")
    return count['count']


def get_total_indices() -> int:
    """
    Get count of elasticsearch indexes

    :return: int of count
    """
    indexes = client.cat.indices(format='json')
    return len(indexes)


def get_index_info(index: str) -> dict or None:
    """
    Get information about elasticsearch index

    :return: dict of index or None
    """
    try:
        indexes = client.cat.indices(index=index, format='json', h=['index', 'docs.count', 'store.size'])
    except exceptions.NotFoundError:
        return

    data = []
    for index in indexes:
        data.append({
            'index': index['index'],
            'documents': index['docs.count'],
            'size': index['store.size']
        })

    return data[0]


def get_indexes_info() -> list:
    """
    Get information about all elasticsearch indexes

    :return: list of indexes
    """
    indexes = client.cat.indices(format='json')

    data = []
    for index in indexes:
        data.append({
            'index': index['index'],
            'health': index['health'],
            'documents': index['docs.count'],
            'size': index['store.size'],
            'status': index['status']
        })

    return sorted(data, key=lambda item: item['index'])


def get_index_mapping(index: str) -> list or None:
    """
    Get information about mapping of elasticsearch index

    :return: dict of mapping
    """
    try:
        mapping = client.indices.get_mapping(index=index)
    except exceptions.NotFoundError:
        return

    return mapping


def get_indexes_size() -> float:
    """
    Get information about size of elasticsearch indexes

    :return: float of size
    """
    indexes = client.indices.stats()

    size = indexes['_all']['total']['store']['size_in_bytes']
    size = size / 1024 ** 3

    return round(size, 2)


def get_documents(query: str) -> dict:
    """
    Get documents by query

    :param query: str of query
    :return: dict of results
    """
    body = {
        "size": 150,
        "query": {
            "query_string": {
                "query": query,
            }
        },
        "highlight": {
            "fields": {
                "*": {}
            },
            "require_field_match": False
        }
    }
    documents = client.search(index="*", body=body, request_timeout=500)

    return parse_search(documents)


def get_document_by_id(index: str, id_: str) -> dict:
    body = {
        "query": {
            "match": {
                "_id": id_
            }
        },
        "highlight": {
            "fields": {
                "*": {}
            },
            "require_field_match": False
        }
    }
    document = client.search(index=index, body=body)

    return parse_search(document)


def parse_search(documents: dict) -> dict | None:
    """

    :param documents:
    :return:
    """
    total = documents['hits']['total']['value']

    if total == 0:
        return

    items = []
    for document in documents['hits']['hits']:
        highlights = document.get('highlight')

        if highlights is not None:
            highlights_unique = []
            for v in highlights.values():
                for k in v:
                    if k not in highlights_unique:
                        highlights_unique.append(k)

            highlights = ', '.join(highlights_unique)

        items.append({
            'index': document['_index'],
            'id': document['_id'],
            'score': document['_score'],
            'source': document['_source'],
            'highlight': highlights
        })

    data = {
        'total': total,
        'data': items
    }

    return data
