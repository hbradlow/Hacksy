#!/usr/bin/env python
import os
import sys
from django.conf import settings

from hacksy.apps import *


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hacksy.settings")
    sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, "apps"))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
