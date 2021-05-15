import re
import datetime
from asciimatics.screen import Screen
import textwrap
import string
from time import sleep
# Globals
viewMode = 0  # 0:day 1:week 2:month
todayDate = datetime.date.today()
dayDelta = 0
calFile = ['date', 'time', 'name', 'description']
# today += datetime.timedelta(days=7)
# date=today.strftime("%d/%m/%Y")

# open calendar


def openCal(name):
    calFile = open(name, "r").read().split("\n")
    for i in range(len(calFile)):
        calFile[i] = calFile[i].split(",")
    return calFile


def saveCal(name):
    global calFile
    output = ""
    for event in calFile:
        print(event)
        output += ",".join(event[0:4])+"\n"
    print(output)
    outputFile = open(name, "w")
    outputFile.write(output)
    outputFile.close()


calName = "cal.csv"
calFile = openCal(calName)

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


def dayDraw(screen, day, maxWidth, location):
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
        allEvent = textwrap.shorten(allEvent, width=maxWidth, placeholder="..")
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


def weekDraw(screen, days):
    maxWidth = screen.width-16
    maxWidth = maxWidth//7
    for i in range(1, 8):
        x = maxWidth-len(days[i-1])
        x = x//2
        y = i-1
        z = maxWidth*y
        z += 16
        x = x+z
        screen.print_at(days[i-1], x, 0, 7)
        dayDraw(screen, days[i-1], maxWidth-1, z)


def dayViewExe(screen):
    global viewMode
    global dayDelta
    global todayDate
    viewMode = 0
    tempDate = todayDate + datetime.timedelta(days=dayDelta)
    currentDate = tempDate.strftime("%d/%m/%Y")
    screen.clear()
    dateDraw(screen)
    dayDraw(screen, currentDate, screen.width-17, 17)


def weekViewExe(screen):
    #monday = now - timedelta(days = now.weekday())
    global viewMode
    global dayDelta
    global todayDate
    viewMode = 1
    tempDate = todayDate + datetime.timedelta(days=dayDelta)
    tempDate = tempDate-datetime.timedelta(days=tempDate.weekday())
    currentDate = []
    for i in range(7):
        currentDate.append(tempDate.strftime("%d/%m/%Y"))
        tempDate = tempDate+datetime.timedelta(1)
    screen.clear()
    dateDraw(screen)
    weekDraw(screen, currentDate)


def crapInput(screen, height):
    charecters = ""
    while True:
        ev = screen.get_key()
        print(ev)
        if ev == -301:
            return charecters
        elif ev == -300:
            charecters = charecters[:-1]
            screen.print_at(charecters+" ", 0, height, 6)
            screen.refresh()
        elif ev != None and ev not in [-203, -205, -204, -206, -300, -207, -208, -102, -1]:
            charecters = charecters+chr(ev)
            screen.print_at(charecters, 0, height, 6)

            screen.refresh()


