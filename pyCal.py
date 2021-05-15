# python 3.9
import re
import datetime
from asciimatics.screen import Screen
import textwrap
import string

# Globals
viewMode = 0  # 0:day 1:week
todayDate = datetime.date.today()
dayDelta = 0
calFile = ['date', 'time', 'name', 'description']


def openCal(name):
    """open the file containg the events from CSV

    Args:
        name (string): name/location of CSV

    Returns:
        2d list: all of the CSV
    """
    calFile = open(name, "r").read().split("\n")
    for i in range(len(calFile)):
        if calFile[i] == "":
            calFile.pop(i)
            i -= 1
        else:
            calFile[i] = calFile[i].split(",")
    return calFile


def saveCal(name):
    """saves the global calendar variable to the CSV

    Args:
        name (string): file name/location
    """
    global calFile
    output = ""
    for event in calFile:
        output += ",".join(event[0:4])+"\n"
    outputFile = open(name, "w")
    outputFile.write(output)
    outputFile.close()


calName = "cal.csv"
calFile = openCal(calName)


def findDay(day):
    """search for all of the events from a day

    Args:
        day (string): date as string

    Returns:
        2d list: all of the events for a day 
    """
    global calFile
    output = []
    for i in range(len(calFile)):
        if calFile[i][0] == day:
            output.append(calFile[i])
    return output


def daySort(a):
    """sort the events for a single day by time

    Args:
        a (list): input list to be sorted

    Returns:
        list: sorted list
    """
    for i in range(len(a)):
        replaceable = (re.split(":| ", a[i][1]))
        if replaceable[2] == "PM":
            PMint = 12
        else:
            PMint = 0
        z = int(replaceable[1])/60
        a[i].append(int(replaceable[0])+z+PMint)
    a = sorted(a, key=lambda x: x[4])
    return a


def dayDraw(screen, day, maxWidth, location):
    """draw the events for a single day

    Args:
        screen (screen object): object to refrence screen
        day (string): date string
        maxWidth (int): the maximum width of each event
        location (int): y axis location of the column of events
    """
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
    """show the time down the left hand side

    Args:
        screen (screen object): object to refrence screen
    """
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
    """draw the dates for the week that is being displayed

    Args:
        screen (screen object): object to refrence screen
        days (list): the dates of teh days to be displayed
    """
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
    """execute the dayview function

    Args:
        screen (screen object): object to refrence screen
    """
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
    """execute the week view, call to show the view

    Args:
        screen (screen object): object to refrence screen
    """
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


def crapInput(screen, width, height):
    """a rubish not very user friendly basic input solution which can have the location of the input display spesified

    Args:
        screen (screen object): object to refrence screen
        width (int): y axis location of the variable data shown on screen
        height (int): x axis location of the variable data shown on screen

    Returns:
        string: string with all the charecters inputed
    """
    charecters = ""
    while True:
        ev = screen.get_key()
        print(ev)
        if ev == -301:
            return charecters
        elif ev == -300:
            charecters = charecters[:-1]
            screen.print_at(charecters+" ", width, height, 6)
            screen.refresh()
        elif ev != None and ev not in [-203, -205, -204, -206, -300, -207, -208, -102, -1]:
            charecters = charecters+chr(ev)
            screen.print_at(charecters, width, height, 6)

            screen.refresh()


def viewEvent(screen):
    """view or edit a event, asks which event and then displays it with options to edit it

    Args:
        screen (screen object): object to refrence screen
    """
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
            "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
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
        elif ev == ord(":"):
            screen.clear()
            return
        elif ev == ord("d"):
            display[0] = crapInput(screen, 0, 0)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("t"):
            display[1] = crapInput(screen, 0, 1)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("n"):
            display[2] = crapInput(screen, 0, 2)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("i"):
            display[3] = crapInput(screen, 0, 3)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()


def addEvent(screen):
    """create a new event, based on template

    Args:
        screen (screen object): object to refrence screen
    """
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
            "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
    screen.refresh()
    while True:
        ev = screen.get_key()
        if ev == ord(";"):
            calFile.append(display)
            screen.clear()
            return
        elif ev == ord(":"):
            screen.clear()
            return
        elif ev == ord("d"):
            display[0] = crapInput(screen, 0, 0)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("t"):
            display[1] = crapInput(screen, 0, 1)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("n"):
            display[2] = crapInput(screen, 0, 2)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()
        elif ev == ord("i"):
            display[3] = crapInput(screen, 0, 3)
            screen.clear()
            for i in range(4):
                screen.print_at(display[i], 0, i, 5)
                screen.print_at(
                    "Back and Save (;) | Back and Cancel (:)| Edit Date(d) | Edit Time(t) | Edit Name(n) | Edit Info(i) | Save Edit (tab)", 0, screen.height-1, 2)
            screen.refresh()


def delEvent(screen):
    """delete a events, ask which event and then pop it from global array

    Args:
        screen (screen object): object to refrence screen
    """
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
    screen.print_at("Type letter to delete | Back to Main(;)",
                    0, screen.height-1, 2)
    screen.refresh()
    flag = True
    while flag:
        ev = screen.get_key()
        if ev == ord(";"):
            main(screen)
        for i in range(min(len(events), len(charecters))):
            if ev == ord(charecters[i]):
                for j in range(len(calFile)):
                    if calFile[j] == events[i]:
                        calFile.pop(j)
                        flag = False
                        break
            if flag == False:
                break


def refreshMain(screen):
    """display all events on the screen

    Args:
        screen (screen object): object to refrence screen
    """
    global viewMode
    if viewMode == 0:
        dayViewExe(screen)
    elif viewMode == 1:
        weekViewExe(screen)


def menu(screen):
    """prints the menu on the main screen and intiates all exeuctions

    Args:
        screen (screen object): object to refrence screen
    """
    global viewMode
    global dayDelta
    global todayDate
    global calName
    while True:
        screen.print_at(
            "Day(0) | Week (1) | Add(a) | Delete(d) | View/Edit(v) | Previous(p) | Next (n) | Go To Date(g) | Quit(q)", 0, screen.height-1, 2)
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
            delEvent(screen)
            refreshMain(screen)
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
            screen.print_at("Enter date:", 0, screen.height-2, 1)
            screen.refresh()
            tempString = crapInput(screen, 12, screen.height-2)
            tempDate = datetime.datetime.strptime(tempString, "%d/%m/%Y")
            tempDate = tempDate.date()
            if todayDate == tempDate:
                dayDelta = 0
            elif todayDate > tempDate:
                dayDelta = 0-abs((tempDate-todayDate).days)
            elif todayDate < tempDate:
                dayDelta = 0+abs((tempDate-todayDate).days)

            if viewMode == 0:
                dayViewExe(screen)
            elif viewMode == 1:
                weekViewExe(screen)
            break
        elif ev == ord("q"):
            saveCal(calName)
            quit()
        screen.refresh()


def main(screen):
    """main execution point

    Args:
        screen (screen object): object to refrence screen
    """
    dayViewExe(screen)
    while True:
        dateDraw(screen)
        menu(screen)

#call main and pass through object
Screen.wrapper(main)
