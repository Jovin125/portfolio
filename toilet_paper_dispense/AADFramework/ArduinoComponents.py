#####################################################
# Program file name: ArduinoComponents.py
# -----------------------------------------------------
# Author: Zhang Binglu
# ---------------------------------------------------
# version: 2021_06_02
# ---------------------------------------------------
# since:  2021-07-8
# --------------------------------------------------------
# Arduino Application Development Framework - ADF has been implemented
# in this program file. Following software components which are almost
# one to one related with physical Arduino components:
# 1. ControlBoard  - related to Arduino Control Board
# 2. Digital Input Device - related to Arduino Digital Inout Device
# 3. Digital Output Deice - related to Arduino Digital Output Device
# 4. Servo Motor  -  related to Arduino Servo Motor
# 5  InputMonitor  - related to no Arduino components
# --------------------------------------------------------
# Please refer to ADFramework User Manual and Samples of Using
# ADFramework for more details.
# --------------------------------------------
# Public Properties for Motor:
# 1. status
# 2. name
# 3. pin
# 4. minAngle
# 5. maxAngle
# 6. homePos
# ---------------------------------------------------
# Public methods for Motor:
# 1. home()
# 2. turnTo(degree, speed=2, restTime=0)
# 3. turnPath(path, repeatNo=1, restGapTime=0)
# 4. threadTurnTo(degree, speed=2, restTime=0)
# 5. threadTurnPath(path, reptNo=1, restGapTime=0)
# 6. threadTurnPaths(paths, reptNo=1, restGapTime=0)
# ----------------------------------------------------
#####################################################
import math

from pyfirmata import Arduino, util
import time
import threading
import os.path
from os import path


class utility:
    def __init__(self):
        pass

    def menuGeneratorA(self, title, itemList, divider, template, messages):
        print(divider)
        print('{:^45s}'.format('Input/Motor Messages'))
        print(divider)
        for x in messages:
            print(x)
        print(divider)
        print('{:^45s}'.format(title))
        print(divider)

        for i in range(len(itemList)):
            print(template.format(i + 1, itemList[i]))
        print(template.format(len(itemList) + 1, 'Quit'))
        print(divider)
        while True:
            try:
                rpl = int(input('Your choice ({} - {}):\t'.format(1, len(itemList) + 1)))
                print(divider)
                if rpl <= 0 or rpl > len(itemList) + 1:
                    print('Invalid input. Please press RETURN to try again ')
                    continue
                return rpl
            except:
                print('Invalid input. Please press RETURN to try again ')

    def menuGenerator(self, title, itemList):
        divider = 45 * '*'
        template = '{:2d} ----------- {:<20s}'
        print(divider)
        print('{:^45s}'.format(title))
        print(divider)

        for i in range(len(itemList)):
            print(template.format(i + 1, itemList[i]))
        print(template.format(len(itemList) + 1, 'Quit'))
        print(divider)
        while True:
            try:
                rpl = int(input('Your choice ({} - {}):\t'.format(1, len(itemList) + 1)))
                print(divider)
                if rpl <= 0 or rpl > len(itemList) + 1:
                    print('Invalid input. Please press RETURN to try again ')
                    continue
                return rpl
            except:
                print('Invalid input. Please press RETURN to try again ')

    def showTreadsInfo(self):
        startThreads = threading.enumerate()
        print('        current threads:')
        print('*' * 30)
        for x in startThreads:
            print(x)

    def pause(self, time):
        time.sleep(time)


class ArduinoDeviceType:
    DIGITAL_OUTPUT = 1
    DIGITAL_INPUT = 2
    SERVO_MOTOR = 3
    ANALOG_INPUT = 4
    ANALOG_OUTPUT = 5


class ControlBoard:
    # status data
    RUNNING = 1
    IDLE = 0
    FAULTY = -1

    def __init__(self, comPort):
        self._name = None
        self._compPort = comPort
        self._status = ControlBoard.IDLE
        self._iterator = None
        self._deviceList = []
        self._arBoard = None
        self._deviceType = None
        self._inputMonitor = None
        self._arBoard = Arduino(self._compPort)

    @property
    def inputMonitor(self):
        return self._inputMonitor

    @inputMonitor.setter
    def inputMonitor(self, value):
        self._inputMonitor = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def arBoard(self):
        return self._arBoard

    def isPinNoUsed(self, pinNo):
        for x in self._deviceList:
            if x.pinNo == pinNo:
                return True
        return False

    def buildDigitalInput(self, pinNo, name='No Name'):
        inputX = DigitalInput(self, pinNo, name)
        return inputX

    def buildDigitalOutput(self, pinNo, name='No Name'):
        outputX = DigitalOutput(self, pinNo, name)
        return outputX

    def buildServoMotor(self, pinNo, name='No Name'):
        svrMotor = ServoMotor(self, pinNo, name)
        return svrMotor

    def buildInputMonitor(self):
        self._inputMonitor = InputMonitor(self)
        return self._inputMonitor

    def displayDiviceTableOnBoard(self):
        devider = 50 * '*'
        template = '{:^5d}|{:^20s}|{:^15s}|{:^6d}|'
        print('\n' + devider)
        print('{:^50s}'.format('Components on Board'))
        print(devider)
        print('{:^5s}|{:^20s}|{:^15s}|{:^6s}|'.format('S/N', 'Device Type', 'Name', 'Pin No'))
        print(devider)
        count = 1
        for x in self._deviceList:
            print(template.format(count, x.deviceTypeString(), x.name, x.pinNo))
            count += 1
        print(devider)

    def _outputDeviceTester(self):
        print("Testing output devices now")
        print('-' * 40)
        print('Your output device is going to On/Off twice during the test')
        for x in self._deviceList:
            if x.deviceType == ArduinoDeviceType.DIGITAL_OUTPUT:
                input('Test {:10s} press ENTER to start'.format(x.name))
                for i in range(2):
                    x.turnOn()
                    time.sleep(0.5)
                    x.turnOff()

        print("-" * 40)
        print("Testing output devices is completed")
        print("-" * 40)

    def _inputDeviceTester(self):

        for x in self._deviceList:
            if x.deviceType == ArduinoDeviceType.DIGITAL_INPUT:
                x._count = 0

        print("Testing input devices now")
        print('-' * 40)
        print('You need take action on your input device during test for next a few seconds')
        print('-' * 40)
        time.sleep(1)
        for x in self._deviceList:
            if x.deviceType == ArduinoDeviceType.DIGITAL_INPUT:
                input('Test {:10s}... press ENTER to start'.format(x.name))
                time.sleep(2)
        time.sleep(3)
        print('+' * 40)
        print('Device count value after the test')
        print("-" * 40)
        self._inputMonitor.deviceCountDisplay()
        print("+" * 40)
        print("Testing input devices is completed")
        print('Check the count value of the device. If it is 0, that device is not functioning!')
        print("-" * 40)
        input('Press ENTER to continue...')
        for x in self._deviceList:
            if x.deviceType == ArduinoDeviceType.DIGITAL_INPUT:
                x._count = 0

    def _servoMotorTester(self):
        print("Testing servo motor devices now")
        print('-' * 40)
        for x in self._deviceList:
            if x.deviceType == ArduinoDeviceType.SERVO_MOTOR:
                input('Test {:10s} ...press ENTER to start'.format(x.name))
                x.home()
                x.turnTo(30, 1, 1)
                x.turnTo(10, 1, 0)
                time.sleep(1)
        print("-" * 40)
        print("Testing servo motor devices is completed")
        print("-" * 40)

    def boardComponentsTester(self):

        menuTitle = 'Arduino Board Component Tester'
        choises = ['Show component table',
                   'Test output devices',
                   'Test input devices',
                   'Test servo motors']
        rpl = input('Do you want to run Board Components Tester?(y/n):\t')
        if rpl == 'y':
            self._inputMonitor.start(0.2)
            while True:
                choise = menuGenerator(menuTitle, choises)
                if choise == 1:
                    self.displayDiviceTableOnBoard()
                    input('Press any key to continue...')
                elif choise == 2:
                    self._outputDeviceTester()
                elif choise == 3:
                    self._inputDeviceTester()
                elif choise == 4:
                    self._servoMotorTester()
                else:
                    break
            self._inputMonitor.shutdown()
            print('Wait for a while!')
            while self._inputMonitor._status != 0:
                time.sleep(0.3)
            print('-' * 45)
            print("Congratulations! All your device tests have been completed.")
            print('If some of your  devices are not functioning, \n'
                  'check the component wire connection first before report to your lecturer')
            print('-' * 45)
            print('Tahnk you very much for using  Arduno Board Component Tester!')
            print('-' * 45)

    def start(self):

        # self._arBoard = Arduino(self._compPort)
        self._iterator = util.Iterator(self._arBoard)
        self._iterator.start()
        self._status = ControlBoard.RUNNING
        self._inputMonitor = self.buildInputMonitor()
        self.boardComponentsTester()
        print('Arduino Control System has been started!')

    def shutdown(self):
        if self._inputMonitor is not None:
            self._inputMonitor.shutdown()
        self._arBoard.exit()
        print('Arduino Control System has been shutdown!')


