import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.lang import Builder
from  kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from collections import Counter
from gensim.parsing.preprocessing import strip_non_alphanum, preprocess_string
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
            print("Exception handled..!! Picture could not be captured properly. Please check lighting")
            self.mood='Neutral'
        bot.setname(self.textforcamera.text) 
        print(bot.getname())
        ChatWindow.mood=self.mood
        self.textforcamera.text = ''


class ChatWindow(Screen):
    one=True
    prev=""
    mood=''
    bot.pre_processing()
    counter=1
    #bot.chatcode()
    def on_enter(self, *args):
        print(self.mood)
        greeting_msg="Hey "+bot.getname()+", my name is Cafe Buddy consider me a friend of yours!!\n"
        #self.chat_history.text="Hey "+bot.getname()+", what brings you here today!!\n Current Mood: "+self.mood+" !! "
        #emo     = ['Angry', 'Fear', 'Happy','Sad', 'Surprise', 'Neutral']
        
        if self.mood=='Happy':
            buddy_msg="you seem quite happy. Is there still anything that disturbs you?\n"
            self.chat_history.text=greeting_msg+buddy_msg
        if self.mood=='Angry':
            buddy_msg="you seem quite disturbed. Is there anything that disturbs you?\n"
            self.chat_history.text=greeting_msg+buddy_msg
        if self.mood=='Fear' or self.mood=='Surprise' or self.mood=='Neutral':
            buddy_msg="Is everything okay? You are looking stressed?\n"
            self.chat_history.text=greeting_msg+buddy_msg
        if self.mood=='Sad':
            buddy_msg="hey, what is it that worries you so much? Why are you looking so sad?\n"
            self.chat_history.text=greeting_msg+buddy_msg
            

        


    def send_message(self):
        message=self.text.text
        self.text.text=''
        #self.history.update_chat_history(f'[color=dd2020]{chat_app.connect_page.username.text}[/color] > {message}')
        self.chat_history.text = '\n' +"User: "+message
        if self.mood=='Happy':
            if self.counter==1:
                if (bot.predict(message) >= 0.55):
                    buddy_msg='That is good. In case you ever feel otherways. Please feel free to have a session with me\n'
                else:
                    self.mood='Neutral'  
                    buddy_msg = 'Please express yourself freely, i am hearing.\n'  
                self.chat_history.text += '\n'+"Cafe Buddy: "+buddy_msg
        else:
            print(self.counter)
            if self.counter==1:
                keyword=[word for word in preprocess_string(message.lower()) if word in ('friend','work','education','school','college','family','studi','exam','fight')]
                print(keyword)
                if len(keyword)>0:
                    buddy_msg = 'Will you please tell me in a bit more detail about it?'
                    self.one=True
                else:
                    buddy_msg='I understand. Seems like something\'s bothering you. '\
                     'Could you further describe it, in short?'
                    self.one=False
                self.counter+=1
                self.chat_history.text += '\n'+"Cafe Buddy: "+buddy_msg
            elif self.counter==2:
                if self.one==True:
                    keyword=[]
                    print(bot.predict(message))
                    keyword.extend([preprocess_string(message.lower())][0])
                    print(keyword)
                    if 'friend' in keyword and bot.predict(message)[0][0] <= 0.6:
                        buddy_msg = "Many people tend to expect too much of others, their family, "\
                            "their friends or even just acquaintances. It's a usual mistake"\
                            ", people don't think exactly the way you do.\nDon't let the "\
                            "opinions of others make you forget what you deserve. You are "\
                            "not in this world to live up to the expectations of others, "\
                            "nor should you feel that others are here to live up to yours."\
                            "\nThe first step you should take if you want to learn how to "\
                            "stop expecting too much from people is to simply realize and "\
                            "accept the fact that nobody is perfect and that everyone "\
                            "makes mistakes every now and then."
                    elif 'work' in keyword or 'studi' in keyword or 'exam' in keyword:
                        if bot.predict(message)[0][0] <= 0.6:
                            buddy_msg = bot.getname() + ", don't take too much stress. I can list some really cool "\
                            "ways to handle it.\nYou should develop healthy responses which "\
                            "include doing regular exercise and taking good quality sleep. "\
                            "You should have clear boundaries between your work or academic "\
                            "life and home life so you make sure that you don't mix them.\n"\
                            "Tecniques such as meditation and deep breathing exercises can be "\
                            "really helping in relieving stress.\n  Always take time to "\
                            "recharge so as to avoid the negative effects of chronic stress "\
                            "and burnout. We need time to replenish and return to our pre-"\
                            "stress level of functioning."
                    elif 'famili' in keyword and bot.predict(message)[0][0]<=0.6:
                        buddy_msg=bot.getname() + ", don't take too much stress. All you need to do is adjust "\
                            "your priorities. Don't take on unnecessary duties and "\
                            "responsibilities.\nTake advice from people whose opinion you "\
                            "trust, and get specific advice when issues arise.\nYou should "\
                            "use stress management techniques and always hope for the best. "\
                            "These situations arise in everyone's life and what matters the "\
                            "most is taking the right decision at such moments."
                    else:
                        if self.prev == "":
                            buddy_msg="It's ohk can you tell me something about your day... Did anything happen today that made you feel worried?\n"
                            self.prev="same"
                            self.one=False
                        
                    
                
                else:
                    buddy_msg='It looks like you might be feeling comfortable talking '\
                        'about yourself. Could you share your feelings?\n'
                    self.one=False
                    self.counter+=1

                self.chat_history.text += '\n'+"Cafe Buddy: "+buddy_msg

            elif self.counter==3:
                if not self.one:
                    print("Welcome to level 3")
                    keyword=[word for word in preprocess_string(message.lower()) if word in ('friend','work','education','school','college','family','studi','exam','fight')]
                    if len(keyword)>0:
                        buddy_msg = 'Will you please tell me in a bit more detail about it?'
                        self.one=True
                        self.counter=2
                    else:
                        buddy_msg= 'I see. Among the thoughts occuring in your mind, which one upsets you the most and why?\n'
                self.chat_history.text += '\n'+"Cafe Buddy: "+buddy_msg
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