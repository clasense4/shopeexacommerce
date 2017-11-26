import unittest
from src.shopee_api import ShopeeApi
import shopee_order_detail_output
import src.settings

class ShopeeApiTestCase(unittest.TestCase):
    def test_orders_list(self):
        shopee_api = ShopeeApi()
        ordersn_list = shopee_api.orders_list()
        # print (ordersn_list)
        self.assertEqual([u'160810114909313', u'160810115809314'], ordersn_list)

    def test_order_detail(self):
        shopee_api = ShopeeApi()
        ordersn_list = [u'160810114909313', u'160810115809314']
        # print (ordersn_list)

        orders_detail = shopee_api.order_detail(ordersn_list)
        self.assertEqual(shopee_order_detail_output.output, orders_detail)

    def test_order_detail_with_extra_payload(self):
        payload = {
            'partner_id': src.settings.SHOPEE_PARTNER_ID,
            'shopid': src.settings.SHOPEE_SHOP_ID,
            'timestamp': 1511686055
        }
        shopee_api = ShopeeApi()
        ordersn_list = [u'160810114909313', u'160810115809314']
        # print (ordersn_list)

        orders_detail = shopee_api.order_detail(ordersn_list, payload)
        self.assertEqual(shopee_order_detail_output.output, orders_detail)


if __name__ == '__main__':
    unittest.main()
