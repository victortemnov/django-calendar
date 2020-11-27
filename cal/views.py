import calendar
from datetime import date, datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.safestring import mark_safe

from cal.forms import EventForm
from cal.models import Event
from cal.utils import Calendar


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('cal:calendar')
    template_name = 'event_create.html'


class EventRead(ListView):
    model = Event
    template_name = 'event_read.html'


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('cal:calendar')
    template_name = 'event_update.html'


class EventDelete(DeleteView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('cal:calendar')
    template_name = 'event_delete.html'


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'event.html', {'form': form})


class CalendarView(ListView):
    model = Event
    # 111
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
    