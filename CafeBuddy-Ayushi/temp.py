import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from  kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from collections import Counter
import time


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
    pass

class ChatWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv=Builder.load_file('design_edit.kv')

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