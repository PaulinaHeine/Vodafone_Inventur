
from Editing_pictures import canny
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'


img = cv2.imread('/Users/paulinaheine/s-l1600.jpg')
#img = cv2.imread('/Users/paulinaheine/IMG_3120.png')
img_canny = canny(img)
#plt.imshow(img)

images = [img,img_canny]
configs = [r'--oem 3 --psm 6',r'--psm 4', r"--psm 11 --oem 3"
]

def text_rec(images, configs):
    '''
    Bilder mit versch. Bearbeitungen werden mit versch. configurationen ausgelesen
    ,anschließendwird gefiltert, so dass keine Sonderzeichen und zu kurze Fragmente ausgegeben werden.
    '''
    res_set = set()

    for con in configs:
        for i in images:

            # Alle sinnvollen Einstellungen werden durchprobiert
            print("read")
            res_list = pytesseract.image_to_string(i, config=con)
            # Alle Einträge werden in einzelne snippets unterteilt
            print("split")
            res_list_2 = res_list.split("\n")
            # Alle leeren Einträge werden entfernt
            print("blanks")
            while '' in res_list_2:
                res_list_2.remove('')
            print("isalnum")
            for x in range(len(res_list_2)):
                res_set.add(''.join(filter(str.isalnum, res_list_2[x])))

    # Alle Einträge mit weniger als 3 Einträgen werden entferht
    print("charlimit")
    res_set = list(filter(lambda el: len(el) > 3, res_set))
    res_set = list(filter(lambda el: len(el) < 30, res_set))
    print("done")
    res_set = sorted(res_set)

    return res_set



