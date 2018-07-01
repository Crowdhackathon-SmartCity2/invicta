
import time
import random
import csv
from graphics import *
##lane_A = {"waiting":0,"count":randint(10,20),"size":randint(3,5),"id":0,"master":True,"move":True,"rank":0,"maturation_factor":0} If you uncomment these and comment the following ones
##lane_B = {"waiting":0,"count":randint(1,10),"size":randint(1,2),"id":1,"master":False,"move":False,"rank":0,"maturation_factor":0} you can get the algorith's functionality on random data
lane_A = {"waiting":0,"count":0,"size":1,"id":0,"master":True,"move":True,"rank":0,"maturation_factor":0}
lane_B = {"waiting":0,"count":0,"size":1,"id":1,"master":False,"move":False,"rank":0,"maturation_factor":0}
data_A = {}
data_B = {}
win = GraphWin('Face', 800, 700)
pt_A_R = Point(25, 25)
cir_A_R = Circle(pt_A_R, 25)
cir_A_R.setOutline('red')
cir_A_R.setFill('red')
cir_A_R.draw(win)
pt_A_G = Point(25, 80)
cir_A_G = Circle(pt_A_G, 25)
cir_A_G.setOutline('green')
cir_A_G.setFill('green')
cir_A_G.draw(win)

pt_B_R = Point(775, 25)
cir_B_R = Circle(pt_B_R , 25)
cir_B_R.setOutline('red')
cir_B_R.setFill('red')
cir_B_R.draw(win)
pt_B_G = Point(775, 80)
cir_B_G = Circle(pt_B_G, 25)
cir_B_G.setOutline('green')
cir_B_G.setFill('green')
cir_B_G.draw(win)
def lane_A_tf(lane_A):
    cir_A_R.undraw()
    cir_A_G.undraw()
    cir_B_R.undraw()
    cir_B_G.undraw()

    color_A_green = 'white'
    color_A_red = 'white'
    color_B_green = 'white'
    color_B_red = 'white'
    if(lane_A["move"]):
        color_A_green = 'green'
        color_B_red = 'red'
    else:
        color_B_green = 'green'
        color_A_red = 'red'
    cir_A_G.setFill(color_A_green)
    cir_B_R.setFill(color_B_red)
    cir_B_G.setFill(color_B_green)
    cir_A_R.setFill(color_A_red)
    cir_A_R.draw(win)
    cir_A_G.draw(win)
    cir_B_R.draw(win)
    cir_B_G.draw(win)
with open('data_A.csv', mode='r') as infile:
    reader = csv.reader(infile,delimiter=',', quotechar='"')
    for row in reader:
        if row:
            data_A[int(row[0])]=int(row[1])
with open('data_B.csv', mode='r') as infile:
    reader = csv.reader(infile,delimiter=',', quotechar='"')
    for row in reader:
        if row:
            data_A[int(row[0])]=int(row[1])
def add_cars(lane_A,lane_B,cars_A,cars_B):
    lane_A["count"]+=cars_A
    lane_B["count"]+=cars_B
    return lane_A,lane_B
def coordinate(lane_A,lane_B):

    if(lane_A["count"]>lane_B["count"]):
        lane_A["rank"]+=1
    elif(lane_A["count"]<lane_B["count"]):
        lane_B["rank"]+=1
    lane_A["master"] = lane_A["rank"] >= lane_B["rank"]
    lane_B["master"] = (not lane_A["master"])
    if(lane_A["move"]):
        lane_A["waiting"] = 0
        lane_A["count"] -= lane_A["size"]
        if (lane_A["count"]<0):
            lane_A["count"]=0
            lane_A["maturation_factor"]=0
    else:
        lane_A["waiting"] +=1
        lane_A["maturation_factor"]=lane_A["count"]* ((lane_A["rank"]+1)/(lane_B["rank"]+lane_A["rank"]+1)) *  (lane_A["waiting"]/10)/(abs(lane_A["count"]-lane_B["count"]+1))

    if(lane_B["move"]) :
        lane_B["waiting"] = 0
        lane_B["count"] -= lane_B["size"]
        if (lane_B["count"]<0):
            lane_B["count"]=0
            lane_B["maturation_factor"]=0
    else:
        lane_B["waiting"] +=1
        lane_B["maturation_factor"]=lane_B["count"] * ((lane_B["rank"]+1)/(lane_B["rank"]+lane_A["rank"]+1)) * (lane_B["waiting"]/10)/(abs(lane_A["count"]-lane_B["count"]+1))
    return lane_A,lane_B

##def add_random_cars(lane_a,lane_B): Use this instead of add_car to get random data functionality
##	lane_A["count"] += random.randint(0,lane_A["size"])
##	lane_B["count"] += random.randint(0,lane_B["size"])

def change_move(lane_A,lane_B,light_session):
    temp = lane_A["move"]
    lane_A["move"]=lane_A["maturation_factor"]>=lane_B["maturation_factor"]
    lane_B["move"]= (not lane_A["move"])
    if (temp != lane_A["move"]):
        if (lane_A["move"]):
            print("\n\n\n\n\nLight switch! \n Lane A gets the green light. \n Lane B is put on hold. \n Previous green light period was ",light_session," seconds. \n\n\n\n\n")
            lane_A["waiting"] = 0
            lane_B["waiting"] =  1
            light_session = 0
        else:
            print("\n\n\n\n\nLight switch! \n Lane B gets the green light. \n Lane A is put on hold. \n Previous green light period was ",light_session," seconds. \n\n\n\n\n")
            light_session = 0
            lane_A["waiting"] = 1
            lane_B["waiting"] = 0


    return lane_A,lane_B,light_session

lane_A["master"]= lane_A["count"] >= lane_B["count"]
lane_A["move"] = lane_A["master"]
lane_B["master"] = (not lane_A["move"])
lane_B["move"] = lane_B["master"]
time_elapsed = 0
light_session = 0
time_delay = 0
data =[]
while True:
    if time_elapsed in (list(data_A.keys())):
        add_cars(lane_A,lane_B,data_A[time_elapsed],0)
    if time_elapsed in (list(data_B.keys())):
        add_cars(lane_A,lane_B,0,data_B[time_elapsed])
    if(time_delay>=1000):
        lane_A_tf(lane_A)
##	add_random_cars(lane_A,lane_B)  ##invert the commented with the uncommented to get rng data functionality
        lane_A,lane_B = coordinate(lane_A,lane_B)
        if ((lane_A["count"]==0) or (lane_B["count"]==0)):
            lane_A,lane_B,light_session = change_move(lane_A,lane_B,light_session)
        if (lane_A["waiting"]>5) or (lane_B["waiting"] > 5):
            lane_A,lane_B,light_session = change_move(lane_A,lane_B,light_session)
        time_delay = 0
        print ("Time:"+str(time_elapsed))
        print ("A:" + str(lane_A))
        print ("B:" + str(lane_B))
        data.append({"time":time,"A":lane_A,"B":lane_B})

    else:
        time_delay+=1
    time_elapsed +=1
    light_session +=1
    time.sleep(0.001)
