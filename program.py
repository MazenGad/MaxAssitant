from __future__ import print_function
from tkinter import *
import PyPDF2
import pywhatkit
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, display_icon, display_images, extract_images,  resize_image, copy_text, save_all, save_image

import pyjokes

import random

import datetime
import os.path
import subprocess
import pywhatkit
import wikipedia

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import time
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import pytz


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 145)
    engine.say(text)
    engine.runAndWait()


def get_audio():
  recognize = sr.Recognizer()
  with sr.Microphone() as source:
    audio = recognize.listen(source)
    voice = ""

    try:
      voice = recognize.recognize_google(audio)
      print(voice)
    except Exception as e:
      print("Exception : "+str(e))

  return voice




def authintaction():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        return service

    except HttpError as error:
        print('An error occurred: %s' % error)


def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # NEW STUFF STARTS HERE
    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            speak(event["summary"])

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

def tell_joke():
    speak(pyjokes.get_joke())

def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass


    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1


    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)
def Set_User():

    Name = get_audio()
    return Name

def Chrome():
    program = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen(program)


def fifa():
    program = "D:\Games\Fifa 18\FIFA18.exe"
    subprocess.Popen(program)


def questions(que):
    Wiki_Str=['who is', 'what is', 'wiki', 'wikipedia']

    for n in Wiki_Str:
        if n in que:
            anoun = que.replace(n, '')
            try:
                info = wikipedia.summary(anoun, 2)
                speak(info)
                display_textbox(info, 4, 1, root)
                return True
            except Exception as e:
                print("Exception : " + str(e))


def playVideo(command):
    if "play" in command:
        video = command.replace("play","")
        speak("playing "+video)
        print("playing...")
        pywhatkit.playonyt(video)
        return True


def mood():
    mood = [
        'good', 'bad', 'Not Your Buisness', 'I am great', 'I am fine and you',
        'I fell sick', 'shut up '
    ]
    current_mood = str(random.choice(mood))
    speak(current_mood)


