import os
from pywebio.platform.flask import wsgi_app
from api.web import home_page

app = wsgi_app(home_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080))