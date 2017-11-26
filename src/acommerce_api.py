import requests
import json
import settings
import subprocess
import datetime
import dateutil.parser


class AcommerceApi:
    def __init__(self):
        self.base_url = 'https://fulfillmentcpms-acommerce.mockable.io/'
        self.auth_token = self.read_token()

    def read_token(self):
        subprocess.check_output('cd ' + settings.PROJECT_DIR, shell=True)
        try:
            raw_token = subprocess.check_output('cat ' + settings.PROJECT_TOKEN_FILE, shell=True)
        except subprocess.CalledProcessError:
            print ('token file not exist, creating')
            # Call authentication
            self.authentication()
            raw_token = subprocess.check_output('cat ' + settings.PROJECT_TOKEN_FILE, shell=True)

        # Token is in simple csv format but has extra \n
        raw_token = raw_token.replace('\n', '')

        # If raw_token is not correct
        try:
            token = raw_token.split(',')[0]
            expires_at = raw_token.split(',')[1]
        except IndexError:
            print ('TOKEN_FILE is broken')
            self.authentication()
            return self.read_token()

        # Check token expired
        if self.is_token_expired(expires_at):
            print ('Token is expired')
            self.authentication()
            return self.read_token()
        else:
            return token

    def is_token_expired(self, expires_at):
        """Token example format 2018-11-22T17:00:10.641926Z"""
        t1 = dateutil.parser.parse(expires_at)
        epoch_token = int(t1.strftime("%s"))

        t2 = datetime.datetime.now()
        epoch_local = int(t2.strftime("%s"))

        return epoch_token < epoch_local

    def headers(self):
        headers = {
            'X-Subject-Token': self.auth_token,
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': settings.ACOMMERCE_USER_AGENT
        }
        print(headers)
        return headers

    def authentication(self):
        url = self.base_url + 'identity/token'
        payload = {
            'auth': {
                'apiKeyCredentials': {
                    'username': settings.ACOMMERCE_USERNAME,
                    'apiKey': settings.ACOMMERCE_API_KEY
                }
            }
        }
        r = requests.post(url, data=json.dumps(payload))
        token = r.json()['token']

        # Save to simple file
        subprocess.check_output('cd ' + settings.PROJECT_DIR, shell=True)
        subprocess.check_output(
            'echo ' + token['token_id'] + ',' + token['expires_at'] + ' > ' + settings.PROJECT_TOKEN_FILE,
            shell=True
        )
        return token

    def sales_order_create(self, orderId, payload):
        url = self.base_url + 'channel/shopee_test/order/' + orderId
        r = requests.put(url, headers=self.headers(), data=json.dumps(payload))
        return {
            'data': r.json(),
            'code': r.status_code
        }
