# py -m pip install SpeechRecognition
# py -m pip install dearpygui
# py -m pip install PyAudio

from tkinter import *
import tkinter as tk
from sunau import AUDIO_UNKNOWN_SIZE
import speech_recognition as sr 
import dearpygui.dearpygui as dpg

listOfReminders=[]
reminders=dict({})
reminderToAdd=""
reminderToRemove=""
reminder=""
# Record Audio
rstr = ""
newStr = ""

def change_label(text, color):
  feedbacklabel.config(text = text, bg=color)
  frame.update()

def edit_helper(reminderToEdit,reminders):
  change_label("What should I change the time to?", "blue")
  r = sr.Recognizer()
  # with(dpg.window(label='EDIT', pos=(0,150), width = 1440)):
  #   dpg.add_text('What should I change the time to?')
  feedbackList.insert(0, "What should I change the time to?")
  print("What should I change the time to?")
  with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)
    rstr = r.recognize_google(audio)
    #print("You said: " + rstr)
    feedbackList.insert(0, 'You said: ' + rstr)
    return rstr

def substring_after(s, delim):
    return s.partition(delim)[2]

def speak_callback():
  bSpeak["state"] = "disable"

  change_label("Say something!", "red")
  with sr.Microphone() as source:
    # feedbackList.insert(0, "Say something!")
    print("Say something!")
    r = sr.Recognizer()

    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    print (r.recognize_google(audio))
    #print("You said: " + r.recognize_google(audio))
  # print("a")
  # Speech recognition using Google Speech Recognition
  try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    rstr = r.recognize_google(audio)
    feedbackList.insert(0, 'You said: ' + rstr)
    # reminder = parse(rstr)
    
    if("add reminder" in rstr or 'new reminder' in rstr or 'create reminder' in rstr or 'set reminder' in rstr):
      if('at' not in rstr):
        reminderToAdd=substring_after(rstr,'reminder')
        reminderToAdd=reminderToAdd.strip()
        #listOfReminders.append(reminderToAdd)
        reminders[reminderToAdd]='NO TIME GIVEN'
      else:
        reminderToAdd=substring_after(rstr,'reminder')
        reminderToAdd=reminderToAdd.split('at',1)[0]
        timeToAdd = substring_after(rstr,'at')
        reminderToAdd=reminderToAdd.strip()
        #listOfReminders.append(reminderToAdd)
        reminders[reminderToAdd]= timeToAdd
    if("remove reminder" in rstr or 'delete reminder' in rstr or 'cancel reminder' in rstr or 'clear reminder' in rstr):
      reminderToRemove=substring_after(rstr,'reminder')
      reminderToRemove=reminderToRemove.strip()
      #listOfReminders.remove(reminderToRemove)
      if(reminderToRemove in reminders):
        reminders.pop(reminderToRemove)
        feedbackList.insert(0, 'Removed reminder '+reminderToRemove)
    if("edit reminder" in rstr or 'change reminder' in rstr or 'update reminder' in rstr):
      reminderToEdit=substring_after(rstr,'reminder')
      reminderToEdit=reminderToEdit.strip()
      if(reminderToEdit in reminders):
        newTime=edit_helper(reminderToEdit,reminders)
        
        print("NEW TIME IS: " + newTime)
        feedbackList.insert(0, 'Time changed from '+reminders[reminderToEdit]+' to '+newTime)
        reminders[reminderToEdit]=newTime
      

    # dpg.add_text("Add - Add reminder x at y")
    # dpg.add_text("Remove - Remove reminder x")
    # dpg.add_text("Edit - Edit reminder x, new x")
    #dpg.add_text(r.recognize_google(audio))
    # print("You said: " + rstr)
    #------------------------

    global newStr
    newStr = "ABC"
    print("TESTING: ")
    print(*listOfReminders,sep=', ')
    #with dpg.window(label="reminder"):
    #  for i in listOfReminders:
    #    dpg.add_text(i)

    # with reminderWindow:
    #   for i in reminders:
    #     mStr=i+" " + reminders[i]
    #     dpg.add_text(mStr)
    # size = len(reminders)
    # reminderList.insert(END, mStr)
    reminderList.delete(0,END)
    for i in reminders:
      mStr=i+" " + reminders[i]
      reminderList.insert(END, mStr)
        
    print(reminders)
  

      
  except sr.UnknownValueError:
    feedbackList.insert(0, "Google Speech Recognition could not understand audio")
    print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
    feedbackList.insert(0, "Could not request results from Google Speech Recognition service; {0}")
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
  
  bSpeak["state"] = "active"
  change_label("", "white")


root = tk.Tk()
stvar=tk.StringVar()
stvar.set("one")

canvas=tk.Canvas(root, width=0, height=100, background='white')

frame = Frame(root)

option=tk.OptionMenu(frame, stvar, "one", "two", "three")

# root.geometry("1000x800")
root.title('Counting Seconds')
button = Button(frame, text='Stop', width=25, command=root.destroy)
# button.pack()
bSpeak = Button(frame, text='Speak', width=25, command=speak_callback, bg="lightblue")
# bSpeak.pack()

scrollbar = Scrollbar(root)
# scrollbar.pack( side = LEFT, fill = Y)
scrollbar2 = Scrollbar(root)
# scrollbar2.pack( side = RIGHT, fill = Y)

reminderList = Listbox(frame, yscrollcommand = scrollbar.set , width = 100)
feedbackList = Listbox(frame, yscrollcommand = scrollbar2.set , width = 100)
rlabel = Label(frame, text="Reminders list", font="10")
flabel = Label(frame, text="Feedback list", font="10")
# for line in range(20):
#    feedbackList.insert(0, 'This is line number       ' + str(line))
# for line in range(20):
#    reminderList.insert(END, 'This is line number            ' + str(line))
# reminderList.pack( side = TOP, fill = BOTH )
# feedbackList.pack( side = BOTTOM, fill = BOTH )
# scrollbar.config( command = reminderList.yview )
# scrollbar2.config( command = feedbackList.yview )

help_label = Label(frame, text="""*** COMMANDS ***
Add - Add reminder x at y
Edit - Edit reminder x. (Say new time)
Remove - Remove reminder x
\nEX: 
  \"add reminder HOMEWORK at 6\"
  \"edit reminder HOMEWORK (wait) 8\"
  \"remove reminder HOMEWORK\"""")
help_label.config(fg="red")

feedbacklabel = Label(frame, text="", borderwidth=1, relief="solid", width=30, height=3, font="bold 25")

canvas.grid(row=0,column=1)
frame.grid(row=0,column=0, sticky="n")
button.grid(row=0,column=0,columnspan=1, sticky="nw")
bSpeak.grid(row=0,column=1,columnspan=1, sticky="n")
help_label.grid(row=1, column=0, columnspan=2)
rlabel.grid(row=2, column=0, sticky="w")
reminderList.grid(row=3,column=0,columnspan=3)
feedbacklabel.grid(row=4, column=0, columnspan=2) # label for what to do
flabel.grid(row=5, column=0, sticky="w")
feedbackList.grid(row=6,column=0,columnspan=3)


# if __name__== '__main__':
#   root=tk.Tk()
#   gui=Gui(root)
#   root.mainloop()

root.mainloop()
