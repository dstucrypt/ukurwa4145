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
def test_mod(domain):
    moded = Field.mod(0xaff3ee09cb429284985849e20de5742e194aa631490f62ba88702505629a65890)
    assert moded == 0xff3ee09cb429284985849e20de5742e194aa631490f62ba88702505629a60895

@on_curve('DSTU_257')
def test_mul(domain):
    mul = Field.mul(
        0xaff3ee09cb429284985849e20de5742e194aa631490f62ba88702505629a65890,
        0xa3391f6f341d627ab958fc4223ee8871e336c8d9dda30f407c369268363f0cccb
    )
    assert mul == 0xbeb7d8390bb24fcf6882086cddd4ebe5270c1ed345bc516b40efb92b44530d5f

@on_curve('DSTU_257')
def test_inv(domain):
    neg = Field.inv(0xaff3ee09cb429284985849e20de5742e194aa631490f62ba88702505629a65890)
    assert neg == 0xf5ae84d0c4dc2e7e89c670fb2083d124be50b413efb6863705bd63a5168352e0

@on_curve('DSTU_257')
def test_expand(domain):
    x, y  = Point.expand(0)
    assert x == 0

    x, y = Point.expand(0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB6)
    assert x == 0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB7
    assert y == 0x010686D41FF744D4449FCCF6D8EEA03102E6812C93A9D60B978B702CF156D814EF

    x, y = Point.expand(0x01A77131A7C14F9AA6EA8C760D39673D5F0330FAB1118D55B55B7AF0735975485F)
    assert x == 0x01A77131A7C14F9AA6EA8C760D39673D5F0330FAB1118D55B55B7AF0735975485F
    assert y == 0xDC058ADA665D99084038B5F914FB9CF7214760A4865B49CAF7F4BE7379F3A395


def from_bytes(data):
    ret = 0
    for pos, part in enumerate(data):
        ret = (part << (pos * 8)) | ret

    return ret

@on_curve('DSTU_431')
def test_expand_even(domain):
    point_data = [0xb7, 0x1b, 0xf9, 0xbd, 0x4b, 0x62, 0xca, 0xab, 0x2c, 0x39, 0x50, 0xf5, 0xc5, 0x1d, 0x5f, 0xa8, 0xd, 0x70, 0x7e, 0x0, 0x7b, 0x52, 0x5b, 0x70, 0x67, 0x67, 0xdc, 0xe5, 0xcd, 0x1b, 0xaf, 0x6e, 0x27, 0x68, 0xda, 0xd0, 0xc6, 0xa8, 0x4f, 0xc2, 0x2f, 0x99, 0x5, 0x1d, 0x91, 0x34, 0x35, 0xf4, 0xeb, 0x1e, 0xb1, 0x9a, 0xd5, 0x44]
    x, y = Point.expand(from_bytes(point_data))
    assert (x, y) == (
        0x44d59ab11eebf43534911d05992fc24fa8c6d0da68276eaf1bcde5dc6767705b527b007e700da85f1dc5f550392cabca624bbdf91bb7L,
        0x2a0ec18f2654d32707a697c56716526738c142553e99dd2554ae61e7fef2df86dadb9c03d69ef2145e755a8e5c88615677d6cf1449c2L,
    )

@on_curve('DSTU_431')
def test_expand_odd(domain):
    point_data = [0xb6, 0x1b, 0xf9, 0xbd, 0x4b, 0x62, 0xca, 0xab, 0x2c, 0x39, 0x50, 0xf5, 0xc5, 0x1d, 0x5f, 0xa8, 0xd, 0x70, 0x7e, 0x0, 0x7b, 0x52, 0x5b, 0x70, 0x67, 0x67, 0xdc, 0xe5, 0xcd, 0x1b, 0xaf, 0x6e, 0x27, 0x68, 0xda, 0xd0, 0xc6, 0xa8, 0x4f, 0xc2, 0x2f, 0x99, 0x5, 0x1d, 0x91, 0x34, 0x35, 0xf4, 0xeb, 0x1e, 0xb1, 0x9a, 0xd5, 0x44]
    x, y = Point.expand(from_bytes(point_data))
    assert (x, y) == (
        0x44d59ab11eebf43534911d05992fc24fa8c6d0da68276eaf1bcde5dc6767705b527b007e700da85f1dc5f550392cabca624bbdf91bb7L,
        0x6edb5b3e38bf271233378ac0fe3990289007928f56beb38a4f63843b9995afdd88a09c7da6935a4b43b0afde65a4ca9c159d72ed5275L
    )

