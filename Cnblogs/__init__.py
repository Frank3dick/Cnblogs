import os.path
import sys

import pymysql
pymysql.install_as_MySQLdb()
from django.conf import settings

Filter_path = os.path.join(settings.BASE_DIR, 'text_app', 'html_filter')
sys.path.insert(0, Filter_path)
