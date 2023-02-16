#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 07:12:11 2022

@author: levi

Code reverso tiré de 
#https://stackoverflow.com/questions/60342192/is-it-possible-to-get-example-sentences-with-the-words-translations-from-revers


"""
import deepl 
import googletrans
import requests
from bs4 import BeautifulSoup



class examples_loader:
    def __init__(self,source="german", target="english"):
        self.source = source.lower()
        self.target = target.lower()
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.DeeplT = deepl.Translator("A Deepl API key is required here") 
        self.GoogleT = googletrans.Translator()
        
    def retrieve(self,group_of_words):
        start_adress = "https://context.reverso.net/translation/"
        dic = self.source+"-"+self.target+"/"
        
       #print(self.source, self.target)
        req = requests.get(start_adress+dic+group_of_words, headers = self.headers)
        
        soup = BeautifulSoup(req.text, 'lxml')

        sentences = [x.text.strip() for x in soup.find_all('span', {'class':'text'}) if '\n' in x.text]
        return sentences
    
    def update_param(self, source, target):
        self.source = source.lower()
        self.target = target.lower()
        
        
    def translateD(self,text):
        dict_lang_s = {"english":"EN", "german":"DE", "french":"FR"}
        dict_lang_t = {"english":"EN-US", "german":"DE", "french":"FR"}

        source = dict_lang_s[self.source]
        target = dict_lang_t[self.target]
        result = self.DeeplT.translate_text(text, source_lang=source, target_lang = target)
        return result.text
        
    
    def translateG(self, text):
        dict_lang = {"english":"en", "german":"de", "french":"fr"}
        source = dict_lang[self.source]
        target = dict_lang[self.target]
        
        print(source, target)
        result = self.GoogleT.translate(text, dest=target, src=source)
        return result.text
                




        

