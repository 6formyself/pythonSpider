# import json
# b = b'code":1,"data":{"goods_id":"200804003481283581899383414786",' \
#     b'"goods_name":"\xe5\xbe\x97\xe9\xb2\x9c\xe6\xb8\xa9\xe5\x92\x8c\xe8\xa1\xa5\xe6\xb0\xb4\xe9\x9d\xa2\xe8\xb4\xb4' \
#     b'\xe8\x86\x9c\xe3\x80\x90\xe9\x99\x90\xe7\x94\xa8\xe6\x97\xa5\xe6\x9c\x9f2021\xe5\xb9\xb407\xe6\x9c\x8830\xe6' \
#     b'\x97\xa5\\/\xe4\xbf\x9d\xe8\xb4\xa8\xe6\x9c\x9f1095\xe5\xa4\xa9\xe3\x80\x91","start_time":"2020-08-04 ' \
#     b'18:00:00","end_time":"2020-09-03 03:00:00","brand":"\xe5\xbe\x97\xe9\xb2\x9cthe SAEM",' \
#     b'"description":"87001\xe3\x80\x81 \xe5\xbe\x97\xe9\xb2\x9cthe ' \
#     b'SAEM\xe9\x9d\xa2\xe8\x86\x9c-\xc2\xa529.90\\n\xe5\xb0\xba\xe7\xa0\x81 ' \
#     b'21ml*10\xe7\x89\x87\xef\xbc\x88\xe8\x9c\x82\xe8\x9c\x9c\xef\xbc\x89 \\n\xe6\xac\xbe\xe5\xbc\x8f ' \
#     b'\xe5\xbe\x97\xe9\xb2\x9c\xe6\xb8\xa9\xe5\x92\x8c\xe8\xa1\xa5\xe6\xb0\xb4\xe9\x9d\xa2\xe8\xb4\xb4\xe8\x86\x9c' \
#     b'\xe3\x80\x90\xe9\x99\x90\xe7\x94\xa8\xe6\x97\xa5\xe6\x9c\x9f2021\xe5\xb9\xb407\xe6\x9c\x8830\xe6\x97\xa5\\/\xe4' \
#     b'\xbf\x9d\xe8\xb4\xa8\xe6\x9c\x9f1095\xe5\xa4\xa9\xe3\x80\x91\\n\xe6\xac\xbe\xe5\x8f\xb7 ZH2007140019813",' \
#     b'"picture":["https:\\/\\/akmer.aikucun.com\\/goods-web' \
#     b'\\/536fb9fabb4da4dc9545d7a00baf1941bf2ce309_1594707831907_32.jpg",' \
#     b'"https:\\/\\/akmer.aikucun.com\\/goods-web\\/03474238df2a94c1f3a372f79585bef6880378a8_1594707832331_74.jpg",' \
#     b'"https:\\/\\/akmer.aikucun.com\\/goods-web\\/ebc6decbd602a67ba43d3ec750338c7e1e0c2d08_1594707832909_66.jpg",' \
#     b'"https:\\/\\/akmer.aikucun.com\\/goods-web\\/d59308150b1c43fe3756789ea01d12a738d8c040_1594707833422_24.jpg"],' \
#     b'"tag_price":"99.00","price":"29.90","settlement_price":"22.90","profit":"7.00",' \
#     b'"brand_size_url":"https:\\/\\/akmer.aikucun.com\\/goods-web' \
#     b'\\/d59308150b1c43fe3756789ea01d12a738d8c040_1594707833422_24.jpg","weight":"null","volume":"null",' \
#     b'"video_url":"","sku_attribute_list":[{"attributeName":"\xe9\xa2\x9c\xe8\x89\xb2",' \
#     b'"attributeValue":"\xe6\x97\xa0"},{"attributeName":"\xe5\xb0\xba\xe7\xa0\x81",' \
#     b'"attributeValue":"21ml*10\xe7\x89\x87\xef\xbc\x88\xe8\x9c\x82\xe8\x9c\x9c\xef\xbc\x89"}],"sku_list":[{' \
#     b'"skuId":"1283581901220519938","attributeList":[{"attributeName":"\xe9\xa2\x9c\xe8\x89\xb2",' \
#     b'"attributeValue":"\xe6\x97\xa0"},{"attributeName":"\xe5\xb0\xba\xe7\xa0\x81",' \
#     b'"attributeValue":"21ml*10\xe7\x89\x87\xef\xbc\x88\xe8\x9c\x82\xe8\x9c\x9c\xef\xbc\x89"}]}],"goods_materia":[],' \
#     b'"support_exchange":1,"deliver_time":"","statement_by_day":0,' \
#     b'"activity_name":"\xe3\x80\x90\xe5\xb8\xb8\xe9\x94\x80\xe9\xa2\x91\xe9\x81\x93\xe3\x80\x91\xe5\xbe\x97\xe9\xb2' \
#     b'\x9cthe SAEM\xe7\xbe\x8e\xe5\xa6\x860804\xe8\x87\xaa\xe9\x87\x87","is_add_to_goods":0},"msg":"" '
#
# # print(b.decode('utf-8')[-10:])
# x = json.loads(b.decode('utf-8').replace('\\/', '/')[15:-10])
# print(x['goods_name'])
# print(x['goods_name'])

print([1, 2, 3, 4][::-1])
