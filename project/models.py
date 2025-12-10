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


    def __str__(self):
        """ Returning string representation of Patient object """
        pcd = 'No' if self.primaryCareDoctor == None else f"{self.primaryCareDoctor.lastName}, {self.primaryCareDoctor.firstName}"
        return f"P: {self.lastName}; {self.firstName}, {self.middleName} | Age: {self.age} | {self.isAdult} | PCD: {pcd}" #PCD: Primary Care Doctor
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
        return f"D: {self.lastName}, {self.firstName} | {self.specialty}"
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
        ("NA", "Nurse Appointment"), 
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
        return f"P: {self.patient.lastName}, {self.patient.firstName} | {self.patient.age} | {self.dateTime.date()} {self.dateTime.time()} | {self.appointmentType} | {self.problem}"
    #enddef

    def get_nurses(self):
        """ Creating a method to get all nurses associated with this appointment. This helper function is used at least
        twice in the application, once to show the specific details of any individual Appointment record, and another time
        within the Patient Detail View"""

        nurse_list = []
        nurse_provider = list(NurseProvider.objects.filter(appointmentID=self.pk))
        for n in nurse_provider:
            nurse_list.append(Nurse.objects.filter(pk=n.nurseID.pk)[0]) # this might be a queryset
        #endfor

        return nurse_list
    #enddef

    def get_doctors(self, **kwargs):
        """ Creating a method to get all doctors associated with this appointment record."""
        doctor_list = []
        doctor_provider = list(DoctorProvider.objects.filter(appointmentID=self.pk))
        for d in doctor_provider:
            doctor_list.append(Doctor.objects.filter(pk=d.doctorID.pk)[0])
        #endfor
        return doctor_list
    #enddef

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
        return f"D: {doctor.firstName} {doctor.lastName} | {doctor.specialty} | {app.dateTime.date()} {app.dateTime.time()} "
    #enddef

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

    def __str__(self):
        """Returning string representation of NurseProvider object"""
        nurse = Nurse.objects.filter(pk=self.nurseID.pk)[0]
        app = Appointment.objects.filter(pk=self.appointmentID.pk)[0]
        return f"N: {nurse.firstName} {nurse.lastName} | {app.dateTime.date()} {app.dateTime.time()} "
#endclass
