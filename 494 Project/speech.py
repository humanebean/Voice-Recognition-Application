# import audioop
# import posix
from sunau import AUDIO_UNKNOWN_SIZE
import speech_recognition as sr
import dearpygui.dearpygui as dpg

posX = 0
posY = 0

def substring_after(s, delim):
    return s.partition(delim)[2]

def parse(str):
  create = "create "
  add = "add "
  lstr = str.lower()
  print(f"string:{lstr}")
  idxCreate = lstr.find("create")
  idxAdd = lstr.find("add")
  # print(f"create {idxCreate}")
  # print(f"add {idxAdd}")

  # get lower command and add everything after
  # create exists but add doesnt or create lower index
  if idxCreate != -1 and (idxAdd == -1 or idxCreate < idxAdd):
    idx = idxCreate
    size = len(create)
  # create doesnt exist but add does or add lower index
  elif idxAdd != -1 and (idxCreate == -1 or idxCreate > idxAdd):
    idx = idxAdd
    size = len(add)
  else:
    return ""
  # print(f"idx {idx}")
  # print(f"size {size}")
  # print(f"string from idx:{str[(idx+size):]}")
  return str[(idx+size):]

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
listOfReminders=[]
reminders=dict({})
reminderToAdd=""
reminderToRemove=""
reminder=""
# Record Audio
str = ""
def edit_helper(reminderToEdit,reminders):
  r = sr.Recognizer()
  with(dpg.window(label='EDIT', pos=(0,150), width = 1440)):
    dpg.add_text('What should I change the time to?')
  with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    audio=r.listen(source)
    str = r.recognize_google(audio)
    #print("You said: " + str)
    return str
newStr = ""
def speak_callback():
  with sr.Microphone() as source:
      r = sr.Recognizer()
      print("Say something!")
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
      str = r.recognize_google(audio)
      reminder = parse(str)
      
      if("add reminder" in str or 'new reminder' in str):
        myString = parse(str)
        if('at' not in str):
          reminderToAdd=substring_after(str,'reminder')
          reminderToAdd=reminderToAdd.strip()
          #listOfReminders.append(reminderToAdd)
          reminders[reminderToAdd]='NO TIME GIVEN'
        else:
          reminderToAdd=substring_after(str,'reminder')
          reminderToAdd=reminderToAdd.split('at',1)[0]
          timeToAdd = substring_after(str,'at')
          reminderToAdd=reminderToAdd.strip()
          #listOfReminders.append(reminderToAdd)
          reminders[reminderToAdd]= timeToAdd
      if("remove reminder" in str):
        myString = parse(str)
        reminderToRemove=substring_after(str,'reminder')
        reminderToRemove=reminderToRemove.strip()
        #listOfReminders.remove(reminderToRemove)
        if(reminderToRemove in reminders):
          reminders.pop(reminderToRemove)
      if("edit reminder" in str):
        myString = parse(str)
        reminderToEdit=substring_after(str,'reminder')
        reminderToEdit=reminderToEdit.strip()
        if(reminderToEdit in reminders):
          newTime=edit_helper(reminderToEdit,reminders)
          print("NEW TIME IS: " + newTime)
        reminders[reminderToEdit]=newTime
        

    # dpg.add_text("Add - Add reminder x at y")
    # dpg.add_text("Remove - Remove reminder x")
    # dpg.add_text("Edit - Edit reminder x, new x")
    #dpg.add_text(r.recognize_google(audio))
      print("You said: " + str)
      with dpg.window(label="Feedback", pos=(0, 720), width = 1440):
        # global newStr
        dpg.add_text("You said: " + str)
      global newStr
      newStr = "ABC"
      print("TESTING: ")
      print(*listOfReminders,sep=', ')
      #with dpg.window(label="reminder"):
      #  for i in listOfReminders:
      #    dpg.add_text(i)

      with dpg.window(label='reminder', pos=(0,150), width = 1440, height = 570):
        for i in reminders:
          mStr=i+" " + reminders[i]
          dpg.add_text(mStr)
          
      print(reminders)

      
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

def save_callback():
    print("Save Clicked")
   #a = str



with dpg.window(label="speak", pos=(620, 0), height=150):
    dpg.add_text("Press Speak before giving command")
    dpg.add_text("Add - Add reminder x at y")
    dpg.add_text("Remove - Remove reminder x")
    dpg.add_text("Edit - Edit reminder x, new x")
    #dpg.add_text(r.recognize_google(audio))

    dpg.add_button(label="SPEAK", callback=speak_callback, width= 250)

# make sure we got a command
if reminder != "":
  with dpg.window(label="reminder"):
    dpg.add_text(reminder)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
