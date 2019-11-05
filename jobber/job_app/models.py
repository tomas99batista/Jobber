from django.contrib.auth.models import User
from django.db import models
from .choices import *

# Create your models here.


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Details
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    b_date = models.DateField()
    curriculum = models.FileField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    website = models.URLField()
    sector = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} Profile'


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Details
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    website = models.URLField()
    company_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user.username} Empresa'


class Emprego(models.Model):
    id = models.AutoField(primary_key=True)  # Id_autogerated
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    location = models.IntegerField(choices=LOCATION,
                                   default=1)  # Pode ser Remote, no Local da empresa ou noutra sede ou sth else
    # Professional Details
    job_sector = models.CharField(choices=JOB_SECTOR, max_length=50)  # IT, Economy
    experience_level = models.IntegerField(choices=EXPERIENCE_LEVEL, default=1)
    file = models.FileField(blank=True)  # Can post a PDF with more details of the job, but it's totally optional

    def __str__(self):
        return str(self.id) + self.title
