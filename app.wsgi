activate_this = '/var/www/yesql_app/venv/bin/activate_this.py'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))
  
import sys
sys.path.insert(0, '/var/www/yesql_app')
from app import app as application
