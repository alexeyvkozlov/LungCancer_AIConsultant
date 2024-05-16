#~ USAGE
# cd c:\LungCancer_AIConsultant
# .\lcenv\Scripts\activate
#~~~~~~~~~~~~~~~~~~~~~~~~
# python lcaic_face_vgen.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ подключаем библиотеку машинного зрения
import cv2
#~ библиотека для вызова системных функций
import os

from settings_reader import SettingsReader
from dirfile_worker import DirectoryFileWorker


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ объект для формирования изображений лица из кадров видео-потока
#~ V - video stream
#~~~~~~~~~~~~~~~~~~~~~~~~
class FaceVGenerator:
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ путь к папке из которой запустили программу
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.prog_path = os.getcwd()
    print(f'[INFO] program path: `{self.prog_path}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ читаем настройки из ini-фала
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(self.prog_path)
    self.pseudo_camera_fmov = self.ini_reader.get_pseudo_camera_fmov()
    self.user_id = self.ini_reader.get_fid_userid()
    self.face_offset = self.ini_reader.get_fid_faceoffsetpix()
    self.train_dataset = self.ini_reader.get_fid_train_dataset()
    print(f'[INFO]  self.pseudo_camera_fmov: `{self.pseudo_camera_fmov}`')
    print(f'[INFO]  self.user_id: {self.user_id}')
    print(f'[INFO]  self.face_offset: {self.face_offset}')
    print(f'[INFO]  self.train_dataset: `{self.train_dataset}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаем объект для поиска лиц по примитивам Хаара
    self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~v - video
  def vrun(self):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаем папку для датасета
    #~~~~~~~~~~~~~~~~~~~~~~~~
    dir_filer = DirectoryFileWorker()
    dir_filer.create_directory(self.train_dataset)
    # print(f'[INFO] create_directory: `{self.train_dataset}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ счётчик изображений
    #~~~~~~~~~~~~~~~~~~~~~~~~
    i = 0
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ получаем доступ к камере vcam - video camera
    # vcam = cv2.VideoCapture(0)
    vcam = cv2.VideoCapture(self.pseudo_camera_fmov)
    #~~~~~~~
    print(f'[INFO] video-camera is opened: `{vcam.isOpened()}`')
    if not vcam.isOpened():
      print('[ERROR] can`t open video-camera')
      exit()
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ пока не нажата клавиша `q` — выполняем цикл
    # while True:
    while cv2.waitKey(1) != ord('q'):
    # while cv2.waitKey(500) != ord('q'):
      #~ получаем очередной кадр с камеры
      hasFrame,frame = vcam.read()
      #~ если кадра нет
      if not hasFrame:
        #~ останавливаемся и выходим из цикла
        cv2.waitKey()
        print('[ERROR] can`t receive frame (stream end?), exiting ...')
        break
      #~~~~~~~~~~~~~~~~~~~~~~
      #~ высота и ширина кадра
      frameHeight = frame.shape[0]
      frameWidth = frame.shape[1]
      # print(f'frame: w: {frameWidth}, h: {frameHeight}')
      #~~~~~~~~~~~~~~~~~~~~~~
      #~ переводим всё в ч/б для простоты
      gray_im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #~ настраиваем параметры распознавания и получаем лицо с камеры
      faces = self.detector.detectMultiScale(gray_im, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
      # print(f'faces: length: `{len(faces)}`')
      if 0 == len(faces):
        #~ добавляем текст в кадр, что нет лиц
        cv2.putText(frame, 'NO FACE', (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow('face-id', frame)
        continue
      elif len(faces) > 1:
        #~ добавляем текст в кадр, что нет лиц
        cv2.putText(frame, 'FACE COUNT > 1', (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)
        cv2.imshow('face-id', frame)
        continue
      #~~~~~~~~~~~~~~~~~~~~~~
      #~ обрабатываем лица
      for(x,y,w,h) in faces:
        #~ проверяем, что рамка лица находится в видео-кадре
        x1 = x-self.face_offset
        y1 = y-self.face_offset
        x2 = x+w+self.face_offset
        y2 = y+h+self.face_offset
        err_bbox = False
        # if w < 256 or h < 256:
        #   err_bbox = True
        if x1 < 0 or y1 < 0 or x2 >= frameWidth or y2 >= frameHeight:
          err_bbox = True
        if err_bbox:
          cv2.putText(frame, 'ERROR FACE BBOX', (100,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2, cv2.LINE_AA)
          cv2.imshow('face-id', frame)
          continue
        #~~~~~~~~~~~~~~~~~~~~~~
        #~ отображаем детектированное лицо на экране
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
        cv2.imshow('face-id', frame)
        #~~~~~~~~~~~~~~~~~~~~~~
        #~ записываем файл на диск
        fname1 = str(self.user_id) +'.'+ str(i) + '.png'
        fname2 = os.path.join(self.train_dataset, fname1)
        # print(f'[INFO] fname1: `{fname1}`, fname2: `{fname2}`')
        gray_imbbox = gray_im[y1:y2,x1:x2]
        gray_imres = cv2.resize(gray_imbbox, (256, 256))
        cv2.imwrite(fname2, gray_imres)
      #~~~~~~~~~~~~~~~~~~~~~~
      #~ увеличиваем счётчик кадров
      #~ если у нас хватает кадров, останавливаем цикл
      i = i + 1
      if i > 256:
        break
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ закрываем камеру и окна
    vcam.release()
    cv2.destroyAllWindows()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ the start of the code
if __name__ == '__main__':
  #~ make an instance of the class
  fvg = FaceVGenerator()
  #~ call the function run()
  fvg.vrun()