import re
import datetime
from asciimatics.screen import Screen
import textwrap
# Globals
viewMode = 0  # 0:day 1:week 2:month
todayDate = datetime.date.today()
dayDelta = 0
calFile = []
# today += datetime.timedelta(days=7)
# date=today.strftime("%d/%m/%Y")

# open calendar


def openCal(name):
    calFile = open(name, "r").read().split("\n")
    for i in range(len(calFile)):
        calFile[i] = calFile[i].split(",")
    return calFile


calFile = openCal("cal.csv")

# find all events on a day


def findDay(day):
    global calFile
    output = []
    for i in range(len(calFile)):
        if calFile[i][0] == day:
            output.append(calFile[i])
    return output

# sort series of events by time


def daySort(a):
    for i in range(len(a)):
        replaceable = (re.split(":| ", a[i][1]))
        if replaceable[2] == "PM":
            PMint = 12
        else:
            PMint = 0
        z = int(replaceable[1])/60
        a[i].append(int(replaceable[0])+z+PMint)
    # for i in range(len(a)):
    #    elm = a[i]
    #    j = i-1
    #    while j > 0 and a[j][4] < elm[4]:
    #        a[j+1] = a[j]
    #        j = j-1
    #    a[j+1] = elm
    #a = a[::-1]
    a = sorted(a, key=lambda x: x[4])
    return a


def dayDraw(screen, day, maxWidth,location):
    screen.print_at(day, 17, 0)
    events = daySort(findDay(day))
    for i in range(24):
        allEvent = ""
        for j in range(len(events)):
            replaceable = (re.split(":| ", events[j][1]))
            if replaceable[2] == "PM":
                PMint = 12
            else:
                PMint = 0
            z = int(replaceable[0])+PMint
            if z == i:
                allEvent += events[j][2]+" @ "+events[j][1]+" | "
        allEvent=textwrap.shorten(allEvent, width=maxWidth, placeholder="..")
        screen.print_at(allEvent, location, i+1, 5)


def dateDraw(screen):
    screen.print_at('████████████████', 0, 0, 7)
    for i in range(24):
        if i < 12:
            if i == 0:
                meridian = "AM"
                x = "12"
            else:
                meridian = "AM"
                x = i
        else:
            mTwelve = i-12
            if mTwelve == 0:
                x = 12
            else:
                x = mTwelve
            meridian = "PM"
        timeBlock = str(x)+":00 "+meridian
        lenTime = 10-len(timeBlock)
        for j in range(lenTime):
            timeBlock = timeBlock+" "
        screen.print_at('██ '+timeBlock+'███', 0, i+1, 7)
    screen.print_at('████████████████', 0, i+2, 7)

def weekDraw(screen,days):
    maxWidth=screen.width-16
    maxWidth=maxWidth//7
    for i in range(1,8):
        x=maxWidth-len(days[i-1])
        x=x//2
        y=i-1
        z=maxWidth*y
        z+=16
        x=x+z
        screen.print_at(days[i-1],x,0,7)
        dayDraw(screen,days[i-1],maxWidth-1,z)


def adder(screen):
    charecters = ""
    while len(charecters) < 10:
        ev = screen.get_key()
        if ev != None:
            charecters = charecters+chr(ev)
    return charecters


def dayViewExe(screen):
    global viewMode
    global dayDelta
    global todayDate
    viewMode = 0
    tempDate = todayDate + datetime.timedelta(days=dayDelta)
    currentDate = tempDate.strftime("%d/%m/%Y")
    screen.clear()
    dateDraw(screen)
    dayDraw(screen, currentDate,screen.width-17,17)

def weekViewExe(screen):
    #monday = now - timedelta(days = now.weekday())
    global viewMode
    global dayDelta
    global todayDate
    viewMode = 1
    tempDate = todayDate + datetime.timedelta(days=dayDelta)
    tempDate=tempDate-datetime.timedelta(days=tempDate.weekday())
    currentDate = []
    for i in range(7):
        currentDate.append(tempDate.strftime("%d/%m/%Y"))
        tempDate=tempDate+datetime.timedelta(1)
    screen.clear()
    dateDraw(screen)
    weekDraw(screen, currentDate)

