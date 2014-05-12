#!/usr/bin/env python
# encoding: utf-8
#
# Ukrainional national cryptography standard DSTU 4145.
#
# Ilya Petrov, 2014

def bitl(val):
    return val.bit_length()


class Pubkey(object):
    def __init__(self, dp, W):
        self.dp = dp
        self.W = W


class Field(object):
    def __init__(self, v):
        self.v = self.mod(v)

    @classmethod
    def mod(self, val):

        if self.modulus == 0:
            raise TypeError("Field class not configured")

        if val <= self.modulus:
            return val

        rv = val
        bitm_l = bitl(self.modulus)
        while bitl(rv) >= bitm_l:
            mask = self.modulus << (bitl(rv) - bitm_l)
            rv = rv ^ mask

        return rv

    @classmethod
    def mul(self, val_a, val_b):
        val_c = 0
        for j in range(bitl(val_a)):
            if val_a & (1<<j):
                val_c = val_c ^ val_b
            val_b = val_b << 1

        return self.mod(val_c)

    @classmethod
    def add(self, val_a, val_b):
        return val_a ^ val_b

    @classmethod
    def inv(cls, val_a):
        b = 1
        c = 0
        u = cls.mod(val_a)
        v = cls.modulus

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
    def set_modulus(cls, k3, k2, k1):
        modulus = 0
        modulus |= 1<<k3
        modulus |= 1<<k2
        modulus |= 1<<k1

        cls.modulus = modulus


class Point(object):
    def __init__(self, x, y):
        self.x = Field(x)
        self.y = Field(y)

    def is_zero(self):
        return (self.x.v == 0) and (self.y.v == 0)

    def __repr__(self):
        return '<Point X:{:x} Y:{:x}>'.format(self.x.v, self.y.v)


class Curve(object):
    def __init__(self, field_a, field_b):
        self.field_a = field_a
        self.field_b = field_b

    def add(self, point_0, point_1):
        a = self.field_a
        b = self.field_b

        x0, y0 = point_0.x.v, point_0.y.v
        x1, y1 = point_1.x.v, point_1.y.v

        point_2 = Point(0, 0)

        if point_0.is_zero():
            return point_1

        if point_1.is_zero():
            return point_0

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

    def mul(self, param_n, point):
        if param_n == 0:
            raise ValueError("create point with no params")

        if param_n < 0:
            raise ValueError("dunno")

        point_s = Point(0, 0)
        for j in range(bitl(param_n) - 1, -1, -1):
            point_s = self.add(point_s, point_s)
            if param_n & (1<<j):
                point_s = self.add(point_s, point)

        return point_s


class Domain(object):
    def __init__(self, param_m, nom_k, curve, order, base, cofactor):
        self.param_m = param_m
        self.nom_k = nom_k
        self.curve = curve
        self.order = order
        self.base = base
        self.cofactor = cofactor


def dstu257():

    Field.set_modulus(257, 12, 0)

    PARAM_A = 0
    PARAM_B = 0x01CEF494720115657E18F938D7A7942394FF9425C1458C57861F9EEA6ADBE3BE10
    ORDER = 0x800000000000000000000000000000006759213AF182E987D3E17714907D470D
    BASE_X = 0x002A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB7
    BASE_Y = 0x010686D41FF744D4449FCCF6D8EEA03102E6812C93A9D60B978B702CF156D814EF
    base_point = Point(BASE_X, BASE_Y)

    return Domain(257, 12, Curve(PARAM_A, PARAM_B), ORDER, base_point)


def main():
    domain = dstu257()
    curve = domain.curve

    pointQ = Point(0x00AFF3EE09CB429284985849E20DE5742E194AA631490F62BA88702505629A6589, 
                  0x01B345BC134F27DA251EDFAE97B3F306B4E8B8CB9CF86D8651E4FB301EF8E1239C)

    print pointQ

    r = 0x61862343DBE63F38EA5041F60E33DFF508164DD691F4E4EBCB1B69B2A1D07C4E
    s = 0x0F131F2A6961079F956A85CED6B34DE0AC22E594532ACBDB0BF8CF170EAAFB91

    mulQ = curve.mul(r, pointQ)
    print mulQ

    mulS = curve.mul(s, domain.base)

    print mulS

if __name__ == '__main__':
    main()