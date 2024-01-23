from app.models import Lexicon, Phonology, VerbInflections, NounInflections
from sqlalchemy import func, desc
import re


def ipacreate(word):
    # Punctuation is removed from the string
    word = word.replace(".", "")
    word = word.replace(",", "")
    # The process is repeated twice, in case any un-transcribed characters remain.
    for i in range(2):
        # The whole word is converted into lowercase, as that is what the database uses.
        word = word.casefold()
        # An empty array is created to store all the phonemes that are used in the language
        # and its conscript equivalent.
        phonemes = []
        exists = Phonology.query.filter(Phonology.exists == True).all()
        for phoneme in exists:
            phonemes.append(phoneme)
        # It is sorted using a selection sort from longest to shortest string.
        phonemes = ipalengthsort(phonemes)
        # Now that the array has been sorted, substrings will be replaced with its IPA equivalents.
        for phoneme in phonemes:
            word = word.replace(phoneme.romanized, phoneme.ipa)
        # In IPA notation, long (or geminated) sounds are expressed with the ː symbol. For instance,
        # /nn/ would instead be /nː/. Here, the loop finds two identical characters in a row,
        # and replaces the latter with ː.
        for index in range(0, len(word) - 1):
            if word[index] == word[index + 1]:
                word = word[:index + 1] + "ː" + word[index + 2:]
    return word


def concreate(word):
    # The saved custom replacements are loaded from the .txt file...
    reptxt = open("app/static/replacements.txt", "r", encoding="utf-8")
    # ...and are saved to a variable.
    rep = reptxt.read()
    reptxt.close()
    # The blank line between every entry is removed.
    customreps = rep.split("\n")
    # When saving to a .txt, single new lines erroneously get saved as double new
    # lines. This removes any objects which are only composed of whitespace.
    customreps[:] = [x for x in customreps if x.strip()]
    for rep in customreps:
        # Every replacement is saved in the format romanization,transcription (separated by a comma).
        # The string is split into two around the comma, and what comes before the comma is replaced by
        # what comes after.
        subs = rep.split(",")
        word = word.replace(subs[0],subs[1])
    for i in range(2):
        word = word.casefold()
        phonemes = []
        exists = Phonology.query.filter(Phonology.exists == True).all()
        for phoneme in exists:
            phonemes.append(phoneme)
        phonemes = conlengthsort(phonemes)
        for phoneme in phonemes:
            word = word.replace(phoneme.romanized, phoneme.conscript)
        for index in range(0, len(word) - 1):
            if word[index] == word[index + 1]:
                word = word[:index + 1] + "ː" + word[index + 2:]
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
    # Every word from the dictionary is put into an array,
    # ordered from longest to shortest word length.
    words = Lexicon.query.order_by(desc(func.length(Lexicon.word))).all()
    # The sentence is split into an array, separated at each space.
    sen = sen.split(" ")
    # A parallel array is used to store the resulting gloss.
    trans = sen.copy()
    # All regular and irregular inflections are loaded.
    revin = VerbInflections.query.filter(VerbInflections.irregular == 0).all()
    irvin = VerbInflections.query.filter(VerbInflections.irregular == 1).all()
    renin = NounInflections.query.filter(NounInflections.irregular == 0).all()
    irnin = NounInflections.query.filter(NounInflections.irregular == 1).all()
    # Looping through every word in the sentence (iw finds the index of the
    # word within the array)
    for iw, word in enumerate(sen):
        # This boolean assumes that the word doesn't exist.
        exist = False
        # All punctuation is removed from the word.
        word = re.sub(r"[,.!?]", '', word)
        # Now, the current word in the sentence is compared against every word in the dictionary.
        for sec in words:
            # The word is made to be all lowercase when comparing to prevent any issues.
            if sec.word.casefold() in word.casefold():
                # If it exists, the boolean will become true.
                exist = True
                # As per glossing conventions, spaces are replaced with underscores.
                # The word is replaced with its definition.
                trans[iw] = trans[iw].casefold().replace(sec.word.casefold(), sec.definition.replace(" ", "_"))
                # Here, the word is tested to see if it ends in a regular conjugation suffix. If so, the
                # corresponding notation is appended to the gloss.
                if sec.partofspeech == "Verb" and word != "":
                    for asp in revin:
                        if word.endswith(asp.fs):
                            new = "-" + asp.gloss + ".1S"
                            trans[iw] = new.join(trans[iw].rsplit(asp.fs, 1))
                        elif word.endswith(asp.ss):
                            new = "-" + asp.gloss + ".2S"
                            trans[iw] = new.join(trans[iw].rsplit(asp.ss, 1))
                        elif word.endswith(asp.other):
                            new = "-" + asp.gloss + ".NSP"
                            trans[iw] = new.join(trans[iw].rsplit(asp.other, 1))
                if sec.partofspeech == "Noun" and word != "":
                    for asp in renin:
                        if word.endswith(asp.NOM) and asp.number == "PL":
                            new = "-NOM." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.NOM, 1))
                        elif word.endswith(asp.ACC):
                            new = "-ACC." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.ACC, 1))
                        elif word.endswith(asp.GEN):
                            new = "-GEN." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.GEN, 1))
                        elif word.endswith(asp.DAT):
                            new = "-DAT." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.DAT, 1))
                        elif word.endswith(asp.OBL):
                            new = "-OBL." + asp.number
                            trans[iw] = new.join(trans[iw].rsplit(asp.OBL, 1))
        # The same process of comparing the word being glossed is repeated, but this time
        # against the list of irregular inflections, which are not included in the Lexicon database.
        for irr in irvin:
            if word.casefold() == irr.fs.casefold() and irr.fs != "":
                word = ""
                # The string is split, only keeping the first portion of the aspect column,
                # which has the word needed. Irregular conjugations are saved in the format
                # "word aspect".
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
        # During the lowercase comparison process, it may end up turning gloss notation,
        # which should be in uppercase to lowercase. This script takes any suffixes, identifiable
        # by the hyphen that separates it from the definition, and capitalizes anything after.
        if "-" in trans[iw]:
            tempx = trans[iw].split("-", 1)
            tempx[1] = tempx[1].upper()
            trans[iw] = tempx[0] + "-" + tempx[1]
        # If exist is still not true (a match has not been found) after comparing against every single
        # word, it is simply left untranslated with an asterisk prefixed to it.
        if not exist:
            trans[iw] = "*" + trans[iw]
    return " ".join(trans)


def ipalengthsort(array):
    size = len(array)
    for ind in range(size):
        min_index = ind
        for i in range(ind + 1, size):
            if len(array[i].romanized) > len(array[min_index].romanized):
                min_index = i
        (array[ind], array[min_index]) = (array[min_index], array[ind])
    print(array)
    return array


def conlengthsort(array):
    size = len(array)
    for ind in range(size):
        min_index = ind
        for i in range(ind + 1, size):
            if len(array[i].romanized) > len(array[min_index].romanized):
                min_index = i
        (array[ind], array[min_index]) = (array[min_index], array[ind])
    print(array)
    return array
