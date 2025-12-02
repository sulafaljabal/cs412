from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Appointment

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    #end constructor

    def formatday(self, day, appointments):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for appointment in appointment_per_day:
            d += f'<li class="calendar_list"> {appointment.get_html_url} </li>'
        if day != 0:
             f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    #enddef 

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'
    #enddef

    def formatmonth(self, withyear=True):
        events = Appointment.objects.filter(start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
    #enddef