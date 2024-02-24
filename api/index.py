from flask import Flask
from pywebio.platform.flask import webio_view
from web import home_page

app = Flask(__name__)
app.add_url_rule('/', 'webio_view_1', webio_view(home_page), methods=['GET', 'POST', 'OPTIONS'])
