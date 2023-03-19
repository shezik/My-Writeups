from PIL import Image
import os
import subprocess
import base64

imageFilename = 'response.png'

if os.path.exists(imageFilename):
    os.remove(imageFilename)

subproc = subprocess.Popen('curl -X POST --form "f=@myPNG.png" 127.0.0.1:24042/print --output response.png', shell=True)
subproc.wait()


imageFile = Image.open(imageFilename)
imageMap = imageFile.load()

bitStringList = list()

for x in range(50, 1150 + 1, 20):  # Drop trailing eight FFs
    bitString = ''

    for y in range(50, 190 + 1, 20):
        if imageMap[x, y] != (255, 255, 255):
            bitString += '1'
        else:
            bitString += '0'

    bitStringList.append(bitString)


snIndex = 23
snList = bitStringList[snIndex : -1]  # Drop '\n'
snByteArray = bytearray()

for i in snList:
    snByteArray.append(int(i, 2))

encodedSN = base64.b64encode(bytearray(snByteArray)).decode('utf-8')

subproc = subprocess.Popen('curl -X POST --data "sn={}" 127.0.0.1:24042/serial-number'.format(encodedSN), shell=True)
subproc.wait()
