# @Author: Nicholas Bloedel
# @Date: 03-08-2021
# @File: minimalPomo.py



import sys
import winsound
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication, QLabel
from PyQt5.QtCore import *
import itertools

#GLOBALS
POMO_TIME = 1500; #1500 seconds -> 25 minutes
BREAK_TIME = 315; #315 seconds -> 5 minutes + 15 seconds to pause work
TIME_SWITCH = itertools.cycle([BREAK_TIME, POMO_TIME])



#Converting our total seconds into a clock format
def seconds_conv(seconds: int):
    minutes = seconds // 60;
    seconds = seconds % 60;

    timeLeft = f'{minutes:02}:{seconds:02}'

    return timeLeft


class TimerWindow(QWidget):

    def __init__(self):
        super().__init__()

        #initialize GUI widgets
        self.timerLabel = QLabel(self)
        self.startButton = QPushButton('Start')
        self.pauseButton = QPushButton('Pause')
        self.rstButton = QPushButton('Reset')

        #timer setup
        self.timeLeft = POMO_TIME
        self.timeBool = True
        self.studyTimer = QTimer(self)
        self.studyTimer.setInterval(1000)
        self.studyTimer.timeout.connect(self.pomo_timeout)

        #button on-click events
        self.startButton.clicked.connect(self.startTime)
        self.pauseButton.clicked.connect(self.pauseTime)
        self.rstButton.clicked.connect(self.resetTime)

        #setting layout of GUI
        winLayout = QVBoxLayout()
        winLayout.addStretch()
        winLayout.addWidget(self.timerLabel)
        winLayout.addWidget(self.startButton)
        winLayout.addWidget(self.pauseButton)
        winLayout.addWidget(self.rstButton)
        winLayout.addStretch()
        
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('Pomodoro Timer')
        self.setGeometry(0, 0, 400, 400)
        self.update()
        self.setLayout(winLayout)
        self.show()


    def startTime(self):
        self.studyTimer.start()
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)
        self.rstButton.setEnabled(True)

    
    def pauseTime(self):
        self.studyTimer.stop()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.rstButton.setEnabled(False)
    
    def resetTime(self):
        self.timeLeft = POMO_TIME
        self.update()
        self.studyTimer.stop()
        self.startButton.setEnabled(True)
        if(TIME_SWITCH.__next__() == BREAK_TIME):
            next(TIME_SWITCH)

    def update(self):
        self.timerLabel.setText(seconds_conv(self.timeLeft))
    
    def pomo_timeout(self):
        self.timeLeft -= 1
        #if time is over, switch timer length and alert user
        if self.timeLeft == 0:
            if self.timeBool == True:
                winsound.Beep(1000, 1500)
                self.timeBool = False
            elif self.timeBool == False:
                winsound.Beep(1000, 1500)
                self.timeBool = True
            self.timeLeft = next(TIME_SWITCH)

        self.update()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    styleSheets = """
                    QWidget{
                        background: #262D37;
                    }
                    QPushButton{
                        color: white;
                        border: solid;
                        border-color: white;
                        border-width: 2px;
                        border-radius: 10px;
                        padding: 24px 24px;
                        margin: 10px;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: bold;
                        font-size: large;
                    }
                    QPushButton:pressed{
                        background-color: green;
                    }
                    QLabel{
                        color: white;
                        font-family: Arial, Helvetica, sans-serif;
                        font-weight: bold;
                        font-size: 50px;
                    }
    """
    app.setStyleSheet(styleSheets)
    window = TimerWindow()
    sys.exit(app.exec_())
