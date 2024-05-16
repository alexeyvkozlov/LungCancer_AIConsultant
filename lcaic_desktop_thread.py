#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ библиотека для вызова системных функций
import os
#~ библиотека для работы с массивами данных
import numpy as np
#~ подключаем библиотеку компьютерного зрения
import cv2
#~ 
from PyQt6 import QtCore

from settings_reader import SettingsReader
from lcaic_model2101 import Model2101Worker


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ десктопный поток для работы нейронкой
#~~~~~~~~~~~~~~~~~~~~~~~~
class LungCancerDesktopThread(QtCore.QThread):
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ connect сигнал подключения или не подключения
  #~ str - access|id|FullName|Status
  conn_signal = QtCore.pyqtSignal(str)
  #~~~ сигнал отработки предикта по модели 2101
  pred2101_signal = QtCore.pyqtSignal(str)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, prog_path: str, parent=None):
    QtCore.QThread.__init__(self, parent)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Флаг выполнения
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.running = False
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ читаем настройки из ini-фала
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(prog_path)
    self.ucredentials = self.ini_reader.get_ucredentials()
    self.faceid_fname = self.ini_reader.get_trainer_fyml()
    self.pseudo_camera_fmov = self.ini_reader.get_pseudo_camera_fmov()
    print(f'[INFO]  ucredentials: `{self.ucredentials}`')
    print(f'[INFO]  faceid_fname: `{self.faceid_fname}`')
    print(f'[INFO]  self.pseudo_camera_fmov: `{self.pseudo_camera_fmov}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ 0 - none
    #~ 1 - вход по логину-паролю
    #~ 2 - вход по фотографии face-id
    #~ 3 - предсказание нейронки -> модель 2100
    #~ 4 - предсказание нейронки -> модель 2101
    self.client_mode = 0
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ нейронка для распознавания лиц
    self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    #~ добавляем в него модель, которую мы обучили на прошлых этапах
    self.recognizer.read(self.faceid_fname)
    #~ указываем, что мы будем искать лица по примитивам Хаара
    #~ имя шаблона притивов Хаара -> 'haarcascade_frontalface_default.xml'
    self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ нейронка для работы с моделью 2101 - иммунотерапия
    self.m2101_obj = Model2101Worker(prog_path)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ значения учетной записи пользователя\доктора
    #~~~~~~~
    #~ 0     1        2      3  4        5    
    #~ login|password|access|id|FullName|Status
    #~ 0                 1     2 3 4                5    
    #~ natalia.tsarikova|pass8|0|8|Наталья Царикова|стажёр
    #~ alexey.v.kozlov|pass9|1|9|Козлов Алексей Вадимович|стажёр
    #~ data[2]+'|'+data[3]+'|'+data[4]+'|'+data[5]
    self.doctor_id = -1
    self.doctor_name = ''
    self.doctor_status = ''
    #~~~~~~~
    self.user_login = ''
    self.user_password = ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ 1 - вход по логину-паролю
  def server_connect1(self, user_login, user_password):
    self.doctor_id = -1
    self.doctor_name = ''
    self.doctor_status = ''
    self.user_login = user_login
    self.user_password = user_password
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.client_mode = 1
    # print(f'[INFO] user_login: `{self.user_login}`, user_password: `{self.user_password}`, client_mode: `{self.client_mode}`')
    if not self.isRunning():
      self.start()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ 2 - вход по фотографии face-id
  def server_connect2(self):
    self.doctor_id = -1
    self.doctor_name = ''
    self.doctor_status = ''
    self.user_login = ''
    self.user_password = ''
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.client_mode = 2
    if not self.isRunning():
      self.start()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ запрос предсказания нейронки -> модель 2101
  def make_report2101(self, patient_name: str, patient_health_cip: str,
                      inxHumanRace: int, inxGender: int, inxAge: int,
                      inxSmokingStatus: int, inxECOG: int, inxTumorLoad: int,
                      inxCo_mutationKRAS: int, inxCo_mutationp53: int, inxCo_mutationSTK11: int,
                      inxCo_mutationKEAP1: int, inxPeriodFromCLT: int, inxMolecularStatus: int,
                      inxPD_L1Status: int, inxPatientPreference: int,
                      inxMedication: int, inxConfidence: int, inxAlternative: int, inxComment: int):
    self.patient_name = patient_name
    self.patient_health_cip = patient_health_cip
    #~~~
    self.inxHumanRace = inxHumanRace
    self.inxGender = inxGender
    self.inxAge = inxAge
    self.inxSmokingStatus = inxSmokingStatus
    self.inxECOG = inxECOG
    self.inxTumorLoad = inxTumorLoad
    self.inxCo_mutationKRAS = inxCo_mutationKRAS
    self.inxCo_mutationp53 = inxCo_mutationp53
    self.inxCo_mutationSTK11 = inxCo_mutationSTK11
    self.inxCo_mutationKEAP1 = inxCo_mutationKEAP1
    self.inxPeriodFromCLT = inxPeriodFromCLT
    self.inxMolecularStatus = inxMolecularStatus
    self.inxPD_L1Status = inxPD_L1Status
    self.inxPatientPreference = inxPatientPreference
    #~~~
    self.inxMedication = inxMedication
    self.inxConfidence = inxConfidence
    self.inxAlternative = inxAlternative
    self.inxComment = inxComment
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ 4 - предсказание нейронки -> модель 2101
    self.client_mode = 4
    # print(f'thread> make_report2101....')
    if not self.isRunning():
      # print(f'thread> not self.isRunning')
      self.start()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def run(self):
    # print(f'thread>run>: start...')
    self.running = True
    #~~~~~~~~~~~~~~~~~~~~~~~~
    if (1 == self.client_mode):
      #~ 1 - вход по логину-паролю
      print(f'[INFO] user_login: `{self.user_login}`, user_password: `{self.user_password}`')
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ 0 - пользователя нет в базе
      #~ 1 - пользователь есть и доступ разрешен
      #~ 2 - пользователь есть, но доступ запрещен
      #~ 0     1        2      3  4        5    
      #~ login|password|access|id|FullName|Status
      #~ 0                 1     2 3 4                5    
      #~ natalia.tsarikova|pass8|0|8|Наталья Царикова|стажёр
      #~ alexey.v.kozlov|pass9|1|9|Козлов Алексей Вадимович|стажёр
      user_access = 0
      self.doctor_id = -1
      self.doctor_name = ''
      self.doctor_status = ''
      with open(self.ucredentials, 'r', encoding='UTF-8') as f:
        for line in f:
          data = line.strip().split('|')
          if 6 == len(data):
            if data[0] == self.user_login and data[1] == self.user_password:
              user_access = int(data[2])
              self.doctor_id = int(data[3])
              self.doctor_name = data[4]
              self.doctor_status = data[5]
              break
      print(f'[INFO] user_access: `{user_access}`')
      print(f'[INFO] self.doctor_id: `{self.doctor_id}`')
      print(f'[INFO] self.doctor_name: `{self.doctor_name}`')
      print(f'[INFO] self.doctor_status: `{self.doctor_status}`')
      #~~~~~~~~~~~~~~~~~~~~~~~~
      doctor_info = ''
      if user_access > 0:
        if 1 == user_access:
          doctor_info = '1|'+self.doctor_name
        else:
          doctor_info = '2|'+self.doctor_name
      self.conn_signal.emit(doctor_info)
    elif (2 == self.client_mode):
      #~ 2 - подключение к серверу по фотографии face-id
      doctor_info = ''
      user_access = 0
      self.doctor_id = -1
      self.doctor_name = ''
      self.doctor_status = ''
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ t - total
      id_tnum = 0
      id8_num = 0
      id9_num = 0
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ получаем доступ к камере v-video
      #vcam = cv2.VideoCapture(0)
      #~~~~~~~
      # video_fname = os.path.join(self.faceid_path, '2023_1012_115956_009.MOV')
      # video_fname = os.path.join(self.faceid_path, 'NataliaTsarikova360.mp4')
      # video_fname = os.path.join(self.faceid_path, 'x-person360.mp4')
      # vcam = cv2.VideoCapture(video_fname)
      vcam = cv2.VideoCapture(self.pseudo_camera_fmov)
      if not vcam.isOpened():
        print("[ERROR] thread>run>: can`t open video-camera")
        self.conn_signal.emit(doctor_info)
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ пока не нажата любая клавиша или число кадров менее 100 — выполняем цикл
      while cv2.waitKey(1) < 0:
        #~ получаем очередной кадр с камеры
        hasFrame,frame = vcam.read()
        #~ если кадра нет
        if not hasFrame:
          #~ останавливаемся и выходим из цикла
          cv2.waitKey()
          break
        #~ высота и ширина кадра
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        #~~~~~~~~~~~~~~~~~~~~~~~~
        #~ переводим цветной кадр в ч/б
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #~ улучшение контраста - необязательно делать - ухудшает для детектирования
        # gray_frame = cv2.equalizeHist(gray_frame)
        #~~~~~~~~~~~~~~~~~~~~~~~~
        #~ определяем лица на видео
        faces = self.faceCascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
        #~ перебираем все найденные лица
        for(x,y,w,h) in faces:
          #~ получаем id пользователя (predicted id) и минимальное расстояние до лица при детектировании
          pred_id, face_mindist = self.recognizer.predict(gray_frame[y:y+h,x:x+w])
          #~ рисуем прямоугольник вокруг лица
          x1 = x-50
          y1 = y-50
          x2 = x+w+50
          y2 = y+h+50
          if 0 < x1 and 0 < y1 and x2 < frameWidth and y2 < frameHeight:
            id_tnum = id_tnum + 1
            if (8 == pred_id):
              id8_num = id8_num + 1
            elif (9 == pred_id):
              id9_num = id9_num + 1
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
        #~ отображаю детектированное лицо    
        cv2.imshow('face-id', frame)
        # cv2.imshow('face-id', gray_frame)
        if id_tnum > 99:
          break
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ when everything done, release the capture
      vcam.release()
      cv2.destroyAllWindows()
      #~~~~~~~~~~~~~~~~~~~~~~~~
      print(f'[INFO] thread>run>: id_tnum: `{id_tnum}`')
      print(f'[INFO] thread>run>: id8_num: `{id8_num}`')
      print(f'[INFO] thread>run>: id9_num: `{id9_num}`')
      if id8_num > 98:
        self.doctor_id = 8
      elif id9_num > 98:
        self.doctor_id = 9
      #~~~~~~~~~~~~~~~~~~~~~~~~
      #~ 0     1        2      3  4        5    
      #~ login|password|access|id|FullName|Status
      with open(self.ucredentials, 'r', encoding='UTF-8') as f:
        for line in f:
          data = line.strip().split('|')
          if 6 == len(data):
            print(f'[INFO] data[3]: {data[3]}, self.doctor_id: {self.doctor_id}')
            if int(data[3]) == self.doctor_id:
              user_access = int(data[2])
              # self.doctor_id = int(data[3])
              self.doctor_name = data[4]
              self.doctor_status = data[5]
              break
      print(f'[INFO] user_access: `{user_access}`')
      print(f'[INFO] self.doctor_id: `{self.doctor_id}`')
      print(f'[INFO] self.doctor_name: `{self.doctor_name}`')
      print(f'[INFO] self.doctor_status: `{self.doctor_status}`')
      #~~~~~~~~~~~~~~~~~~~~~~~~
      if user_access > 0:
        if 1 == user_access:
          doctor_info = '1|'+self.doctor_name
        else:
          doctor_info = '2|'+self.doctor_name
      self.conn_signal.emit(doctor_info)
    elif (4 == self.client_mode):
      # print(f'[INFO] thread>run>: predict 2101...')
      report_marker = self.m2101_obj.make_report(self.doctor_id, self.doctor_name, self.doctor_status,
                                                 self.patient_name, self.patient_health_cip,
                                                 self.inxHumanRace, self.inxGender, self.inxAge,
                                                 self.inxSmokingStatus, self.inxECOG, self.inxTumorLoad,
                                                 self.inxCo_mutationKRAS, self.inxCo_mutationp53, self.inxCo_mutationSTK11,
                                                 self.inxCo_mutationKEAP1, self.inxPeriodFromCLT, self.inxMolecularStatus,
                                                 self.inxPD_L1Status, self.inxPatientPreference,
                                                 self.inxMedication, self.inxConfidence, self.inxAlternative, self.inxComment)
      # print(f'[INFO] thread>run>: predict2101: {report_marker}')
      self.pred2101_signal.emit(report_marker)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.running = False
    self.client_mode = 0
    # print(f'thread>run>: finish!')