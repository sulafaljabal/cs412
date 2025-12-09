# project/utils.py 
# Sulaf Al Jabal (U78815065) 12/03/2025
# File description: this file helps make views.py less clunky since calendar is created multiple times depending on what you want to do on the application
# helper functions for calendar. plan to fit all helper functions in here unless this file becomes too large, then I might consider created more specific utils files

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
        """Format a single day in the calendar"""
        if day == 0:
            return '<td></td>'
            
        appointments_per_day = appointments.filter(dateTime__day=day)
        
        d = ''
        for appointment in appointments_per_day:
            d += f'<li class="calendar_list"><a href="/project/appointment/{appointment.pk}">{appointment.patient.lastName}, {appointment.patient.firstName} - {appointment.dateTime.strftime("%I:%M %p")}</a></li>'
        
        # Make the day number clickable to go to day schedule view
        day_url = f'/day_schedule/?date={self.year}-{self.month}-{day}'
        day_link = f'<a href="/project{day_url}" class="day-number">{day}</a>'
        
        return f"<td><span class='date'>{day_link}</span><ul>{d}</ul></td>"
    #enddef 

    def formatweek(self, theweek, appointments):
        """Format a week as a table row"""
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, appointments)
        return f'<tr>{week}</tr>'
    #enddef

    def formatmonth(self, withyear=True):
        """Format a month as an HTML table"""
        appointments = Appointment.objects.filter(dateTime__year=self.year, dateTime__month=self.month)
        
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, appointments)}\n'
        cal += '</table>'
        return cal
    #enddef