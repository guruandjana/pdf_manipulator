import sys
sys.path.insert(0, '/var/www/mainapp/mainapp')



activate_this = '/home/server/.local/share/virtualenvs/mainapp-c6pGQO_3/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from mainapp import app as application

