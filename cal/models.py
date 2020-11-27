from django.db import models
from django.urls.base import reverse


class Event(models.Model):
    title = models.CharField(max_length=250)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_update', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
        
    def __str__(self):
        return self.title
        