class ArduinoDevice:
    def __init__(self, deviceType, ctrlBoard, pinNo, name):
        self._ctrlBoard = ctrlBoard
        self._deviceType = deviceType
        self._name = name
        self._pin = None
        if self._ctrlBoard.isPinNoUsed(pinNo):
            raise Exception('Pin numbere: {} has been used by other device'.format(pinNo))
        else:
            self._pinNo = pinNo

        if self._deviceType == ArduinoDeviceType.DIGITAL_INPUT:
            self._pin = self._ctrlBoard.arBoard.get_pin('d:' + str(self._pinNo) + ':i')
        elif self._deviceType == ArduinoDeviceType.DIGITAL_OUTPUT:
            self._pin = self._ctrlBoard.arBoard.get_pin('d:' + str(self._pinNo) + ':o')
        elif self._deviceType == ArduinoDeviceType.SERVO_MOTOR:
            self._pin = self._ctrlBoard.arBoard.get_pin('d:' + str(self._pinNo) + ':s')
        else:
            raise Exception('in valid device type!')
        self._status = None
        self._ctrlBoard._deviceList.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def deviceType(self):
        return self._deviceType

    @deviceType.setter
    def deviceType(self, value):
        self._deviceType = value

    @property
    def pinNo(self):
        return self._pinNo

    @property
    def pin(self):
        return self._pin

    def deviceTypeString(self):
        if self.deviceType == ArduinoDeviceType.DIGITAL_OUTPUT:
            return ('DIGITAL_OUTPUT')
        elif self.deviceType == ArduinoDeviceType.DIGITAL_INPUT:
            return ('DIGITAL_INPUT')
        elif self.deviceType == ArduinoDeviceType.SERVO_MOTOR:
            return ('SERVO_MOTOR')
        elif self.deviceType == ArduinoDeviceType.ANALOG_INPUT:
            return ('ANALOG_INPUT')
        elif self.deviceType == ArduinoDeviceType.ANALOG_OUTPUT:
            return ('ANALOG_OUTPUT')
        else:
            return ('Not defined')


class DigitalInput(ArduinoDevice):
    def __init__(self, ctrlBoard, pinNo, name):
        ArduinoDevice.__init__(self, ArduinoDeviceType.DIGITAL_INPUT, ctrlBoard, pinNo, name)

        self._count = 0
        self._undetectedValue = None

    @property
    def count(self):
        return self._count

    def detect(self):
        return self.pin.read()

    def getCountValue(self, resetCount=True):
        count = self._count
        if resetCount:
            self._count = 0
        return count


class DigitalOutput(ArduinoDevice):
    def __init__(self, ctrlBoard, pinNo, name):
        ArduinoDevice.__init__(self, ArduinoDeviceType.DIGITAL_OUTPUT, ctrlBoard, pinNo, name)

    def turnOn(self):
        self.pin.write(1)

    def turnOff(self):
        self.pin.write(0)

    def turn(self, isOn):
        self.pin.write(isOn)


