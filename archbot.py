from __future__ import print_function
from flask import Flask, render_template, request
import re
import random

class Chat(object):
    def __init__(self, pairs,reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len, reverse=True)
        return re.compile(r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE)
    def _substitute(self, str):
        return self._regex.sub( lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower())

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find('%')
        return response
        
    def respond(self, str):
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            if match:
                resp = random.choice(response) 
                resp = self._wildcards(resp, match)  

                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'
                return resp

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}
pairs = [

 

      [
         r"Blogs",
         ["Prawal"]

   ],
     [
          r"^\w+$",
         ["Select one of the items from the menu:</br>Blogs</br> Projects </br> Feedback"]

   ]
  

]
def chatty():
    #print("Hi,Welcome to HeroBot.\n Please enter your name? \n Type quit to leave \n Use Format: i am [your name]\n Use Format: Myself [your name]\n Use Format: My name is [your name]  ")
    chat = Chat(pairs,reflections)
    x = chat.respond('Nic')
    print(x)
    
app = Flask(__name__)

#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    chat = Chat(pairs,reflections)
    return (chat.respond(userText))
    
if __name__ == "__main__":
    app.run(port=6353)