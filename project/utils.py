# project/utils.py
# Sulaf Al Jabal (U78815065) 11/24/25
# file description: Utility functions including Calendar class for generating HTML calendars

from calendar import HTMLCalendar
from .models import Appointment
from django.urls import reverse

class Calendar(HTMLCalendar):
    """Custom calendar that displays appointments"""
    
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, appointments):
        """
        Format a single day in the calendar.
        Returns an HTML table cell with the day number and any appointments.
        """
        appointments_per_day = appointments.filter(
            dateTime__day=day
        )
        
        d = ''
        for appointment in appointments_per_day:
            d += f'<li> {appointment.get_appointmentType_display()}</li>'
        
        if day != 0:
            # Use reverse() to get the proper URL with all prefixes
            day_url = reverse('day_schedule') + f'?date={self.year}-{self.month}-{day}'
            day_link = f'<a href="{day_url}" class="day-number">{day}</a>'
            return f"<td><span class='date'>{day_link}</span><ul> {d} </ul></td>"
        
        return '<td></td>'
    
    def formatweek(self, theweek, appointments):
        """
        Format a week as a table row.
        """
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, appointments)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, withyear=True):
        """
        Format a month as a table.
        """
        appointments = Appointment.objects.filter(
            dateTime__year=self.year,
            dateTime__month=self.month
        )
        
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, appointments)}\n'
        
        cal += '</table>'
        return cal