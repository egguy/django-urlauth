# Installation of django-urlauth

`pip install django-urlauth-egguy`

##  configuration

* Add `urlauth` to INSTALLED_APPS
* Put `urlauth.middleware.AuthKeyMiddleware' into MIDDLEWARES (between SessionMiddleware and AuthenticationMiddleware)
* Do syncdb or migrate
