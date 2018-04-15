from http import HTTPStatus
import traceback

from django.core.files import File
from django.utils import timezone
from celery import shared_task
import requests


@shared_task
def build_graph(graph_id):
    from .models import Graph

    try:
        graph = Graph.objects.get(id=graph_id)
        res = requests.post('http://data-generator/generate',
                            json={
                                'function': graph.function,
                                'interval': graph.interval,
                                'dt': graph.dt,
                            })
        if res.status_code != HTTPStatus.OK:
            if res.status_code == HTTPStatus.BAD_REQUEST:
                graph.error = 'Invalid function'
            else:
                graph.error = 'Unknown error while generating series data'
            graph.save()
            return
        series = res.json()

        res = requests.post('http://graph-generator/generate',
                            json=series, stream=True)
        if res.status_code != HTTPStatus.OK:
            graph.error = 'Unknown error while generating graph'
            graph.save()
            return
        graph.image.save('graph.png', File(res.raw))
        graph.processed = timezone.now()
        graph.save()
    except Exception as e:
        try:
            error = traceback.format_exception_only(type(e), e)[0]
            Graph.objects.filter(id=graph_id).update(image=None, error=error)
        except Exception:
            pass