class ServoMotor(ArduinoDevice):
    MotorSpeedSeed = 0.0155

    def __init__(self, ctrlBoard, pinNo, name):
        ArduinoDevice.__init__(self, ArduinoDeviceType.SERVO_MOTOR, ctrlBoard, pinNo, name)

        self._homePos = 0
        self._status = 0
        self._minAngle = 0
        self._maxAngle = 0
        self._headDownDegree = 0  # for five-bar robot
        self._headUpDegree = 0  # for five-bar robot
        self._parkDegree = 0  # for five-bar robot
        self._baseZeroAngle = 0  # for five-bar robot
        self._lock = threading.Lock()
        self._mainThread = threading.currentThread()
        self._motorSpeedTimer = ServoMotor.MotorSpeedSeed
        self._emergenceStopFlag = False

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def baseZeroAngle(self):
        return self._baseZeroAngle

    @baseZeroAngle.setter
    def baseZeroAngle(self, value):
        self._baseZeroAngle = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def minAngle(self):
        return self._minAngle

    @minAngle.setter
    def minAngle(self, value):
        self._minAngle = value

    @property
    def maxAngle(self):
        return self._maxAngle

    @maxAngle.setter
    def maxAngle(self, value):
        self._maxAngle = value

    @property
    def headDownDegree(self):
        return self._headDownDegree

    @headDownDegree.setter
    def headDownDegree(self, value):
        self._headDownDegree = value

    @property
    def headUpDegree(self):
        return self._headUpDegree

    @headUpDegree.setter
    def headUpDegree(self, value):
        self._headUpDegree = value

    @property
    def parkDegree(self):
        return self._parkDegree

    @parkDegree.setter
    def parkDegree(self, value):
        self._parkDegree = value

    # Private methods
    # ---------------
    def _currentAngle(self):
        return self._pin.read()

    def _setAngle(self, angle):
        if self._emergenceStopFlag:
            return

        if angle > self._maxAngle:
            angle = self._maxAngle
        if angle < self._minAngle:
            angle = self._minAngle

        newAngle = angle - self.baseZeroAngle
        if newAngle < 0:
            newAngle = 0
        self._pin.write(newAngle)
        time.sleep(ServoMotor.MotorSpeedSeed)

    def _changeStatus(self, status):
        self._lock.acquire()
        try:
            self._status = status
        finally:
            self._lock.release()

    # public methods
    # --------------
    def turnTo(self, degree, speed=2, restTime=0):

        pos = self._currentAngle()
        if degree < pos:
            step = -speed
        else:
            step = speed
        for x in range(pos, degree, step):
            self._setAngle(x)
        self._setAngle(degree)
        time.sleep(restTime)

    def home(self):
        self.turnTo(self._parkDegree)

    def emergencyStop(self, stopTime=0):

        def threadFunc(stopTime):
            time.sleep(stopTime)
            self._emergenceStopFlag = True

        # runner = threading.Thread(target=threadFunc, args=(path, reptNo,restGapTime))
        runner = threading.Thread(target=threadFunc, args=(stopTime,))
        runner.start()

    def emergencyRemove(self):
        self.waitForThreadTurnStop()
        self._emergenceStopFlag = False

    def turnPath(self, path, reptNo=1, restGapTime=0):
        if self._status == 1:
            print("Motor is running. Can not run for anther path!")
            return
        self._status = 1
        for x in range(reptNo):
            for sect in path:
                self.turnTo(sect[0], sect[1])
            time.sleep(restGapTime)
        self._status = 0

    def threadTurnPath(self, path, reptNo=1, restGapTime=0):
        def threadFunc(path, reptNo, restGapTime):
            # self.waitForThreadTurnStop()
            # if self._status == 1:
            #     print("Motor is running. Can not run for anther path!")
            #     return
            if Constants.isDebugging:
                print('{}  thread just starts'.format(self.name))
            self._status = 1
            for x in range(reptNo):
                for sect in path:
                    self.turnTo(sect[0], sect[1])
                time.sleep(restGapTime)
            self._status = 0
            if Constants.isDebugging:
                print('{} thread just finished'.format(self.name))
            return

        # runner = threading.Thread(target=threadFunc, args=(path, reptNo,restGapTime))
        runner = threading.Thread(target=threadFunc, args=(path, reptNo, restGapTime))
        runner.start()

    def threadTurnTo(self, degree, speed=2, restTime=0):
        def threadFunc(degree, speed, restTime):

            # self.waitForThreadTurnStop()
            # if self._status == 1:
            #     print("Motor is running. Can not run for anther path!")
            #     return
            if Constants.isDebugging:
                print('{}  thread just starts'.format(self.name))
            self._status = 1
            pos = self._currentAngle()
            if degree < pos:
                step = -speed
            else:
                step = speed
            for x in range(pos, degree, step):
                self._setAngle(x)
            self._setAngle(degree)
            time.sleep(restTime)
            self._status = 0
            if Constants.isDebugging:
                print('{} thread just finished'.format(self.name))
            return

        runner = threading.Thread(target=threadFunc, args=(degree, speed, restTime))
        runner.start()

    def threadTurnPaths(self, pathes, reptNo=1, restGapTime=0):
        def threadFunc(pathes, reptNo, restGapTime):
            # self.waitForThreadTurnStop()
            # if self._status == 0:
            #     print("Motor is running. Can not run for anther path!")
            #     return
            if Constants.isDebugging:
                print('{}  thread just starts'.format(self.name))
            self._status = 1
            for i in range(reptNo):
                for x in pathes:
                    for sect in x:
                        self.turnTo(sect[0], sect[1])
                    time.sleep(restGapTime)
                    # print(x)
            self._status = 0
            if Constants.isDebugging:
                print('{} thread just finished'.format(self.name))
            return

        runner = threading.Thread(target=threadFunc, args=(pathes, reptNo, restGapTime))
        runner.start()

    def waitForThreadTurnStop(self):
        while self._status == 1:
            if Constants.isDebugging:
                print('{} thread is still running.'.format(self.name))
            time.sleep(0.5)


class InputMonitor:
    def __init__(self, ctrlBoard, detectingGapTime=0.1):
        self._ctrlBoard = ctrlBoard
        self._inputDeviceList = []
        self._status = 0
        self._frequency = detectingGapTime
        self._isDebugging = True
        for x in self._ctrlBoard._deviceList:
            if x.deviceType == ArduinoDeviceType.DIGITAL_INPUT:
                self._inputDeviceList.append(x)
        self._eventMessages = []
        self._responder = None

    @property
    def responder(self):
        return self._responder

    @responder.setter
    def responder(self, value):
        self._responder = value

    @property
    def eventMessages(self):
        return self._eventMessages

    @property
    def status(self):
        return self._status

    def _deviceTesting(self):
        for x in range(30):
            no = 0
            for x in self._inputDeviceList:
                x.status = x.detect()
                if x.status is not None:
                    x._noDetectedValue = x.status
                    no += 1
                else:
                    x.status = -1
            if no == len(self._inputDeviceList):
                return True
            else:
                time.sleep(0.5)

        for x in self._inputDeviceList:
            if x.status == -1:
                print('{} is faulty'.format(x.name))
        return False

    def _threadRun(self):
        def threadFunc():
            global messages
            # initialization set input device status
            self._status = 1
            print("Monitor is running")
            while self._status == 1:
                for x in self._inputDeviceList:
                    if self._status == 0:
                        break
                    if x.detect() != x._noDetectedValue:
                        x._count = x._count + 1
                        if self._responder is not None and self._status == 1:
                            self._responder.turnOn()
                            time.sleep(0.2)
                            self._responder.turnOff()
                        if not self._isDebugging:
                            print('From monitor: {} has detected input. Recorded count is {}'.format(x.name, x._count))
                    time.sleep(self._frequency)

        runner = threading.Thread(target=threadFunc, args=())
        runner.start()

    def addDevice(self, device):
        self._inputDeviceList.append(device)

    def start(self, frequency=0.1, isDebugingging=True, ):
        if self._status == 0:
            if not self._deviceTesting():
                return
            self._isDebugging = isDebugingging
            self._frequency = frequency
            self._threadRun()
        else:
            print('The monitor is running and can not start again!')

    def shutdown(self):
        self._status = 0  # shutdown status

    def deviceCountDisplay(self):
        for x in self._inputDeviceList:
            print('{}: recorded count is {}'.format(x.name, x._count))

    def clearDeviceCount(self):
        for x in self._inputDeviceList:
            x._count = 0
            print('{}: recorded count is {}'.format(x.name, x._count))


