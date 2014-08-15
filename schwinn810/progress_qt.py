""" Simple QT progress indicator """

from PyQt4.QtGui import QDialog, QMessageBox, QApplication
from ui_progress import Ui_Dialog

# Shall we use QProgressDialog instead?

class QtProgress(QDialog):

    def __init__(self):
        super(QtProgress, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.show()

    def _update(self):
        QApplication.processEvents()

    def track(self, name, at, end, points):
        self.ui.trackBar.setMaximum(end)
        self.ui.trackBar.setValue(at-1)
        self.ui.trackCountLabel.setText("{:d}/{:d}".format(at, end))
        self._update()

    def point(self, at, end):
        if at % 100 == 0:
            self.ui.pointBar.setMaximum(end)
            self.ui.pointBar.setValue(at-1)
            self.ui.pointCountLabel.setText("{:d}/{:d}".format(at, end))
            self._update()
