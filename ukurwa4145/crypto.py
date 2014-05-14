from .math import Field
import random


class ParamError(TypeError):
    pass


class Pubkey(object):
    def __init__(self, point):
        self.point = point

    def _help_check(self, value, s, r, domain=None):

        if s == 0 or r == 0:
            raise ValueError("Signature cannot be zero")

        if s > domain.order or r > domain.order:
            raise ValueError("Signature value cannot be grater than order")

        mulQ = self.point * r
        mulS = domain.base * s

        pointR = mulS + mulQ
        if pointR.infinity:
            raise ValueError("Invalid signature. R point is infinity")

        value = Field.truncate(value)
        r1 = Field.mul(value, pointR.x.v)
        r1 = Field.truncate(r1)
        return r1 == r

    def validate(self, domain):
        pub_q = self.point
        if pub_q.infinity:
            raise ValueError('Pub Q is intity')

        if pub_q not in domain.curve:
            raise ValueError('Pub Q is not on curve')

        pt = pub_q * domain.order
        if not pt.infinity:
            raise ValueError('Pub Q * N should equal infinity')

    def __eq__(self, other):
        return self.point == other.point

class Priv(object):
    def __init__(self, d):
        self.param_d = d

    @classmethod
    def generate(cls, domain=None):
        rand_d = random.randint(1, domain.order)

        while True:
            priv = cls(rand_d)
            pub = priv.pub(domain)

            try:
                pub.validate(domain)
            except ValueError:
                continue

            return priv, pub

    def pub(self, domain=None):
        point_q = (domain.base * self.param_d).negate()
        return Pubkey(point_q)

    def sign(self, value=None, value_hash=None, domain=None):
        if not value and not value_hash:
            raise ValueError("Nothing to sign")

        if not value_hash:
            raise ValueError("Hashing is not supported yet")

        truncated = Field.truncate(value_hash, domain.param_m)
        while True:
            try:
                rand_e = random.randint(1, domain.order)
                return self._help_sign(truncated, rand_e, domain)
            except ParamError:
                pass

    def _help_sign(self, value, rand_e, domain):
        eG = domain.base * rand_e
        if eG.x.v == 0:
            raise ParamError("Random point have zero X coord")

        value = Field.truncate(value, domain.param_m)
        r = Field.mul(value, eG.x.v)
        r = Field.truncate(r)
        if r == 0:
            raise ParamError("Got zero R")

        s = (self.param_d * r) % domain.order

        s = (s + rand_e) % domain.order

        return s, r
