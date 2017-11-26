import unittest
import requests
from src.shopee_transformer import ShopeeTransformer


class ShopeeTransformerTestCase(unittest.TestCase):
    order_detail = {
        u'actual_shipping_cost': u'',
        u'cod': True,
        u'country': u'SG',
        u'create_time': 1467887672,
        u'currency': u'SGD',
        u'escrow_amount': u'372.00',
        u'estimated_shipping_fee': u'',
        u'items': [{
            u'item_name': u'several models test',
            u'item_sku': u'100',
            u'variation_discounted_price': u'100.00',
            u'variation_name': u'{% checkout %}',
            u'variation_original_price': u'100.00',
            u'variation_quantity_purchased': 1,
            u'variation_sku': u'10'},
            {u'item_name': u'sellerpromotionwithmodel',
             u'item_sku': u'100',
             u'variation_discounted_price': u'0.10',
             u'variation_name': u'a',
             u'variation_original_price': u'0.10',
             u'variation_quantity_purchased': 1,
             u'variation_sku': u'10'},
            {u'item_name': u'sellerpromotionwithmodel',
             u'item_sku': u'100',
             u'variation_discounted_price': u'0.10',
             u'variation_name': u'b',
             u'variation_original_price': u'0.50',
             u'variation_quantity_purchased': 1,
             u'variation_sku': u'10'},
            {
                u'item_name': u'veryloggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggfffgffffffffffffffffffffffffff',
                u'item_sku': u'100',
                u'variation_discounted_price': u'100.00',
                u'variation_name': u'',
                u'variation_original_price': u'100.00',
                u'variation_quantity_purchased': 1,
                u'variation_sku': u'10'}],
        u'message_to_seller': u'',
        u'order_status': u'ORDER_ESCROW_VERIFIED',
        u'ordersn': u'160707183487980',
        u'payment_method': u'PAY_COD',
        u'recipient_address': {u'city': u'',
                               u'country': u'SG',
                               u'district': u'',
                               u'full_address': u'39 CORONATION ROAD WEST, #13 , SG, 266321',
                               u'name': u'very  long name Long long long long long long long long long lon',
                               u'phone': u'6587773905',
                               u'state': u'',
                               u'town': u'',
                               u'zipcode': u'266321'},
        u'shipping_carrier': u'NINJAVAN',
        u'total_amount': u'372.00',
        u'tracking_no': u'758IEPV0L617T931',
        u'update_time': 1471254360
    }
    # Base result
    result = {
        'currUnit': u'SGD',
        'customerInfo': {
            'address1': '964 Rama 4 Road',
            'addressee': 'Dan Happiness',
            'country': 'Thailand',
            'email': '',
            'phone': '081-000-0000',
            'postalCode': '10500',
            'province': 'Bangkok'
        },
        'grossTotal': 200.2,
        'orderItems': [
            {
                'itemId': u'100',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': 100.0
            },
            {
                'itemId': u'100',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': 0.1
            },
            {
                'itemId': u'100',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': 0.5
            },
            {
                'itemId': u'100',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': 100.0
            },
            {
                'itemId': 'Discount',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': -0.4
            },
            {
                'itemId': 'Shipping Charges',
                'partnerId': 'planetsports',
                'qty': 1,
                'subTotal': 0
            }
        ],
        'orderShipmentInfo': {
            'address1': u'39 CORONATION ROAD WEST, #13 , SG, 266321',
            'address2': '',
            'addressee': u'very  long name Long long long long long long long long long lon',
            'city': u'',
            'country': u'SG',
            'district': u'',
            'phone': u'6587773905',
            'postalCode': u'266321',
            'province': u'',
            'subDistrict': u''
        },
        'paymentType': 'COD',
        'shippingType': 'STANDARD_2_4_DAYS'
    }

    def test_local_result_same_day(self):
        # days_to_ship 0
        order_detail_1 = self.order_detail.copy()
        order_detail_1[u'days_to_ship'] = 0
        order_detail_1[u'actual_shipping_cost'] = ''

        # SAME_DAY
        result_1 = self.result.copy()
        result_1['orderItems'][5]['subTotal'] = 0
        result_1['shippingType'] = 'SAME_DAY'

        self.maxDiff = None
        shopee = ShopeeTransformer()

        shopee.prepare(order_detail_1)
        self.assertEqual(result_1, shopee.process().result)

    def test_local_result_next_day(self):
        # days_to_ship 1
        order_detail_2 = self.order_detail.copy()
        order_detail_2[u'days_to_ship'] = 1
        order_detail_2[u'actual_shipping_cost'] = 0

        # NEXT_DAY
        result_2 = self.result.copy()
        result_2['orderItems'][5]['subTotal'] = 0
        result_2['shippingType'] = 'NEXT_DAY'

        self.maxDiff = None
        shopee = ShopeeTransformer()

        shopee.prepare(order_detail_2)
        self.assertEqual(result_2, shopee.process().result)

    def test_local_result_express(self):
        # days_to_ship 2
        order_detail_3 = self.order_detail.copy()
        order_detail_3[u'days_to_ship'] = 2
        order_detail_3[u'actual_shipping_cost'] = ''

        # EXPRESS_1_2_DAYS
        result_3 = self.result.copy()
        result_3['orderItems'][5]['subTotal'] = 0
        result_3['shippingType'] = 'EXPRESS_1_2_DAYS'

        self.maxDiff = None
        shopee = ShopeeTransformer()

        shopee.prepare(order_detail_3)
        self.assertEqual(result_3, shopee.process().result)

    def test_local_result_standard(self):
        # days_to_ship 4
        order_detail_4 = self.order_detail.copy()
        order_detail_4[u'days_to_ship'] = 4
        order_detail_4[u'actual_shipping_cost'] = 0

        # STANDARD_2_4_DAYS
        result_4 = self.result.copy()
        result_4['orderItems'][5]['subTotal'] = 0
        result_4['shippingType'] = 'STANDARD_2_4_DAYS'

        self.maxDiff = None
        shopee = ShopeeTransformer()

        shopee.prepare(order_detail_4)
        self.assertEqual(result_4, shopee.process().result)

    def test_local_result_nation_wide(self):
        # days_to_ship 5
        order_detail_5 = self.order_detail.copy()
        order_detail_5[u'days_to_ship'] = 5
        order_detail_5[u'actual_shipping_cost'] = 10

        # NATIONWIDE_3_5_DAYS
        result_5 = self.result.copy()
        result_5['grossTotal'] = 210.2
        result_5['orderItems'][5]['subTotal'] = 10
        result_5['shippingType'] = 'NATIONWIDE_3_5_DAYS'

        self.maxDiff = None
        shopee = ShopeeTransformer()

        shopee.prepare(order_detail_5)
        self.assertEqual(result_5, shopee.process().result)

    def test_api_result(self):
        url = 'https://etc-acommerce.mockable.io/shopee/api/v1/orders/detail'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'b37c061daf2fcfa2baffe7539110938be5b7525041c147e78ad8afa78cc1a72d'
        }

        body = {
            'partner_id': '123',
            'shopid': 'planet-sport',
            'timestamp': 123123123
        }
        r = requests.post(url, headers=headers)
        order_detail_api = r.json()['orders'][0]
        shopee = ShopeeTransformer()
        shopee.prepare(order_detail_api)

        self.maxDiff = None
        self.assertEqual(self.result, shopee.process().result)


if __name__ == '__main__':
    unittest.main()
