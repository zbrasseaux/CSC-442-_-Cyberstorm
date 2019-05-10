from pynput.keyboard import Key, Controller
from time import sleep
from random import uniform
from termios import tcflush, TCIFLUSH
from sys import stdin, stdout

keyboard = Controller()

password = raw_input()
password = password.split(",")
password = password[:len(password)/2+1]
password = "".join(password)

timings = raw_input()
timings = timings.split(",")
timings = [float(a) for a in timings]

keypress = timings[:len(timings)/2+1]
keyinterval = timings[len(timings)/2:]
keyinterval.append(0.0)

i = 0

for char in password:
    keyboard.press(char)
    sleep(keypress[i])
    keyboard.release(char)
    sleep(keyinterval[i])
    i+=1

tcflush(stdin, TCIFLUSH)