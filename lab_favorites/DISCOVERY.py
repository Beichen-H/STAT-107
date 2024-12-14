import pandas as pd
from PIL import Image

def df_image(fileName):
  data = loadImage(fileName)
  return createImageDataFrame(data)

def loadImage(fileName, resize=False, format="RGB"):
  # Open the image using the PIL library
  image = Image.open(fileName)

  # Convert it to an (x, y) array:
  return imageToArray(image, format, resize)


# Resize the image to an `outputSize` x `outputSize` square, where `outputSize` is defined (globally) above.
def squareAndResizeImage(image, resize):
  import PIL

  w, h = image.size
  d = min(w, h)
  image = image.crop( (0, 0, d, d) ).resize( (resize, resize), resample=PIL.Image.LANCZOS )
  
  return image


# https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python
def rgb2lab(inputColor):
  num = 0
  RGB = [0, 0, 0]

  for value in inputColor:
    value = float(value) / 255

    if value > 0.04045:
      value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
    else :
      value = value / 12.92

    RGB[num] = value * 100
    num = num + 1

  XYZ = [0, 0, 0]

  X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
  Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
  Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
  XYZ[ 0 ] = round( X, 4 )
  XYZ[ 1 ] = round( Y, 4 )
  XYZ[ 2 ] = round( Z, 4 )

  XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
  XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
  XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

  num = 0
  for value in XYZ:
    if value > 0.008856:
      value = value ** ( 0.3333333333333333 )
    else:
      value = ( 7.787 * value ) + ( 16 / 116 )

    XYZ[num] = value
    num = num + 1

  Lab = [0, 0, 0]

  L = ( 116 * XYZ[ 1 ] ) - 16
  a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
  b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

  Lab [ 0 ] = round( L, 4 )
  Lab [ 1 ] = round( a, 4 )
  Lab [ 2 ] = round( b, 4 )

  return Lab


# Convert (and resize) an Image to an Lab array
def imageToArray(image, format, resize):
  import numpy as np

  w, h = image.size
  if resize:
    image = squareAndResizeImage(image, resize)

  image = image.convert('RGB')
  rgb = np.array(image)
  if format == "RGB":
    rgb = rgb.astype(int)
    return rgb.transpose([1,0,2])
  elif format == "Lab":
    lab = rgb.astype(float)
    for i in range(len(rgb)):
      for j in range(len(rgb[i])):
        lab[i][j] = rgb2lab(lab[i][j])
    return lab.transpose([1,0,2])
  else:
    raise Exception(f"Unknown format {format}")



def createImageDataFrame(img):
  data = []
  width = len(img)
  height = len(img[0])

  for x in range(width):
    for y in range(height):
      pixel = img[x][y]
      r = pixel[0]
      g = pixel[1]
      b = pixel[2]

      d = {"x": x, "y": y, "r": r, "g": g, "b": b}
      data.append(d)  

  return pd.DataFrame(data)