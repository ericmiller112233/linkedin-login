from bs4 import BeautifulSoup
import urllib
import httplib2
import requests
import Cookie
import time

linkedin_login(user, pw) # replace with user@email.com and password for account you want to log into.

# Login, the user login data will come from a database.
def linkedin_login(user, pw):

    global url
    url = "https://www.linkedin.com/uas/login"

    get(url)
    get_login_csrf_param()
    get_csrf_token()
    get_source_alias()

    global payload
    payload = {
        'isJsEnabled': 'yes',
        'source_app': '',
        'tryCount': '',
        'clickedSuggestion': 'false',
        'session_key': user,
        'session_password': pw,
        'signin': 'Sign In',
        'session_redirect': '',
        'trk': '',
        'loginCsrfParam': csrf_param,
        'fromEmail': '',
        'csrfToken': csrf_token,
        'sourceAlias': source_alias
    }

    global url
    url = "https://www.linkedin.com/uas/login-submit"
    post(url)


def post(url):
#    http = httplib2.Http()

    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    raw = urllib.urlencode(payload)

    # This is the HTML from login post, use to get tokens
    global POST
    POST = session.post(url, data=raw, cookies=sessionCookies, headers=headers).text
    print POST
    print "^^^that was post"

def get(url):
    # Uses sessions to contain cookies,
    # see http://docs.python-requests.org/en/latest/user/advanced/#session-objects
    global session
    session = requests.Session()

    session.get(url, verify=False)
    response = session.get(url, verify=False)
    global sessionCookies
    sessionCookies = session.cookies

    print(response.text)
    print "^^^that was the response text"


    global soup
    soup = BeautifulSoup(response.text)
    print (soup.prettify())



def get_login_csrf_param():
    global csrf_param
    csrf_param = soup.find(id="loginCsrfParam-login")['value']
    print "loginCsrfParam"
    print csrf_param

def get_csrf_token():
    global csrf_token
    csrf_token = soup.find(id="csrfToken-login")['value']
    print "csrf token:"
    print csrf_token

    print soup

def get_source_alias():
    print "^^^that was soup"
    global source_alias
    source_alias = soup.find(id="sourceAlias-login")['value']
    print "sourceAlias:"
    print source_alias
