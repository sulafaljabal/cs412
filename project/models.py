# project/models.py
# Sulaf Al Jabal (U78815065) 11/20/2025
# File Description: where all models of final project will be defined

from django.db import models
import datetime

# Create your models here.

class Patient(models.Model):
    """Definition of Patient model"""
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    middleName = models.TextField(blank=True)
    DOB = models.DateField(auto_now=False)
    primaryCareDoctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, blank=True, null=True)

    @property
    def age(self):
        """Calculates the patient's current age."""
        today = datetime.date.today()
        return today.year - self.DOB.year - (
            (today.month, today.day) < (self.DOB.month, self.DOB.day)
        )
    #enddef

    @property
    def isAdult(self):
        """Returns 'A' for adult or 'C' for child based on Patient age."""
        if self.age >= 18:
            return 'Adult'
        return 'Child'
    #enddef
    # might need some more legal things such as: power of attorney priveldges/whether individual is in right state of mind
    # to make medical decisions for themselves, this might lead to another model being created for people who have this
    # power over certain patients such as children/dependents, elderly, patients in a comotose/vegetative state, etc.
    # Maybe even emancipated children (rare...)

    def __str__(self):
        """ Returning string representation of Patient object """
        pcd = 'No' if self.primaryCareDoctor == None else f"{self.primaryCareDoctor.lastName}, {self.primaryCareDoctor.firstName}"
        return f"{self.lastName}; {self.firstName}, {self.middleName} |\nDOB: {self.DOB} | {self.isAdult} | PC Doc: {pcd}"
#endclass

class Doctor(models.Model):
    """ Definition of Doctor model """
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)

    def __str__(self):
        """ Returning string representation of Doctor object. 
        This will need to change, not sure what attributes are important here. Maybe start with specialty?"""
        return f"D: {self.lastName}, {self.firstName}"
    #enddef
#endclass

class Nurse(models.Model):
    """ Definition of Nurse model """
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)

    def __str__(self):
        """ Returning string representation of Nurse object. Similar issue to Doctor object"""
        return f"N: {self.lastName}, {self.firstName}"
    #enddef
#endclass

class Appointment(models.Model):
    """ Definition of Appointment model 
    Attributes:
    patient: primary key of patient
    dateTime: Date and Time of appointment
    headDoctor: primary key of head Doctor responsible for appointment
    otherDoctors: list of primary keys of other Doctors who will be present for this appointment. This can be blank. Option for multiple other doctors is for operations 
    headNurse: primary key of head Nurse on this appointment. For routine checkups and smaller procedures the head nurse might be the only nurse 
    otherNurses: list of primary keys of other Nurses who will be present at the appointment. Larger procedures, such as operations, might need multiple nurses on hand.
    problem: text field with name of problem
    problemDescription: text field with description of the wider patient ailment
    appointmentType: char field. Defined options of appointment types. This serves mostly as a shorthand description of the appointment type.
    The only field I suspect will cause tangible issues with the application as a whole will be the ('ER', "Emergency Care) option since it might force 
    me to add double-booking for nurses and doctors (more accurately represents what hospital scheduling is like, but might cause me great issues later down the road)"""

    app_choices = [
        ('CU', 'Checkup'),
        ('PO', "Post Operation"),
        ('SP', "Specialist Consultation"),
        ("FU", "Follow-up Visit"),
        ("NA", "Nurse Appointment"), # as it states, wrt this application, head doctor field shall be null
        ("PE", "Pre-operation Visit"),
        ("CO", "Counselling Session"),
        ("TH", "Telehealth/Virtual Visit"),
        ("VA", "Vaccination Appointment"),
        ("A", "Annual Checkup"),
        ("BC", "Birth Control Consultation"),
        ("MC", "Medication Check"), # reserved typically for children taking specific medications
    ]
    # this is set at a certain time for a date in the future, so it can't make use of auto_now
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now=False)
    headDoctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE,
        related_name='head_appointments_doctor') # lets me call doctor.head_appointments.all()
    otherDoctors = models.ManyToManyField(
        Doctor,
        related_name='other_appointments_doctor', # lets me call doctor.other_appointments.all()
        blank=True
    )
    headNurse = models.ForeignKey(
        Nurse, 
        related_name='head_appointments_nurse',
        on_delete=models.CASCADE)
    otherNurses = models.ManyToManyField(
        Nurse,
        blank=True,
        related_name='other_appointments_nurse'
    )
    problem = models.TextField() # main description of problem
    problemDescription = models.TextField()
    appointmentType= models.CharField() # choices already defined above, new ones can be added as time goes on