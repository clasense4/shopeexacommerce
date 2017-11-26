import unittest
import src.settings
import subprocess
from src.acommerce_api import AcommerceApi
import acommerce_create_order_payload


class AcommerceApiTestCase(unittest.TestCase):
    def test_retrieve_token(self):
        src.settings.PROJECT_DIR = '~/shopeexacommerce/test'
        src.settings.PROJECT_TOKEN_FILE = 'token.txt'

        acommerce_api = AcommerceApi()
        auth_token = '9757ad5231d24eea853e987c4e50e85e'

        self.assertEqual(auth_token, acommerce_api.auth_token)

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output('rm -rf ' + src.settings.PROJECT_TOKEN_FILE, shell=True)

    def test_broken_token(self):
        src.settings.PROJECT_DIR = '~/shopeexacommerce/test'
        src.settings.PROJECT_TOKEN_FILE = 'broken_token.txt'

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output('touch ' + src.settings.PROJECT_TOKEN_FILE, shell=True)

        acommerce_api = AcommerceApi()
        # print(acommerce_api.auth_token)

        # Check file is created
        file_output = subprocess.check_output('ls ' + src.settings.PROJECT_TOKEN_FILE, shell=True)
        file_output = file_output.replace('\n','')
        self.assertEqual(
            src.settings.PROJECT_TOKEN_FILE,
            file_output
        )

        # Check content is same
        token_output = subprocess.check_output('cat ' + src.settings.PROJECT_TOKEN_FILE, shell=True)
        token_output = token_output.replace('\n', '')
        self.assertEqual(
            '9757ad5231d24eea853e987c4e50e85e,2018-11-22T17:00:10.641926Z',
            token_output
        )

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output('rm -rf ' + src.settings.PROJECT_TOKEN_FILE, shell=True)

    def test_token_expired(self):
        src.settings.PROJECT_DIR = '~/shopeexacommerce/test'
        src.settings.PROJECT_TOKEN_FILE = 'expired_token.txt'

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output(
            'echo 9757ad5231d24eea853e987c4e50e85e,2016-11-22T17:00:10.641926Z >' + src.settings.PROJECT_TOKEN_FILE,
            shell=True
        )

        acommerce_api = AcommerceApi()
        # print(acommerce_api.auth_token)

        # Check file is created
        file_output = subprocess.check_output('ls ' + src.settings.PROJECT_TOKEN_FILE, shell=True)
        file_output = file_output.replace('\n','')
        self.assertEqual(
            src.settings.PROJECT_TOKEN_FILE,
            file_output
        )

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output('rm -rf ' + src.settings.PROJECT_TOKEN_FILE, shell=True)

    def test_sales_order_create(self):
        acommerce_api = AcommerceApi()

        output = acommerce_api.sales_order_create('123', acommerce_create_order_payload.payload)
        self.maxDiff = None
        self.assertEqual(201, output['code'])

        subprocess.check_output('cd ' + src.settings.PROJECT_DIR, shell=True)
        subprocess.check_output('rm -rf ' + src.settings.PROJECT_TOKEN_FILE, shell=True)


if __name__ == '__main__':
    unittest.main()
