from src.shopee_api import ShopeeApi
from src.shopee_transformer import ShopeeTransformer
from src.acommerce_api import AcommerceApi
import pprint


pp = pprint.PrettyPrinter(indent=2)
# acommerce = AcommerceApi()
# token = acommerce.read_token()
# pp.pprint(token)

shopee_api = ShopeeApi()
ordersn_list = shopee_api.orders_list()
# pp.pprint(ordersn_list)

orders_detail = shopee_api.order_detail(ordersn_list)
# pp.pprint(orders_detail)

for order in orders_detail['orders']:
    order_id = order['ordersn']
    # pp.pprint(order['ordersn'])

    shopee = ShopeeTransformer()
    shopee.prepare(order)
    payload = shopee.process().result
    # pp.pprint(payload)

    acommerce = AcommerceApi()
    token = acommerce.read_token()
    # pp.pprint(token)
    create_order = acommerce.sales_order_create(order_id, payload)
    pp.pprint(create_order)
