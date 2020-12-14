from flask import url_for

URL_PREFIX = '/usr/133'

def vs_url_for(view, **values):
	url = url_for(view, **values)
	url = URL_PREFIX + url
	return url


                      
