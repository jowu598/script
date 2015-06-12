mport os,glob
import Image
import math

def getBinary(x):
     index = 32;

     while ((1<<index) & x == 0):
          index = index -1;
     print index
     # for sqrt in range(32, 0, -1)
     #      if (0 != (1>>sqrt) & x):
     #           break;

     if (1<<index) == x:
          return x;
     else:
          return 1<<(index+1)

def resavePng(path):
     imgslist = glob.glob(path +'/*.png')
     for imgs in imgslist:
          imgspath, ext = os.path.splitext(imgs)

          print("imgspath is", imgspath)
          img = Image.open(imgs)
          (x,y) = img.size
          width = getBinary(x)
          height = getBinary(y)
          print("originWidth, originHeight, width height", x, y, width, height)
          newImg = img.resize((width,height),Image.ANTIALIAS)
          newImg.save(imgspath + ".png")

def transfromPng(sourceDir):
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        if os.path.isdir(sourceF):
            print sourceF
            resavePng(sourceF)
            transfromPng(sourceF)

if __name__ == '__main__':
     transfromPng(os.getcwd())
     print "transfrom done!!"
