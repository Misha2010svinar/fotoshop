from PyQt5.QtWidgets import *
import os
from PIL.ImageFilter import *
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap

papka = ""
app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background: #211e1e;
        color: white;
    }

    QPushButton {
        color: white;
        font-family: Monotype Corsiva;
        font-size: 12px;
    }
""")
window = QWidget()
window.resize(800, 600)
window.setWindowTitle("ІЗІ ФОТОШОП")

folderBtn = QPushButton("Папка")
leftBtn = QPushButton("Ліворуч")
rightBtn = QPushButton("праворуч")
mirrorBtn = QPushButton("дзеркало")

imgLbl = QLabel("фоточка")
fileList = QListWidget()

mainLine = QHBoxLayout()
columnLeft = QVBoxLayout()
columnLeft.addWidget(folderBtn)
columnLeft.addWidget(fileList)
mainLine.addLayout(columnLeft)
columnRight = QVBoxLayout()
columnRight.addWidget(imgLbl)
line1 = QHBoxLayout()
line1.addWidget(leftBtn)
line1.addWidget(rightBtn)
line1.addWidget(mirrorBtn)
columnRight.addLayout(line1)
mainLine.addLayout(columnRight)

def openPapka():
    global papka
    papka = QFileDialog.getExistingDirectory()
    print(papka)
    files = os.listdir(papka)
    fileList.clear()
    fileList.addItems(files)

class WorkPhoto:
    def __init__(self):
        self.image = None
        self.folder = None
        self.filename = None

    def load(self):
        imagePath = os.path.join(self.folder, self.filename)
        self.image = Image.open(imagePath)

    def showImage(self):
        pixel = pil2pixmap(self.image)
        imgLbl.setPixmap(pixel)

    def doBlackWhite(self):
        self.image = self.image.convert("L")
        self.showImage()

    def doLeft(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage()

    def doRight(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage()

    def doMirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

workPhoto = WorkPhoto()
def showChosenImage():
    workPhoto.folder = papka
    workPhoto.filename = fileList.currentItem().text()
    workPhoto.load()
    workPhoto.showImage()

fileList.currentRowChanged.connect(showChosenImage)
folderBtn.clicked.connect(openPapka)
rightBtn.clicked.connect(workPhoto.doRight)
leftBtn.clicked.connect(workPhoto.doLeft)
mirrorBtn.clicked.connect(workPhoto.doMirror)

window.setLayout(mainLine)
window.show()
app.exec_()



