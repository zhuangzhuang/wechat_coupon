#coding: utf8
import requests

from wechat.consts import COUPON_SEND_URL
from wechat.entity import Entity
from wechat.fields import IntField, StrField


class CouponEntity(Entity):
    coupon_stock_id  = StrField(example=1757)
    openid_count     = IntField(example=1)
    partner_trade_no = StrField(example='1000009820141203515766')
    openid           = StrField(example='onqOjjrXT-776SpHnfexGm1_P7iE')
    appid            = StrField(slen=32, example='wx5edab3bdfba3dc1c')
    mch_id           = StrField(slen=32, example='10000098')
    op_user_id       = StrField(slen=32, required=False, example='10000098')
    device_info      = StrField(slen=32, required=False)
    nonce_str        = StrField(slen=32, example='1417574675')
    sign             = StrField(slen=32, example='841B3002FE2220C87A2D08ABD8A8F791')
    version          = StrField(slen=32, required=False)
    type             = StrField(slen=32, required=False, example='xml')


class CouponResponseEntity(Entity):
    IS_RESPONSE = True

    return_code  = StrField(example='SUCCESS')
    return_msg   = StrField(required=False, example='')
    appid        = StrField(slen=32, example='wx5edab3bdfba3dc1c')
    mch_id       = StrField(slen=32, example='10000098')
    device_info  = StrField(slen=32, required=False, example='123456sb')
    nonce_str    = StrField(slen=32, example='1417574675')
    sign         = StrField(slen=32, example='841B3002FE2220C87A2D08ABD8A8F791')
    result_code  = StrField(slen=16, example='SUCCESS')
    err_code     = StrField(slen=32, required=False, example='')
    err_code_des = StrField(slen=128, required=False, example='')
    coupon_stock_id = StrField(example='1567')
    resp_count   = IntField(example=1)

    success_count = IntField(example=1)
    failed_count  = IntField(example=1)
    openid        = StrField(example='onqOjjrXT-776SpHnfexGm1_P7iE')
    ret_code      = StrField(example='SUCCESS')
    coupon_id     = StrField(example='1870')
    ret_msg       = StrField(required=False, example=u'用户已达领用上限')


class WechatCoupon(object):
    def __init__(self, key, cert, url=None):
        self.key = key
        self.cert = cert
        if url is None:
            url = COUPON_SEND_URL
        self.url = url

    def send(self, entity):
        data = entity.to_xml_str(self.key)
        res = requests.post(self.url, data=data.encode('utf8'), cert=self.cert, verify=False)
        res_entity = CouponResponseEntity.from_xml_str(res.content)
        return res_entity


if __name__ == '__main__':
    from datetime import datetime
    from util import gen_partner_trade_no, gen_noise_str
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

    from test.config import Config

    entity = CouponEntity()
    mch_id = Config.mch_id
    entity.coupon_stock_id = Config.coupon_stock_id
    entity.openid_count = 1
    entity.partner_trade_no = gen_partner_trade_no(mch_id)
    entity.openid = Config.openid
    entity.appid = Config.app_id
    entity.mch_id = mch_id
    entity.nonce_str = gen_noise_str()

    coupon = WechatCoupon(key=Config.api_key, cert=Config.cert_pair)
    res = coupon.send(entity)
    print(res)







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

