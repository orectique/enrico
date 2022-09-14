from io import BytesIO
import streamlit as st

from rake_nltk import Rake

import pyunsplash
import urllib.request

from io import BytesIO

from dotenv import load_dotenv

load_dotenv()

import os

from PIL import ImageDraw, Image, ImageFont, ImageFilter

from colorthief import ColorThief

from IPython.display import display

import textwrap

st.set_page_config(
    page_title= 'enrico.',
    page_icon = '🧔‍♂️',
    layout= 'centered'
)

def keywords(content):
    r = Rake()

    r.extract_keywords_from_text(content)

    strOut = ''
    keys = r.get_ranked_phrases()[:5]

    for key in keys:
        strOut += ', ' + key.lower()

    if 'goodnight' not in strOut:
        strOut += ', goodnight'
    
    return strOut

def imageProcess(query, content):
    pu = pyunsplash.PyUnsplash(api_key=os.getenv('U_KEY'))

    search = pu.search(type_='photos', page = 1, per_page = 1, query=query)

    for photo in search.entries:
        response = urllib.request.urlopen(photo.link_download)

    place = Image.open(BytesIO(response.read()))
    place.save('placeholder.jpg')

    ct = ColorThief('placeholder.jpg')

    colors = ct.get_palette(color_count=6)

    light = 0
    dark = float('inf')

    for i in colors:
        if sum(i) < dark:
            dark = sum(i)
            dark_color = i
        if sum(i) > light:
            light = sum(i)
            light_color = i

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
    font = ImageFont.truetype('./Assets/PlayfairDisplay-Italic-VariableFont_wght.ttf', 50)  

    wrapper = textwrap.TextWrapper(width=50) 
    word_list = wrapper.wrap(text=content) 
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]

    textWidth, _ = draw.textsize(caption_new, font = font)

    draw.text(xy = ((1500 - textWidth)/2, 1455), text = caption_new, font = font, fill = dark_color)

    return img

def enrico(content): 
    
    query = keywords(content)
    
    img = imageProcess(query, content)

    return img



st.title('enrico.')

filename = st.text_input('file you call what?', 'enricoImage')

content = st.text_area('what to say? ', value = "It's enough for me to be sure that you and I exist at this moment.", placeholder = "It's enough for me to be sure that you and I exist at this moment.", max_chars = 450)

if st.button('process'):
    #try:
    out = enrico(content)
    st.image(out)   
    buf = BytesIO()
    out.save(buf, format="PNG")
    byte_im = buf.getvalue()

    btn = st.download_button(
    label="Download Image",
    data=byte_im,
    file_name=f"{filename}.png",
    mime="image/jpeg",
    )
    st.success('success!')
    #except:
        #st.error('something went wrong. orectique was too lazy to implement error handling. sucks to be you.')