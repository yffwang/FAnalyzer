import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import time

from fanalyzer import FAnalyzer


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class Worker(QThread):
    def __init__(self, analyzer):
        super().__init__()
        self.analyzer = analyzer

    def run(self):
        print("[Version 1.0.0]")
        self.analyzer.analyze()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.old_stdout = None
        self.button = None
        self.textEdit = None
        self.layout = None
        self.worker = None
        self.init_ui()
        self.analyzer = FAnalyzer('stocks.xlsx')

    def init_ui(self):
        self.setWindowTitle('FAnalyzer')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit)

        self.button = QPushButton('Start Task', self)
        self.button.clicked.connect(self.start_task)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.old_stdout = sys.stdout
        sys.stdout = EmittingStream(textWritten=self.write_to_text_edit)

    def write_to_text_edit(self, text):
        self.textEdit.append(text)

    def start_task(self):
        self.worker = Worker(self.analyzer)
        self.worker.start()

    def closeEvent(self, event):
        sys.stdout = self.old_stdout
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
