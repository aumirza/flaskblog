from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask import send_file
import os

def draw_placeholder_image(size,bgcolor,color,text):

    if 'x' in size:
        size = size.split('x', 2)
        img_height = int(size[0])
        img_width = int(size[1])
    else:
        img_height = img_width = int(size)

    if text is None:
        text = str(img_height) +'X'+ str(img_width)
    
    text_size = 50
    text_lines = [(text, './static/OpenSans-Regular.ttf',text_size)]

    img_color = hex_to_rgb(bgcolor)
    text_color = hex_to_rgb(color)

    img = Image.new('RGB', (img_height, img_width), color =img_color)
    d = ImageDraw.Draw(img)

    text_layouts = layout_text( img_height, img_width,  0, text_lines)

    for text_layout in text_layouts:
        text, font, pos = text_layout
        d.text(pos, text, fill=text_color, font=font)
    del d

    return serve_pil(img)

def serve_pil(pil_img):
    file = BytesIO()
    pil_img.save(file, 'png')
    file.name = 'image.png'
    file.seek(0)
    return send_file(file, mimetype='image/png')

def hex_to_rgb(hex):
    hex = hex.lstrip('#') if '#' in hex else hex
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def layout_text(canvas_height, canvas_width,  line_spacing, list_of_texts=[]):
  '''
  This method is most likely _not_ optimized. I certainly welcome any refactoring that
  will either make it faster or do it better
  given canvas_width, canvas_height, line_spacing, [(text1, ttf1, max_point1), (text2, ttf2, max_point2), ...]
  return [(font1, pos1), (font2, pos2), ...]
  '''
  target_reduction = 0.8 # the amount to reduce by if the text is too large


  if len(list_of_texts):
    ratios = []
    text_heights = []
    text_widths = []
    fonts = []
    text_sizes = []
    for text_attr in list_of_texts:
      text, ttf, max_point = text_attr
      font = ImageFont.truetype(ttf, max_point)
      fonts += [font]
      text_size = font.getsize(text)
      width, height = text_size
      text_sizes += [tuple(text_size)]
      
      #pdb.set_trace()

      text_heights += [float(height)]
      text_widths += [float(width)]

    total_text_height = sum(text_heights)
    max_text_width = max(text_widths)

    ratios = [h/total_text_height for h in text_heights]


    # the height needs to be reduced because it won't fit in the current canvas
    if (total_text_height * ((1-target_reduction)+1) ) > canvas_height:
      target_height = canvas_height * target_reduction
      total_reduction = target_height / total_text_height # this is what the point size needs to be reduced by
      text_heights = []
      fonts = []
      text_sizes = []
      
      for idx, text_attr in enumerate(list_of_texts):
        text, ttf, max_point = text_attr
        new_font = ImageFont.truetype(ttf, int( total_reduction * max_point) )
        fonts += [new_font]
        text_size = new_font.getsize(text)
        width, height = text_size
        text_sizes += [text_size]
        text_heights += [height]

    # the width needs to be reduced because it won't fit in the current canvas
    if (max_text_width * ((1-target_reduction)+1) ) > canvas_width:
      target_width = canvas_width * target_reduction
      total_reduction = target_width / max_text_width # this is what the point size needs to be reduced by
      text_heights = []
      fonts = []
      text_sizes = []
      
      for idx, text_attr in enumerate(list_of_texts):
        text, ttf, max_point = text_attr
        new_font = ImageFont.truetype(ttf, int( total_reduction * max_point) )
        fonts += [new_font]
        text_size = new_font.getsize(text)
        width, height = text_size
        text_sizes += [text_size]
        text_heights += [height]


    total_text_height = sum(text_heights)

    first_top = (canvas_height - total_text_height)/2

    layouts = []
    top = 0
    for idx, text_attr in enumerate(list_of_texts):
      if idx == 0:
        top = first_top
      layouts += [(text_attr[0], fonts[idx], ( ( (canvas_width/2) - (text_sizes[idx][0]/2) ), top) )]
      top += text_heights[idx]

    return layouts

  else:
    return []