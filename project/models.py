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
    address = models.TextField(blank=True)
    picture = models.ImageField(blank=True)

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
    #enddef

    def getPrimaryCareDoctor(self):
        """ Returns name of primary care doctor associated with a Patient record or no if this is blank"""
        if self.primaryCareDoctor == None:
            return "no"
        return self.primaryCareDoctor
    #enddef

#endclass

class Doctor(models.Model):
    """ Definition of Doctor model """
    firstName = models.TextField(blank=True)
    lastName = models.TextField(blank=True)
    specialty = models.TextField(blank=True) # this might need to change later for Doctor search capabilities
    picture = models.ImageField(blank=True)

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
    picture = models.ImageField(blank=True)


    def __str__(self):
        """ Returning string representation of Nurse object. Similar issue to Doctor object"""
        return f"N: {self.lastName}, {self.firstName}"
    #enddef

    def getPicture(self):
        if self.picture == None:
            return 'media\Default_pfp.jpg'.url
        return self.picture.url
#endclass

class Appointment(models.Model):
    """ Definition of Appointment model 
    Attributes:
    patient: primary key of patient
    dateTime: Date and Time of appointment
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
    problem = models.TextField() # main description of problem
    problemDescription = models.TextField()
    appointmentType= models.CharField(
        max_length = 2,
        choices=app_choices
    ) # choices already defined above, new ones can be added as time goes on
    # dont think I need to include DoctorProvider and NurseProvider since the appointmentID will be added to those
    # record

    def __str__(self):
        """Returns a string representation of Appointment record"""
        return f"{self.dateTime} - type: {self.appointmentType}, patient: {self.patient.lastName}"

#endclass

class DoctorProvider(models.Model):
    """ Helper model which allows certain appointments to have multiple providers (Doctor)
    If multiple doctors will be present at an appointment, then multiple records of the DoctorProvider table will share the
    same appointmentID
    Attributes:
    appointmentID: links to Appointment table
    doctorID: PK of doctor if they are working on a certain appointment (can be blank if this is a Nurse only appointment)
    """
    appointmentID = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    doctorID = models.ForeignKey("Doctor", on_delete=models.CASCADE)

    def __str__(self):
        """ Returning string representation of DoctorProvider record"""
        doctor = Doctor.objects.filter(pk=self.doctorID.pk)[0]
        app = Appointment.objects.filter(pk=self.appointmentID.pk)[0]
        return f"Date: {app.dateTime} Doctor: {doctor.firstName} {doctor.lastName}"
#endclass

class NurseProvider(models.Model):
    """ Helper model which allows certain appointments to have multiple providers (Nurse)
    If multiple nurses will be present at an appointment, then multiple records of theNurseProvider table will share the same
    appointmentID
    Attributes:
    appointmentID: links to Appointment table
    nurseID"""
    appointmentID = models.ForeignKey("Appointment", on_delete=models.CASCADE)
    nurseID = models.ForeignKey("Nurse", on_delete=models.CASCADE)
#endclass
