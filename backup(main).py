import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from  kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from collections import Counter
import bot
import time
import tensorflow as tf
import facialrecognition as fr
import cv2

class Home(Screen):
    pass


class Questions(Screen):
    
    
    ques_path='Personality Test(base)\Questions.txt'
    personalities={'isfj':'Defender','esfj':'Cousellor','istj':'Logistician','estp':'Entrepreneur','esfp':'Entertainer','istp':'Virtuoso','isfp':'Adventurer','entj':'Commander','entp':'Debator','intj':'Architect','intp':'Logician','enfj':'Protagonist','enfp':'Campaigner','infj':'Advocate','infp':'Mediator','estj':'Executive'}
    personality=''
    questions=[]
    question_1 = ObjectProperty(None)
    question_2 = ObjectProperty(None)
    counter=1
    answers=[0]*20
    with open(ques_path) as quest_file:
        questions=[r.split('SPLIT') for r in quest_file.readlines()]
    
    def personality_exam(self,answers):
        e,s,j,t=['e','i'],['s','n'],['j','p'],['t','f']
        e.extend([answers[r] for r in range(0,20,4)]) 
        s.extend([answers[r] for r in range(1,20,4)]) 
        t.extend([answers[r] for r in range(2,20,4)]) 
        j.extend([answers[r] for r in range(3,20,4)]) 
        personality='' 
        for option in e,s,t,j: 
            temp=Counter(option) 
            personality+=option[0] if temp['a']>temp['b'] else option[1] 
        Report.personality=personality
    
    def on_enter(self, *args):
        self.question_1.text=self.questions[0][0]
        self.question_2.text=self.questions[0][1]
    
    def ask_question1(self):
        if(self.counter==20):
            self.answers[self.counter-1]='a'
            self.personality_exam(self.answers)
            self.counter=1
            sm.current = 'rep'
            
        else:
            self.question_1.text=self.questions[self.counter][0]
            self.question_2.text=self.questions[self.counter][1] 
            self.answers[self.counter-1]='a'
            self.counter+=1

    def ask_question2(self):
        if(self.counter==20):
            self.answers[self.counter-1]='b'
            self.personality_exam(self.answers)
            self.counter=1
            sm.current = 'rep'
            
        else:
            self.question_1.text=self.questions[self.counter][0]
            self.question_2.text=self.questions[self.counter][1] 
            self.answers[self.counter-1]='b'
            self.counter+=1

    

class Report(Screen):
    personality=''
    def on_enter(self, *args):
        self.per.text=Questions.personalities[self.personality]+'\n'+'('+self.personality+')'
        self.image.source= Report.personality+'\INTRODUCTION\Image.png'
class Description(Screen):
    def on_enter(self, *args):
        self.persona.text=Questions.personalities[Report.personality]
        file_path=Report.personality+'\INTRODUCTION\Introduction.txt'
        with open(file_path) as file:
            self.detail.text=file.read()

class CareerOptions(Screen):
    def on_enter(self, *args):
        self.persona.text=Questions.personalities[Report.personality]
        file_path=Report.personality+'\career.txt'
        with open(file_path) as file:
            self.detail.text=file.read()

class Strengths(Screen):
    def on_enter(self, *args):
        self.persona.text=Questions.personalities[Report.personality]
        file_path=Report.personality+'\STRENGTHS\Strengths.txt'
        with open(file_path) as file:
            self.detail.text=file.read()

class CameraClick(Screen):

    emo     = ['Angry', 'Fear', 'Happy',
           'Sad', 'Surprise', 'Neutral']
    model = tf.keras.models.load_model("facial_1 (1)")
    buddy=''
    mood=''


    def prepare(self, filepath):
        IMG_SIZE = 48  
        img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)        
    
    def capture(self):
        
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        name="IMG_{}.png".format(timestr)
        camera.export_to_png(name)
        print("Captured")
        fc=fr.FaceCropper().generate(name,True)
        try:
            prediction = self.model.predict([self.prepare(fc)])
            prediction=list(map(float,prediction[0]))
        except:
            prediction="prepare function could not run(0 faces detected)"
            self.mood='Neutral'
        print(prediction)
        try:
            self.mood=self.emo[prediction.index(max(prediction))] # self.emo[list(prediction[0]).index(1)]
        except:
            print("Exception handled..!! Picture could not be cleared properly. Please check lighting")
            self.mood='Neutral'
        bot.setname(self.textforcamera.text) 
        print(bot.getname())
        ChatWindow.mood=self.mood


class ChatWindow(Screen):
    mood=''
    bot.pre_processing()
    #bot.chatcode()
    def on_enter(self, *args):
        self.chat_history.text="Hey "+bot.getname()+", what brings you here today!!\n Current Mood: "+self.mood+" !! "
    def send_message(self):
        message=self.text.text
        self.text.text=''
        #self.history.update_chat_history(f'[color=dd2020]{chat_app.connect_page.username.text}[/color] > {message}')
        self.chat_history.text += '\n' +"User: "+message

        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at teh bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        #self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

class WindowManager(ScreenManager):
    pass

kv=Builder.load_file('design.kv')

sm = WindowManager()
screens=[Home(name="home"), Questions(name="quest"), Report(name="rep"), Description(name='description'), CareerOptions(name='career'), Strengths(name='strengths'), ChatWindow(name='chat'),CameraClick(name='camera')]
for screen in screens:
    sm.add_widget(screen)
sm.current = "home"

class CafeApp(App):
    def build(self):
        return sm

if __name__=='__main__':
    CafeApp().run()