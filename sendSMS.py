# coding: utf-8
from urllib.request import urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from urllib.parse import urlencode

twilio_number = "+12055397721"
phone_number = "+13026904809"
account_sid = "AC8937212616c209386d1abb1d1ee393e8"
auth_token = "d2ab46e1e2ea2af831e0cbf133deabb7"
message = "Test Joined your Zoom Meeting Room"

# -- twilio API url
url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages".format(account_sid)

# -- payload
data = {
    "From": "{}".format(twilio_number),
    "To": "{}".format(phone_number),
    "Body": "{}".format(message),
}
data_encoded = urlencode(data).encode()

# -- authentication
pass_manager = HTTPPasswordMgrWithDefaultRealm()
pass_manager.add_password(None, url, account_sid, auth_token)
auth_handler = HTTPBasicAuthHandler(pass_manager)
opener = build_opener(auth_handler)
install_opener(opener)

# -- send sms
'''
with urlopen(url, data_encoded) as r:
    response = r.read().decode()
'''