class Constants:
    isDebugging = False
    waitForThreadFinishTimeForDrawing = 5
    waitForThreadFinishTimeForMoving = 2
    HEAD_DOWNN = 1
    HEAD_UP = 2
    HEAD_PARK = 3
    LEFT_MOTOR_ASSEMBLY_DEGREE = 90
    RIGHT_MOTOR_ASSEMBLY_DEGREE = 90
    HEAD_MOTOR_ASSEMBLY_DEGREE  = 0


def menuGeneratorA(title, itemList, divider, template, messages):
    print(divider)
    print('{:^45s}'.format('Input/Motor Messages'))
    print(divider)
    for x in messages:
        print(x)
    print(divider)
    print('{:^45s}'.format(title))
    print(divider)

    for i in range(len(itemList)):
        print(template.format(i + 1, itemList[i]))
    print(template.format(len(itemList) + 1, 'Quit'))
    print(divider)
    while True:
        try:
            rpl = int(input('Your choice ({} - {}):\t'.format(1, len(itemList) + 1)))
            print(divider)
            if rpl <= 0 or rpl > len(itemList) + 1:
                print('Invalid input. Please press RETURN to try again ')
                continue
            return rpl
        except:
            print('Invalid input. Please press RETURN to try again ')


def menuGenerator(title, itemList):
    print('\n' * 5)
    divider = 50 * '*'
    template = '{:2d} ----------- {:<20s}'
    print(divider)
    print('{:^45s}'.format(title))
    print(divider)

    for i in range(len(itemList)):
        print(template.format(i + 1, itemList[i]))
    print(template.format(len(itemList) + 1, 'Quit'))
    print(divider)
    while True:
        try:
            rpl = int(input('Your choice ({} - {}):\t'.format(1, len(itemList) + 1)))
            print(divider)
            if rpl <= 0 or rpl > len(itemList) + 1:
                print('Invalid input. Please press RETURN to try again ')
                continue
            return rpl
        except:
            print('Invalid input. Please press RETURN to try again ')


def showTreadsInfo():
    startThreads = threading.enumerate()
    print('        current threads:')
    print('*' * 30)
    for x in startThreads:
        print(x)


class MotorRobot:
    def __init__(self):
        self._name = "Motorized Robot"
        self._pin = None
        self._homePos = [0, 0, 0]
        self._status = 0
        self._xMotor = None
        self._yMotor = None
        self._zMotor = None

    @property
    def xMotor(self):
        return self._xMotor

    @xMotor.setter
    def xMotor(self, value):
        self._xMotor = value

    @property
    def yMotor(self):
        return self._yMotor

    @yMotor.setter
    def yMotor(self, value):
        self._yMotor = value

    @property
    def zMotor(self):
        return self._zMotor

    @zMotor.setter
    def zMotor(self, value):
        self._zMotor = value

    def home(self):
        self.headUp()
        time.sleep(0.3)
        self.driveTo(self.xMotor._parkDegree, self._yMotor._parkDegree, 1)
        self._zMotor.home()

    def emergencyStop(self):
        print("Emergency Stop Now!!!")
        self.xMotor.emergencyStop()
        self.yMotor.emergencyStop()
        self.zMotor.emergencyStop()

    def _waitForThreadsToFinish(self, waitTime):
        if Constants.isDebugging:
            print('Please wait ...')
        time.sleep(waitTime)

    #######################################
    # Two motors are turning coordinately
    # still under development
    #######################################

    def headUp(self):
        self._zMotor.turnTo(self._zMotor._headUpDegree)
        time.sleep(0.5)

    def headDown(self):
        self._zMotor.turnTo(self._zMotor._headDownDegree)
        time.sleep(0.5)

    def motorsCoordinatedTurning(self):
        for i in range(2):
            for i in range(0, 90, 5):
                self.xMotor.turnTo(180 - i, 5)
                self._yMotor.turnTo(i)
            for i in range(90, 0, -5):
                self.xMotor.turnTo(180 - i, 5)
                self.yMotor.turnTo(i)
        self.home()
        ############################################

    def driveTo(self, xPos, yPos, speed=1):  # left-middle edge (155,60) right-middle edge (90,0)

        self.xMotor.threadTurnTo(xPos, speed)
        self.yMotor.threadTurnTo(yPos, speed)

        self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing)
        # self.xMotor.waitForThreadTurnStop()
        # self.yMotor.waitForThreadTurnStop()
        # while self.xMotor.status == 1 or self.yMotor.status == 1:
        #     time.sleep(0.2)


