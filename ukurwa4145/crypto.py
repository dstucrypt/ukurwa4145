from .math import Field
import random


class Pubkey(object):
    def __init__(self, point):
        self.point = point

    def _help_check(self, value, s, r, domain=None):

        mulQ = self.point * r
        mulS = domain.base * s

        pointR = mulS + mulQ

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

    def sign(self, value=None, value_hash=None, domain=None):
        if not value and not value_hash:
            raise ValueError("Nothing to sign")

        if not value_hash:
            raise ValueError("Hashing is not supported yet")

        rand_e = random.randint(1, domain.order)
        return self._help_sign(Field.truncate(value_hash), rand_e, domain)

    def pub(self, domain=None):
        point_q = (domain.base * self.param_d).negate()
        return Pubkey(point_q)

    def _help_sign(self, value, rand_e, domain):
        eG = domain.base * rand_e

        r = Field.mul(value, eG.x.v)
        r = Field.truncate(r)

        s = (self.param_d * r) % domain.order

        s = (s + rand_e) % domain.order

        return s, r
