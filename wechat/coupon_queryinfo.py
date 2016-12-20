#coding: utf8
import requests

from wechat.consts import COUPON_QUERY_INFO_URL
from wechat.entity import Entity
from wechat.fields import IntField, StrField


class CouponQueryInfoEntity(Entity):
    coupon_id = StrField(example='1565')
    openid    = StrField(example='onqOjjrXT-776SpHnfexGm1_P7iE')
    appid     = StrField(slen=32, example='wx5edab3bdfba3dc1c')
    mch_id    = StrField(slen=32, example='10000098')
    stock_id  = StrField(slen=32, example='58818')
    op_user_id= StrField(slen=32, required=False, example='10000098')
    device_info=StrField(slen=32, required=False, example='')
    nonce_str = StrField(slen=32, example='1417574675')
    sign      = StrField(slen=32, example='841B3002FE2220C87A2D08ABD8A8F791')
    version   = StrField(slen=32, required=False, example='1.0')
    type      = StrField(slen=32, required=False, example='XML')


class CouponQueryInfoResponseEntity(Entity):
    IS_RESPONSE = True

    return_code = StrField(example='SUCCESS')
    return_msg  = StrField(required=False, example='')
    appid       = StrField(slen=32, example='wx5edab3bdfba3dc1c')
    mch_id      = StrField(slen=32, example='10000098')
    sub_mch_id  = StrField(slen=32, required=False, example='10000098')
    device_info =StrField(slen=32, required=False, example='123456sb')
    nonce_str   = StrField(slen=32, example='1417574675')
    sign        = StrField(slen=32, required=False, example='841B3002FE2220C87A2D08ABD8A8F791') #?? 实际测试字段没有
    result_code = StrField(slen=16, example='SUCCESS')
    err_code    = StrField(slen=32, required=False, example='')
    err_code_des = StrField(slen=128, required=False, example='')
    coupon_stock_id   = StrField(example='1567')
    coupon_stock_type = IntField(example=1)
    coupon_id         = StrField(example='4242')
    coupon_value      = IntField(example=4)
    coupon_mininum    = IntField(required=False, example=10) #?? 实际测试字段是 coupon_minimum
    coupon_name       = StrField(example=u'测试代金券')
    coupon_state      = IntField(example=2)
    coupon_type       = IntField(example=1)
    coupon_desc       = StrField(example=u'微信支付-代金券')
    coupon_use_value  = IntField(example=0)
    coupon_remain_value= IntField(example=4)
    begin_time        = StrField(example='1943787483')
    end_time          = StrField(example='1943787484')
    send_time         = StrField(example='1943787420')
    use_time          = StrField(required=False, example='1943787483')
    trade_no          = StrField(required=False, example='20091227091010')
    consumer_mch_id   = StrField(required=False, example='10000098')
    consumer_mch_name = StrField(required=False, example=u'测试商户')
    consumer_mch_appid= StrField(required=False, example='wx5edab3bdfba3dc1c')
    send_source       = StrField(example='1')
    is_partial_use    = StrField(required=False, example='1')


class WechatCouponQueryInfo(object):
    def __init__(self, key, url=None):
        self.key = key
        if url is None:
            url = COUPON_QUERY_INFO_URL
        self.url = url

    def send(self, entity):
        data = entity.to_xml_str(self.key)
        res = requests.post(self.url, data=data.encode('utf8'), verify=False)
        res_entity = CouponQueryInfoResponseEntity.from_xml_str(res.content)
        return res_entity


if __name__ == '__main__':
    from test.config import Config
    from util import gen_noise_str
    queryInfoEntity = CouponQueryInfoEntity()
    queryInfoEntity.coupon_id = '1077223085'
    queryInfoEntity.openid = Config.openid
    queryInfoEntity.appid = Config.app_id
    queryInfoEntity.mch_id = Config.mch_id
    queryInfoEntity.stock_id =Config.coupon_stock_id
    queryInfoEntity.nonce_str = gen_noise_str()

    queryInfo = WechatCouponQueryInfo(key=Config.api_key)
    res = queryInfo.send(entity=queryInfoEntity)
    print(res)


#------------- doc -----------------

'''
查询代金券
doc url: https://pay.weixin.qq.com/wiki/doc/api/tools/sp_coupon.php?chapter=12_5
'''

___SEND_SAMPLE ='''
<xml>
<appid>121512345</appid>
<coupon_id>121512345456</coupon_id>
<mch_id>10010405</mch_id>
<nonce_str>1417575784</nonce_str>
<openid>onqOjjrXT-776SpHnfexGm1_P7iE</openid>
<sign>16F1415792512A5C340170B35F6C60E6</sign>
</xml>
'''

__RECEIVE_SAMPLE = '''
<xml>
  <return_code>SUCCESS</return_code>
  <appid>wx5edab3bdfba3dc1c</appid>
  <mch_id>10000098</mch_id>
  <nonce_str>1417586982</nonce_str>
  <sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
  <result_code>SUCCESS</result_code>
  <coupon_stock_id>1717</coupon_stock_id>
  <coupon_stock_type>1</coupon_stock_type>
  <coupon_id>1442</coupon_id>
  <coupon_value>5</coupon_value>
  <coupon_mininum>10</coupon_mininum>
  <coupon_name>测试代金券</coupon_name>
  <coupon_state>2</coupon_state>
  <coupon_type>1</coupon_type>
  <coupon_desc>微信支付-代金券</coupon_desc>
  <coupon_use_value>0</coupon_use_value>
  <coupon_remain_value>5</coupon_remain_value>
  <begin_time>1943787483</begin_time>
  <end_time>1943787484</end_time>
  <send_time>1943787420</send_time>
  <send_source>1</send_source>
</xml>
'''

__RECEIVE_ERR_SAMPLE = '''
<xml>
  <return_code>SUCCESS</return_code>
  <appid>wx5edab3bdfba3dc1c</appid>
  <mch_id>10000098</mch_id>
  <nonce_str>1417586982</nonce_str>
  <sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
  <result_code>SUCCESS</result_code>
  <err_code>268456007</err_code>
  <err_code_des>你已领取过包</err_code_des>
  <coupon_stock_id>1717</coupon_stock_id>
  <coupon_stock_type>1</coupon_stock_type>
  <coupon_id>1442</coupon_id>
  <coupon_value>5</coupon_value>
  <coupon_mininum>10</coupon_mininum>
  <coupon_name>测试代金券</coupon_name>
  <coupon_state>2</coupon_state>
  <coupon_type>1</coupon_type>
  <coupon_desc>微信支付-代金券</coupon_desc>
  <coupon_use_value>0</coupon_use_value>
  <coupon_remain_value>5</coupon_remain_value>
  <begin_time>1943787483</begin_time>
  <end_time>1943787484</end_time>
  <send_time>1943787420</send_time>
  <send_source>1</send_source>
</xml>
'''
