#coding: utf8

import hashlib
import socket
import datetime
import string
import random
import json
from xml.dom.minidom import parseString, getDOMImplementation, Node
from xml.parsers.expat import ExpatError


from wechat.exceptions import WechatXmlException, WechatResponseException

noise_sample_with_letter = string.letters + string.digits
noise_sample_number = string.digits

SUCCESS = 'SUCCESS'


def to_partial_sign_str(entity, fields):
    temp_lst = [u"{field}={value}".format(field=field, value=getattr(entity, field)) for field in fields]
    return u'&'.join(temp_lst)


def sign_str(entity, fields, key):
    '''
    doc: https://pay.weixin.qq.com/wiki/doc/api/tools/sp_coupon.php?chapter=4_3
    '''
    tmp_str = to_partial_sign_str(entity, fields) + u'&key={key}'.format(key=key)
    m = hashlib.md5()
    m.update(tmp_str.encode('utf8'))
    return m.hexdigest().upper()


def get_ip():
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    return ip


def check_send_success(data):
    data_str = json.dumps(data)
    if 'result_code' not in data:
        raise WechatXmlException(u'xml中未发现 result_code -- %s' % data_str)
    result_code = data['result_code']
    if result_code == 'SUCCESS':
        return True
    for e in ('err_code', 'err_code_des'):
        if e not in data:
            raise WechatXmlException(u'xml 中未发现 字段 %s -- %s' % (e, data_str))
    err_code = data['err_code']
    err_code_desc = data['err_code_des']
    raise WechatResponseException(u'err_code:%s, err_code_desc:%s -- %s'% (err_code, err_code_desc, data_str))


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType in (Node.CDATA_SECTION_NODE, Node.TEXT_NODE):
            rc.append(node.data)
    return ''.join(rc)


class XMLUtil(object):
    ROOT_NAME = 'xml'

    @classmethod
    def serializer(cls, data):
        impl = getDOMImplementation()

        new_doc = impl.createDocument(None, cls.ROOT_NAME , None)
        top_element= new_doc.documentElement
        for key in data:
            val = data[key]
            elem = new_doc.createElement(key)
            text = new_doc.createTextNode(str(val))
            elem.appendChild(text)
            top_element.appendChild(elem)
        return top_element.toxml()

    @classmethod
    def deserializer(cls, xml_str):
        try:
            dom = parseString(xml_str)
            childs = dom.childNodes
            if len(childs) != 1:
                raise WechatXmlException(u'xml格式错误:'+u'包含多个根')
            root = childs[0]
            if root.nodeName != cls.ROOT_NAME:
                raise WechatXmlException(u'xml格式错误:'+u'root格式错误')
            data = {}
            for child in root.childNodes:
                if child.nodeType != Node.ELEMENT_NODE:
                    continue
                key = child.nodeName
                val = getText(child.childNodes)
                data[key] = val
            return data
        except ExpatError as e:
            raise WechatXmlException(u'解析xml错误:' + e.message)


def gen_noise_str(slen=10, only_number=True):
    if only_number:
        sample = noise_sample_number
    else:
        sample = noise_sample_with_letter

    res = []
    for _ in range(slen):
        r = random.choice(sample)
        res.append(r)
    return ''.join(res)


def gen_partner_trade_no(mch_id, day=None, no=None):
    if day is None:
        day = datetime.datetime.now()
    day_str = day.strftime('%Y%m%d')
    if no is None:
        no = gen_noise_str(8)
    return ''.join([str(mch_id), day_str, no])


if __name__ == '__main__':
    xml_str = XMLUtil.serializer({'sign': 'xx', 'nono':'vv'})
    # print(xml_str)

    __RECEIVE_SAMPLE = '''
    <xml>
    <return_code>FAILED</return_code>
    <appid>wx5edab3bdfba3dc1c</appid>
    <mch_id>10000098</mch_id>
    <nonce_str>1417579335</nonce_str>
    <sign>841B3002FE2220C87A2D08ABD8A8F791</sign>
    <result_code>FAILED</result_code>
    <coupon_stock_id>1717</coupon_stock_id>
    <resp_count>1</resp_count>
    <success_count>1</success_count>
    <failed_count>0</failed_count>
    <openid>onqOjjrXT-776SpHnfexGm1_P7iE</openid>
    <ret_code>FAILED</ret_code>
    <coupon_id>6954</coupon_id>
    </xml>
    '''
    data = XMLUtil.deserializer(__RECEIVE_SAMPLE)
    # print(data)
    # print(check_send_success(data))

    # print(gen_noise_str())
    # print (gen_partner_trade_no(10000098))
    class TestEntity:
        appid = 'wxd930ea5d5a258f4f'
        mch_id = 10000100
        device_info= 1000
        body = 'test'
        nonce_str = 'ibuaiVcKdpRxkhJA'
    key = '192006250b4c09247ec02edce69f6a2d'
    fields = ['appid', 'mch_id', 'device_info', 'body', 'nonce_str']
    fields.sort()

    res = sign_str(TestEntity, fields, key)
    print(res)


