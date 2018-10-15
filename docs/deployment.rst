Django project secret key
=========================

The project's secret ket is named DJANGOCASE_SECRET_KEY and is loaded via an environment variable. You have received it from me by e-mail in a separate file.


Data API authentication
=======================

The data are obtained from http://rachel.maykinmedia.nl/djangocase/city.csv and 'http://rachel.maykinmedia.nl/djangocase/hotel.csv and the password for these is loaded via an environment variable called DJANGOCASE_PASSWORD.


APScheduler
===========

The database is loaded from HTTP every 24 hours. The first time will be 24 hours after deployment.