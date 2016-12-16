# run.py
import os
from project import app

# application must run on a random port specified by Heroku
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
