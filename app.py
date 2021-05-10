
import os
import streamlit as st
from db import Video
from social_distance_detector import use_video
from social_distancing_webcam import use_webcam
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        vid = Video(path=path)
        db.add(vid)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

st.title("Distance Violation Detection for Social Distancing")
st.info('This project is used to provide data to maintain social distancing ')
if st.checkbox("Videos"):
        video=st.file_uploader('Upload a video',type=['mp4','3gp'])
        if video and st.button("UPLOAD"):
          path=os.path.join('uploads',f'{video.name}')
          with open(path,'wb') as f:
            f.write(video.getbuffer())
            save_file(path)
            st.info('upload succesfully') 
if st.checkbox("detect on vid file"):
  db = opendb()
  videos=db.query(Video).all()
  db.close()
  vid = st.selectbox('select a video to play',videos)
  if vid and os.path.exists(vid.path) and st.button('start detection'):
      use_video(vid.path,"output/out.mp4")

if st.checkbox("Webcam"):
   if st.button('open webcam'):
       use_webcam()
    
if st.checkbox("About Project"):
    st.image('social.png')
    st.info('In the fight against the COVID-19, social distancing has proven to be a very effective measure to slow down the spread of the disease. People are asked to limit their interactions with each other, reducing the chances of the virus being spread with physical or close contact.In past also AI/Deep Learning has shown promising results on a number of daily life problems. In this, we will go through detailed explanation of how we can use Python, Computer Vision to monitor social distancing at public places and workplaces.To ensure social distancing protocol in public places and workplace, we are developing social distancing detection tool that can monitor if people are keeping a safe distance from each other by analyzing recorded videos by using cameras.')
    
if st.checkbox("Creator info"):
    st.header("About The Project Creators")
    st.write('Anchal Singh')
    st.write('Deepmala')
    st.image('code.jpg')

