import pytest
from Buyer_wb import *

my_class = Buyer_waildberries()


class TestCase():
    def test_create_dict_open_card(self):
        bank_cards = [
            {
                'isBlocked': False,
                'isSberPay': False,
                'id': 'f598cbdd-a2a6-11ec-a146-964d458f538c',
                'name': '427638******8131',
                'createNew': False,
                'system': 'visa',
                'expireDt': '06/24'
            },
            {
                'isBlocked': False,
                'isSberPay': False,
                'default': True,
                'id': '8fd3acaa-a51f-11ec-87a9-86dab503933b',
                'name': '479004******5522', 'createNew': False,
                'system': 'visa', 'expireDt': '11/25'
            },
            {'isBlocked': False,
             'isSberPay': False,
             'id': '_newcardid',
             'name': 'Привязать новую карту',
             'createNew': True, 'system': ''
             },
            {
                'isSberPay': False,
                'id': '_newcardid',
                'name': 'WB Pay',
                'createNew': True,
                'system': 'wbcard'
            }]
        srver_answer = my_class.create_dict_open_card(bank_cards)
        good_answer = {'427638******8131': {'id': 'f598cbdd-a2a6-11ec-a146-964d458f538c',
                                            'select': False,
                                            'system': 'visa'},
                       '479004******5522': {'id': '8fd3acaa-a51f-11ec-87a9-86dab503933b',
                                            'select': False,
                                            'system': 'visa'}}
        assert srver_answer == good_answer
