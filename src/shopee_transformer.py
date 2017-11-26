class ShopeeTransformer:
    def __init__(self):
        self.result = {}
        self.partner_id = 'planetsports'
        self.gross_total = 0

    def prepare(self, order_detail):
        self.order_detail = order_detail

    def payment_type(self, payment_method):
        method = {
            'PAY_COD': 'COD',
            'PAY_BANK_TRANSFER': 'NON_COD',
            'PAY_SHOPEE_WALLET': 'NON_COD'
        }

        return method[payment_method]

    def shipping_type(self, days_to_ship):
        if days_to_ship == 0:
            return 'SAME_DAY'
        elif days_to_ship == 1:
            return 'NEXT_DAY'
        elif 1 <= days_to_ship <= 2:
            return 'EXPRESS_1_2_DAYS'
        elif 2 <= days_to_ship <= 4:
            return 'STANDARD_2_4_DAYS'
        elif days_to_ship > 4:
            return 'NATIONWIDE_3_5_DAYS'

    def create_order_items(self, items):
        result = []
        for item in items:
            new_item = {
                'partnerId': self.partner_id,
                'itemId': item['item_sku'],
                'qty': item['variation_quantity_purchased'],
                'subTotal': self.calculate_subtotal(
                    item['variation_quantity_purchased'],
                    item['variation_original_price']
                )
            }

            result.append(new_item)

        return result

    def create_order_shipment_info(self, recipient_adress):
        result = {
            'addressee': recipient_adress['name'],
            'address1': recipient_adress['full_address'],
            'address2': '',
            'subDistrict': recipient_adress['district'],
            'district': recipient_adress['district'],
            'city': recipient_adress['city'],
            'province': recipient_adress['state'],
            'postalCode': recipient_adress['zipcode'],
            'country': recipient_adress['country'],
            'phone': recipient_adress['phone']
        }

        return result

    def parse_price(self, variation_original_price):
        return float(variation_original_price)

    def calculate_subtotal(self, qty, variation_original_price):
        subtotal = qty * self.parse_price(variation_original_price)

        # Add to gross total
        self.gross_total = self.gross_total + subtotal
        return subtotal

    def calculate_discount(self, items):
        total_discount = 0

        for item in items:
            discount_price = float(item['variation_discounted_price'])
            original_price = float(item['variation_original_price'])
            if discount_price != original_price:
                discount = original_price - discount_price
                total_discount = total_discount + discount

        # Add total_discount to gross_total
        self.gross_total = self.gross_total - total_discount

        return -total_discount

    def process(self):
        self.result['customerInfo'] = {
            'addressee': 'Dan Happiness',
            'address1': '964 Rama 4 Road',
            'province': 'Bangkok',
            'postalCode': '10500',
            'country': 'Thailand',
            'phone': '081-000-0000',
            'email': ''
        }
        self.result['orderShipmentInfo'] = self.create_order_shipment_info(
            self.order_detail['recipient_address']
        )
        self.result['currUnit'] = self.order_detail['currency']
        self.result['shippingType'] = self.shipping_type(self.order_detail['days_to_ship'])
        self.result['paymentType'] = self.payment_type(self.order_detail[u'payment_method'])
        self.result['orderItems'] = self.create_order_items(self.order_detail['items'])

        # Add discount
        discount = {
            'partnerId': self.partner_id,
            'itemId': 'Discount',
            'qty': 1,
            'subTotal': self.calculate_discount(self.order_detail['items'])
        }
        self.result['orderItems'].append(discount)

        # Add Shipping Charges
        if self.order_detail['actual_shipping_cost']:
            shipping_cost = float(self.order_detail['actual_shipping_cost'])
        else:
            shipping_cost = 0
        shipping_charges = {
            'partnerId': self.partner_id,
            'itemId': 'Shipping Charges',
            'qty': 1,
            'subTotal': shipping_cost
        }
        self.result['orderItems'].append(shipping_charges)
        self.gross_total = self.gross_total + shipping_cost

        self.result['grossTotal'] = float(self.gross_total)
        self.gross_total = 0

        return self