Ecliptic Kurwa
==============

Partial, broken and unusable implementation of DSTU 4145-200.

![We](https://raw.githubusercontent.com/muromec/ukurwa4145/master/kdpv.jpg)

Usage
-----

Generate key and select curve to sign or verify data:

    ````
    from ukurwa4145 import curve, Priv

    with curve('DSTU_257') as cd:
        priv, pub = Priv.generate()

        s, r = priv.sign(value_hash=0xFEFEFEFEFEFDEADF0)
        pub.verify(value_hash=0xFEFEFEFEFEFDEADF0, s=s, r=r)

        pub.verify(value_hash=0xFEFEFEFEFEFDEADF0, s=123, r=123)

        # Exception:
        #    ukurwa4145.crypto.SignatureError: Signature does not match
    ````

DSTU 4145 spec: http://info-stand.com/downloads/dstu/dstu-4145-2002/dstu-4145-2002.pdf
