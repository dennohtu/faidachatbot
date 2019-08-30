# -*- coding: utf-8 -*-
"""chat_bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18vrw3w7NrI9pN3-Y4e9jtht2_oR0jasX


!pip install nltk

!pip install numpy

!pip install tflearn

!pip install tensorflow
"""

"""
{"intents":[
{"tag":"greeting",
"patterns":["Hi","Hello","How are you","Good day"],
"responses":["Hello!", "Good to see ya!","Hello. How can I help?"],
"context_set":""
},...
]}
"""
import os.path
import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import tflearn
import numpy as np
import tensorflow as tf
import random
import json
import pickle
class Faida:
  def __init__(self):
    self.load_data()
    self.train()

  def load_data(self):
    #Load intents file
    with open("intents.json") as file: 
      self.data = json.load(file)
    
    try:
      with open("data.pickles", "rb") as f:
        self.words, self.labels, self.training, self.output = pickle.load(f)
    except:
      #print(data["intents"])
      self.words = []
      self.labels = []
      self.docs_x = []
      self.docs_y = [] #classify our patterns in docs_x

      #Loop through intents dictionary picking each intent
      for intent in self.data["intents"]:
        #Loop through the pattern in each intent
        for pattern in intent["patterns"]:
          #Stem the pattern. Bring words down to their root meanings
          #1. tokenize the words
          wrds = nltk.word_tokenize(pattern)
          #2. add tokenized words in words list
          self.words.extend(wrds)
          self.docs_x.append(wrds)
          self.docs_y.append(intent["tag"])
          if intent["tag"] not in self.labels:
            self.labels.append(intent["tag"])

      self.words = [stemmer.stem(w.lower()) for w in self.words if w != "?"]
      self.words = sorted(list(set(self.words))) #remove duplicates, recovert to list and sort

      self.labels = sorted(self.labels) #sort labels

      ##Bag of words. NN understandable format. Using 'one hot encoded'. if word exists in list 1,
      ##else 0
      self.training = []
      self.output = []

      out_empty = [0 for _ in range(len(self.labels))]
      #print(out_empty)

      for x, doc in enumerate(self.docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in self.words:
          if w in wrds:
            bag.append(1)
          else:
            bag.append(0)

        output_row = out_empty[:]
        output_row[self.labels.index(self.docs_y[x])] = 1

        self.training.append(bag)
        self.output.append(output_row)

      #print(training)
      self.training = np.array(self.training)
      self.output = np.array(self.output)
      
      with open("data.pickle", "wb") as f:
        pickle.dump((self.words, self.labels, self.training, self.output), f)

  def train(self):
    ##Begin model
    tf.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(self.training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    ##Gives probability to output layer with the appropriate label
    net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
    net = tflearn.regression(net)

    self.model = tflearn.DNN(net)
    ##Model complete

    if os.path.exists('model.tflearn.index'):
      self.model.load("model.tflearn")
    else:
      self.model.fit(self.training, self.output, n_epoch=2000, batch_size=8, show_metric=True)
      self.model.save("model.tflearn")
    

  def bag_of_words(self, s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    
    for se in s_words:
      for i, w in enumerate(words):
        if w == se:
          bag[i] = 1
    return np.array(bag)

  def chat_cli(self):
    print("..............Bot Ready!..........")
    print("Type quit to stop")
    while(True):
      inp = input("You:")
      if inp.lower() == "quit":
        print("See you later:)")
        break
        
      results = self.model.predict([self.bag_of_words(inp, self.words)])[0]
      results_index = np.argmax(results)
      tag = self.labels[results_index]
      if results[results_index] < 0.6 :
        print("I didn't get that")
      else:
        for tg in data["intents"]:
          if tg['tag'] == tag:
            responses = tg["responses"]

        print(random.choice(responses))
      
  def chat_gui(self, message):
    results = self.model.predict([self.bag_of_words(message, self.words)])[0]
    results_index = np.argmax(results)
    tag = self.labels[results_index]
    if results[results_index] < 0.6 :
      return "Sorry, I didn't get that"
    else:
      for tg in self.data["intents"]:
        if tg['tag'] == tag:
          responses = tg["responses"]
      return random.choice(responses)