class FiveBarDrawingRobot(MotorRobot):

    def __init__(self):
        MotorRobot.__init__(self)
        self._headStatus = Constants.HEAD_UP
        self._scale = 0.66  # for drawing number use
        self._leftMotor = None
        self._rightMotor = None
        self._headMotor = None
        self._controller = None
        self._configFile = '.\\setup.dat'
        self._setupDataChanged = False
        self._drawingWidth = 40
        self._drawingTop = 70
        self._drawingBottom = 30

    def build(self, controller, leftMotorPin, rightMotorPin, headMotorPin):

        self._controller = controller
        # build needed motors
        leftMotor = controller.buildServoMotor(leftMotorPin, 'leftMotor')
        leftMotor.baseZeroAngle = 1
        leftMotor.parkDegree = 32

        rightMotor = controller.buildServoMotor(rightMotorPin, 'rightMotor')
        print(rightMotor.name)
        rightMotor.baseZeroAngle = -1
        rightMotor.parkDegree = 26

        headMotor = controller.buildServoMotor(headMotorPin, 'headMotor')
        headMotor.parkDegree = 5
        headMotor.headUpDegree = 10
        headMotor.headDownDegree = 30

        # assembly machine
        # machine = FiveBarDrawingRobot()

        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        self.headMotor = headMotor

        if path.exists(self._configFile):
            self._openConfigurationToFile()
        else:
            print("The configuration file does not exist. The robot is built with default setting")

    @property
    def drawingAreaTop(self):
        return self._drawingTop

    @property
    def headStatus(self):
        return self._headStatus

    @headStatus.setter
    def headStatus(self, value):
        self._headStatus = value

    @property
    def leftMotor(self):
        return self._leftMotor

    @leftMotor.setter
    def leftMotor(self, value):
        self._leftMotor = value
        self._leftMotor._minAngle = value.baseZeroAngle
        self._leftMotor._maxAngle = 180 + value.baseZeroAngle
        self._xMotor = value

    @property
    def rightMotor(self):
        return self._rightMotor

    @rightMotor.setter
    def rightMotor(self, value):
        self._rightMotor = value
        self._rightMotor._minAngle = value.baseZeroAngle
        self._rightMotor._maxAngle = 180 + value.baseZeroAngle
        self._yMotor = value

    @property
    def headMotor(self):
        return self._headMotor

    @headMotor.setter
    def headMotor(self, value):
        self._headMotor = value
        self._headMotor._minAngle = 0
        self._headMotor._maxAngle = 180
        self._zMotor = value

    def _waitForThreadsToFinish(self, waitTime):
        # if Constants.isDebugging:
        print('Please wait ...')
        time.sleep(waitTime)

    # Public methods
    # ----------------

    def home(self):
        self.driveTo(self.leftMotor.parkDegree, self.rightMotor.parkDegree, 1)
        self.headPark()

    def headUp(self):
        if self.headStatus != Constants.HEAD_UP:
            self.headMotor.turnTo(self.headMotor.headUpDegree)
            self.headStatus = Constants.HEAD_UP
            time.sleep(1)

    def headDown(self):
        if self.headStatus != Constants.HEAD_DOWNN:
            self.headMotor.turnTo(self.headMotor.headDownDegree)
            self.headStatus = Constants.HEAD_DOWNN
            time.sleep(1)

    def headPark(self):
        if self.headStatus != Constants.HEAD_PARK:
            self.headMotor.turnTo(self.headMotor.parkDegree)
            self.headStatus = Constants.HEAD_PARK
            time.sleep(1)

    def driveTo(self, xPos, yPos, speed=1):  # left-middle edge (155,60) right-middle edge (90,0)

        if self.headStatus != Constants.HEAD_UP:
            self.headUp()
            time.sleep(2)
        self.leftMotor.threadTurnTo(xPos, speed)
        self.rightMotor.threadTurnTo(yPos, speed)
        self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing)

    def _showDraingArea(self):
        print('Drawing Area: TopLeft ({},{}) and BottomRight({},{})'.
              format(int(-self._drawingWidth / 2), self._drawingTop, int(self._drawingWidth / 2), self._drawingBottom))

    def _pointsValidationChecking(self, points):
        for x in points:
            if x.isOutOfRange:
                input(x.errorMessage + '... press any key to continue')
                return

        for pt in points:
            if pt.byXY:

                if pt.x < - self._drawingWidth / 2 or pt.x > self._drawingWidth / 2:
                    self._showDraingArea()
                    input(
                        ' position of ({},{}) is out of valid drawing area. ...Press any key to continue...'.format(
                            pt.x, pt.y))
                    return False
                if pt.y < self._drawingBottom or pt.y > self._drawingTop:
                    self._showDraingArea()
                    input(
                        ' position of ({},{}) is out of valid drawing area. ...Press any key to continue...'.format(
                            pt.x, pt.y))
                    return False
        return True

    def drawPoints(self, points, drawingSpeed=1, movingSpeed=2, restTime=0):

        if not self._pointsValidationChecking(points):
            return

        if self.headStatus != Constants.HEAD_UP:
            self.headUp()
        for pt in points:
            if pt.mode == ToPoint.MOVING:
                self.headUp()
                speed = movingSpeed
            else:
                speed = drawingSpeed
                self.headDown()

            self._xMotor.threadTurnTo(pt.xDegree, speed, restTime)
            self._yMotor.threadTurnTo(pt.yDegree, speed, restTime)
            self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing)
        print('Head up now ,,,,')
        self.headUp()

    def moveTo(self, point):
        self.drawPoints([point])

    def drawLine(self, startPoint, endPoint, drawingSpeed=1, movingSpeed=2):
        points = [startPoint, endPoint]
        for x in points:
            if x.isOutOfRange:
                input(x.errorMessage + '... press any key to continue')
                return
        self.drawPoints(points, drawingSpeed, movingSpeed)

    def drawLines(self, points, drawingSpeed=1, movingSpeed=2):
        for x in points:
            if x.isOutOfRange:
                input(x.errorMessage + '... press any key to continue')
                return
        self.drawPoints(points, drawingSpeed, movingSpeed)

    def drawNumber(self, number, posX, posY=50, size=1, speed=1):
        points = self._generateNumberPoints(number, posX, posY, self._scale, size)
        self._pointsValidationChecking(points)
        self.drawPoints(points, speed)

    def systemCalibration(self):
        self._setupDataChanged = False
        menuTitle = 'System  Setup and Calibration'
        items = ['Pre-assembly Motor Degree Setting',
                 'Head down/up degree',
                 'Motor Base Zero Point',
                 'Machine parking Position',
                 'Drawing area identification'
                 ]

        while True:
            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                self._preAssemblyMotorSetting()
            elif rpl == 2:
                self._headDownUpPosCalibration()
            elif rpl == 3:
                self._motorBaseZeroDegreeCalibration()
            elif rpl == 4:
                self._motorParkingPosCalibration()
            elif rpl == 5:
                self._drawingAreaDetecting()
            else:
                break
        if self._setupDataChanged:
            rpl = input(' Your system setup data has been changed. Do you want to save? (y/n):\t')
            if rpl == 'y' or rpl == 'Y':
                self._saveConfigurationToFile()

    def goodByePage(self):
        print('Thank you very much for using NYP Five-Bar Drawing Robot!')

    # Private methods
    # ----------------

    def _generateNumberPoints(self, number, posX, posY, scale, size=1):
        baseW = 4
        baseH = 6
        width = baseW * size
        height = baseH * size

        points = []
        if number == 0:
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING)),
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.DRAWING))

        elif number == 1:
            points.append(ToPoint(posX + width / 2 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width / 2 * scale, posY - height, ToPoint.DRAWING))

        elif number == 2:
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING)),
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))
        elif number == 3:
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING)),
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))

        elif number == 4:
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))

        elif number == 5:

            points.append(ToPoint(posX + width * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING)),
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))

        elif number == 6:
            points.append(ToPoint(posX + width * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING))

        elif number == 7:
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))

        elif number == 8:
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING))

        elif number == 9:
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.MOVING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))

        elif number == 111:  # draw chinese word- king
            width = width * 3
            height = height
            points.append(ToPoint(posX + 0 * scale, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height / 2, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY - height / 2, ToPoint.DRAWING))
            points.append(ToPoint(posX + 0 * scale, posY - height, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale, posY - height, ToPoint.DRAWING))
            points.append(ToPoint(posX + width * scale / 2, posY, ToPoint.MOVING))
            points.append(ToPoint(posX + width * scale / 2, posY - height, ToPoint.DRAWING))
        else:
            pass
        return points

    # Calibration and setup related methods


    def _preAssemblyMotorSetting(self):
        print('---------------------------------')
        print('Pre-assembly Motor Degree Setting')
        print('---------------------------------')
        print('Left  Motor to be set  at   {}'.format(Constants.LEFT_MOTOR_ASSEMBLY_DEGREE))
        print('Right Motor to be set  at   {}'.format(Constants.RIGHT_MOTOR_ASSEMBLY_DEGREE))
        print('Head  Motor to be set  at   {}'.format(Constants.HEAD_MOTOR_ASSEMBLY_DEGREE))
        print('---------------------------------')
        rlp = input('Have you connected all motors with Arduino Board properly? (y/n)')
        if rlp == 'y':
            self.leftMotor.turnTo(Constants.LEFT_MOTOR_ASSEMBLY_DEGREE)
            self.rightMotor.turnTo(Constants.RIGHT_MOTOR_ASSEMBLY_DEGREE)
            self.headMotor.turnTo(Constants.HEAD_MOTOR_ASSEMBLY_DEGREE)
            input('All the motors have turned to specified degrees. Press ENTER to continue...')
        else:
            input('Please connect all motors with your Arduino Baord and then come back.')
            time.sleep(1)



    def _saveConfigurationToFile(self, fileName='.\\setup.dat'):
        outfile = open(fileName, "w")
        dataList = []

        x = self.leftMotor
        temp = 'leftMotor' + ',' + str(x.baseZeroAngle) + ',' + str(x.parkDegree)

        dataList.append(temp)

        x = self.rightMotor
        temp = 'rightMotor' + ',' + str(x.baseZeroAngle) + ',' + str(x.parkDegree)
        dataList.append(temp)

        x = self.headMotor
        temp = 'headMotor' + ',' + str(x.parkDegree) + ',' + str(x.headDownDegree) + ',' + str(x.headUpDegree)
        dataList.append(temp)

        temp = 'areaTop' + ',' + str(self._drawingTop)
        dataList.append(temp)

        temp = 'areaBottom' + ',' + str(self._drawingBottom)
        dataList.append(temp)

        temp = 'areaWidth' + ',' + str(self._drawingWidth)
        dataList.append(temp)

        buffer = ""
        for x in dataList:
            print(x)
            buffer = buffer + x + ','

        outfile.writelines(buffer)
        outfile.close()

    def _openConfigurationToFile(self, fileName='.\\setup.dat'):
        inFile = open(fileName, "r")
        data = inFile.readline()
        inFile.close()

        items = data.split(",")

        for i in range(len(items)):
            if items[i] == 'leftMotor':
                self.leftMotor.baseZeroAngle = int(items[i + 1])
                self.leftMotor.parkDegree = int(items[i + 2])
            if items[i] == 'rightMotor':
                self.rightMotor.baseZeroAngle = int(items[i + 1])
                self.rightMotor.parkDegree = int(items[i + 2])
            if items[i] == 'headMotor':
                self.headMotor.parkDegree = int(items[i + 1])
                self.headMotor.headDownDegree = int(items[i + 2])
                self.headMotor.headUpDegree = int(items[i + 3])
            if items[i] == 'areaTop':
                self._drawingTop = int(items[i + 1])
            if items[i] == 'areaBottom':
                self._drawingBottom = int(items[i + 1])
            if items[i] == 'areaWidth':
                self._drawingWidth = int(items[i + 1])

    def _motorRotatingTest(self):
        self.leftMotor.threadTurnPath([[30, 1, 0], [120, 1, 0], [30, 1, 0]], 3)
        self.rightMotor.threadTurnPath([[30, 1, 0], [120, 1, 0], [30, 1, 0]], 3)

    def _motorSpeedSeedSetup(self):
        menuTitle = 'Motor Speed-seed Setup '
        items = ['Try current speed ',
                 'Change speed-seed ',
                 ]
        while True:
            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                print('Current speed-seed value: {:2.5f}'.format(ServoMotor.MotorSpeedSeed))
                self._motorRotatingTest()
                self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing * 2)
                input('Wait until moving stops ... and press ENTER to continue')

            elif rpl == 2:
                print('Current speed-seed value: {:2.5f}'.format(ServoMotor.MotorSpeedSeed))
                ServoMotor.MotorSpeedSeed = float(input('Enter a new speed-seed value:\t'))
                self._setupDataChanged = True
                self._motorRotatingTest()
                self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing * 2)
                input('Wait until moving stops ... and press ENTER to continue')
            else:
                break

    def _headDownUpPosCalibration(self):
        self.driveTo(130, 60)
        while True:
            menuTitle = 'Calibration of Head Motor:'
            items = ['Head down degree  = {}'.format(self.headMotor.headDownDegree),
                     'Head up degree = {}'.format(self.headMotor.headUpDegree),
                     'Draw line to check'
                     ]
            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                self.headUp()
                while True:
                    self.headStatus = Constants.HEAD_UP
                    self.headDown()
                    choice = input('Head down degree = {}\n press A for increase: D for decrease. Q for quit:\t'.format(
                        self.headMotor.headDownDegree))
                    if choice == 'A' or choice == 'a':
                        self.headMotor.headDownDegree += 1
                        self._setupDataChanged = True
                    elif choice == 'D' or choice == 'd':
                        if self.headMotor.headDownDegree == 0:
                            input(' You have reach ZERO,no more decrease.  Press  ENTER to continue..')
                            continue
                        self.headMotor.headDownDegree -= 1
                        self._setupDataChanged = True
                    else:
                        break
            elif rpl == 2:
                self.headUp()
                while True:
                    self.headStatus = Constants.HEAD_DOWNN
                    self.headUp()
                    currentDegree = self.headMotor.headUpDegree
                    choice = input('Head up degree = {}\n press A for increase: D for decrease. Q for quit:\t'.format(
                        currentDegree))
                    if choice == 'A' or choice == 'a':
                        self.headMotor.headUpDegree += 1
                        self._setupDataChanged = True
                    elif choice == 'D' or choice == 'd':
                        if self.headMotor.headUpDegree == 0:
                            input(' You have reach ZERO,no more decrease.  Press  ENTER to continue..')
                            continue
                        self.headMotor.headUpDegree -= 1
                        self._setupDataChanged = True
                    else:
                        break
            elif rpl == 3:
                self._drawLineToCheckResult()
            else:
                return

    def _motorParkingPosAdjustment(self, motor):
        while True:
            motor.turnTo(motor.parkDegree)
            choice = input('{} parking degree = {}\n press A for increase: D for decrease. Q for quit:\t'.format(
                motor.name, motor.parkDegree))
            if choice == 'A' or choice == 'a':
                motor.parkDegree += 1
                self._setupDataChanged = True
            elif choice == 'D' or choice == 'd':
                motor.parkDegree -= 1
                self._setupDataChanged = True
            else:
                break

    def _motorParkingPosCalibration(self):
        while True:
            self.home()
            menuTitle = 'Calibration of Motor Parking Position '
            items = ['Lef Motor: parking degree  = {}'.format(self.leftMotor.parkDegree),
                     'Right Motor: parking degree = {}'.format(self.rightMotor.parkDegree),
                     'Head Motor: parking degree = {}'.format(self.headMotor.parkDegree)
                     ]
            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                self._motorParkingPosAdjustment(self.leftMotor)
            elif rpl == 2:
                self._motorParkingPosAdjustment(self.rightMotor)
            elif rpl == 3:
                self._motorParkingPosAdjustment(self.headMotor)
            else:
                return

    def _baseZeroDegreeAdjustment(self, motor):
        while True:
            motor.turnTo(90)
            currentDegree = motor.baseZeroAngle
            choice = input('{} base zero degree = {}\n press A for increase: D for decrease. Q for quit:\t'.format(
                motor.name, currentDegree))
            if choice == 'A' or choice == 'a':
                motor.baseZeroAngle += 1
                self._setupDataChanged = True
            elif choice == 'D' or choice == 'd':
                motor.baseZeroAngle -= 1
                self._setupDataChanged = True
            else:
                break

    def _drawLineToCheckResult(self):
        input('Mount the marker before press ENTER ...')
        startPt = ToPoint(-self._drawingWidth / 2, self._drawingTop - 10, ToPoint.MOVING)
        endPt = ToPoint(self._drawingWidth / 2, self._drawingTop - 10, ToPoint.DRAWING)
        self.drawPoints([startPt, endPt], 1, 2)

    def _motorBaseZeroDegreeCalibration(self):
        while True:
            self.driveTo(90, 90)
            self._waitForThreadsToFinish(Constants.waitForThreadFinishTimeForDrawing)
            menuTitle = 'Calibration of Motor Base Zero Degree:'
            items = ['Lef Motor: base zero degree = {}'.format(self.leftMotor.baseZeroAngle),
                     'Right Motor: base zero degree = {}'.format(self.rightMotor.baseZeroAngle),
                     'Draw Line to check distortion'
                     ]

            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                self._baseZeroDegreeAdjustment(self.leftMotor)
            elif rpl == 2:
                self._baseZeroDegreeAdjustment(self.rightMotor)
            elif rpl == 3:
                self._drawLineToCheckResult()

            else:
                return

    def _drawingAreaDetecting(self):

        while True:
            menuTitle = 'Identify valid drawing area'
            items = ['drawing area width   = {}'.format(self._drawingWidth),
                     'drawing area top     = {}'.format(self._drawingTop),
                     'drawing area bottom  = {}'.format(self._drawingBottom),
                     'draw a rectangle around drawing area'
                     ]
            rpl = menuGenerator(menuTitle, items)
            if rpl == 1:
                while True:
                    print('The current drawing area width is {}'.format(self._drawingWidth))
                    self.drawLine(ToPoint(-self._drawingWidth / 2, self._drawingTop, ToPoint.MOVING),
                                  ToPoint(self._drawingWidth / 2, self._drawingTop, ToPoint.DRAWING))
                    choice = input('Press A for adding 5;D for decreasing 5; Q for quit ')
                    if choice == 'A' or choice == 'a':
                        self._drawingWidth += 4
                        self._setupDataChanged = True
                    elif choice == 'D' or choice == 'd':
                        self._drawingWidth -= 4
                        self._setupDataChanged = True
                    else:
                        break
            elif rpl == 2:
                while True:
                    print('The current drawing area Top is {}'.format(self._drawingTop))
                    self.drawLine(ToPoint(-self._drawingWidth / 2, self._drawingTop, ToPoint.MOVING),
                                  ToPoint(self._drawingWidth / 2, self._drawingTop, ToPoint.DRAWING))
                    choice = input('Press A for adding 5;D for decreasing 5; Q for quit ')
                    if choice == 'A' or choice == 'a':
                        self._drawingTop += 5
                        self._setupDataChanged = True
                    elif choice == 'D' or choice == 'd':
                        self._drawingTop -= 5
                        self._setupDataChanged = True
                    else:
                        break
            elif rpl == 3:
                while True:
                    print('The current drawing area Bottom is {}'.format(self._drawingBottom))
                    self.drawLine(ToPoint(-self._drawingWidth / 2, self._drawingBottom, ToPoint.MOVING),
                                  ToPoint(self._drawingWidth / 2, self._drawingBottom, ToPoint.DRAWING))
                    choice = input('Press A for adding 5;D for decreasing 5; Q for quit ')
                    if choice == 'A' or choice == 'a':
                        self._drawingBottom += 5
                        self._setupDataChanged = True
                    elif choice == 'D' or choice == 'd':
                        self._drawingBottom -= 5
                        self._setupDataChanged = True
                    else:
                        break
            elif rpl == 4:
                input('Mount a marker on the robot head before press ENTER...')
                pointList = []
                topLeft = ToPoint(-self._drawingWidth / 2, self._drawingTop, ToPoint.MOVING)
                topRight = ToPoint(self._drawingWidth / 2, self._drawingTop, ToPoint.DRAWING)
                bottomRight = ToPoint(self._drawingWidth / 2, self._drawingBottom, ToPoint.DRAWING)
                bottomLeft = ToPoint(-self._drawingWidth / 2, self._drawingBottom, ToPoint.DRAWING)
                backToTopLeft = ToPoint(-self._drawingWidth / 2, self._drawingTop, ToPoint.DRAWING)
                pointList = [topLeft, topRight, bottomRight, bottomLeft, backToTopLeft]
                self.drawPoints(pointList)

            else:
                break


