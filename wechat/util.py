#coding: utf8

import hashlib
import socket
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError


from wechat.exceptions import WechatXmlException, WechatResponseException


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


def getCDataText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.CDATA_SECTION_NODE:
            rc.append(node.data)
    return ''.join(rc)


def check_send_success(content):
    try:
        dom = parseString(content)
        result_codes = dom.getElementsByTagName('result_code')
        if not result_codes:
            raise WechatXmlException(u'xml中未发现 result_code')
        result_code = result_codes[0]
        text = getCDataText(result_code.childNodes)
        if text == 'SUCCESS':
            return True
        else:
            err_code_dess = dom.getElementsByTagName('err_code_des')
            if not err_code_dess:
                raise WechatXmlException(u'xml 中未发现 err_code_des')
            err_code_des = err_code_dess[0]
            err_code_text = getCDataText(err_code_des.childNodes)
            raise WechatResponseException(err_code_text)
    except ExpatError as e:
        raise WechatXmlException(u'解析xml错误:'+e.message)
