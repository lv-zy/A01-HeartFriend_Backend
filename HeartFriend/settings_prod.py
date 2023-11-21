from HeartFriend.settings import *



DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "seproject",
        "USER": "root",
        "PASSWORD": "se2023",
        "HOST": "mysql",
        "PORT": "3306",
    }
}
