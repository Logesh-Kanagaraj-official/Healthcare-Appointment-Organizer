from django.db import models

# Create your models here.
class Register(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=100)
    mobno = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=254)
    pwrd = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)   # Admin flag for UI admin dashboard

    def __str__(self):
        return f"{self.uname} ({self.email})"

class Patent(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)                 # Fixed: was max_length=20
    mobno = models.CharField(max_length=15, null=True)       # Fixed: was IntegerField
    email = models.EmailField(max_length=254)                # Fixed: was CharField(max_length=20)
    patdt = models.DateTimeField()
    docname = models.CharField(max_length=100)               # Fixed: was max_length=20
    prpse = models.CharField(max_length=200)                 # Fixed: was max_length=20

    def __str__(self):
        return f"{self.fname} - {self.docname} ({self.patdt})"