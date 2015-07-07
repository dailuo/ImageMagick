# ----------------------------------------
# generate photo
# 1.fonts(and the attributes)       get
# 2.shadow                          not yet
# 3.position                        not yet
# 4.color                           get
# 5.rotation                        get
# 6.projective distortion           not yet
# ----------------------------------------
import PythonMagick
import random
import os
import math
import python2access
import time


def pathwalk(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            paths.append([root, fn])
    return paths

time1 = time.time()

for i in range(10):
    word = python2access.randomWords()
    # ---------------generate background color----------------------------
    redQuantum = random.randint(0, 65525)
    greenQuantum = random.randint(0, 65535)
    blueQuantum = random.randint(0, 65535)

    # --------------------------------------------------------------------

    color = PythonMagick.Color(redQuantum, greenQuantum, blueQuantum)

    # -----------------create photo-----------------------
    img = PythonMagick.Image('100x32', color)
    img.xResolution = 96
    img.yResolution = 96
    # ----------------------------------------------------

    # ---------------------generate font-------------------------------------------------------------------
    fonts = pathwalk('D:\code\MC lab\\usingImageMagick\\fonts\\font_en\\')
    randomFont = random.choice(fonts)
    randomFont = randomFont[0] + randomFont[1]

    initialPointsize = 40

    img.font(randomFont)
    fontcolor = PythonMagick.Color(random.randint(0, 65535), random.randint(0, 65535), random.randint(0, 65535))

    wordLength = len(word)
    # while initialPointsize * wordLength * 0.7 > 100 and initialPointsize > 15:
    #     initialPointsize -= 5

    tmp = int(math.floor(abs(random.gauss(0, 1))*6))
    if random.randint(1, 2) == 1:
        rotateX = random.randint(0, tmp)
    else:
        rotateX = random.randint(360-tmp, 360)

    # ----------------------------------------------------------------

    # -------------shadow-----------------------------------------------
    # geoShadow = PythonMagick.Geometry('100x32+2+2')
    # img.fontPointsize(initialPointsize)
    # img.fillColor(PythonMagick.Color('black'))
    # img.annotate(word, geoShadow, PythonMagick.GravityType.CenterGravity, rotateX)

    # ------------------------------------------------------------------

    # -----------------------print word----------------------------------
    img.fontPointsize(initialPointsize)
    img.fillColor(fontcolor)
    metric = PythonMagick.TypeMetric()
    img.fontTypeMetrics(word, metric)

    while metric.textWidth() > 100:
        initialPointsize -= 5
        img.fontPointsize(initialPointsize)
        img.fontTypeMetrics(word, metric)
    print(metric.textWidth(), '    ', metric.textHeight())
    # if int(math.floor(abs(random.gauss(0, 1)))) > 0.8:
    #     img.strokeColor(fontcolor)
    #     img.strokeWidth(2)


    # img.annotate(word, PythonMagick.Geometry(10, 4))
    geo = PythonMagick.Geometry('100x32')
    img.annotate(word, geo, PythonMagick.GravityType.CenterGravity, rotateX)

    if int(math.floor(abs(random.gauss(0, 1)))) > 1:
        underline = ''
        for i in range(wordLength):
            underline += '_'
        img.annotate(underline, geo, PythonMagick.GravityType.CenterGravity, rotateX)

    # 这就是下划线
    # -------------------------------------------------------------------

    img.colorSpace(PythonMagick.ColorspaceType.GRAYColorspace)
    # -----------------------save image----------------------------------
    img.magick('jpg')
    print(word)
    img.write('.\photo1\\'+str(i+1)+'.jpg')
    # -------------------------------------------------------------------


time2 = time.time()
print(time2-time1)