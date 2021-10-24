import cv2

def write_key(key):
  file = open('key.txt','w')
  file.write(key)
  file.close()

def check_spell():
  file = open('key.txt','r')
  return (file.read())

def binarize(message):
  for c in message:
    yield ord(c)

def get_image(image_location):
  img = cv2.imread(image_location)
  return img

def encode(image_location, message, key):
  write_key(key)
  
  img = get_image(image_location)
  msg = binarize(message)
  
  pattern = 8
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i+1 * j+1) % pattern == 0:
        try:
          img[i-1][j-1][0] = next(msg)
        except StopIteration:
          img[i-1][j-1][0] = 0
          return img

def decode(img_loc,password):
  key = check_spell()
  img = get_image(img_loc)

  if password != key:
    print ("Wrong Password")
    return
  
  pattern = 8
  message = ''
  for i in range(len(img)):
    for j in range(len(img[0])):
      if (i-1 * j-1) % pattern == 0:
        if img[i-1][j-1][0] != 0:
          message = message + chr(img[i-1][j-1][0])
        else:
          return message

img = encode('crypto.png','I am a secret message','A long long time ago')
cv2.imwrite('encrypted.png', img)
message = decode('encrypted.png','A long long time ago')
print ("Message from encrypted:")
print (message)

original = cv2.imread('crypto.png')
modified = cv2.imread('encrypted.png')

grayModified = cv2.cvtColor(modified, cv2.COLOR_RGB2GRAY)

cv2.imwrite('grayMod.png', grayModified)

cv2.imshow("Original", original)
cv2.imshow("Modified", modified)
cv2.imshow ("Gray Modified", grayModified)

grayMessage = decode('grayMod.png', 'A long long time ago')
print ("Message from gray encrypted:")
print (grayMessage)

cv2.waitKey(0)
