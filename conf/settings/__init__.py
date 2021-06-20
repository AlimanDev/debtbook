import os

DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'LOCAL')

if DEVELOPMENT_MODE == 'PRODUCTION':
    from .production import *
else:
    from .locale import *
