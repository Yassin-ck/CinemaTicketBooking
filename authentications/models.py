from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.gis.db import models 

class MyUserManager(BaseUserManager):
    def create_user(self,phone=None,email=None,username=None,password=None ,**kwargs):

        user = self.model(
            phone=phone,
            email=self.normalize_email(email),
            username=username,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone=None,username=None,password=None,**kwargs):
        user = self.create_user(
            phone=phone,
            username=username            
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(
        max_length=20,
        null=True
    )
    email = models.EmailField(max_length=255,unique=True,null=True,blank=True)
    date_joined = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255,null=True,
        blank=True
    )
    

    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        if self.username is not None:
            return self.username
        elif self.email is not None:
            return self.email
        else:
            return str(self.phone)
            

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



class Location(models.Model):
    coordinates = models.PointField(srid=4326)
    country = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    

    @property
    def longitude(self):
        return self.coordinates.x
    
    @property
    def latitude(self):
        return self.coordinates.y
    
    
class RequestLocation(models.Model):
    STATUS = [
        ('PENDING','PENDING'),
        ('ACCEPTED','ACCEPTED'),
        ('REJECTED','REJECTED')
    ]
    
    current_location = models.PointField(srid=4326,null=True,blank=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    country = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    place = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(default='PENDING',choices=STATUS,max_length=10)
    
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True,related_name='userprofile')
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    address = models.TextField(null=True)
    location = models.PointField(srid=4326,null=True)
    
    
   