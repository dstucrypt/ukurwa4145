from ukurwa4145 import curve, Point, Priv, Pubkey, on_curve, Field

@on_curve('DSTU_163')
def test_zz(domain):
    dA  =  0x00000304991F9AC1A8094F6FBFA009250D4A8099320D55
    QAx = 0x3001C56A32991307626D09B5FF069C6CB80B794D39BD
    QAy = 0x0001B9858C28B9BCDCA17BA35E6D5F034B23AA7433C7
    dB = 0x0001FC8617116074A8FF81B42F85CA2516CF11CE2E13
    QBx = 0x0001F336B1E8024BE4ABE92D26CA7F30220E1650BC1A
    QBy = 0x0002F8757B1E7E72E3E546B2604177463D3FC3BE63C9
    
    expectZZ = 0x07F84ADBA62457C5DA5D959447C4F6C1864C9B288E

    pointQA = Point(QAx, QAy, raw=True)
    pointQA.x.v = Field.truncate(QAx)
    pointQB = Point(QBx, QBy)
    privA = Priv(dA)
    privB = Priv(dB)
    pubA = privA.pub()
    pubB = privB.pub()

    assert pointQA == pubA.point
    assert pointQB == pubB.point

    h = domain.COFACTOR
    KA = pointQB * dA * h
    KB = pointQA * dB * h
    ZZ = KA.x.v

    assert KA == KB
    assert ZZ == expectZZ


@on_curve('DSTU_431')
def test_zz_431(domain):
    dA = 0x4B3A1707F870D0C1D4CE438E88AA2B361506916286F36FF35F9CBE9C0FBDBE1F776BB5C25878BAE1C54958D1B039B12FF547E00863
    QAx = 0x1221632E63D90AEB4DB431B99DE5A87B7418023DD712B501156414A0F84C0741B1278765E63EA714B3D4B68EA6A1045308B679AD9669
    QAy = 0x403D64C6F51562B700ACCD27ABCA662F8797744E112168015E0A143AD029627A1378EBBA934870D1641216A48A3F1017FA221149F683
    dB = 0x06FE211C555CB9D3A27B7EC2E2FFBB4CB167EE86BB7F111E7BCD8F6564E8835B09E047B9286FBA7F83507879BFEE4C33ECBA41C5DAB5
    QBx = 0x50B07373CFEE5B3F7C287099E3B306AEB1690C7E66926DC502D188D881FC17DC75AFD6CE2B1E9CED7C16FFD329CF411A4B0ABC9853F5
    QBy = 0x569FF592E58A9A4FC8EF7EB997A1AAAC46105D9032F789D77C6B3F7C7BAED2BEF4C2AE1042E2B25A98AD00749A436391CC98F27C435A
    expectZZ = 0x4BCA28D648A50DEEF85F8A34735BAE5C1AFEA72D3515E16639E5F166DD0A47EDE333EA5AB3415DBC4FDBB7B68BE249FF3C5B75F82B55

    pointQA = Point(QAx, QAy)
    pointQB = Point(QBx, QBy)
    privA = Priv(dA)
    privB = Priv(dB)
    pubA = privA.pub()
    pubB = privB.pub()
    assert pointQA == pubA.point
    assert pointQB == pubB.point


    h = domain.COFACTOR
    KA = pointQB * dA * h
    KB = pointQA * dB * h
    ZZ = KA.x.v

    assert KA == KB
    assert ZZ == expectZZ

