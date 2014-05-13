#!/usr/bin/env python
# encoding: utf-8
#
# Ukrainional national cryptography standard DSTU 4145.
#
# Ilya Petrov, 2014

from contextlib import contextmanager
import threading

ldata = threading.local()

bitl = long.bit_length


@contextmanager
def curve():
    ldata.curve_domain = dstu257()
    ldata.curve = ldata.curve_domain.curve
    ldata.modulus = ldata.curve_domain.modulus
    yield ldata.curve_domain
    del ldata.curve_domain
    del ldata.curve
    del ldata.modulus


class Pubkey(object):
    def __init__(self, dp, W):
        self.dp = dp
        self.W = W


class Field(object):
    def __init__(self, v):
        self.v = self.mod(v)

    @classmethod
    def mod(self, val):
        modulus = ldata.modulus

        if modulus == 0:
            raise TypeError("Field class not configured")

        if val <= modulus:
            return val

        rv = val
        bitm_l = bitl(modulus)
        while bitl(rv) >= bitm_l:
            mask = modulus << (bitl(rv) - bitm_l)
            rv = rv ^ mask

        return rv

    @classmethod
    def truncate(cls, val):
        domain = ldata.curve_domain
        bitl_o = bitl(domain.order)
        xbit = bitl(val)
        while bitl_o <= xbit:
            val = val ^ (1<<(xbit - 1))
            xbit = bitl(val)

        return val

    @classmethod
    def mul(self, val_a, val_b):
        val_c = 0
        for j in xrange(bitl(val_a)):
            if val_a & (1<<j):
                val_c = val_c ^ val_b
            val_b = val_b << 1

        return self.mod(val_c)

    @classmethod
    def add(self, val_a, val_b):
        return val_a ^ val_b

    @classmethod
    def inv(cls, val_a):
        modulus = ldata.modulus
        b = 1
        c = 0
        u = cls.mod(val_a)
        v = modulus

        while bitl(u) > 1:
            j = bitl(u) - bitl(v)
            if j < 0:
                u, v = v, u
                c, b = b, c
                j = -j

            u = cls.add(u, v << j)
            b = cls.add(b, c << j)
         
        return b

    @classmethod
    def comp_modulus(cls, k3, k2, k1):
        modulus = 0
        modulus |= 1<<k3
        modulus |= 1<<k2
        modulus |= 1<<k1

        return modulus


class Point(object):
    def __init__(self, x, y):
        self.x = Field(x)
        self.y = Field(y)

    def add(self, point_1):
        a = ldata.curve.field_a

        x0, y0 = self.x.v, self.y.v
        x1, y1 = point_1.x.v, point_1.y.v

        point_2 = Point(0, 0)

        if self.is_zero():
            return point_1

        if point_1.is_zero():
            return self

        if x0 != x1:
            lbd = Field.mul(
                Field.add(y0, y1),
                Field.inv(Field.add(x0, x1))
            )
            x2 = Field.add(a, Field.mul(lbd, lbd))
            x2 = Field.add(x2, lbd)
            x2 = Field.add(x2, x0)
            x2 = Field.add(x2, x1)

        elif y0 != y1:
            return point_2
        elif x1 == 0:
            return point_2
        else:
            lbd = Field.add(x1, Field.mul(y1, Field.inv(x1)))
            x2 = Field.add(a, Field.mul(lbd, lbd))
            x2 = Field.add(x2, lbd)

        y2 = Field.mul(Field.add(x1, x2), lbd)
        y2 = Field.add(y2, x2)
        y2 = Field.add(y2, y1)

        point_2.x.v = x2
        point_2.y.v = y2

        return point_2

    __add__ = add

    def negate(self):
        ret = Point(0, 0)
        ret.x.v = self.x.v
        ret.y.v = self.y.v + self.x.v
        return ret

    def mul(self, param_n):
        if param_n == 0:
            raise Point(0, 0)

        if param_n < 0:
            param_n = -param_n
            point = self.negate()
        else:
            point = self

        point_s = Point(0, 0)
        for j in xrange(bitl(param_n) - 1, -1, -1):
            point_s = point_s + point_s
            if param_n & (1<<j):
                point_s = point_s + point

        return point_s

    __mul__ = mul

    def is_zero(self):
        return (self.x.v == 0) and (self.y.v == 0)

    def __repr__(self):
        return '<Point X:{:x} Y:{:x}>'.format(self.x.v, self.y.v)


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
        self.modulus = Field.comp_modulus(param_m, *self.nom_k)

    def __exit__(self, exc_type, exc_value, tracebac):
        pass


class DSTU_257(Domain):
    BASE_X = 0x002A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB7
    BASE_Y = 0x010686D41FF744D4449FCCF6D8EEA03102E6812C93A9D60B978B702CF156D814EF

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


def dstu257():

    PARAM_A = 0
    PARAM_B = 0x01CEF494720115657E18F938D7A7942394FF9425C1458C57861F9EEA6ADBE3BE10
    ORDER = 0x800000000000000000000000000000006759213AF182E987D3E17714907D470D
    
    return DSTU_257(257, [12, 0], Curve(PARAM_A, PARAM_B), ORDER)

def verify(e, s, r, pub):
    pass
