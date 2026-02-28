from django.db import models
from django.conf import settings


class Pet(models.Model):

    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('adopted', 'Adopted'),
        ('rescued', 'Rescued'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    contact_info = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='pets/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lost')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.breed if self.breed else "Pet"