def viewEvent(screen):
    global viewMode
    global dayDelta
    global todayDate
    global calFile
    screen.clear()
    if viewMode == 1:
        tempDate = todayDate + datetime.timedelta(days=dayDelta)
        tempDate = tempDate-datetime.timedelta(days=tempDate.weekday())
        currentDate = []
        screen.clear()
        for i in range(7):
            currentDate.append(tempDate.strftime("%d/%m/%Y"))
            screen.print_at(str(i)+": "+tempDate.strftime("%d/%m/%Y"), 0, i, 7)
            tempDate = tempDate+datetime.timedelta(1)
        screen.refresh()
        inp = 0
        while True:
            ev = screen.get_key()
            if ev == ord("0"):
                inp = 0
                break
            elif ev == ord("1"):
                inp = 1
                break
            elif ev == ord("2"):
                inp = 2
                break
            elif ev == ord("3"):
                inp = 3
                break
            elif ev == ord("4"):
                inp = 4
                break
            elif ev == ord("5"):
                inp = 5
                break
            elif ev == ord("6"):
                inp = 6
                break
        daytoOut = currentDate[inp]
    else:
        tempDate = todayDate + datetime.timedelta(days=dayDelta)
        daytoOut = tempDate.strftime("%d/%m/%Y")
    events = daySort(findDay(daytoOut))
    charecters = string.ascii_letters+string.digits
    charecters = [char for char in charecters]
    screen.clear()
    for i in range(min(len(events), len(charecters))):
        screen.print_at(charecters[i]+": "+events[i]
                        [2]+" @ "+events[i][1], 0, i, 5)
    screen.print_at("Type letter to view | Back to Main(;)",
                    0, screen.height-1, 2)
    screen.refresh()
    flag = True
    display = []
    while flag:
        ev = screen.get_key()
        if ev == ord(";"):
            main(screen)
        for i in range(min(len(events), len(charecters))):
            if ev == ord(charecters[i]):
                display = events[i]
                flag = False
                break
    displayConst = display
    screen.clear()
    for i in range(4):
        screen.print_at(display[i], 0, i, 5)
        screen.print_at(
            "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
    screen.refresh()
    while True:
        ev = screen.get_key()
        if ev == ord(";"):
            for i in range(len(calFile)):
                if calFile[i] == displayConst:
                    calFile[i] = display
                    break
            screen.clear()
            return
        elif ev == ord("d"):
            display[0] = crapInput(screen, 0)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("t"):
            display[1] = crapInput(screen, 1)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("n"):
            display[2] = crapInput(screen, 2)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("i"):
            display[3] = crapInput(screen, 3)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()


def addEvent(screen):
    global viewMode
    global dayDelta
    global todayDate
    global calFile
    display = [todayDate.strftime(
        "%d/%m/%Y"), "00:00 AM", "name", "more information"]
    screen.clear()
    for i in range(4):
        screen.print_at(display[i], 0, i, 5)
        screen.print_at(
            "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
    screen.refresh()
    while True:
        ev = screen.get_key()
        if ev == ord(";"):
            calFile.append(display)
            screen.clear()
            return
        elif ev == ord("d"):
            display[0] = crapInput(screen, 0)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("t"):
            display[1] = crapInput(screen, 1)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("n"):
            display[2] = crapInput(screen, 2)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("i"):
            display[3] = crapInput(screen, 3)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back To Main (;) | Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()

#def delEvent(screen):


def refreshMain(screen):
    if viewMode == 0:
        dayViewExe(screen)
    elif viewMode == 1:
        weekViewExe(screen)


def menu(screen):
    global viewMode
    global dayDelta
    global todayDate
    global calName
    while True:
        screen.print_at(
            "Day(0) | Week (1) | Add Event(a) | Delete Event(d) | View/Edit Event(v) | Previous(p) | Next (n) | Go To Date(g) | Quit(q)", 0, screen.height-1, 2)
        ev = screen.get_key()
        if ev == ord("0"):
            dayViewExe(screen)
            break
        elif ev == ord("1"):
            weekViewExe(screen)
            break
        elif ev == ord("a"):
            addEvent(screen)
            refreshMain(screen)
            break
        elif ev == ord("d"):
            screen.clear()
            screen.print_at("Delete Event", 20, screen.height-5, 1)
            break
        elif ev == ord("v"):
            viewEvent(screen)
            refreshMain(screen)
            break
        elif ev == ord("p"):
            if viewMode == 0:
                dayDelta -= 1
                dayViewExe(screen)
            elif viewMode == 1:
                dayDelta -= 7
                weekViewExe(screen)
            break
        elif ev == ord("n"):
            if viewMode == 0:
                dayDelta += 1
                dayViewExe(screen)
            elif viewMode == 1:
                dayDelta += 7
                weekViewExe(screen)
            break
        elif ev == ord("g"):
            screen.clear()
            screen.print_at("Go To Date", 20, screen.height-5, 1)
            break
        elif ev == ord("q"):
            saveCal(calName)
            quit()
        screen.refresh()


def main(screen):
    dayViewExe(screen)
    while True:
        dateDraw(screen)
        menu(screen)
    #    ev = screen.get_key()
    #    screen.print_at("Change Mode(;)", 0, screen.height-1, 2)
    #    # Day(0) | Week (1) | Add Event(a) | Delete Event(d) | View Event(v) | Previous(←) | Next (→) | Set Date(s)
    #    if ev == ord(";"):
    #        menu(screen)
    #    else:
    #        screen.refresh()


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
