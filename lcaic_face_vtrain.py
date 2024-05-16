#~ USAGE
# cd c:\LungCancer_AIConsultant
# .\lcenv\Scripts\activate
#~~~~~~~~~~~~~~~~~~~~~~~~
# python lcaic_face_vtrain.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ подключаем библиотеку машинного зрения
import cv2
#~ библиотека для вызова системных функций
import os
#~ для обучения нейросетей
import numpy as np
#~ встроенная библиотека для работы с изображениями
from PIL import Image 

from settings_reader import SettingsReader
from dirfile_worker import DirectoryFileWorker


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ объект для обучения и формирования модели распознавания лиц из фрагментов кадров видео-потока
#~ V - video stream
#~~~~~~~~~~~~~~~~~~~~~~~~
class FaceVTrain:
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
    self.train_dataset = self.ini_reader.get_fid_train_dataset()
    self.faceid_fname = self.ini_reader.get_trainer_fyml()
    print(f'[INFO]  self.train_dataset: `{self.train_dataset}`')
    print(f'[INFO]  faceid_fname: `{self.faceid_fname}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаём новый распознаватель лиц
    self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    #~ указываем, что мы будем искать лица по примитивам Хаара
    self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ получаем картинки и подписи из датасета
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_images_and_labels(self, datapath):
    #~ получаем путь к картинкам
    image_paths = [os.path.join(datapath, f) for f in os.listdir(datapath)]
    #~ списки картинок и подписей на старте пустые
    images = []
    labels = []
    #~ перебираем все картинки в датасете 
    for image_path in image_paths:
      #~ читаем картинку и сразу переводим в ч/б
      image_pil = Image.open(image_path).convert('L')
      #~ переводим картинку в numpy-массив
      image = np.array(image_pil, 'uint8')
      #~ получаем id пользователя из имени файла
      nbr = int(os.path.split(image_path)[1].split(".")[0].replace('face-', ""))
      #~ определяем лицо на картинке
      faces = self.faceCascade.detectMultiScale(image)
      #~ если лицо найдено
      for (x, y, w, h) in faces:
        #~ добавляем его к списку картинок 
        images.append(image[y: y + h, x: x + w])
        #~ добавляем id пользователя в список подписей
        labels.append(nbr)
        #~ выводим текущую картинку на экран
        cv2.imshow('[INFO]  Adding faces to traning set...', image[y: y + h, x: x + w])
        #~ делаем паузу
        cv2.waitKey(100)
    #~ возвращаем список картинок и подписей
    return images, labels

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~v - video
  def vrun(self):
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ получаем список картинок и подписей
    images, labels = self.get_images_and_labels(self.train_dataset)
    #~ обучаем модель распознавания на наших картинках и учим сопоставлять её лица и подписи к ним
    self.recognizer.train(images, np.array(labels))
    #~ сохраняем модель
    dir_filer = DirectoryFileWorker()
    model_dir = dir_filer.get_file_directory(self.faceid_fname)
    # print(f'[INFO]  model_dir: `{model_dir}`, faceid_fname: `{self.faceid_fname}`')
    dir_filer.create_directory(model_dir)
    self.recognizer.save(self.faceid_fname)
    #~ удаляем из памяти все созданные окнаы
    cv2.destroyAllWindows()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ the start of the code
if __name__ == '__main__':
  #~ make an instance of the class
  fvt = FaceVTrain()
  #~ call the function run()
  fvt.vrun()