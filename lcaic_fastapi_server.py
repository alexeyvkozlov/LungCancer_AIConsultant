#~ USAGE
# cd c:\LungCancer_AIConsultant
# .\lcenv\Scripts\activate
#~~~~~~~~~~~~~~~~~~~~~~~~
#~ сервер
# python lcaic_fastapi_server.py
#~~~~~~~~~~~~~~~~~~~~~~~~
#~ клиент
# http://127.0.0.1:8000
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
from fastapi import FastAPI
import uvicorn
from fastapi import Request, Body, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from settings_reader import SettingsReader
from lcaic_model2100 import Model2100Worker
from lcaic_model2101 import Model2101Worker


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class FastAPIServer:
  def __init__(self):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ путь к папке из которой запустили программу
    #~~~~~~~~~~~~~~~~~~~~~~~~
    print('~'*70)
    #~ ИИ-помощник по лечению Рака Легких (НМИЦ онкологии им. Н.Н. Блохина)
    print('[INFO] NMITS FastAPI-Server ver.2024.05.15')
    print('~'*70)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаем FastAPI-Сервер
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.app = FastAPI()
    #~ подключаем папку с статическими файлами (например, изображениями)
    self.app.mount("/static", StaticFiles(directory="static"), name="static")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ путь к папке из которой запустили программу
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.prog_path = os.getcwd()
    print(f'[INFO] program path: `{self.prog_path}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ читаем настройки из ini-фала
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(self.prog_path)
    self.serv_host = self.ini_reader.get_server_host()
    self.serv_port = self.ini_reader.get_server_port()
    self.ucredentials = self.ini_reader.get_ucredentials()
    self.htmltemplates_dir = self.ini_reader.get_htmltemplatesdir()
    print('[INFO] FastAPI server:')
    print(f'[INFO]   host: `{self.serv_host}`, port: {self.serv_port}')
    print(f'[INFO]   ucredentials: `{self.ucredentials}`')
    print(f'[INFO]   htmltemplates_dir: `{self.htmltemplates_dir}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ словарь пользователей
    self.users = {}
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ объекты для работы с моделями
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создание объекта для работы с моделью 2100
    self.m2100_obj = Model2100Worker(self.prog_path)
    #~ создание объекта для работы с моделью 2101
    self.m2101_obj = Model2101Worker(self.prog_path)
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def start(self):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ загрузка стартовой страницы html_pages/index.html
    @self.app.get("/")
    async def read_root():
    # async def read_root(request: Request):
      print('[INFO] FastAPIserver.read_root')
      html_name = os.path.join(self.htmltemplates_dir, 'index.html')
      return FileResponse(html_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ проверка уровня доступа пользователя
    @self.app.post("/hello/user")
    # def hello_user(data = Body()):
    def hello_user(request: Request, data=Body()):
      user_login = str(data["name"])
      user_password = str(data["pass"])
      #~ получаем IP-адрес клиента
      client_ip = request.client.host
      print(f'[INFO] user_login: `{user_login}`, user_password: `{user_password}`, client_ip: `{client_ip}`')
      #~ 0 - пользователя нет в базе
      #~ 1 - пользователь есть и доступ разрешен
      #~ 2 - пользователь есть, но доступ запрещен
      #~ 0     1        2      3  4        5    
      #~ login|password|access|id|FullName|Status
      #~ 0                 1     2 3 4                5    
      #~ natalia.tsarikova|pass8|0|8|Наталья Царикова|стажёр
      #~ alexey.v.kozlov|pass9|1|9|Козлов Алексей Вадимович|стажёр
      user_access = 0
      user_id = -1
      user_name = ''
      user_status = ''
      with open(self.ucredentials, 'r', encoding='UTF-8') as f:
        for line in f:
          data = line.strip().split('|')
          if 6 == len(data):
            if data[0] == user_login and data[1] == user_password:
              user_access = int(data[2])
              user_id = int(data[3])
              user_name = data[4]
              user_status = data[5]
              break
      print(f'[INFO] user_access: `{user_access}`')
      print(f'[INFO] user_id: `{user_id}`')
      print(f'[INFO] user_name: `{user_name}`')
      print(f'[INFO] user_status: `{user_status}`')
      #~~~~~~~~~~~~~~~~~~~~~~~~
      mess_str = ''
      if 0 == user_access:
        #~ 0 - пользователя нет в базе
        mess_str = "Ой, а Вас нет в базе..."
      elif 1 == user_access:
        #~ 1 - пользователь есть и доступ разрешен
        mess_str = user_name + ", добро пожаловать!"
        #~ пользователю доступ разрешен, добавляем его в словарь пользователей
        if not client_ip in self.users:
          # добавляем пользователя только если его нет в словаре
          self.users[client_ip] = {
            "id": user_id,
            "name": user_name,
            "status": user_status
          }
          print(f'[INFO] первое подключение - пользователь успешно добавлен: `{self.users}`')
        else:
          print(f'[INFO] повторное подключение: `{self.users}`')
      elif 2 == user_access:
        #~ 2 - пользователь есть, но доступ запрещен
        mess_str = user_name + ", Вам доступ запрещен!"
      #~~~~~~~~~~~~~~~~~~~~~~~~
      print(f'[INFO] mess_str: `{mess_str}`')
      return {"user_access": user_access, "user_id": user_id, "user_name": user_name, "user_status": user_status, "message": mess_str}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ загрузка страницы page210.html
    @self.app.get("/page210")
    def load_page210():
      html_name = os.path.join(self.htmltemplates_dir, 'page210.html')
      return FileResponse(html_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.get("/page2100")
    def load_page2100():
      html_name = os.path.join(self.htmltemplates_dir, "page2100.html")
      return FileResponse(html_name)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.post("/model2100")
    # def model_2100(data = Body()):
    def model_2100(request: Request, data = Body()):
      strPatientFullName = str(data["strPatientFullName"])
      strPatientHealthCIP = str(data["strPatientHealthCIP"])
      inxStage = int(data["inxStage"])
      inxHistology = int(data["inxHistology"])
      inxECOG = int(data["inxECOG"])
      inxAge = int(data["inxAge"])
      inxGender = int(data["inxGender"])
      inxMolecularStatus = int(data["inxMolecularStatus"])
      inxPD_L1Status = int(data["inxPD_L1Status"])
      inxSmokingStatus = int(data["inxSmokingStatus"])
      inxContraindicationsRT = int(data["inxContraindicationsRT"])
      inxPatientPreference = int(data["inxPatientPreference"])
      inxMedication = int(data["inxMedication"])
      inxChemotherapyVariant = int(data["inxChemotherapyVariant"])
      inxAltChemotherapyVariant = int(data["inxAltChemotherapyVariant"])
      inxConfidence = int(data["inxConfidence"])
      inxAlternative = int(data["inxAlternative"])
      inxComment = int(data["inxComment"])
      #~
      client_ip = request.client.host
      person_id = self.users[client_ip]['id']
      person_name = self.users[client_ip]['name']
      person_status = self.users[client_ip]['status']
      print(f'[INFO] client_ip: `{client_ip}`')
      print(f'[INFO]  person: id: {person_id}, name: `{person_name}`, status: `{person_status}`')
      report_marker = self.m2100_obj.make_report(person_id, person_name, person_status,
                                                 strPatientFullName, strPatientHealthCIP,
                                                 inxStage, inxHistology, inxECOG, inxAge,
                                                 inxGender, inxMolecularStatus, inxPD_L1Status,
                                                 inxSmokingStatus, inxContraindicationsRT, inxPatientPreference,
                                                 inxMedication, inxChemotherapyVariant, inxAltChemotherapyVariant,
                                                 inxConfidence, inxAlternative, inxComment)
      return {"report_marker": report_marker}
    #~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.get("/report2100")
    def load_report2100(pmarker: str):
      html_name = os.path.join(self.htmltemplates_dir, pmarker)
      return FileResponse(html_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.get("/page2101")
    def load_page2101():
      html_name = os.path.join(self.htmltemplates_dir, "page2101.html")
      return FileResponse(html_name)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.post("/model2101")
    # def model_2101(data = Body()):
    def model_2101(request: Request, data = Body()):
      strPatientFullName = str(data["strPatientFullName"])
      strPatientHealthCIP = str(data["strPatientHealthCIP"])
      inxHumanRace = int(data["inxHumanRace"])
      inxGender = int(data["inxGender"])
      inxAge = int(data["inxAge"])
      inxSmokingStatus = int(data["inxSmokingStatus"])
      inxECOG = int(data["inxECOG"])
      inxTumorLoad = int(data["inxTumorLoad"])
      inxCo_mutationKRAS = int(data["inxCo_mutationKRAS"])
      inxCo_mutationp53 = int(data["inxCo_mutationp53"])
      inxCo_mutationSTK11 = int(data["inxCo_mutationSTK11"])
      inxCo_mutationKEAP1 = int(data["inxCo_mutationKEAP1"])
      inxPeriodFromCLT = int(data["inxPeriodFromCLT"])
      inxMolecularStatus = int(data["inxMolecularStatus"])
      inxPD_L1Status = int(data["inxPD_L1Status"])
      inxPatientPreference = int(data["inxPatientPreference"])
      inxMedication = int(data["inxMedication"])
      inxConfidence = int(data["inxConfidence"])
      inxAlternative = int(data["inxAlternative"])
      inxComment = int(data["inxComment"])
      #~
      client_ip = request.client.host
      person_id = self.users[client_ip]['id']
      person_name = self.users[client_ip]['name']
      person_status = self.users[client_ip]['status']
      print(f'[INFO] client_ip: `{client_ip}`')
      print(f'[INFO]  person: id: {person_id}, name: `{person_name}`, status: `{person_status}`')
      report_marker = self.m2101_obj.make_report(person_id, person_name, person_status,
                                                 strPatientFullName, strPatientHealthCIP,
                                                 inxHumanRace, inxGender, inxAge,
                                                 inxSmokingStatus, inxECOG, inxTumorLoad,
                                                 inxCo_mutationKRAS, inxCo_mutationp53, inxCo_mutationSTK11,
                                                 inxCo_mutationKEAP1, inxPeriodFromCLT, inxMolecularStatus,
                                                 inxPD_L1Status, inxPatientPreference, 
                                                 inxMedication, inxConfidence, inxAlternative, inxComment)
      return {"report_marker": report_marker}
    #~~~~~~~~~~~~~~~~~~~~~~~~
    @self.app.get("/report2101")
    def load_report2101(pmarker: str):
      html_name = os.path.join(self.htmltemplates_dir, pmarker)
      return FileResponse(html_name)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    uvicorn.run(self.app, host=self.serv_host, port=self.serv_port)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  server = FastAPIServer()
  server.start()