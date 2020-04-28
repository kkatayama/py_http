import getpass
from gmail import GMail, Message

try:
    import configparser
except:
    from six.moves import configparser

if __name__ == '__main__':
    print('Gmail login and send email test.'.upper())
    print('need one-time password to connect with Gmail account...')
    print("  1. Enable 2-Step Verification [any method (ex: text message)]: https://myaccount.google.com/u/2/security")
    print("  2. Create an App Password: https://myaccount.google.com/u/2/apppasswords")
    print("     [Select app] = Mail")
    print("     [Select device] = <Other (Custom name)> === [HOSTNAME]")
    print("  3. Click [GENERATE]")
    
    # -- setup parameters
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config['gmail'] = {}
    email = input('Enter Gmail Email Address: ')
    password = getpass.getpass('Enter App Password: ')

    # -- test send email
    mail = GMail(email, password)
    msg = Message('test message', email, text="this is a test from python")
    mail.send(msg)
    print('check your inbox...\n')

    # -- export data to confgi.ini
    config['gmail']['email'] = email
    config['gmail']['password'] = password

    # -- phone sms test
    sms_config_file = 'sms_config.ini'
    sms_config = configparser.ConfigParser()
    sms_config.read(sms_config_file)

    print('Would you like to test SMS message as well?')
    ans = input('(y/n): ')

    if len(ans) > 0 and ans[0].lower() == 'n':
        # -- export data to confgi.ini
        config['gmail']['pmail'] = 'NO'
        pass
    else:
        phone = input('Enter Phone Number (eg: 3026904809): ')
        print('Select Your Phone Provider:')
        print('='*40)
        print('ID # | Phone Provider')
        print('_'*40)
        temp = []
        for index, provider in enumerate(sms_config.sections()):
            temp.append(provider)
            print('{:>3} | {}'.format(index, provider))
        print('-'*40)
        p_id = int(input('Enter ID#: '))
        pmail = sms_config[temp[p_id]]['sms'].replace('[insert 10-digit number]', phone)
        print('loaded: {}'.format(pmail))
        msg = Message('test sms message', pmail, text="this is a test from python")
        mail.send(msg)
        print('check your phone...')
        config['gmail']['pmail'] = pmail

    with open('config.ini', 'w') as f:
        config.write(f)
