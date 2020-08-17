
#Logan
#Pillow, SciPy, Tikinter, S-Lang
#image = "C:\\Users\\Code\\Desktop\\7qrh3donqsd51.png"
image = "C:\\Users\\Code\\Desktop\\Untitled.png"

width = ''
height = ''
bitDepth = ''
colorType = ''
compressionMethod = ''
filterMethod = ''
interlaceMethod = ''

sRGBrenderingIntent = ''

gamma = ''

pixelsPerUnitX = ''
pixelsPerUnitY = ''
unitSpecifier = ''

imageData = b''

readingFile = None

def IHDR(chunkData):
    global width
    global height
    global bitDepth
    global colorType
    global compressionMethod
    global filterMethod
    global interlaceMethod
    width = chunkData[0|3]
    height = chunkData[4|7]
    bitDepth = chunkData[8]
    colorType = chunkData[9]
    compressionMethod = chunkData[10]
    filterMethod = chunkData[11]
    interlaceMethod = chunkData[12]

def sRGB(chunkData):
    global sRGBrenderingIntent
    sRGBrenderingIntent = int.from_bytes(chunkData,byteorder='big')

def gAMA(chunkData):
    global gamma
    gamma = int.from_bytes(chunkData,byteorder='big')

def pHYs(chunkData):
    global pixelsPerUnitX
    global pixelsPerUnitY
    global unitSpecifier
    pixelsPerUnitX = chunkData[0|3]
    pixelsPerUnitY = chunkData[4|7]
    unitSpecifier = chunkData[8]

def IDAT(chunkData):
    global imageData
    imageData += chunkData

def IEND(chunkData):
    file.close()
    global readingFile
    readingFile = False

def chunkRead(file):
    dataLen = int.from_bytes(file.read(4),byteorder='big')
    chunkRead.chunkType = file.read(1)+file.read(1)+file.read(1)+file.read(1)
    chunkRead.chunkData = file.read(dataLen)
    chunkRead.chunkCRC = int.from_bytes(file.read(4),byteorder='big')

def chunkDiscriminator(chunkType,chunkData):
    if chunkType == b'IHDR':
        IHDR(chunkData)
    if chunkType == b'sRGB':
        sRGB(chunkData)
    if chunkType == b'gAMA':
        gAMA(chunkData)
    if chunkType == b'pHYs':
        pHYs(chunkData)
    if chunkType == b'IDAT':
        IDAT(chunkData)
    if chunkType == b'IEND':
        IEND(chunkData)

def bitUnpacker(byte):
    #reverse order
    bits = []
    if byte&1 != 0: bits.append(1)
    else: bits.append(0)
    if byte&2 != 0: bits.append(1)
    else: bits.append(0)
    if byte&4 != 0: bits.append(1)
    else: bits.append(0)
    if byte&8 != 0: bits.append(1)
    else: bits.append(0)
    if byte&16 != 0: bits.append(1)
    else: bits.append(0)
    if byte&32 != 0: bits.append(1)
    else: bits.append(0)
    if byte&64 != 0: bits.append(1)
    else: bits.append(0)
    if byte&128 != 0: bits.append(1)
    else: bits.append(0)
    return bits
########DELETE
def btINT(bits):
    btINT = 0
    if bits[0] == 1:
        btINT += 1
    if bits[1] == 1:
        btINT += 2
    return btINT
########DELETE
def bfINT(bits):
    #Four bit (1/0 array) to Int
    bfINT = 0
    if bits[0] == 1:
        bfINT += 1
    if bits[1] == 1:
        bfINT += 2
    if bits[2] == 1:
        bfINT += 4
    if bits[3] == 1:
        bfINT += 8
    return bfINT

def bINT(bits):
    bINT = 0
    for i in range(len(bits)):
        if i == 0:
            if bits[i] == 1:
                bINT += 1
        if i == 1:
            if bits[i] == 1:
                bINT += 2
        if i == 2:
            if bits[i] == 1:
                bINT += 4
        if i == 3:
            if bits[i] == 1:
                bINT += 8
        if i == 4:
            if bits[i] == 1:
                bINT += 16
        if i == 5:
            if bits[i] == 1:
                bINT += 32
        if i == 6:
            if bits[i] == 1:
                bINT += 64
        if i == 7:
            if bits[i] == 1:
                bINT += 128
    return bINT

def CMF(bits):
    CMa = []
    CINFOa = []
    for i in range(len(bits)):
        #print(bits[i])
        #print(i)
        if i < 4:
            CMa.append(bits[i])
        elif i < 8:
            CINFOa.append(bits[i])
    CM = bINT(CMa)
    CINFO = bINT(CINFOa)
    return CM,CINFO

def FLG(bits):
    FCHECKa = []
    FDICTa = []
    FLEVELa = []
    for i in range(len(bits)):
        if i < 5:
            FCHECKa.append(bits[i])
        elif i < 6:
            FDICTa.append(bits[i])
        elif i < 8:
            FLEVELa.append(bits[i])
    FCHECK = bINT(FCHECKa)
    FDICT = bINT(FDICTa)
    FLEVEL = bINT(FLEVELa)
    return FCHECK,FDICT,FLEVEL

def ZLIB(imageData):
    CM,CINFO = CMF(bitUnpacker(imageData[0]))
    FCHECK,FDICT,FLEVEL = FLG(bitUnpacker(imageData[1]))
    F_CHECK = (imageData[0]*256+imageData[1])%31==0
    print('F_CHECK',F_CHECK)
    print("CM",CM)
    print('CINFO',CINFO)
    print('FCHECK',FCHECK)
    print('FDICT',FDICT)
    print('FLEVEL',FLEVEL)
    #bits = bitUnpacker(imageData[0])
    #return CMF(bits)

    return True
    #https://tools.ietf.org/html/rfc1950
    #byte 1 bit 0|3 CM compression method
    #byte 1 bit 4|7 CINFO compression info
    #byte 2 bit 0|4 FCHECK
    #byte 2 bit 5 FDICT
    #byte 2 bit 6|7 FLG
    #6 byte ADLER32 checksum at end

def chunkCRCverify(chunkData,chunkCRC):
    return True

with open(image,"rb") as file:
    readingFile = True
    file.seek(0,0)
    signature = [137,80,78,71,13,10,26,10]
    check = True
    for i in signature:
        if i != int.from_bytes(file.read(1),byteorder='big'):
            check = False
    if check == True:
        print('This is a PNG file')
    else:
        readingFile = False
    while readingFile == True:
        chunkRead(file)
        chunkDiscriminator(chunkRead.chunkType,chunkRead.chunkData)

    print('width',width)
    print('height',height)
    print('bitDepth',bitDepth)
    print('colorType',colorType)
    print('compressionMethod',compressionMethod)
    print('filterMethod',filterMethod)
    print('interlaceMethod',interlaceMethod)
    print('sRGBrenderingIntent',sRGBrenderingIntent)
    print('gamma',gamma)
    print('pixelsPerUnitX',pixelsPerUnitX)
    print('pixelsPerUnitY',pixelsPerUnitY)
    print('unitSpecifier',unitSpecifier)
    ZLIB(imageData)
    file.close()

#4 byte unsigned int gives number of bytes in chunk's data field. Must not exceed 2^31
#4 byte chunk type code.
#chunk data appropriate to chunk type
#4 byte Cyclic Redundancy Check (see CRC algo)