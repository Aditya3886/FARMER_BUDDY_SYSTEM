import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import natsort
import xlwt
import datetime

import mysql.connector
 
 

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="Aditya@123", db="logo")
    c = _conn.cursor()
    print("successful")
    return c, _conn

# -------------------------------register-----------------------------------------------------------------
def user_reg(id,username, password, email, mobile, address,):
    try:
        print("hello")
        c, conn = db_connect()
        print(id,username, password, email,
               mobile, address)
        j = c.execute("insert into register (id,username,password,email,mobile,address) values ('"+id+"','"+username +
                      "','"+password+"','"+email+"','"+mobile+"','"+address+"')")
        conn.commit()
        conn.close()
        print("successful")
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
# -------------------------------------Login --------------------------------------
def user_loginact(username, password):
    try:
        print("*************************")
        print("in userlogin act")
        print("*************************")
        
        c, conn = db_connect()
        j = c.execute("select * from register where username='" +
                      username+"' and password='"+password+"'")
        data = c.fetchall()
        print(data)
        for a in data:
            print(a[0])
            session['uname'] = a[0]       
        c.fetchall()
        conn.close()
        print("***************************")
        print("in try")
        return j
    except Exception as e:
        print("**************************")
        print("exception")
        return(str(e))
#-------------------------------------Upload Image------------------------------------------
def user_upload(id,name, image):
    try:
        c, conn = db_connect()
        print(name,image)
        username = session['username']
        j = c.execute("insert into upload (id,name,image,username) values ('"+id+"','"+name+"','"+image +"','"+username +"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

#---------------------------------------View Images---------------------------------------
def user_viewimages(username):
    c, conn = db_connect()
    c.execute("select * from upload where  username='"+username +"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
#------------------------------------Track----------------------------------------------------
def view_pred(prediction):
    c, conn = db_connect()
    print("track before")
    c.execute("Select * From crop where id='"+str(prediction)+"'")
    print("track agter")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
# ----------------------------------------------Update Items------------------------------------------

def image_info(image_path):
    print("#####################################")
    print(image_path)
    print("##################################")
    classes = {0:"Alluvial",1:"Black",2:"Clay",3:"Red"}
# dimensions of our images
    img_width, img_height = 224,224
# load the model we saved
    model = load_model('vgg19_98_86_25epochs.h5')
# predicting images
    img = image.load_img(image_path, target_size=(img_width, img_height))
    # image = image.load_img(image_path,target_size=(224,224))
    x = image.img_to_array(img)
    # x = image/255
    x = np.expand_dims(x,axis=0)

#model = load_model('soilnew.h5')
    result = model.predict(x)
    print(result)
    a=np.argmax(result[0])
    prediction = classes[a]
        
    print(image_path)  
    #result="Alluvial"
    c, conn = db_connect()
    c.execute("SELECT * FROM soilcrop WHERE soiltype ='"+prediction+"' ORDER BY RAND() LIMIT 1")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

if __name__ == "__main__":
    db_connect()