@on_curve('DSTU_431')
def test_czo_pubkey(domain):
    point_data = [0xb6, 0x1b, 0xf9, 0xbd, 0x4b, 0x62, 0xca, 0xab, 0x2c, 0x39, 0x50, 0xf5, 0xc5, 0x1d, 0x5f, 0xa8, 0xd, 0x70, 0x7e, 0x0, 0x7b, 0x52, 0x5b, 0x70, 0x67, 0x67, 0xdc, 0xe5, 0xcd, 0x1b, 0xaf, 0x6e, 0x27, 0x68, 0xda, 0xd0, 0xc6, 0xa8, 0x4f, 0xc2, 0x2f, 0x99, 0x5, 0x1d, 0x91, 0x34, 0x35, 0xf4, 0xeb, 0x1e, 0xb1, 0x9a, 0xd5, 0x44]
    x, y = Point.expand(from_bytes(point_data))
    pub = Pubkey(Point(*Point.expand(from_bytes(point_data))))


    tbs = from_bytes([0xaa, 0x80, 0x7b, 0x32, 0x3c, 0x70, 0x3b, 0x64, 0x6d, 0xbd, 0x4a, 0xcc, 0xdc, 0x44, 0xc9, 0x52, 0x9f, 0xaa, 0x8d, 0x3b, 0x3, 0x1e, 0x33, 0xa4, 0xd1, 0x14, 0x1e, 0x96, 0xf8, 0x3d, 0x8, 0x72])

    sig = list([45, 198, 153, 197, 239, 40, 87, 174, 13, 80, 243, 49, 48, 124, 29, 230, 145, 170, 122, 18, 199, 123, 216, 238, 223, 165, 82, 21, 16, 69, 52, 178, 148, 99, 120, 54, 80, 164, 153, 23, 77, 202, 24, 20, 99, 63, 11, 87, 150, 21, 183, 48, 59, 0, 173, 9, 151, 47, 145, 159, 85, 45, 23, 158, 140, 146, 44, 113, 144, 229, 31, 133, 13, 110, 3, 137, 83, 188, 186, 193, 193, 55, 106, 133, 40, 119, 205, 157, 32, 250, 76, 189, 249, 91, 12, 249, 143, 106, 183, 217, 128, 215, 124, 17, 15, 207, 5, 22])
    r = from_bytes(sig[:54])
    s = from_bytes(sig[54:])

    assert pub.verify(value_hash=tbs, s=s, r=r)

@on_curve('DSTU_257')
def test_point_dbl(domain):
    point_Q = Point(PUB_X, PUB_Y)

    point_2Q = point_Q + point_Q
    assert point_2Q == Point(
        0x176dbde19773dfd335665597e8d6a0ab678721a5bb7030f25dc4c48b809ef3520,
        0x6e75301556ea5d571403086691030f024c026907c8e818b2eedd9184d12040ee
    )

@on_curve('DSTU_257')
def test_point_add(domain):
    point_Q = Point(PUB_X, PUB_Y)
    point_2Q = Point(
        0x176dbde19773dfd335665597e8d6a0ab678721a5bb7030f25dc4c48b809ef3520,
        0x6e75301556ea5d571403086691030f024c026907c8e818b2eedd9184d12040ee
    )
    point_3Q = point_Q + point_2Q
    assert point_3Q == Point(
        0x9a826cff814626da47bc409383d83922f65ec3e890e3b41a60e89f3a864c2766,
        0x1e465ea7610428ec6b0b56be039dd73f3fe18d7d7731d60a18ff9224caaf43b76
    )

@on_curve('DSTU_257')
def test_point_mul(domain):
    point_Q = Point(PUB_X, PUB_Y)
    point_MQ = point_Q * 0x2A45EAFE4CD469F811737780C57253360FBCC58E134C9A1FDCD10B0E4529A143
    assert point_MQ == Point(
        0x8c3d388b1c51116cf0ed041718309b360f775d8df86e9fc141822e79a3b0da8b,
        0xa8624188d9f4ab0afafbde6230cd8cf7c28b38f42fcbb4021ff0c0244a5ddbbd
    )

@on_curve('DSTU_257')
def test_compress(domain):
    pt = Point(0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB7,
               0x010686D41FF744D4449FCCF6D8EEA03102E6812C93A9D60B978B702CF156D814EF);

    compressed = pt.compress()
    assert compressed == 0x2A29EF207D0E9B6C55CD260B306C7E007AC491CA1B10C62334A9E8DCD8D20FB6


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
