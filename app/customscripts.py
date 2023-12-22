from app.models import Lexicon, Phonology
def ipacreate(word):
    check = word
    dg = []
    mg = []
    exists = Phonology.query.filter(Phonology.exists == True).all()
    for phoneme in exists:
        if len(phoneme.romanized) == 2:
            dg.append(phoneme)
        else:
            mg.append(phoneme)
    for di in dg:
        din = word.find(di.romanized)
        if(din >= 0):
            if(check[din] != '!'):
                word = word.replace(di.romanized, di.ipa)
                check = check.replace(di.romanized, '!!')
    for mo in mg:
        mon = word.find(mo.romanized)
        if (mon >= 0):
            if (check[mon] != '!'):
                word = word.replace(mo.romanized, mo.ipa)
                check = check.replace(di.romanized, '!')
    return word

def concreate(word):
    check = word
    ow = word
    dg = []
    mg = []
    exists = Phonology.query.filter(Phonology.exists == True).all()
    for phoneme in exists:
        if len(phoneme.romanized) == 2:
            dg.append(phoneme)
        else:
            mg.append(phoneme)
    for di in dg:
        din = ow.find(di.romanized)
        if(din >= 0):
            if(check[din] != '!'):
                word = word.replace(di.romanized, di.conscript)
                check = check.replace(di.romanized, '!!')
    for mo in mg:
        mon = ow.find(mo.romanized)
        if (mon >= 0):
            if (check[mon] != '!'):
                word = word.replace(mo.romanized, mo.conscript)
                check = check.replace(mo.romanized, '!')
    return word

def midcheck(c, w, o):
    str = ""
    for x in c:
        str = str + x
    print(str)
    str2 = ""
    for x in w:
        str2 = str2 + x
    print(str2)
    str3 = ""
    for x in o:
        str3 = str3 + x
    print(str3)