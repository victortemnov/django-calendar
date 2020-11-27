from django.urls import path

from cal.views import EventCreate, EventDelete, EventRead, EventUpdate, CalendarView


app_name = 'cal'

urlpatterns = [
    path('', CalendarView.as_view(), name='calendar'),
    path('event/create/', EventCreate.as_view(), name='event_create'),
    path('event/', EventRead.as_view(), name='event_read'),
    path('event/<int:pk>/', EventUpdate.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDelete.as_view(), name='event_delete'),
]
