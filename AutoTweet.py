#!/usr/bin/python
# coding: utf-8 

from selenium import webdriver
from time import sleep
from datetime import datetime
from threading import Timer
from selenium.webdriver.common.keys import Keys
import sys, os, traceback, time

#Este bot servirá para poder hacer encuestas desde la línea de comandos
#Es muy fácil de usar, a pesar de eso tendrá la documentación necesaria. 
#	$python AutoQuiz.py <nombre de usuario> <contraseña>
#       Seguir instrucciones. 
#Author:Francisco Javier Lendinez Tirado
#Mejoras siguientes: Hacer que funcione. 

#Función para registrarse en la página.
def log_in(Driver,user,passwd):
        elemUser = Driver.find_element_by_xpath("//input[contains(@class,'js-username-field email-input') and contains(@name,'session[username_or_email]')]")
        elemUser.click()
        elemPass = Driver.find_element_by_xpath("//input[contains(@class,'password') and contains(@name,'session[password]')]")
        for car in user:
                elemUser.send_keys(car)
                
        for car in passwd:
                elemPass.send_keys(car)
        elemPass.submit()

        return Driver

def extractComments():
        commentList = []
        textLines = open('.\\comments.txt','r').readlines()
        text = ""
        startWritting = False
        tiempo = None
        
        for line in textLines:
                if line.startswith("##"):
                        startWritting = False
                        if text != "":
                                commentList.append((tiempo,text))
                        text=""
                        tiempo = None
                        continue
                if "[Tweet]" in line:
                        startWritting = True
                else:
                        if line.startswith("[["):
                                tiempoStr = line.replace("[","").replace("]","").strip()
                                tiempo = datetime.strptime(tiempoStr, "%d/%m/%Y %H:%M:%S")
                        else:
                                if(startWritting):
                                        text+=line.decode("utf-8")
        if text != "":
                commentList.append((tiempo,text))
        return commentList

def comentar(Driver, comentario):
        inBox = Driver.find_element_by_xpath("//div[contains(@class,'tweet-box rich-editor')]")
        inBox.click()
        acBox = Driver.find_element_by_xpath("//div[contains(@class,'tweet-box rich-editor is-showPlaceholder')]")
        if(len(comentario)<140):
                for character in comentario:
                        acBox.send_keys(character)
        submitButton = Driver.find_element_by_xpath("//button[contains(@class,'tweet-action tweet-btn')]")
        submitButton.click()
        return Driver

#Open a Firefox window with the address given
def chargeDriver(address):
	Driver = webdriver.Chrome()
	Driver.get(address)
	return Driver

#Execute all the remain functions
def MainProcess(address, user, passwd):
	try:
		Driver = chargeDriver(address)
		Driver = log_in(Driver, user,passwd)
		commentList =  extractComments()
		for tiempo, comentario in commentList:
                        if(tiempo == None):
                                Driver = comentar(Driver, comentario)
                                sleep(3)
                        else:
                                x=datetime.today()
                                delta_t=tiempo-x
                                secs=delta_t.seconds+1
                                print "Quedan "+ str(secs) + " segundos para enviar el comentario "+ comentario
                                t = Timer(secs, comentar,[Driver,comentario])
                                t.run()
		#Aquí debería ir el script
		Driver.quit()
	except:
                traceback.print_exc()
		raw_input("Ha ocurrido un error, pulsa cualquier tecla para salir.")
		Driver.quit()

if __name__ == '__main__':
 	apps = open('.\\config.txt','r').readlines()
        address = "http://www.twitter.com/login"
        user=""
        passwd=""
        for a in apps:
            if a.find("Username:") != -1:
                user = a.split(":")[1].strip()
                break

        for b in apps:
            if b.find("Password:") != -1:
                passwd = b.split(":")[1].strip()
                break
        try:
            MainProcess(address, user, passwd)
        except:
            traceback.print_exc()
            raw_input(" ")
