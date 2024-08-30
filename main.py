import easyocr
import os



def img2number(image):
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(image, allowlist='0123456789')
    for (x, y, z) in result:
        print(y)
        
        
directory = os.fsencode('img')
for file in os.listdir('img'):
    print(file)
    img2number(f"img/{file}")
    
