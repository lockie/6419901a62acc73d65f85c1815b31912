from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db import connection
from django.utils.safestring import mark_safe

from .models import Graph


def update_selected(modeladmin, request, queryset):
    for graph in queryset:
        graph.update()


@admin.register(Graph)
class GraphModelAdmin(admin.ModelAdmin):
    fields = ('function', 'interval', 'dt')
    list_display = ('function', 'image_tag', 'interval', 'dt',
                    'processing_date')
    list_display_links = None
    actions = (update_selected,)

    def image_tag(self, obj):
        if obj.error is not None:
            return obj.error
        if not obj.image:
            return 'Error: Unknown error'
        return mark_safe(
            '<img src="{}" style="width:300px;height:auto" />'.format(
                obj.image.url))
    image_tag.short_description = 'Graph'

    def processing_date(self, obj):
        return obj.processed.strftime('%F %X.%f')
    processing_date.short_description = 'Processing date'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # force sync with Celery workers
        connection.cursor().execute('COMMIT')

        obj.update(async=False)


admin.site.disable_action('delete_selected')
# NOTE: hiding usual users/groups stuff
admin.site.unregister(User)
admin.site.unregister(Group)
