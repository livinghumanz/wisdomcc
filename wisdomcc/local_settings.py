# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '234567890-dfghjklbnmajaaaaaaaaaddajdj4555555555555555567890-jh#$%^&*()#$%^&*()'

# Security warning: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wisdomcc_db',
        'USER': 'wisdomcc',
        'PASSWORD': 'coldfeet1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
   