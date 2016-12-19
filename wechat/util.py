#coding: utf8

import hashlib
import socket
from xml.dom.minidom import parseString, getDOMImplementation, Node
from xml.parsers.expat import ExpatError


from wechat.exceptions import WechatXmlException, WechatResponseException

SUCCESS = 'SUCCESS'

def to_partial_sign_str(entity, fields):
    temp_lst = [u"{field}={value}".format(field=field, value=getattr(entity, field)) for field in fields]
    return u'&'.join(temp_lst)


def sign_str(entity, fields, key):
    tmp_str = to_partial_sign_str(entity, fields) + u'&key={key}'.format(key=key)
    m = hashlib.md5()
    m.update(tmp_str.encode('utf8'))
    return m.hexdigest().upper()


def get_ip():
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    return ip


def check_send_success(data):
    if 'result_code' not in data:
        raise WechatXmlException(u'xml中未发现 result_code')
    result_code = data['result_code']
    if result_code == 'SUCCESS':
        return True
    if 'err_code_des' not in data:
        raise WechatXmlException(u'xml 中未发现 err_code_des')
    raise WechatResponseException(data['err_code_des'])


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
    print(data)
    print(check_send_success(data))
