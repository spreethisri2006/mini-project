
from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.patient_id} - {self.patient_name}"


class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    doctor_name = models.CharField(max_length=100)
    disease = models.CharField(max_length=200)
    prescription_date = models.DateField()
    medicines = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"
