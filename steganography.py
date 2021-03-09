from PIL import Image
import os

def recoverData(dataPixels):
  recoverD = []
  for i in range(len(dataPixels)):
    for j in range(len(dataPixels[i])):
      if i%3 == 2 and j%3 == 2:
        continue
      recoverD.append(dataPixels[i][j]%2)
  return recoverD

def recoverPixels(pixelMap, x, y):
  dataPixels = []
  p = 0
  for i in range(x):
    for j in range(y):
      if p%3 == 2:
        if pixelMap[i, j][2]%2 == 0:
          dataPixels.append(pixelMap[i, j])
          return dataPixels
      dataPixels.append(pixelMap[i, j])
      p+=1

def decode(recoveredData):
  recoveredData = [ str(x) for x in recoveredData ]
  #print(len(recoveredData))
  recoveredData = '0b'+ ''.join(recoveredData)
  #print(recoveredData)
  origData = int(recoveredData, 2)
  data = origData.to_bytes((origData.bit_length() + 7) // 8, 'big').decode(errors="ignore")
  return data

# Convert encoding data into 8-bit binary 
# form using ASCII value of characters 
def genData(data): 
  newd = []
  for i in data: 
      newd.append(format(ord(i), '08b')) 
  return newd

def embed(pixelMap, pixels, pixReq, x, y):
  p = 0
  for i in range(x):
    for j in range(y):
      if p < pixReq:
        pixelMap[i, j] = pixels[p]
        p+=1

def changePixels(pixels, byteData, n, l):
  for i in range(8):
    x, y = int(i/3), int(i%3)
    if byteData[i] == '0' and pixels[x][y]%2 != 0:
      pixels[x][y] = abs(pixels[x][y] - 1)
    elif byteData[i] == '1' and pixels[x][y]%2 == 0:
      pixels[x][y] = abs(pixels[x][y] - 1)
  i+=1
  x, y = int(i/3), int(i%3)
  if n == l-1:
    if pixels[x][y]%2 != 0:
      pixels[x][y] = abs(pixels[x][y] - 1)
  else:
    if pixels[x][y]%2 == 0:
      pixels[x][y] = abs(pixels[x][y] - 1)

def hide(byteData, pixels, dataLen):
  pixels = [list(x) for x in pixels]

  for i in range(dataLen):
    x = i*3
    y = x+3
    #print(byteData[i])
    changePixels(pixels[x:y], byteData[i], i, dataLen)

  pixels = [tuple(x) for x in pixels]
  return pixels

def getPixels(pixelMap, pixReq, x, y):
  pixels = []
  p = 0
  for i in range(x):
    for j in range(y):
      if p < pixReq:
        pixels.append(pixelMap[i, j])
        p+=1
  return pixels

def main():
  imgLoc = input("Enter image file location: ")
  try:
    img = Image.open(imgLoc)
  except:
    print("Error in opening file")
    return
  x,y = img.size
  pixelMap = img.load()
  print("Options : 1.Encode   2.Decode")
  n = int(input("Enter option: "))
  if n == 1:
    imgDest = input("Enter image destination location: ")
    data = input("Enter data: ").replace('"',"'")
    no_pixels = x*y
    #get bytedata for encoding
    byteData = genData(data)
    dataLen = len(byteData)
    pixReq = dataLen*3
    #check for pixels
    if pixReq > no_pixels:
      print("Data too large to fit")
      print("Either change the image or reduce data")
      return
    #get pixels for embeding
    pixels = getPixels(pixelMap, pixReq, x, y)
    #embed bytedata into pixels
    pixels = hide(byteData, pixels, dataLen)
    #embed pixels back into image
    embed(pixelMap, pixels, pixReq, x, y)
    #save the embedded image
    #file = imgDest + os.path.basename(img.filename).split('.')[0] + '-stegno.png'
    file = imgDest + 'stegno.png'
    img.save(file)
    print("File saved at {} !!".format(file))
  elif n == 2:
    #get encoded pixels
    dataPixels =  recoverPixels(pixelMap, x, y)
    #get databits from datapixels
    recoveredData = recoverData(dataPixels)
    #decode data into plain text
    data = decode(recoveredData)
    if len(data) < 1:
      print("Its a plain image!!")
    else:
      print("Embedded data: " + data)
  else:
    print("Error: Invalid option selected")

main()