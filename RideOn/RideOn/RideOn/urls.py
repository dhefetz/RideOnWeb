from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RideOn.views.home', name='home'),
    url(r'^getDrivers$', 'RideOnApp.views.getDrivers', name='getDrivers'),
    url(r'^addDriver$', 'RideOnApp.views.addDriver', name='addDriver'),
    url(r'^getRiders$', 'RideOnApp.views.getRiders', name='getRiders'),
    url(r'^addRider$', 'RideOnApp.views.addRider', name='addRider'),
    url(r'^getRideRequests$', 'RideOnApp.views.getRideRequests', name='getRideRequests'),
    url(r'^addRideRequest$', 'RideOnApp.views.addRideRequest', name='addRideRequest'),
    url(r'^removeDriver$', 'RideOnApp.views.removeDriver', name='removeDriver'),
    url(r'^removeRider$', 'RideOnApp.views.removeRider', name='removeRider'),
    url(r'^acceptRideRequest$', 'RideOnApp.views.acceptRideRequest', name='acceptRideRequest'),
    url(r'^enterRide$', 'RideOnApp.views.enterRide', name='enterRide'),
    url(r'^exitRide$', 'RideOnApp.views.exitRide', name='exitRide'),
    url(r'^addUser$', 'RideOnApp.views.addUser', name='addUser'),
    url(r'^getUsers$', 'RideOnApp.views.getUsers', name='getUsers'),
    url(r'^removeRideRequest$', 'RideOnApp.views.removeRideRequest', name='removeRideRequest'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
