import can
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)

#GPIO.output(22, True)


bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
can.rc['interface'] = 'sokcetcan_native'


GPIO.output(22, True)

for msg in bus:

    assert isinstance(msg, can.Message)
    if msg.arbitration_id == 0x000:
        GPIO.output(22, True)

    else:
        GPIO.output(22, False)
    print(msg)

