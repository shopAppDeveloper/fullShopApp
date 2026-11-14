"""
Django settings for our shoe/clothing store.

This file controls:
    - Django itself
    - Django Oscar
    - our REST API
    - database connection
    - authentication
    - static files
    - uploaded product images
    - security settings

Important:
We keep configuration here rather than putting business logic
inside this file.
"""

from .env import *  # noqa: F401,F403
from .security import *  # noqa: F401,F403
from .apps import *  # noqa: F401,F403
from .database import *  # noqa: F401,F403
from .general import *  # noqa: F401,F403
from .oscar import *  # noqa: F401,F403
from .api import *  # noqa: F401,F403
from .sms import *  # noqa: F401,F403
from .notifications import *  # noqa: F401,F403