class ToPoint:
    MOVING = 1
    DRAWING = 2

    def __init__(self, x, y, mode, byXY=True):
        self._byXY = byXY
        self._x = x
        self._y = y
        self._mode = mode
        self._isOutOfRange = False
        self._errorMessage = None
        self._calculator = FiveBarRobotCalculator()
        self._xDegree = x
        self._yDegree = y
        if byXY:
            try:
                self._xDegree = self._calculator.coordinatesToDegree(x, y)[0]
                self._yDegree = self._calculator.coordinatesToDegree(x, y)[1]
            except Exception as e:
                print(e)
                self._isOutOfRange = True
                self._errorMessage = 'Coordinates of ({:2.2f}, {:2.2f}) is out of range'.format(x, y)
        else:
            if x < 0 or x > 180 or y < 0 or y > 180:
                self._isOutOfRange = True
                self._errorMessage = 'degree of {:2.2f} of leftMotor and {:2.2f} of rightMotor is out of range'.format(
                    x, y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._y = value

    @property
    def xDegree(self):
        return self._xDegree

    @property
    def yDegree(self):
        return self._yDegree

    @property
    def byXY(self):
        return self._byXY

    @property
    def isOutOfRange(self):
        return self._isOutOfRange

    @property
    def errorMessage(self):
        return self._errorMessage


class FiveBarRobotCalculator:
    def __init__(self):
        self._leftLowArmLength = 35
        self._leftUpperArmLength = 45
        self._rightLowArmLength = 35
        self._rightUpperArmLength = 45
        self._baseArmLength = 25
        self._baseArmLeftEndx = - self._baseArmLength / 2
        self._baseArmRightEndx = self._baseArmLength / 2
        self._baseArmLeftEndy = 0
        self._baseArmRightEndy = self._baseArmLeftEndy
        self._leftMotorInitalDegree = 0
        self._rightMotorInitialDegree = 0

    def returnAngle(self, side1, side2, face):
        # print({'side1 = {:2.2f}  side2 = {:2.2f}  side3 = {:2.2f}'.format(side1, side2, face)})
        return math.acos((side1 * side1 + side2 * side2 - face * face) / (2 * side1 * side2))

    def coordinatesToDegree(self, x, y):
        caseMessage = []
        if x < self._baseArmLeftEndx:
            caseMessage.append(' when x < baseLeftEndX ')
            caseMessage.append('calculate xMotor when x < baseLeftEndX ')
            dx = abs(x - self._baseArmLeftEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            a1 = math.atan2(dy, dx)
            caseMessage.append('for a2: c = {:2.2f}'.format(c))
            a2 = self.returnAngle(self._leftLowArmLength, c, self._leftUpperArmLength)
            xDegree = 180 - math.degrees(a1 - a2)
            caseMessage.append('dx={:2.2f},dy={:2.2f},c={:2.2f},a1={:2.2f},a2={:2.2f},degree={:2.2f}'.format(dx, dy, c,
                                                                                                             math.degrees(
                                                                                                                 a1),
                                                                                                             math.degrees(
                                                                                                                 a2),
                                                                                                             xDegree))
            caseMessage.append('calculate yMotor when x < baseLeftEndX ')
            dx = abs(x - self._baseArmRightEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            b1 = math.atan2(dy, dx)
            caseMessage.append('for b2: c = {:2.2f}'.format(c))
            b2 = self.returnAngle(self._rightLowArmLength, c, self._rightUpperArmLength)
            yDegree = 180 - math.degrees(b1 + b2)
            # return [xDegree,yDegree]
            caseMessage.append('dx={:2.2f},dy={:2.2f},c={:2.2f},b1={:2.2f},b2={:2.2f},degree={:2.2f}'.format(dx, dy, c,
                                                                                                             math.degrees(
                                                                                                                 b1),
                                                                                                             math.degrees(
                                                                                                                 b2),
                                                                                                             yDegree))
        elif x == self._baseArmLeftEndx:
            caseMessage.append('when x == baseLeftEndX')
            caseMessage.append('calculate xMotor when x == baseLeftEndX')
            c = abs(y - self._baseArmLeftEndy)
            a1 = math.pi / 4
            a2 = self.returnAngle(self._leftLowArmLength, c, self._leftUpperArmLength)
            xDegree = 180 - math.degrees(a1 - a2)
            caseMessage.append('calculate yMotor when x == baseLeftEndX ')
            dx = self._baseArmLength
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            a1 = math.atan2(dy, dx)
            a2 = self.returnAngle(self._rightLowArmLength, c, self._rightUpperArmLength)
            yDegree = 180 - math.degrees(a1 + a2)
            # return [xDegree, yDegree]

        elif x < self._baseArmRightEndx:
            caseMessage.append('when x > baseLeftEndX and  x < baseRightEndX ')
            caseMessage.append('calculate xMotor when x > baseLeftEndX and  x < baseRightEndX ')
            dx = abs(x - self._baseArmLeftEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            a1 = math.atan2(dy, dx)
            a2 = self.returnAngle(self._leftLowArmLength, c, self._leftUpperArmLength)
            xDegree = math.degrees(a1 + a2)

            caseMessage.append('dx={:2.2f},dy={:2.2f},c={:2.2f},a1={:2.2f},a2={:2.2f},degree={:2.2f}'.format(dx, dy, c,
                                                                                                             math.degrees(
                                                                                                                 a1),
                                                                                                             math.degrees(
                                                                                                                 a2),
                                                                                                             xDegree))

            caseMessage.append('calculate yMotor when x > baseLeftEndX and  x < baseRightEndX ')
            dx = abs(x - self._baseArmRightEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            b1 = math.atan2(dy, dx)
            b2 = self.returnAngle(self._rightLowArmLength, c, self._rightUpperArmLength)
            yDegree = 180 - math.degrees(b1 + b2)

            caseMessage.append('dx={:2.2f},dy={:2.2f},c={:2.2f},b1={:2.2f},b2={:2.2f},degree={:2.2f}'.format(dx, dy, c,
                                                                                                             math.degrees(
                                                                                                                 b1),
                                                                                                             math.degrees(
                                                                                                                 b2),
                                                                                                             yDegree))
            # return [xDegree,yDegree]
        elif x == self._baseArmRightEndx:
            caseMessage.append('when x == baseRightEndX ')
            caseMessage.append('calculate xMotor when x == baseRightEndX ')
            dx = x - self._baseArmLeftEndx
            dy = y - self._baseArmLeftEndy
            c = math.sqrt(dx * dx + dy * dy)
            a1 = math.atan2(dy, dx)
            a2 = self.returnAngle(self._leftLowArmLength, c, self._leftUpperArmLength)
            xDegree = math.degrees(a1 + a2)
            caseMessage.append('calculate yMotor when x == baseRightEndX ')
            dy = abs(y - self._baseArmLeftEndx)
            c = dy
            b1 = math.pi / 4
            b2 = self.returnAngle(self._rightLowArmLength, c, self._rightUpperArmLength)
            yDegree = 180 - math.degrees(b1 + b2)
            # return [xDegree,yDegree]
        elif x > self._baseArmRightEndx:
            caseMessage.append('when x > baseRightEndX ')
            caseMessage.append('calculate xMotor when x > baseRightEndX ')
            dx = abs(x - self._baseArmLeftEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            a1 = math.atan2(dy, dx)
            a2 = self.returnAngle(self._leftLowArmLength, c, self._leftUpperArmLength)
            xDegree = math.degrees(a1 + a2)
            caseMessage.append('calculate yMotor when x > baseRightEndX ')
            dx = abs(x - self._baseArmRightEndx)
            dy = abs(y - self._baseArmLeftEndy)
            c = math.sqrt(dx * dx + dy * dy)
            b1 = math.atan2(dy, dx)
            b2 = self.returnAngle(self._rightLowArmLength, c, self._rightUpperArmLength)
            yDegree = math.degrees(b1 - b2)
            # return [xDegree, yDegree]

        else:
            raise Exception('wrong coordinate value')

        leftAngle = math.floor(xDegree - self._leftMotorInitalDegree)
        rightAngle = math.floor(yDegree - self._rightMotorInitialDegree)
        # for x in caseMessage:
        #     print(x)
        return [leftAngle, rightAngle]



# def drawNumber():
#     while True:
#         # machine.headUp()
#         xPos = int(input('enter posX for writing:\t'))
#         size = int(input('enter size of number: 1 - 4 :\t'))
#         num = int(input('enter a number between 0 - 9:\t'))
#         robot.drawNumber(num, xPos, robot.drawingAreaTop, size, 2)
#         # machine.headUp()
#         if input('Try again?(y/n)') != 'y':
#             robot.headUp()
#             break


# def writeNumbers(no):  # number less than 3 digits
#
#     sNo = input('input a number between 0 to 999: \t')
#     if len(sNo) == 3:
#         startPos = -20
#     elif len(sNo) == 2:
#         startPos = -10
#     else:
#         startPos = 0
#
#     for x in range(len(sNo)):
#         robot.drawNumber(int(sNo[x]), startPos + x * 15, robot.drawingAreaTop, 2)