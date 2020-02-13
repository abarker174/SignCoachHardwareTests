#! /usr/bin/env python3
# Core imports
import time
import ev3dev.ev3 as ev3

print ('Welcome to ev3')

p = ev3.LargeMotor('outA')
m = ev3.LargeMotor('outB')
w = ev3.MediumMotor('outC')
ts = ev3.TouchSensor()

def runTo(motors, positions):
    n = 6 #more iterations means higher cutoff of imprecision and speed
    threshold = 15 #lower threshold means it gets closer before stopping
    for j in range(n):
        sum = 0
        for i in range(len(motors)):
            current = motors[i].position
            diff = current - positions[i]
            sum = sum + abs(diff)
            motors[i].run_to_abs_pos(position_sp=positions[i],speed_sp=diff)
        print(str(j) + " " + str(sum))
        if sum < threshold:
            break
        time.sleep(0.6) #longer time means more granular slow-down - multiply with n for max time

class Position:
    p_pos = 0
    m_pos = 0
    w_pos = 0
    name = ""
    
    def __init__(self, p, m, w, name):
        self.p_pos = p
        self.m_pos = m
        self.w_pos = w
        self.name = name
    
    def move(self):
        runTo([m,p,w],[self.m_pos,self.p_pos,self.w_pos])
        #runTo(m,self.m_pos,30)
        #runTo(p,self.p_pos,120)
        #runTo(w,self.w_pos,80)
    
    def setPos(self, p, m, w):
        self.p_pos = p
        self.m_pos = m
        self.w_pos = w
    
    def toString(self):
        return self.name + " Values: P: " + str(self.p_pos) + ", M: " + str(self.m_pos) + ", W: " + str(self.w_pos)

home = Position(0, 0, 0, "Home")
current = Position(0,0,0,"Current")

if not (p.connected):
	print("Plug the pointer motor into Port A")
elif (not (m.connected)):
	print("Plug the main joint motor into Port B")
elif not (w.connected):
	print("Plug the waggle motor into Port C")
elif not (ts.connected):
    print("Plug in a touch sensor")
else:
    
    print("All Motors and Sensors Connected, Tap to set Home Position")
    print("ts.value: " + str(ts.value()))
    print("Touch to Set Values")
    while ts.value() == 0:
        current.setPos(p.position,m.position,w.position)
        print(current.toString())
        time.sleep(1)
    home.setPos(p.position, m.position, w.position)
    A = Position(p.position+800,m.position-69,w.position+0,"AIJSY - Fully Curled")
    B = Position(p.position+0,m.position+0,w.position+0,"BDLU - Fully Straight")
    C = Position(p.position+714,m.position+0,w.position+0,"CTX - Pointer Curled")
    E = Position(p.position+977,m.position-37,w.position+0,"EO - Half Curled")
    F = Position(p.position+380,m.position-69,w.position+0,"FGHMNPQ - Main Curled")
    K = Position(p.position+0,m.position+0,w.position-80,"KVW - Waggled Right")
    R = Position(p.position+300,m.position+0,w.position+80,"R - Waggled Left")
    basic_homed_positions = [home, A, home, B, home, C, home, E, home, F, home, K, home, R, home]
    basic_positions = [home,A,B,C,E,F,K,R,home]
    alphabet_positions = [home, A, B, C, B, E, F, F, F, A, A, K, B, F, F, E, F, F, R, A, C, B, K, K, C, A, F, home]
    home_position = [home]
    print("Home Set.")
    print(home.toString())
    #positions = alphabet_positions
    positions = basic_positions
    while ts.value() == 1:
        time.sleep(0.5)
    while True:
        for position in positions:
            print("Next: " + position.name)
            while ts.value() == 0:
                time.sleep(0.1)
            print("Moving To: " + position.name)
            print("---------")
            position.move()
            while ts.value() == 1:
                time.sleep(0.1)
            #out of button press
        #out of for loop
    #out of while loop - unreachable
#out of else block - program end