def menu(screen):
    global viewMode
    global dayDelta
    global todayDate
    while True:
        screen.print_at(
            "Day(0) | Week (1) | Add Event(a) | Delete Event(d) | View Event(v) | Previous(p) | Next (n) | Go To Date(g) | Quit(q)", 0, screen.height-1, 2)
        ev = screen.get_key()
        if ev == ord("0"):
            dayViewExe(screen)
            break
        elif ev == ord("1"):
            weekViewExe(screen)
            break
        elif ev == ord("a"):
            screen.clear()
            #"Add Event"
            screen.print_at(adder(screen), 20, screen.height-5, 1)
            break
        elif ev == ord("d"):
            screen.clear()
            screen.print_at("Delete Event", 20, screen.height-5, 1)
            break
        elif ev == ord("v"):
            #viewMode(screen)
            break
        elif ev == ord("p"):
            screen.clear()
            screen.print_at("Previous", 20, screen.height-5, 1)
            break
        elif ev == ord("n"):
            screen.clear()
            screen.print_at("Next", 20, screen.height-5, 1)
            break
        elif ev == ord("g"):
            screen.clear()
            screen.print_at("Go To Date", 20, screen.height-5, 1)
            break
        elif ev == ord("q"):
            quit()

        screen.refresh()


def main(screen):
    dayViewExe(screen)
    while True:
        dateDraw(screen)
        ev = screen.get_key()
        screen.print_at("Change Mode(;)", 0, screen.height-1, 2)
        # Day(0) | Week (1) | Add Event(a) | Delete Event(d) | View Event(v) | Previous(←) | Next (→) | Set Date(s)
        if ev == ord(";"):
            menu(screen)
        else:
            screen.refresh()


# def main():
#    global viewMode
#    global todayDate
#    global dayDelta
#    while True:
#        option = input(
#            "Day(0) | Week (1) | Add Event(a) | Delete Event(d) | View Event(v) | Previous(←) | Next (→) | Set Date(s) ").lower()
#        if option == "0":
#            viewMode = 0
#            tempDate = todayDate + datetime.timedelta(days=dayDelta)
#            currentDate = tempDate.strftime("%d/%m/%Y")
#            dayDraw(currentDate)
#        elif option == "1":
#            viewMode = 1
#            tempDate = todayDate + datetime.timedelta(days=dayDelta)
#            currentDate = tempDate.strftime("%d/%m/%Y")
#            weekPrint(tempDate)
#        elif option == "a":
#            addEvent()
#        elif option == "d":
#            delEvent()
#        elif option == "v":
#            viewEvent()
#        elif option == "s":
#            dayDraw("1/1/1")
#        elif option == "p":
#            if viewMode == 0:
#                dayDelta += 1
#                tempDate = todayDate + datetime.timedelta(days=dayDelta)
#                currentDate = tempDate.strftime("%d/%m/%Y")
#                dayDraw(currentDate)
#            elif viewMode == 1:
#                dayDelta += 7
#                tempDate = todayDate + datetime.timedelta(days=dayDelta)
#                currentDate = tempDate.strftime("%d/%m/%Y")
#                weekPrint(tempDate)
#        elif option == "n":
#            if viewMode == 0:
#                dayDelta -= 1
#                tempDate = todayDate + datetime.timedelta(days=dayDelta)
#                currentDate = tempDate.strftime("%d/%m/%Y")
#                dayDraw(currentDate)
#            elif viewMode == 1:
#                dayDelta -= 7
#                tempDate = todayDate + datetime.timedelta(days=dayDelta)
#                currentDate = tempDate.strftime("%d/%m/%Y")
#                weekPrint(tempDate)
#        else:
#            print("No Such Option")

Screen.wrapper(main)
