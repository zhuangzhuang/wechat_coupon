#coding: utf8

from wechat.consts import COUPON_QUERY_INFO_URL
from wechat.util import sign_str, check_send_success


COUPON_QUERY_INFO_FIELDS = [

]


class CouponQueryinfoEntity(object):
    coupon_id=None    #require str ex:  1565
    openid=None       #require str ex:  onqOjjrXT-776SpHnfexGm1_P7iE
    appid=None        #require str(32) ex: wx5edab3bdfba3dc1c
    mch_id=None       #require str(32) ex: 10000098
    stock_id=None     #require str(32) ex: 58818
    op_user_id=None   #no_require str(32) ex: 10000098
    device_info=None  #no_require str(32) ex:
    nonce_str=None    #require str(32) ex: 1417574675
    sign=None         #require str(32) ex: 841B3002FE2220C87A2D08ABD8A8F791
    version=None      #no_require str(32) ex: 1.0
    type=None         #no_require str(32) ex: XML`



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
