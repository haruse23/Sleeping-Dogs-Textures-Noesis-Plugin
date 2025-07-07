from inc_noesis import *
import os

# author: haru233
# Rename .perm.bin to ".sd" and .temp.bin to ".sd2"

def registerNoesisTypes():
    print("Registering Perm/Temp Texture plugin")
    handle = noesis.register("Perm/Temp Texture", ".sd")
    noesis.setHandlerTypeCheck(handle, checkType)
    noesis.setHandlerLoadRGBA(handle, LoadTexture)
    return 1

def checkType(data):
    return 1


def LoadTexture(data, texList):
    bs = NoeBitStream(data)

    ChunkID = bs.readUInt()
    ChunkSize = bs.readUInt()

    FileSize = bs.getSize()
    TextureCount = FileSize // (ChunkSize + 16)

    bs.seek(76, 1)
    TextureType = bs.readByte()
    bs.seek(7, 1)

    Width = bs.readUShort()
    Height = bs.readUShort()

    bs.seek(32, 1)
    Offset = bs.readUInt() # Offset in .temp.bin file
    Size = bs.readUInt()
    bs.seek(168, 1)

    # === Find the matching .temp.bin file ===
    permPath = rapi.getInputName()
    baseName = permPath.replace(".sd", "")
    tempPath = baseName + ".sd2"

    if not os.path.exists(tempPath):
        print("ERROR: Companion sd2 file not found:", tempPath)
        return 0

    # === Load pixel data ===
    pixelData = rapi.loadIntoByteArray(tempPath)

    pixelData = pixelData[Offset : Offset + Size]

    if TextureType == 1:
        tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT1)
        texList.append(tex)

    elif TextureType == 2:
        tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT3)
        texList.append(tex)

    elif TextureType == 3:
        tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT5)
        texList.append(tex)

    else:
        print("Unsupported Texture Type: {}".format(TextureType))


    for i in range(TextureCount-1):
        ChunkID = bs.readUInt()
        ChunkSize = bs.readUInt()

        bs.seek(76, 1)
        TextureType = bs.readByte()
        bs.seek(7, 1)

        Width = bs.readUShort()
        Height = bs.readUShort()
     
        bs.seek(32, 1)
        Offset = bs.readUInt()
        Size = bs.readUInt()
        bs.seek(168, 1)
        print(bs.tell())
        # === Find the matching .temp.bin file ===
        permPath = rapi.getInputName()
        baseName = permPath.replace(".sd", "")
        tempPath = baseName + ".sd2"

        if not os.path.exists(tempPath):
            print("ERROR: Companion sd2 file not found:", tempPath)
            return 0

        # === Load pixel data ===
        pixelData = rapi.loadIntoByteArray(tempPath)

        pixelData = pixelData[Offset : Offset + Size]
       
        if TextureType == 1:
            tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT1)
            texList.append(tex)
    
        elif TextureType ==2:
            tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT3)
            texList.append(tex)

        elif TextureType == 3:
            tex = NoeTexture(os.path.basename(baseName), Width, Height, pixelData, noesis.NOESISTEX_DXT5)
            texList.append(tex)

        else:
            print("Unsupported Texture Type: {}".format(TextureType))
    
    return 1
