import time
from gmail import GMail, Message
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
email = config['gmail']['email']
password = config['gmail']['password']
pmail = config['gmail']['pmail']
mail = GMail(email, password)

for i in range(8):
    msg = Message('messgage: {}'.format(i), pmail, text='')
    mail.send(msg)
    time.sleep(3)

