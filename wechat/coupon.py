#coding: utf8
import requests

from wechat.consts import COUPON_SEND_URL
from wechat.util import sign_str, check_send_success

COUPON_FIELDS = [
    'appid',
    'coupon_stock_id',
    'mch_id',
    'nonce_str',
    'openid',
    'openid_count',
    'partner_trade_no'
]

COUPON_FIELDS.sort()

COUPON_FIELDS_WITH_SIGN = COUPON_FIELDS[:]
COUPON_FIELDS_WITH_SIGN.append('sign')


COUPON_XML_TEMPLATE = u'''
<xml>
<appid>{appid}</appid>
<coupon_stock_id>{coupon_stock_id}</coupon_stock_id>
<mch_id>{mch_id}</mch_id>
<nonce_str>{nonce_str}</nonce_str>
<openid>{openid}</openid>
<openid_count>{openid_count}</openid_count>
<partner_trade_no>{partner_trade_no}</partner_trade_no>
<sign>{sign}</sign>
</xml>
'''


class CouponEntity(object):
    coupon_stock_id = None  #require str ex: 1757
    openid_count = 1        #require int ex: 1
    partner_trade_no = None #require str ex: 1000009820141203515766
    openid = None           #require str ex: onqOjjrXT-776SpHnfexGm1_P7iE
    appid = None            #require str(32) ex: wx5edab3bdfba3dc1c
    mch_id = None           #require str(32) ex:10000098
    op_user_id = None       #no_require str(32) ex: 10000098
    device_info = None      #no_require str(32)
    nonce_str = None        #require str(<32) ex: 1417574675
    sign = None             #require str(32)  ex: 841B3002FE2220C87A2D08ABD8A8F791
    version = None          #no_require str(32)
    type = None             #no_require str(32) ex: xml

    def to_xml(self, key):
        self.sign = sign_str(self, COUPON_FIELDS, key)
        data = {k: getattr(self, k) for k in COUPON_FIELDS_WITH_SIGN}
        res = COUPON_XML_TEMPLATE.format(**data)
        return res


class WechatCoupon(object):
    def __init__(self, key, cert, url=None):
        self.key = key
        self.cert = cert
        if url is None:
            url = COUPON_SEND_URL
        self.url = url

    def send(self, entity):
        data = entity.to_xml(self.key)
        res = requests.post(self.url, data=data.encode('utf8'), cert=self.cert, verify=False)
        check_send_success(res.content)
        return res


if __name__ == '__main__':
    from datetime import datetime

    class Billno(object):
        def __init__(self, mch_id):
            self.mch_id = mch_id
            self.next_num = 0

        def next(self):
            now = datetime.now()
            date_str = now.strftime('%Y%m%d')
            no = '%s%s%.10d' % (self.mch_id, date_str, self.next_num)
            self.next_num += 1
            return no


#------------- doc -----------------

'''
发送代金券
doc url: https://pay.weixin.qq.com/wiki/doc/api/tools/sp_coupon.php?chapter=12_3
'''

___SEND_SAMPLE = '''
<xml>
<appid> wx5edab3bdfba3dc1c</appid>
<coupon_stock_id>1757</coupon_stock_id>
<mch_id>10010405</mch_id>
<nonce_str>1417574675</nonce_str>
<openid>onqOjjrXT-776SpHnfexGm1_P7iE</openid>
<openid_count>1</openid_count>
<partner_trade_no>1000009820141203515766</partner_trade_no>
<sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
</xml>
'''

__RECEIVE_SAMPLE = '''
<xml>
<return_code>SUCCESS</return_code>
<appid>wx5edab3bdfba3dc1c</appid>
<mch_id>10000098</mch_id>
<nonce_str>1417579335</nonce_str>
<sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
<result_code>SUCCESS</result_code>
<coupon_stock_id>1717</coupon_stock_id>
<resp_count>1</resp_count>
<success_count>1</success_count>
<failed_count>0</failed_count>
<openid>onqOjjrXT-776SpHnfexGm1_P7iE</openid>
<ret_code>SUCCESS</ret_code>
<coupon_id>6954</coupon_id>
</xml>
'''

__RECEIVE_ERR_SAMPLE = '''
<xml>
  <return_code>SUCCESS</return_code>
  <appid>wx5edab3bdfba3dc1c</appid>
  <mch_id>10000098</mch_id>
  <nonce_str>1417579335</nonce_str>
  <sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
  <result_code>FAIL</result_code>
  <err_code>268456007</err_code>
  <err_code_des>你已领取过该代金券</err_code_des>
  <coupon_stock_id>1717</coupon_stock_id>
  <resp_count>1</resp_count>
  <success_count>0</success_count>
  <failed_count>1</failed_count>
  <openid>onqOjjrXT-776SpHnfexGm1_P7iE</openid>
  <ret_code>FAIL</ret_code>
  <ret_msg>你已领取过该代金券<ret_msg/>
  <coupon_id></coupon_id>
</xml>
'''

