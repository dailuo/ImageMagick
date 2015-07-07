from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
import random
import time
import python2access_cn
import os
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
    # ---------------get three colors-------------------------------
    colorString = random.choice(result)
    color = []
    for i in colorString:
        color += [int(i)]
    # for i in range(len(color)):
    #     color[i] = math.floor(color[i]/255*65535)
    color1 = color[0:3]
    color2 = color[3:6]
    color3 = color[6:9]
    # --------------------------------------------------------------

    # ----------get the base layer texture--------------------------
    Scenes = pathwalk('.\\SceneData\\')
    randomScene = random.choice(Scenes)
    randomScene = randomScene[0] + randomScene[1]
    # print(randomScene)
    randomSceneImage = Image(filename=randomScene)

    widthRange = randomSceneImage.size[0] - 100
    heightRange = randomSceneImage.size[1] - 32

    randomSceneImage.crop(left=random.randint(0, widthRange), top=random.randint(0, heightRange), width=100, height=32)
    # randomSceneImage.save(filename='.\\photoWand\\'+str(j+1) + '_texture.jpg')
    # --------------------------------------------------------------

    # ----------create the base layer, base texture +base color-----
    baseImage = Image(width=100, height=32, background=Color('rgb('+str(color1[0])+','+str(color1[1])+','+str(color1[2])+')'))

    # print('base_color = ' + 'rgb('+str(color1[0])+','+str(color1[1])+','+str(color1[2])+')')
    baseImage.composite_channel(channel='undefined', image=randomSceneImage, operator='blend', left=0, top=0)
    baseImage.gaussian_blur(4, 10)
    baseImage.resolution = (96, 96)
    # --------------------------------------------------------------

    # -----generate font--------------------------------------------
    word = python2access_cn.randomWords_cn()
    fonts = pathwalk('.\\fonts\\font_cn\\')
    randomFont = random.choice(fonts)
    randomFont = randomFont[0] + randomFont[1]

    initialPointsize = 45

    draw = Drawing()
    draw.font = randomFont

    tmp = int(math.floor(abs(random.gauss(0, 1))*6))
    if random.randint(1, 2) == 1:
        rotateX = random.randint(0, tmp)
    else:
        rotateX = random.randint(360-tmp, 360)

    draw.rotate(rotateX)
    # --------------------------------------------------------------
    # --------get suitable FontPointSize----------------------------
    draw.font_size = initialPointsize
    metric = draw.get_font_metrics(image=baseImage, text=word)

    while metric.text_width > 100 or metric.text_height > 36:
        initialPointsize -= 5
        draw.font_size = initialPointsize
        metric = draw.get_font_metrics(image=baseImage, text=word)
    # --------------------------------------------------------------

    # ----------italic----------------------------------------------
    if random.random() > 0.5:
        draw.font_style = 'italic'
    # --------------------------------------------------------------

    # ----------underline-------------------------------------------
    if random.random() > 0.5:
        draw.text_decoration = 'underline'
    # --------------------------------------------------------------

    # ----------gravity---------------------------------------------
    draw.gravity = 'center'
    # --------------------------------------------------------------

    # --------------shadow/border-----------------------------------
    if random.random() < 0.5:
        # shadow
        addx = math.ceil(random.gauss(0, 2))
        addy = math.ceil(random.gauss(0, 2))
        draw.fill_color = Color('black')
        draw.text(x=abs(addx), y=abs(addy), body=word)

    else:
        # border
        draw.stroke_color = Color('rgb('+str(color3[0])+','+str(color3[1])+','+str(color3[2])+')')
        draw.stroke_width = math.ceil(initialPointsize/10)-1
    # --------------------------------------------------------------

    # ----------print word------------------------------------------
    draw.fill_color = Color('rgb('+str(color2[0])+','+str(color2[1])+','+str(color2[2])+')')
    # print('font_color =' + 'rgb('+str(color2[0])+','+str(color2[1])+','+str(color2[2])+')')
    draw.text(x=0, y=0, body=word)
    draw.draw(baseImage)
    # --------------------------------------------------------------

    # ------------gray----------------------------------------------
    baseImage.colorspace = 'gray'
    # --------------------------------------------------------------

    print(word)
    baseImage.save(filename='.\\photoWand_cn\\'+str(j+1)+'.jpg')


time2 = time.time()
print(time2-time1)

# img = Image(width=200, height=200, background=Color('red'))
# draw = Drawing()
# draw.font = 'D:\code\MC lab\src\\rewrite python\GeneratePhoto\\fonts\\font_en\\cambria.ttc'
#
# draw.font_style = 'italic'
# draw.text_decoration = 'underline'
#
# draw.font_size = 40
# draw.gravity = 'center'
# draw.fill_color = Color('black')
# draw.scale(x=4, y=1)
# draw.affine([1, 0, -0.6, 1, 0, 0])
#
# draw.text(5, 5, 'hello')
#
# draw.stroke_width = 1
# draw.stroke_color = Color('orange')
# draw.fill_color = Color('blue')
#
# draw.text(0, 0, 'hello')
#
# draw.draw(img)
#
# img.save(filename='wandtest.jpg')