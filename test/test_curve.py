import re
from ukurwa4145 import curve, Point, Priv, Pubkey, on_curve, Field
import random

PUB_KEY = """
    04:00:af:f3:ee:09:cb:42:92:84:98:58:49:e2:0d:
    e5:74:2e:19:4a:a6:31:49:0f:62:ba:88:70:25:05:
    62:9a:65:89:01:b3:45:bc:13:4f:27:da:25:1e:df:
    ae:97:b3:f3:06:b4:e8:b8:cb:9c:f8:6d:86:51:e4:
    fb:30:1e:f8:e1:23:9c
"""

PUB_X = 0x00AFF3EE09CB429284985849E20DE5742E194AA631490F62BA88702505629A6589
PUB_Y = 0x01B345BC134F27DA251EDFAE97B3F306B4E8B8CB9CF86D8651E4FB301EF8E1239C

@on_curve('DSTU_257')
def test_on_curve(domain):
    point_Q = Point(PUB_X, PUB_Y)
    assert point_Q in domain.curve

    point_INV = Point(1, 1)
    assert point_INV not in domain.curve

@on_curve('DSTU_257')
def test_trace(domain):
    trace = Field.trace(0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB6)
    assert trace == 1


@on_curve('DSTU_257')
def test_expand(domain):
    x, y  = Point.expand(0)
    assert x == 0

    x, y = Point.expand(0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB6)
    assert x == 0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB7
    assert y == 0x010686D41FF744D4449FCCF6D8EEA03102E6812C93A9D60B978B702CF156D814EF

def test_hsign():
    PRIV = 0x2A45EAFE4CD469F811737780C57253360FBCC58E134C9A1FDCD10B0E4529A143
    HASH = 0x6845214B63288A832A772E1FE6CB6C7D3528569E29A8B3584370FDC65F474242
    RAND_E = 0x7A32849E569C8888F25DE6F69A839D75057383F473ACF559ABD3C5D683294CEB

    SIG = (0x0CCC6816453A903A1B641DF999011177DF420D21A72236D798532AEF42E224AB,
        0x491FA1EF75EAEF75E1F20CF3918993AB37E06005EA8E204BC009A1FA61BB0FB2)

    with curve('DSTU_257') as domain:
        priv = Priv(PRIV)
        s, r = priv._help_sign(HASH, rand_e=RAND_E, domain=domain)
        assert SIG == (s, r)

        pub = priv.pub()
        ok = pub._help_verify(HASH, s, r, domain=domain)
        assert ok


def test_sign():
    with curve('DSTU_257') as domain:
        hv = random.randint(1, 2**32)
        hv1 = random.randint(1, 2**32)

        priv, pub = Priv.generate()
        s, r = priv.sign(value_hash=hv)

        ok = pub._help_verify(hv, s, r, domain=domain)
        assert ok

        ok = pub._help_verify(hv1, s, r, domain=domain)
        assert not ok

        ok = pub._help_verify(hv, r, s, domain=domain)
        assert not ok

        ok = pub._help_verify(hv, s, hv1, domain=domain)
        assert not ok




def test_priv_pub():
    with curve('DSTU_257') as domain:
        PRIV = 0x2A45EAFE4CD469F811737780C57253360FBCC58E134C9A1FDCD10B0E4529A143

        priv = Priv(PRIV)
        pub = priv.pub()
        assert pub.point.x.v == PUB_X
        assert pub.point.y.v == PUB_Y


def test_pub_key():
    pub_key = re.sub(r"[ \n:]", '', PUB_KEY)

    with curve('DSTU_257'):
        point = Point.decode(pub_key)
        pointQ = Point(PUB_X, PUB_Y)

        assert point == pointQ


def test_verify():
    with curve('DSTU_257') as domain:
        help_compute(domain)

def test_generate():
    with curve('DSTU_257') as cd:
        priv, pub = Priv.generate()
        assert pub.point in cd.curve
        assert priv.pub() == pub


@on_curve('DSTU_257')
def test_non_eq(domain):
    pointQ = Point(PUB_X, PUB_Y)
    pointB = Point(PUB_X, PUB_X)

    assert pointQ != pointB


def help_compute(domain):

    pointQ = Point(0x00AFF3EE09CB429284985849E20DE5742E194AA631490F62BA88702505629A6589, 
                  0x01B345BC134F27DA251EDFAE97B3F306B4E8B8CB9CF86D8651E4FB301EF8E1239C)

    pub = Pubkey(pointQ)

    r = 0x61862343DBE63F38EA5041F60E33DFF508164DD691F4E4EBCB1B69B2A1D07C4E
    s = 0x0F131F2A6961079F956A85CED6B34DE0AC22E594532ACBDB0BF8CF170EAAFB91
    hash_val =  0x71C910BAC9C494E0F2A6DBDD369C542AAF95E0CF842155C2F76595117EB0F26D


    ok = pub._help_verify(hash_val, s, r, domain=domain)
    assert ok
