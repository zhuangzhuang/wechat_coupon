#coding: utf8


class BaseField(object):
    name = 'base_filed'

    default = None

    def __init__(self, required=True, example=None, **kwargs):
        self.required = required
        self.example = example

    #todo, add more check


class StrField(BaseField):
    name = 'str_field'
    default = None

    def __init__(self, slen=None, required=True, example=None, **kwargs):
        super(StrField, self).__init__(required, example, **kwargs)
        self.slen = slen


class IntField(BaseField):
    name = 'int_field'
    default = None

    def __init__(self, required=True, example=None, **kwargs):
        super(IntField, self).__init__(required, example, **kwargs)
