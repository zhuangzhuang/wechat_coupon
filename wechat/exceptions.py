#coding: utf8


class WechatException(Exception):
    pass


class WechatXmlException(WechatException):
    pass


class WechatResponseException(WechatException):
    pass


class WechatEntityException(WechatException):
    pass