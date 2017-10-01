try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from unidecode import unidecode
from string import digits
import string
'''
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('../tests/words/google-10000-english-no-swears.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
'''
#reads a text file of words and returns a list of all the words
def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]

#takes an image and returns handwritten text within the image, if unable to read, returns "UNABLE TO READ"
def ocr(image):
    text = unidecode(pytesseract.image_to_string(image)) #takes out accents and strange characters and replaces them with the nearest option
    text = text.lower()
    text = text.replace("5", "s").replace("7", "t").replace("sm", "sta")

    #remove all numbers and punctuation
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    words = text.split()

    cleanedwords = []
    l = len(words)
    marker = []

    eng_dict = read_words('./tests/words/google-10000-english-no-swears.txt')

    for i in range(l):
        if i not in marker:
            if words[i] in eng_dict or i == l - 1: #if the word is in the dictionary or it is the last word in the string
                cleanedwords.append(words[i])
            else:
                if (words[i]+words[i+1]) in eng_dict: #if when concatenated with the subsequent word it forms a word
                    cleanedwords.append(words[i]+words[i+1])
                    marker.append(i+1) #update marker to skip the next iteration
                else: cleanedwords.append(words[i])

    '''
    #code using US dictionary - very liberal with word inclusions
    
    import enchant 
    
    d = enchant.Dict("en_US")
    
    for i in range(l):
        if i not in marker:
            if d.check(words[i]) is True or i == l - 1:
                cleanedwords.append(words[i])
            else:
                if d.check(words[i]+words[i+1]) is True:
                    cleanedwords.append(words[i]+words[i+1])
                    marker.append(i+1)
                else:
                    cleanedwords.append(words[i])
    '''

    if not cleanedwords:
        return "UNABLE TO READ"
    else:
        return cleanedwords
        '''
        if len(cleanedwords) == 1:
            if cleanedwords in eng_dict:
                return cleanedwords
            else:
                spellchecked = correction(cleanedwords)
            return spellchecked
            '''


if __name__ == '__main__':
    image = Image.open('../tests/flowchart_images/two_boxes.png')

    text = ocr(image)
    print(text)