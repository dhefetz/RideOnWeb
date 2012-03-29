from django.db import models
#from django.contrib.gis.db import models as gis_models

# Create your models here.
#add password and username
class User(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.name


class Driver(models.Model):
    source = models.CharField(max_length = 100)    
    destination = models.CharField(max_length = 100)
    user = models.ForeignKey("User")
    def __unicode__(self):
        return self.user.name
    
class Rider(models.Model):
    source = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100) 
    user = models.ForeignKey("User")
    def __unicode__(self):
        return self.user.name
    
class RideRequest(models.Model):
    rider = models.ForeignKey("Rider")
    driver = models.ForeignKey("Driver")
    accepted = models.NullBooleanField(default=None, null=True, blank=True)
    entered = models.BooleanField(default=False)
    r_ack = models.BooleanField(default=False)
    d_ack = models.BooleanField(default=False)
    exited = models.BooleanField(default=False)
    def __unicode__(self):
        return u"Rider: %s, Driver: %s" % (self.rider, self.driver)