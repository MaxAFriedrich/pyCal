import datetime
from textwrap import shorten
from re import split
from asciimatics.screen import Screen
from time import sleep
import os


class Event():
    totalEvents = 0

    def __init__(self, date=datetime.date.today(), time="HH:MM AM", name="name", info="information") -> None:
        self.date = date
        self.__strDate = self.date.strftime("%d/%m/%Y")
        self.time = time
        self.name = name
        self.info = info
        Event.totalEvents += 1

    def __str__(self) -> str:
        return [self.date, self.__strDate, self.time, self.name, self.info]

    def labelStr(self, maxWidth):
        return shorten(self.name+" @ "+self.time, maxWidth, placeholder="...")

    def fullStr(self):
        return ",".join([self.__strDate, self.time, self.name, self.info])

    def fullLst(self):
        return [self.__strDate, self.time, self.name, self.info]

    def dateInt(self):
        arrayValues = split("/", self.__strDate)
        output = 0
        for each in arrayValues:
            output += int(each)
        return output

    def timeInt(self):
        arrayValues = split(":| ", self.time)
        output = 0
        if arrayValues[2] == "PM":
            temp = int(arrayValues[1])/60
            output = int(arrayValues[0])+12+temp
        else:
            temp = int(arrayValues[1])/60
            output = int(arrayValues[0])+temp
        return output


class Filer():
    allEvents = []

    def __init__(self) -> None:
        pass

    def open(self, name):
        calFile = open(name, "r").read().split("\n")
        for i in range(len(calFile)):
            if calFile[i] == "":
                calFile.pop(i)
                i -= 1
            else:
                temp = calFile[i].split(",")
                Filer.allEvents.append(Event(datetime.datetime.strptime(
                    temp[0], "%d/%m/%Y").date(), temp[1], temp[2], temp[3]))

    def close(self, name):
        output = ""
        for event in Filer.allEvents:
            output += event.fullStr()+"\n"
        outputFile = open(name, "w")
        outputFile.write(output)
        outputFile.close()


class Display():
    def __init__(self) -> None:
        pass

    def __sort(self, data):
        for i in range(len(data)):
            for j in range(len(data)-1):
                if data[j].timeInt() > data[j+1].timeInt():
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp
        return data

    def __search(self, date):
        output = []
        for event in Filer.allEvents:
            if event.date == date:
                output.append(event)
        return output

    def __times(self):
        output = []
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
            output.append(timeBlock+'██ ')
        return output

    def dayContent(self, date, maxWidth):
        output = []
        events = self.__sort(self.__search(date))
        for event in events:
            output.append(event.labelStr(maxWidth)+"\n")
        return output

    def day(self, date, maxWidth):
        output = ""
        events = self.__sort(self.__search(date))
        i = 0
        times = self.__times()
        for event in events:
            output += times[i]+event.labelStr(maxWidth)+"\n"
            i += 1
        return output, events


def clearConsole():
    for i in range(50):
        print()


def main():
    cal = Filer()
    cal.open("cal.csv")
    calDisplay = Display()
    lastView = 0
    currentDate = datetime.date.today()
    while True:
        usrInp = input(
            "Day(0) | Week (1) | Add(a) | Delete(d) | View/Edit(v) | Previous(p) | Next (n) | Go To Date(g) | Quit(q)").lower()
        if usrInp == "0":
            lastview = 0
            clearConsole()
            output, events = calDisplay.day(datetime.date.today(), 30)
            print(output)
        elif usrInp == "1":
            lastview = 1
            clearConsole()
            print("Week")
        elif usrInp == "a":
            clearConsole()
            Filer.allEvents.append(Event(datetime.datetime.strptime(
                input("Enter date in format DD/MM/YYYY: \n"), "%d/%m/%Y").date(), input("Enter time in form HH:MM P/AM: \n"), input("Enter name: \n"), input("Enter description/information: \n")))
        elif usrInp == "d":
            if lastView == 0:
                events = calDisplay.dayContent(currentDate, 30)
                for i in range(len(events)):
                    print(str(i)+": "+events[i])
            elif lastView == 1:
                events = []
                for j in range(7):
                    events.append(calDisplay.dayContent(
                        currentDate + datetime.timedelta(j), 30))
                for i in range(len(events)):
                    print(str(i)+": "+events[i])
            x = False
            for i in range(len(Filer.allEvents)):
                for j in range(len(events)):
                    if Filer.allEvents[i] == events[j]:
                        Filer.allEvents.pop(i)
                        x = True
                        break
                if x == True:
                    break
        elif usrInp == "v":
            print("View event")
        elif usrInp == "p":
            print("previous page")
        elif usrInp == "n":
            print("next page")
        elif usrInp == "g":
            print("go to")
        elif usrInp == "q":
            break
    cal.close("cal.csv")


main()