#Author Luo.Dai
#Creation Time: 2015.6.15 20:00

import PythonMagick
import random
import time
import os
import python2access
import math


def pathwalk(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            paths.append([root, fn])
    return paths

time1 = time.time()
result = []
fileHandle = open('colorClusters.txt', 'r')
for line in fileHandle.readlines():
    line = line[0:-1]
    result.append(line.split(' '))
fileHandle.close()

for j in range(100):
    colorString = random.choice(result)
    color = []
    for i in colorString:
        color += [int(i)]
    for i in range(len(color)):
        color[i] = math.floor(color[i]/255*65535)
    color1 = color[0:3]
    color2 = color[3:6]
    color3 = color[6:9]
    # -------------------------------------------------------------

    # ---------------get the base layer texture-------------------------------
    Scenes = pathwalk('.\SceneData\\')
    randomScene = random.choice(Scenes)
    randomScene = randomScene[0] + randomScene[1]

    randomSceneImage = PythonMagick.Image(randomScene)
    randomSceneGeo = PythonMagick.Geometry(randomSceneImage.size())
    widthRange = randomSceneGeo.width() - 100
    heightRange = randomSceneGeo.height() - 32

    cutGeo = PythonMagick.Geometry('100x32+'+str(random.randint(0, widthRange))+'+'+str(random.randint(0, heightRange)))
    randomSceneImage.crop(cutGeo)
    # randomSceneImage.write('cutOutImage.jpg')
    # ------------------------------------------------------------------

    # --------create the base layer, base texture + base color----------
    baseImage = PythonMagick.Image('100x32', PythonMagick.Color(color1[0], color1[1], color1[2]))
    # baseImage.write('baseColor.jpg')
    baseImage.composite(randomSceneImage, 0, 0, PythonMagick.CompositeOperator.BlendCompositeOp)
    # baseImage.write('mixture.jpg')
    baseImage.xResolution = 96
    baseImage.yResolution = 96
    baseImage.blur(4, 10)
    # ------------------------------------------------------------------

    # -------------generate font----------------------------------------
    word = python2access.randomWords()
    fonts = pathwalk('.\\googleFonts\\')
    randomFont = random.choice(fonts)
    randomFont = randomFont[0] + randomFont[1]

    initialPointsize = 45

    baseImage.font(randomFont)
    fontcolor = PythonMagick.Color(color2[0], color2[1], color2[2])

    wordLength = len(word)

    tmp = int(math.floor(abs(random.gauss(0, 1))*6))
    if random.randint(1, 2) == 1:
        rotateX = random.randint(0, tmp)
    else:
        rotateX = random.randint(360-tmp, 360)
    # ------------------------------------------------------------------

    # -------------------generate suitable FontPointsize----------------
    baseImage.fontPointsize(initialPointsize)
    metric = PythonMagick.TypeMetric()
    baseImage.fontTypeMetrics(word, metric)

    while metric.textWidth() > 100 or metric.textHeight() > 36:
        initialPointsize -= 5
        baseImage.fontPointsize(initialPointsize)
        baseImage.fontTypeMetrics(word, metric)
    # ------------------------------------------------------------------

    # -----------------generate shadow/border----------------------------------
    if random.random() > 0.5:
        baseImage.strokeColor(PythonMagick.Color(color3[0], color3[1], color3[2]))
        baseImage.strokeWidth(math.ceil(initialPointsize/10)-1)
    else:
        addx = math.ceil(random.gauss(0, 2))
        addy = math.ceil(random.gauss(0, 2))
        if addx >= 0:
            addx = '+' + str(addx)
        else:
            addx = str(addx)
        if addy >= 0:
            addy = '+' + str(addy)
        else:
            addy = str(addy)
        # print(addx+addy)
        geoShadow = PythonMagick.Geometry('100x32'+addx+addy)
        addToPointsize = math.floor(abs(random.gauss(0, 1)))
        # print('addToPointsize = ', addToPointsize)
        baseImage.fontPointsize(initialPointsize+addToPointsize)
        baseImage.fillColor(PythonMagick.Color('black'))
        baseImage.annotate(word, geoShadow, PythonMagick.GravityType.CenterGravity, rotateX)
    # ------------------------------------------------------------------

    # -----------------print word---------------------------------------
    baseImage.fontPointsize(initialPointsize)
    baseImage.fillColor(fontcolor)
    geo = PythonMagick.Geometry('100x32')
    baseImage.annotate(word, geo, PythonMagick.GravityType.CenterGravity, rotateX)
    # ------------------------------------------------------------------

    # -----------------underline----------------------------------------
    if int(math.floor(abs(random.gauss(0, 1)))) > 2:
        underline = ''
        for i in range(wordLength):
            underline += '_'
        baseImage.annotate(underline, geo, PythonMagick.GravityType.CenterGravity, rotateX)
    # ------------------------------------------------------------------

    # ------------------------GREYColorSpace----------------------------
    baseImage.colorSpace(PythonMagick.ColorspaceType.GRAYColorspace)
    # ------------------------------------------------------------------

    baseImage.magick('jpg')
    print(word)
    baseImage.write('.\photo\\'+str(j+1)+'.jpg')


time2 = time.time()
print(time2-time1)