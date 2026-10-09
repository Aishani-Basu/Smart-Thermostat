import machine

def moon_device_control(pin, state):
    pin_obj = machine.Pin(pin, machine.Pin.OUT)
    pin_obj.value(1 if state else 0)
    print(f"LED on pin {pin} turned {'on' if state else 'off'}")
    
def moon_servo_control(servo_pin, servo_angle):
    servo = machine.PWM(machine.Pin(servo_pin), freq = 50)
    duty_cycle = int((servo_angle / 180) * (115 - 40) + 40)
    print(duty_cycle)
    print(type(duty_cycle))
    servo.duty(duty_cycle)
    print(f"Servo on pin {servo_pin} set to {servo_angle} degrees")