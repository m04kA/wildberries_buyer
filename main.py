import requests
import json
from Buyer_wb import *


# Авторизация
url_user = "POST https://www.wildberries.ru/security/spa/signinsignup"
WILDAUTHNEW_V3 = "6A300CC4DF4F97449B3EE9705642AFC57B4A20FA534627C8D07A0B45D9DD644680E32F9A80F0AA9C5642F21E46DCDC6D34ABFE54286194FBB508848A8E8BA9E0409873C9174C207118D39ED6328D068CA32657D389A1D3E16BC9BD0EFDC2012F0388A82ED49420A574C444D94DC6DD4DB065BAD76A9DFB8A904BE99FC8EB26375D10016ACAC16B5D663CE7B09AAE8B2A5D4F69BBB5664E7FFC488C9F0CF8B725775D75F83D5ABB0683BAA1502D79952E994B99E360D4406F34A95C93C75CEFC7719CEBA4962F4A97070DBB0F28D5EA35A6D1FC2337C068BBD2AEC42EE6D201D902B1E158BA4291934AE28286ED548017F54CF3156F79B8D3E932EFFF387DA5BE1F5E6D16EECF36AD64A690A03476CB942775218C922C65181DD2FA8E095D7A7A8A431AFE"


class Buyer:
    def __init__(self):
        self.headers = {}
        self.cooky = []


def main():
    # req_1 = requests.session().request(method='GET', url=url_obj)
    # data = json.loads(req_1.text)
    # print(data)

    # По товару
    id_obj = 24547604
    my_test = Buyer_waildberries()
    # result = my_test.nm_2_cards(id_obj=id_obj)
    cards = my_test.buy_moment(id_obj)
    print(cards)
    # availability
    # if result:
    #     print(my_test.stock_availability(result))


if __name__ == "__main__":
    main()
