import time
from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor

controller = ControlBoard('COM3')  # Change com number as necessary

toilet_paper_checker = controller.buildDigitalInput(2, 'irSensor2')
irSensor = controller.buildDigitalInput(3, 'irSensor')
redLED = controller.buildDigitalOutput(6, 'redLED')
greenLED = controller.buildDigitalOutput(7, 'greenLED')
button = controller.buildDigitalInput(8, 'Button')
buzzer = controller.buildDigitalOutput(9, 'Buzzer')

tolietpapermove = controller.buildServoMotor(11, 'xMotor')
tolietpapermove.homePos = 0
tolietpapermove.minAngle = 0
tolietpapermove.maxAngle = 180

motormover = controller.buildServoMotor(13, 'yMotor')
motormover.homePos = 0
motormover.minAngle = 0
motormover.maxAngle = 180

monitor = controller.buildInputMonitor()
controller.start()
monitor.start()

while True:
    if irSensor.getCountValue() >= 1:
        greenLED.turnOn() #green light indicates device is trying to output toilet paper
        for x in range(0,2):
            motormover.turnTo(30, 1)
            tolietpapermove.turnTo(180, 1)
            motormover.turnTo(0, 1)
            tolietpapermove.turnTo(0, 1)
            motormover.turnTo(30, 1)
            tolietpapermove.turnTo(130, 1)
            motormover.turnTo(0, 1)
            tolietpapermove.turnTo(0, 1)
            if toilet_paper_checker.getCountValue() >= 1: # there is toilet paper dectected to be outputted
                redLED.turnOff()
            elif toilet_paper_checker.getCountValue() == 0: # there is no toilet paper being outputted
                redLED.turnOn() #red light indiciates a problem, either no toilet paper or stuck
                buzzer.turnOn()
                time.sleep(2)  # buzzer is buzzing for  2 secs
                buzzer.turnOff()
            if button.getCountValue() >= 1:  # to stop the device
                break
        greenLED.turnOff()  # indictaes that device has stopped outputting toilet paper
        time.sleep(4) #time for user to take the outputted toilet paper
    if button.getCountValue() >= 1: #stops the device
        break
print("system stopping")
motormover.turnTo(55, 1)
tolietpapermove.turnTo(180, 1)
greenLED.turnOff()
controller.shutdown()