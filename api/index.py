from pywebio.platform.flask import wsgi_app
from api.web import home_page

app = wsgi_app(home_page)
