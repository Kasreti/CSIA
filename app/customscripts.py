from app.models import Lexicon, Phonology, VerbInflections, NounInflections
from sqlalchemy import func, desc
import re


def ipacreate(word):
    print("hi")
    word = word.replace(".", "")
    word = word.replace(",", "")
    for i in range(2):
        word = word.casefold()
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
            if (din >= 0):
                if (check[din] != '!'):
                    word = word.replace(di.romanized, di.ipa)
                    check = check.replace(di.romanized, '!!')
        for mo in mg:
            mon = word.find(mo.romanized)
            if (mon >= 0):
                if (check[mon] != '!'):
                    word = word.replace(mo.romanized, mo.ipa)
                    check = check.replace(di.romanized, '!')
        for index in range(0, len(word) - 1):
            if word[index] == word[index + 1]:
                word = word[:index + 1] + "ː" + word[index + 2:]
    return word


def concreate(word):
    for i in range(2):
        word = word.casefold()
        check = word.casefold()
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
            if (din >= 0):
                if (check[din] != '!'):
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
    renin = NounInflections.query.filter(NounInflections.irregular == 0).all()
    irnin = NounInflections.query.filter(NounInflections.irregular == 1).all()
    for iw, word in enumerate(sen):
        exist = False
        word = re.sub(r"[,.!?]", '', word)
        for sec in words:
            if sec.word.casefold() in word.casefold():
                exist = True
                trans[iw] = trans[iw].casefold().replace(sec.word.casefold(), sec.definition.replace(" ", "_"))
                word = word.casefold().replace(sec.word.casefold(), "")
                if sec.partofspeech == "Verb" and word != "":
                    for asp in revin:
                        if word.endswith(asp.fs):
                            word.replace(asp.fs, "!")
                            new = "-" + asp.gloss + ".1S"
                            trans[iw] = new.join(trans[iw].rsplit(asp.fs, 1))
                        elif word.endswith(asp.ss):
                            word.replace(asp.ss, "!")
                            new = "-" + asp.gloss + ".2S"
                            trans[iw] = new.join(trans[iw].rsplit(asp.ss, 1))
                        elif word.endswith(asp.other):
                            word.replace(asp.other, "!")
                            new = "-" + asp.gloss + ".NSP"
                            trans[iw] = new.join(trans[iw].rsplit(asp.other, 1))
                if sec.partofspeech == "Noun" and word != "":
                    for asp in renin:
                        if word.endswith(asp.NOM) and asp.number == "PL":
                            word.replace(asp.NOM, "!")
                            new = "-NOM." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.NOM, 1))
                        elif word.endswith(asp.ACC):
                            word.replace(asp.ACC, "!")
                            new = "-ACC." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.ACC, 1))
                        elif word.endswith(asp.GEN):
                            word.replace(asp.GEN, "!")
                            new = "-GEN." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.GEN, 1))
                        elif word.endswith(asp.DAT):
                            word.replace(asp.other, "!")
                            new = "-DAT." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.DAT, 1))
                        elif word.endswith(asp.OBL):
                            word.replace(asp.other, "!")
                            new = "-OBL." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.OBL, 1))
        for irr in irvin:
            if word.casefold() == irr.fs.casefold() and irr.fs != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "." + irr.gloss + ".1S"
                exist = True
            elif word.casefold() == irr.ss.casefold() and irr.ss != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "." + irr.gloss + ".2S"
                exist = True
            elif word.casefold() == irr.other.casefold() and irr.other != "":
                word = ""
                verb = irr.aspect.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == verb[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + "." + irr.gloss + ".NSP"
                exist = True
        for irr in irnin:
            if word.casefold() == irr.NOM.casefold() and irr.NOM != "":
                word = ""
                noun = irr.number.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == noun[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + ".NOM." + noun[1]
                exist = True
            elif word.casefold() == irr.ACC.casefold() and irr.ACC != "":
                word = ""
                noun = irr.number.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == noun[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + ".ACC." + noun[1]
                exist = True
            elif word.casefold() == irr.GEN.casefold() and irr.GEN != "":
                word = ""
                noun = irr.number.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == noun[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + ".GEN." + noun[1]
                exist = True
            elif word.casefold() == irr.DAT.casefold() and irr.DAT != "":
                word = ""
                noun = irr.number.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == noun[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + ".DAT." + noun[1]
                exist = True
            elif word.casefold() == irr.OBL.casefold() and irr.OBL != "":
                word = ""
                noun = irr.number.split(" ", 1)
                orig = Lexicon.query.filter(Lexicon.word == noun[0]).first()
                trans[iw] = orig.definition.replace(" ", "_") + ".OBL." + noun[1]
                exist = True
        if "-" in trans[iw]:
            tempx = trans[iw].split("-", 1)
            tempx[1] = tempx[1].upper()
            trans[iw] = tempx[0] + "-" + tempx[1]
        if not exist:
            trans[iw] = "*" + trans[iw]
    return " ".join(trans)

def repwrite(text):
    f = open("app/static/replacements.txt", "w")
    f.write(text)
    f.close()