def Main():

    SERVICE = authintaction()
    Start_text.set("Listining...")
    text = ""
    speak("Hello Im Max , Your Assistant")
    speak("After I Say Talk , Say Your Name to Make me able to know you")
    speak("Say it Now ....")
    print("Talk Now ....")
    Name = Set_User()
    speak(f"Hello {Name} What do you need")

    while True:
        if "bye" in text:
            speak(f"Okay {Name} Good Bye")
            StartBtn()
            break
        else:
            speak("Speak Please")
        print("Start...")
        text = get_audio()

        CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

        for phrase in CALENDAR_STRS:
            if phrase in text.lower():
                date = get_date(text)
                if date:
                    get_events(date, SERVICE)
                    speak("do you want to ask about any thing else")
                    print("Talk..")
                    text = get_audio()
                    if "yes" in text.lower():
                        speak(f"What Do You need{Name}")
                        print("Talk..")
                        text = get_audio()

                else:
                    speak("Please Try Again")
                    print("Talk..")


        NOTE_STRS = ["make a note", "write this down", "remember this", "type this"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down? ")
                print("Talk..")
                write_down = get_audio()
                note(write_down)
                speak("I've made a note of that.")
                speak("do you want to ask about any thing else")
                print("Talk..")
                text = get_audio()
                if "yes" in text.lower():
                    speak(f"What Do You need{Name}")
                    print("Talk..")
                    text = get_audio()


        if "how are you" in text.lower() or "how you doin" in text.lower() :
            mood()
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if "pdf" in text.lower() or "bdf" in text.lower() or "pds" in text.lower() or "document" in text.lower():
            speak("Please Select A file")
            browseBtn()
            pdf= open_file()
            speak(pdf[0])
            time.sleep(2)
            StartBtn()
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if "save" in text.lower() or "safe" in text.lower()  or "sieve" in text.lower():
            speak("Saved successfully")
            save_all(all_images)
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if "chrome" in text.lower() or "krom" in text.lower():
            speak("Opening")
            Chrome()
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if "fifa" in text.lower() or "viva" in text.lower() or "fiva" in text.lower():
            speak("Opening")
            fifa()
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if questions(text.lower()):
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if playVideo(text.lower()):
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if 'time' in text.lower():
            Time = datetime.datetime.now().strftime('%I:%M %p')
            print(Time)
            speak('Current time is ' + Time)
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()

        if 'joke' in text.lower():
            tell_joke()
            time.sleep(2)
            speak("do you want to ask about any thing else")
            print("Talk..")
            text = get_audio()
            if "yes" in text.lower():
                speak(f"What Do You need{Name}")
                print("Talk..")
                text = get_audio()
#######################################################################################################################
#Start The Program



#global parameters, updating dynamically
all_content = []
all_images = []
img_idx = [0]
displayed_img = []

#initiallize a Tkinter root object
root = Tk()
root.geometry('+%d+%d'%(350,50)) #place GUI at x=350, y=10

#ARROW BUTTONS FUNCTIONALITY
#right arrow
def right_arrow(all_images, selected_img, what_text):
    #restrict button actions to the number of avialable images
    if img_idx[-1] < len(all_images) -1:
        #change to the following index
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#left arrow
def left_arrow(all_images, selected_img, what_text):
    #restrict button actions to indices greater than 1
    if img_idx[-1] >= 1:
        #change to the previous index
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#header area - logo & browse button
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

#main content area - text and image extraction
main_content = Frame(root, width=800, height=250, bg="#1e1e1e")
main_content.grid(columnspan=3, rowspan=2, row=4)

def open_file():

    #clear global list of indices
    for i in img_idx:
        img_idx.pop()
    img_idx.append(0) #set global index to 0

    browse_text.set("Selecting...")

    #load a PDF file
    file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])

    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        #select a page
        page = read_pdf.getPage(0)
        #extract text content from page
        page_content = page.extractText()

        #SET A SPECIAL ENCODING OR REPLACE CHARACTERS
        #page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")

        #CLEARING GLOBAL VARIABLES ONCE A NEW PDF FILE IS SELECTED
        #clear the content of the previous PDF file
        if all_content:
            for i in all_content:
                all_content.pop()

        #clear the image list from the previous PDF file
        for i in range(0, len(all_images)):
            all_images.pop()

        #hide the displayed image from the previous PDF file and remove it
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        #BEGIN EXTRACTING
        #extract text
        all_content.append(page_content)
        #extract images
        images = extract_images(page)
        for img in images:
            all_images.append(img)

        #BEGIN DISPLAYING
        #display the first image that was detected
        selected_image = display_images(images[img_idx[-1]])
        displayed_img.append(selected_image)

        #display the text found on the page
        display_textbox(all_content, 4, 0, root)

        #reset the button text back to Browse
        browse_text.set("Start")

        #BEGIN MENUES AND MENU WIDGETS
        #1.image menu on row 2
        img_menu = Frame(root, width=800, height=60)
        img_menu.grid(columnspan=3, rowspan=1, row=2)

        what_text = StringVar()
        what_img = Label(root, textvariable=what_text, font=("shanti", 10))
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
        what_img.grid(row=2, column=1)

        #arrow buttons
        display_icon('arrow_l.png', 2, 0, E, lambda:left_arrow(all_images, selected_image, what_text))
        display_icon('arrow_r.png', 2, 2, W, lambda:right_arrow(all_images, selected_image, what_text))

        #2.save image menu on row 3
        save_img_menu = Frame(root, width=800, height=60, bg="#c8c8c8")
        save_img_menu.grid(columnspan=3, rowspan=1, row=3)

        #create action buttons
        copyText_btn = Button(root, text="copy text",command=lambda:copy_text(all_content, root), font=("shanti", 10), height=1, width=15)
        saveAll_btn = Button(root, text="save all images", command=lambda:save_all(all_images), font=("shanti", 10), height=1, width=15)
        save_btn = Button(root, text="save image", command=lambda:save_image(all_images[img_idx[-1]]), font=("shanti", 10), height=1, width=15)

        #place buttons on grid
        copyText_btn.grid(row=3,column=0)
        saveAll_btn.grid(row=3,column=1)
        save_btn.grid(row=3,column=2)
        return [page_content,]

#BEGIN INITIAL APP COMPONENTS
display_logo('logo.png', 0, 0)

#instructions
instructions = Label(root, text="Start Using MAX", font=("Raleway", 10), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

browse_text = StringVar()
def browseBtn():
    #browse button
    browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#1e1e1e", fg="white", height=1, width=15)
    browse_text.set("Browse")
    browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

Start_text = StringVar()
def StartBtn():
    #Start button
    Start_Btn = Button(root, textvariable=Start_text, command=lambda:Main(), font=("Raleway",12), bg="#1e1e1e", fg="white", height=1, width=15)
    Start_text.set("Start")
    Start_Btn.grid(column=2, row=1, sticky=NE, padx=50)

StartBtn()

root.mainloop()
