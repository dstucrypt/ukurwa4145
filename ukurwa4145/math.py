import random
from . context import ldata


bitl = long.bit_length


class Field(object):
    def __init__(self, v):
        if isinstance(v, int):
            v = long(v)

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
    def truncate(cls, val, to_size=None):
        val = long(val)
        domain = ldata.curve_domain
        bitl_o = to_size if to_size else bitl(domain.order)
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
    def trace(cls, val):
        modulus = ldata.modulus

        rv = long(val)
        bitm_l = bitl(modulus)
        for idx in range(1, bitm_l-1):
            rv = long(rv)
            rv = cls.mul(rv, rv)
            rv = rv ^ val

        return rv

    @classmethod
    def squad(cls, val):
        modulus = ldata.modulus

        if modulus & 1:
            ret = cls.squad_odd(val)
        else:
            ret = cls.squad_even(val)

        return cls.mod(ret)

    @classmethod
    def squad_odd(cls, val):
        val_a = cls.mod(val)
        val_z = val_a

        for idx in range(1, ((cls.p0-1)/2) + 1):
            val_z = cls.mul(val_z, val_z)
            val_z = cls.mul(val_z, val_z)
            val_z = cls.add(val_z, val_a)

        val_w = cls.mul(val_z, val_z)
        val_w = cls.add(val_z, val_w)

        assert val_w == val_a

        return val_z

    @classmethod
    def squad_eve(cls, val):
        raise ValueError("Not implemented")

    @classmethod
    def comp_modulus(cls, k3, k2, k1):
        cls.p0 = k3
        modulus = 0
        modulus |= 1<<k3
        modulus |= 1<<k2
        modulus |= 1<<k1

        return modulus

    def __eq__(self, other):
        return long.__cmp__(self.v,  other.v) == 0


class Point(object):
    FORMAT_UNCOMPRESSED = '\x04'

    def __init__(self, x, y):
        self.x = Field(x)
        self.y = Field(y)

    @classmethod
    def expand(cls, val):

        pb = ldata.curve.field_b
        pa = ldata.curve.field_a

        if val == 0:
            return val, Field.mul(pb, pb)

        valmask = (1<<ldata.curve_domain.param_m) - 1
        k = val & 1
        val = (valmask-1) & val

        trace = Field.trace(val)

        if (trace and pa == 0) or (not trace and pa == 1):
            val = val | 1

        x2 = Field.mul(val, val)

        y = Field.mul(x2, val)

        if pa == 1:
            y = Field.add(y, x2)

        y = Field.add(y, pb)
        x2 = Field.inv(x2)

        y = Field.mul(y, x2)

        y = Field.squad(y)

        trace_y = Field.trace(y)

        if (k and not trace_y) or (not k and trace_y):
            y += 1

        y = Field.mul(y, val)
        return val, y

    @classmethod
    def decode(cls, data, in_hex=True):
        if in_hex:
            data = data.decode('hex')

        sz = len(data) - 1
        hsz = sz / 2
        code, data_x, data_y = data[0], data[1:hsz+1], data[hsz+1:]

        if code[0] == cls.FORMAT_UNCOMPRESSED:
            point_x = int(data_x.encode('hex'), 16)
            point_y =  int(data_y.encode('hex'), 16)

            return cls(point_x, point_y)

        raise ValueError("Only uncompressed points supported")

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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def negate(self):
        ret = Point(0, 0)
        ret.x.v = self.x.v
        ret.y.v = Field.add(self.y.v, self.x.v)
        return ret

    def mul(self, param_n):
        if param_n == 0:
            raise Point(0, 0)

        if param_n < 0:
            param_n = long(-param_n)
            point = self.negate()
        else:
            param_n = long(param_n)
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

    infinity = property(is_zero)

    def __repr__(self):
        return '<Point X:{:x} Y:{:x}>'.format(self.x.v, self.y.v)


