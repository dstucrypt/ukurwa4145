from contextlib import contextmanager
import threading

ldata = threading.local()


@contextmanager
def curve(name):
    ldata.curve_domain = StandardDomain.resolve(name)()
    ldata.curve = ldata.curve_domain.curve
    ldata.modulus = ldata.curve_domain.modulus
    yield ldata.curve_domain
    del ldata.curve_domain
    del ldata.curve
    del ldata.modulus


class Curve(object):
    def __init__(self, field_a, field_b):
        self.field_a = field_a
        self.field_b = field_b


class Domain(object):
    def __init__(self, param_m, nom_k, curve, order, base=None):
        self.param_m = param_m
        self.nom_k = nom_k
        self.curve = curve
        self.order = order
        self._base = base
        print param_m, nom_k
        self.modulus = Field.comp_modulus(param_m, *self.nom_k)

    def __exit__(self, exc_type, exc_value, tracebac):
        pass


class RegisterDomain(type):
    def __new__(cls, name, bases, attrs):
        curve_name = attrs.get('NAME')

        ret = super(RegisterDomain, cls).__new__(cls, name, bases, attrs)

        if curve_name is not None:
            StandardDomain.register(curve_name, ret)

        return ret


class StandardDomain(Domain):
    REGISTRY = {}
    __metaclass__ = RegisterDomain
    def __init__(self):
        curve = Curve(self.PARAM_A, self.PARAM_B)
        super(StandardDomain, self).__init__(self.PARAM_M, self.PARAM_K, curve, self.ORDER)

    @classmethod
    def register(cls, name, curve):
        cls.REGISTRY[name] = curve

    @classmethod
    def resolve(cls, name):
        try:
            return cls.REGISTRY[name]
        except KeyError:
            raise ValueError("Standard curve {} not found".format(name))

    @property
    def base(self):
        try:
            base = self._base
            if base is None:
                raise AttributeError()
        except AttributeError:
            base = Point(self.BASE_X, self.BASE_Y)
            self._base = base

        return base

from . math import Field, Point
