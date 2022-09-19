from io import BytesIO
import streamlit as st

from rake_nltk import Rake

import pyunsplash
import urllib.request

from io import BytesIO

from dotenv import load_dotenv

load_dotenv()

import os

from PIL import ImageDraw, Image, ImageFont

from colorsys import rgb_to_hsv, hsv_to_rgb

from colorthief import ColorThief

import textwrap

st.set_page_config(
    page_title= 'enrico.',
    page_icon = '🧔‍♂️',
    layout= 'wide'
)

columns = st.columns(4)

def complementary(r, g, b):
   hsv = rgb_to_hsv(r, g, b)
   return hsv_to_rgb((hsv[0] + 0.5) % 1, hsv[1], hsv[2])

def keywords():
    r = Rake()

    r.extract_keywords_from_text(content)

    strOut = ''
    keys = r.get_ranked_phrases()[:5]

    for key in keys:
        strOut += ', ' + key.lower()

    if keyword not in strOut:
        strOut += ', ' + keyword.lower()
    
    return strOut

def imageGet(query):
    pu = pyunsplash.PyUnsplash(api_key=os.getenv('U_KEY'))

    search = pu.search(type_='photos', page = 1, per_page = 4, query=query)

    i = 0

    for photo in search.entries:
        response = urllib.request.urlopen(photo.link_download)
        imageProcess(response, i)
        i += 1

    st.success('Images Generated')

    return

def imageProcess(response, colIndex):
    place = Image.open(BytesIO(response.read()))
    place.save('placeholder.jpg')

    ct = ColorThief('placeholder.jpg')

    colors = ct.get_palette(color_count=6)

    light = 0
    dark = 769

    for i in colors:
        if sum(i) > light:
            light = sum(i)
            light_color = i
        if sum(i) < dark:
            dark = sum(i)
            dark_color = i

    os.remove('placeholder.jpg')

    img = Image.new('RGB', (1500, 2100), color = light_color)

    b, h = place.size
    h = int(1400*h/b)

    place = place.resize((1400, h))

    if h >= 1355:
        place = place.crop((0, 0, 1400, 1355))
    else:
        b, h = place.size
        b = int(1355*b/h)
        place = place.resize((b, 1355))

        s = (b - 1400)/2

        place = place.crop((s, 0, b - s, 1355))

    img.paste(place, (50, 50))

    draw = ImageDraw.Draw(img)

    font2 = ImageFont.truetype('./Assets/PlayfairDisplay-Italic-VariableFont_wght.ttf', 50) 
    font1 = ImageFont.truetype('./Assets/PlayfairDisplay-Italic-VariableFont_wght.ttf', 100) 

    wrapper = textwrap.TextWrapper(width=50) 
    word_list = wrapper.wrap(text=content) 
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]

    textWidth, _ = draw.textsize(caption_new, font = font2)
    capWidth, _ = draw.textsize(keyword, font = font1)

    draw.text(xy = ((1500 - textWidth)/2, 1540), text = caption_new, font = font2, fill = dark_color)
    draw.text(xy = ((1500 - capWidth)/2, 1405), text = keyword, font = font1, fill = dark_color)
    
    with columns[colIndex]:
        st.image(img, use_column_width=True)
    return 
    
st.title('enrico.')

filename = st.text_input('file you call what?', 'enricoImage')

keyword = st.text_input('keyword is what?', 'goodnight')

content = st.text_area('what to say? ', value = "It's enough for me to be sure that you and I exist at this moment.", placeholder = "It's enough for me to be sure that you and I exist at this moment.", max_chars = 350)
buf = BytesIO()


if st.button('process'):
    #try:
    imageGet(keywords()) 

    #except:
        #st.error('something went wrong. orectique was too lazy to implement error handling. sucks to be you.')