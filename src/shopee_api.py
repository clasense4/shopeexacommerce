import requests
import json
import datetime
import hashlib
import hmac
import settings


class ShopeeApi:
    def __init__(self):
        self.base_url = 'https://demo5001235.mockable.io/shopee/'

        t = datetime.datetime.now()
        epoch = int(t.strftime("%s"))

        self.base_payload = {
            'partner_id': settings.SHOPEE_PARTNER_ID,
            'shopid': settings.SHOPEE_SHOP_ID,
            'timestamp': epoch
        }

        self.secret_key = settings.SHOPEE_SECRET_KEY

    def authorization_code(self, body):
        message = bytes(body).encode('utf-8')
        secret = bytes(self.secret_key).encode('utf-8')

        hash = hmac.new(secret, message, hashlib.sha256)
        return hash.hexdigest()

    def headers(self, body):
        return {
            'Content-Type': 'application/json',
            'Authorization': self.authorization_code(body)
        }

    def body(self, payload):
        if payload is None:
            return self.base_payload
        else :
            return payload

    def orders_list(self):
        url = self.base_url + 'api/v1/orders/basics'
        body = self.body(None)
        r = requests.post(url, headers=self.headers(body))
        # print(self.headers(body))
        ordersn_list = []

        for order in r.json()['orders']:
            ordersn_list.append(order['ordersn'])

        return ordersn_list

    def order_detail(self, ordersn_list, payload=None):
        url = self.base_url + 'api/v1/orders/detail'
        self.base_payload['ordersn_list'] = ordersn_list
        body = self.body(payload)
        # print(self.headers(body))
        r = requests.post(url, headers=self.headers(body), data=json.dumps(body))
        return r.json()
