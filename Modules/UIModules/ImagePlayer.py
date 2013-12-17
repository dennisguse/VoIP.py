from PyQt4.QtGui import *
from PyQt4.QtCore import *

def gifMovie(label,  filename):
    movie = QMovie(filename, QByteArray(), label)
    label.setMovie(movie)
    movie.start()
