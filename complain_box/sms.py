import requests

greenweburl = "http://api.greenweb.com.bd/api.php"

# your token code here
token = "9822190714169193203437c8bee9677383732aa677f325682221"


# sms receivers number here (separated by comma)
# to = '+88017xxxxxxx,+88016xxxxxxxx'
# to = "+8801622774190"


def send_sms(to, message):
    data = {'token': token,
            'to': to,
            'message': message}
    responses = requests.post(url=greenweburl, data=data)
    return responses
