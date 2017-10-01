try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from unidecode import unidecode
import re
from string import digits
import string

def ocr(image):
    text = unidecode(pytesseract.image_to_string(image))

    text = text.lower()
    text = text.replace("5", "s").replace("7", "t").replace("sm", "sta")

    #remove all numbers
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    words = text.split()

    cleanedwords = []
    l = len(words)
    marker = []

    def read_words(words_file):
        return [word for line in open(words_file, 'r') for word in line.split()]

    eng_dict = read_words('../tests/words/google-10000-english-no-swears.txt')

    for i in range(l):
        if i not in marker:
            if words[i] in eng_dict or i == l - 1:
                cleanedwords.append(words[i])
            else:
                if (words[i]+words[i+1]) in eng_dict:
                    cleanedwords.append(words[i]+words[i+1])
                    marker.append(i+1)
                else: cleanedwords.append(words[i])

    '''
    #code for US dictionary - very liberal with word inclusions
    
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

    text = cleanedwords

    if not text:
        return "UNABLE TO READ"
    else:
        return text

if __name__ == '__main__':
    image = Image.open('../tests/flowchart_images/two_boxes.png')

    text = ocr(image)
    print(text)