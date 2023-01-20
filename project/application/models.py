from django.db import models

# Create your models here.
class friend(models.Model):
    Name=models.CharField(max_length=20)
    Address=models.CharField(max_length=200)
    Username=models.CharField(max_length=20)
    Password=models.CharField(max_length=20)
    Status = models.BooleanField(default=False)

class Table(models.Model):
    Date = models.DateField(auto_now_add=True)
    User=models.CharField(max_length=50)
    Category = models.CharField(max_length=50)
    Description = models.CharField(max_length=50,null=True)
    Debit=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    Credit = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    Balance=models.DecimalField(max_digits=10, decimal_places=2,null=True)

class Category(models.Model):
    User = models.CharField(max_length=50)
    Category = models.CharField(max_length=50)

