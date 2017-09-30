try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from unidecode import unidecode
import enchant
import re

#text = unidecode(pytesseract.image_to_string(Image.open('../tests/text_imgs/2.png')))

text = unidecode("Sta rt my Fl ow Cha rt") #test string

text = re.sub("(^|\W)\d+($|\W)", " ", text) #removes numbers from the string

d = enchant.Dict("en_US")

words = text.split()

cleanedwords = []
l = len(words)
marker = []

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
    else:
        break

print(cleanedwords)