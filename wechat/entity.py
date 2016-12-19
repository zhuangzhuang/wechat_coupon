#coding: utf8
import six

from wechat.exceptions import WechatEntityException
from wechat.fields import BaseField, StrField, IntField
from wechat.util import sign_str, XMLUtil

_SIGN = 'sign'


class BaseEntity(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(BaseEntity, cls).__new__
        fields = {}
        normal_attrs = {}
        for key in attrs:
            value = attrs[key]
            if isinstance(value, BaseField):
                fields[key] = value
            else:
                normal_attrs[key] = value

        new_class = super_new(cls, name, bases, normal_attrs)
        required_fields = []
        for field in fields:
            value = fields[field]
            if value.required and field != _SIGN:
                required_fields.append(field)
        required_fields_with_sign = required_fields[:] + [_SIGN]
        all_fields = fields.keys()
        required_fields.sort()
        new_class._REQUIRE_FIELDS = required_fields
        new_class._REQUIRE_FIELDS_WITH_SIGN = required_fields_with_sign
        new_class._ALL_FIELDS = all_fields
        new_class._FIELDS = fields
        return new_class


class Entity(six.with_metaclass(BaseEntity)):

    def from_xml_str(self, xml_str):
        pass

    def to_xml_str(self, key):
        self.validate()
        self.sign = sign_str(self, self._REQUIRE_FIELDS, key)
        data = {k: getattr(self, k) for k in self._REQUIRE_FIELDS_WITH_SIGN}
        res = XMLUtil.serializer(data)
        return res

    def validate(self, with_sign=False):
        validate_field = self._REQUIRE_FIELDS_WITH_SIGN if with_sign else self._REQUIRE_FIELDS
        for filed in validate_field:
            value = getattr(self, filed)
            if not value:
                raise WechatEntityException('require field %s', filed)


if __name__ == '__main__':
    class Request(Entity):
        coupon_stock_id = IntField(required=True, example=1234)
        sign = StrField(required=True, example='841B3002FE2220C87A2D08ABD8A8F791')

    req = Request()
    req.coupon_stock_id = 123
    req.sign = '841B3002FE2220C87A2D08ABD8A8F791'
    print(req.to_xml_str('kk'))