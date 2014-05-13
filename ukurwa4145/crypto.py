from .math import Field


class Pubkey(object):
    def __init__(self, point):
        self.point = point

    def _help_check(self, value, s, r, domain=None):

        mulQ = self.point * r
        mulS = domain.base * s

        pointR = mulS + mulQ

        print hex(pointR.x.v)

        value = Field.truncate(value)
        r1 = Field.mul(value, pointR.x.v)
        r1 = Field.truncate(r1)
        print hex(r1), hex(r)
        return r1 == r


class Priv(object):
    def __init__(self, d):
        self.param_d = d

    def pub(self, domain=None):
        return (domain.base * self.param_d).negate()

    def _help_sign(self, value, rand_e, domain):
        eG = domain.base * rand_e

        r = Field.mul(value, eG.x.v)
        r = Field.truncate(r)

        s = (self.param_d * r) % domain.order

        s = (s + rand_e) % domain.order

        return s, r
