from django.db import models

from .tasks import build_graph


class Graph(models.Model):
    function = models.CharField(max_length=128)
    image = models.ImageField(null=True)
    error = models.CharField(max_length=128, null=True)
    interval = models.IntegerField()
    dt = models.IntegerField()
    processed = models.DateTimeField(auto_now=True, null=True)

    def update(self, async=True):
        result = build_graph.apply_async(args=(self.id,))
        if not async:
            result.wait()
