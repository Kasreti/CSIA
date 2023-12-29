from app.models import Lexicon, Phonology, VerbInflections
from sqlalchemy import func, desc
import re
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
    for index in range(0, len(word)-1):
        if word[index] == word[index+1]:
            word = word[:index+1] + "ː" + word[index + 2:]
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
    return

def gloss(sen):
    words = Lexicon.query.order_by(desc(func.length(Lexicon.word))).all()
    sen = sen.split(" ")
    trans = sen.copy()
    revin = VerbInflections.query.filter(VerbInflections.irregular == 0).all()
    irvin = VerbInflections.query.filter(VerbInflections.irregular == 1).all()
    for iw, word in enumerate(sen):
        for sec in words:
            if sec.word.casefold() in word.casefold():
                word = re.sub(sec.word, "", word, re.IGNORECASE)
                trans[iw] = re.sub(sec.word, sec.definition.replace(" ", "_"), trans[iw], re.IGNORECASE)
                if sec.partofspeech == "Verb" and word != "":
                    for asp in revin:
                        if word.find(asp.fs) != 1:
                            word.replace(asp.fs, "!")
                            trans[iw] = trans[iw].replace(asp.fs, "-" + asp.gloss + ".1S")
                        elif word.find(asp.ss) != 1:
                            word.replace(asp.ss, "!")
                            trans[iw] = trans[iw].replace(asp.ss, "-" + asp.gloss + ".2S")
                        elif word.find(asp.other) != 1:
                            word.replace(asp.other, "!")
                            trans[iw] = trans[iw].replace(asp.other, "-" + asp.gloss + ".NSP")
        for irr in irvin:
            if word.casefold() == irr.fs.casefold() and irr.fs != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "-" + irr.gloss + ".1S"
            elif word.casefold() == irr.ss.casefold() and irr.ss != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "-" + irr.gloss + ".2S"
            elif word.casefold() == irr.other.casefold() and irr.other != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "-" + irr.gloss + ".NSP"
    return " ".join(trans)