#!flask/bin/python
from app import app

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = False
  #app.run(debug = False)
  app.run(host = '0.0.0.0', port = 5000)


