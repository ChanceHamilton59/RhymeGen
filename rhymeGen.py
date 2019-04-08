from thesaurus import Word
import pandas as pd
import pronouncing
import nltk
from nltk.corpus import wordnet
nltk.download('cmudict')
import sys
def printf(format, *args):
    sys.stdout.write(format % args)
    
def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return list(rhymes)

def myRhym(word):
    pron = pronouncing.rhymes(word)
    if len(pron) == 0 :
        bupron = []
        i = 5
        while len(bupron) < 5:
            bupron = rhyme(word,i)
            if len(bupron) == 5 :
                burpon = rhyme(word,i-1)
                break
            i-=1
        if word in bupron: bupron.remove(word)    
        return burpon
    else :
        bupron = []
        i = 5
        while len(bupron) < 5:
            bupron = rhyme(word,i)
            if len(bupron) == 5 :
                burpon = rhyme(word,i-1)
                break
            i-=1
        for w in bupron :
            if w not in pron and w != word:
                pron.append(w)
        if word in bupron: bupron.remove(word)
        return pron
        
    
def rhymsyn(word1, word2):
    rhymers = myRhym(word1)
    needers = Word(word2).synonyms()
    poss = pd.DataFrame({'High': [],
                         'Med' : [],
                         'Low' : []})
    #print(needers)
    for words in rhymers :
        if words in needers :
            poss = poss.append({'High': words}, ignore_index=True) 
        try: 
            for syns1 in Word(words).synonyms() :
                if syns1 in needers :
                    poss = poss.append({'Med': words}, ignore_index=True)
                for syns2 in Word(syns1).synonyms() :
                    if syns2 in needers :
                            poss = poss.append({'Low': words}, ignore_index=True)
        except:
             stuff = False
    out = scrub(poss)
    printRhymes(out)
        
    return out

def rhymeGen(word1, word2):
    rhymers = myRhym(word1)
    needers = Word(word2).synonyms()
    poss = pd.DataFrame({'High': [],
                         'Med' : [],
                         'Low' : []})
    #print(needers)
    for words in rhymers :
        if words in needers :
            poss = poss.append({'High': words}, ignore_index=True) 
        try: 
            for syns1 in Word(words).synonyms() :
                if syns1 in needers :
                    poss = poss.append({'Med': words}, ignore_index=True)
                for syns2 in Word(syns1).synonyms() :
                    if syns2 in needers :
                            poss = poss.append({'Low': words}, ignore_index=True)
        except:
             stuff = False
    out = scrub(poss)
    printRhymes(out)
        
    return out
def printRhymes(ryms) :
    print("Low Lvl. Rhymes :")
    for words in ryms[0] :
        printf("\t %s \n", words)
    print(" ")
    print("--------------------------------------------------------------------")
    print("Med Lvl. Rhymes :")
    for words in ryms[1] :
        printf("\t %s \n", words)
    print(" ")
    print("--------------------------------------------------------------------")
    print("High Lvl. Rhymes :")
    for words in ryms[2] :
        printf("\t %s \n", words)
def scrub(k):
    k1 = list(set(k['Low']))
    k2 = list(set(k['Med']))
    k3 = list(set(k['High']))
    kL = []
    kM = []
    kH = []
    for word in k1 :
        if type(word) != float :
            kL.append(word)
    for word in k2 :
        if type(word) != float :
            kM.append(word)
    for word in k3 :
        if type(word) != float :
            kH.append(word)
    for word in kL :
        if word in kH or word in kM:
            kL.remove(word)
    for word in kM :
        if word in kH :
            kM.remove(word)
    return [kL, kM, kH]