from django.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.
class Driver(models.Model):
    source = gis_models.GeometryField    
    location = gis_models.GeometryField
    #userid
    #passengers