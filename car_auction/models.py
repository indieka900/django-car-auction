from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    usertypechoices = (
        ("Seller","Seller"),
        ("Buyer", "Buyer"),
    )
    
    username = None
    email = models.EmailField(_("email address"), unique=True)
    usertype = models.CharField(_('User Type'), max_length=30, choices=usertypechoices, default="Buyer")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class Cars(models.Model):
    make = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    bid_count = models.IntegerField(default=0)
    highest_bid = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads', default='p.png')
    last_bid = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.make 

    # class Meta:
    #     managed = False
    #     db_table = 'cars'
# Create your models here.
