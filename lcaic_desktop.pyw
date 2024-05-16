#~ USAGE
# cd c:\LungCancer_AIConsultant
# .\lcenv\Scripts\activate
#~~~~~~~~~~~~~~~~~~~~~~~~
# python lcaic_desktop.pyw
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QLineEdit

from settings_reader import SettingsReader
from lcaic_desktop_thread import LungCancerDesktopThread

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Lung Cancer Artificial Intelligence Consultant Window
#~~~~~~~~~~~~~~~~~~~~~~~~
class LungCancerAICWindow(QtWidgets.QWidget):
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, parent=None):
    QtWidgets.QWidget.__init__(self, parent)
    uic.loadUi("lcaic_form.ui", self)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ путь к папке из которой запустили программу
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.prog_path = os.getcwd()
    print(f'[INFO] program path: `{self.prog_path}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ читаем настройки из ini-фала
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(self.prog_path)
    #~ путь к папке с логотипами
    self.logo_path = self.ini_reader.get_logodir()
    #~ путь к папке с отчетами
    self.medreport_path = self.ini_reader.get_medreportdir()
    self.htmltemplates_dir = self.ini_reader.get_htmltemplatesdir()
    #~~~~~~~~~~~~~~~~~~~~~~~~
    print('[INFO] Lung Cancer Artificial Intelligence Consultant:')
    print(f'[INFO]  logo_path: `{self.logo_path}`')
    print(f'[INFO]  medreport_path: `{self.medreport_path}`')
    print(f'[INFO]  htmltemplates_dir: `{self.htmltemplates_dir}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создание объектов
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ создание отдельного потока для предсказаний
    #~ lcdc - lung cancer desktop client 
    self.lcdcthread = LungCancerDesktopThread(self.prog_path)
    #~~~~~~~
    self.lcdcthread.conn_signal.connect(self.on_conn_signal,
        QtCore.Qt.ConnectionType.QueuedConnection)
    self.lcdcthread.pred2101_signal.connect(self.on_pred2101_signal,
        QtCore.Qt.ConnectionType.QueuedConnection)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Создаем лого-таймер таймер и устанавливаем интервал в 500 миллисекунд
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.logo_timer = QtCore.QTimer(self)
    self.logo_timer.setInterval(150)
    # Останавливаем таймер
    self.logo_timer.stop()
    self.logo_inx = 0
    self.logo_step = 1
    self.logo_max = 9
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ предстартовые настройки
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ название программы и версия в титуле виджета
    #~ НИИ клинической онкологии им. Н.Н. Трапезникова 
    #~ отделение лекарственных методов лечения (химиотерапевтическое) №17
    #~ Мы - коллектив врачей отделения лекарственных методов лечения №17 
    #~ Национального медицинского исследовательского центра онкологии им. Н. Н. Блохина, 
    #~ являющегося крупнейшей онкологической клиникой России и Европы.
    #~ https://oncopulm.ru/#openismed 
    #~ https://onconext.ru/
    #~ Лактионов Константин Константинович|заведующий отделением, профессор, д.м.н.
    str1 = 'ИИ-помощник по лечению Рака Легких (НМИЦ онкологии им. Н.Н. Блохина)'
    str1 += ' ver.2024.05.16'
    self.setWindowTitle(str1)
    #~~~изображения на форме
    str1 = os.path.join(self.logo_path, "logoa0.png")
    #print(f'str1: {str1}')
    self.lblLogoImg.setPixmap(QPixmap(str1))
    str1 = os.path.join(self.logo_path, "logot.png")
    self.setWindowIcon(QIcon(str1))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ режим формы
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ 1 - вход в программу
    #~ 2 - форма для нейронки -> модель 2100
    #~ 3 - форма для нейронки -> модель 2101
    #~ 4 - отображение результатов предсказания
    self.form_mode = 1
    # print(f'init: self.form_mode: `{self.form_mode}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ наполнение виджетов данными
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ подключение к серверу
    #window.setFixedWidth(992)
    #window.setFixedHeight(292)
    #~ enum EchoMode { Normal, NoEcho, Password, PasswordEchoOnEdit };
    self.edtUserPassword.setEchoMode(QLineEdit.EchoMode.Password)
    #~~~ для отладки
    self.edtUserLogin.setText('alexey.v.kozlov')
    self.edtUserPassword.setText('pass9')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ пациент
    self.edtPatientFullName.setText('Потапова Анастасия Леонтьевна')
    self.edtPatientHealthCIP.setText('1234567890123456')
    #~~~ классификатор Рака Легких
    #~1. Стадия:
    ind_list = []
    model_ftxt = self.ini_reader.get_stage_mode_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxStageMode.addItems(ind_list)
      self.cbxStageMode.setCurrentIndex(2)
    #~2. Размеры клеток:
    model_ftxt = self.ini_reader.get_cell_mode_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxCellMode.addItems(ind_list)
      self.cbxCellMode.setCurrentIndex(1)
    #~3. Операбельность:
    model_ftxt = self.ini_reader.get_operable_mode_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxOperableMode.addItems(ind_list)
      self.cbxOperableMode.setCurrentIndex(0)
    #~4. Терапия:
    model_ftxt = self.ini_reader.get_therapy_mode_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxTherapyMode.addItems(ind_list)
      self.cbxTherapyMode.setCurrentIndex(1)
    #~~~ выписка модель-2101 - заполняю списки параметров
    #~~~1. Раса:
    model_ftxt = self.ini_reader.get_model2101_01_human_race_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxHumanRace2101.addItems(ind_list)
      self.cbxHumanRace2101.setCurrentIndex(1)
    #~~~2. Пол:
    model_ftxt = self.ini_reader.get_model2101_02_gender_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxGender2101.addItems(ind_list)
      self.cbxGender2101.setCurrentIndex(1)
    #~~~3. Возраст:
    model_ftxt = self.ini_reader.get_model2101_03_age_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxAge2101.addItems(ind_list)
      self.cbxAge2101.setCurrentIndex(0)
    #~~~4. Статус курения:
    model_ftxt = self.ini_reader.get_model2101_04_smoking_status_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxSmokingStatus2101.addItems(ind_list)
      self.cbxSmokingStatus2101.setCurrentIndex(2)
    #~~~5. ECOG:
    model_ftxt = self.ini_reader.get_model2101_05_ecog_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxECOG2101.addItems(ind_list)
      self.cbxECOG2101.setCurrentIndex(1)
    #~~~6. Есть опухолевая нагрузка? (симптомная опухоль):
    model_ftxt = self.ini_reader.get_model2101_06_10_no_yes_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxTumorLoad2101.addItems(ind_list)
      self.cbxTumorLoad2101.setCurrentIndex(1)
    #~~~7. Ко-мутации KRAS:
    self.cbxCo_mutationKRAS2101.addItems(ind_list)
    self.cbxCo_mutationKRAS2101.setCurrentIndex(1)
    #~~~8. Ко-мутации p53.:
    self.cbxCo_mutationp532101.addItems(ind_list)
    self.cbxCo_mutationp532101.setCurrentIndex(1)
    #~~~9. Ко-мутации STK11:
    self.cbxCo_mutationSTK112101.addItems(ind_list)
    self.cbxCo_mutationSTK112101.setCurrentIndex(1)
    #~~~10. Ко-мутации KEAP1:
    self.cbxCo_mutationKEAP12101.addItems(ind_list)
    self.cbxCo_mutationKEAP12101.setCurrentIndex(1)
    #~~~11. Срок от окончания ХЛТ:
    model_ftxt = self.ini_reader.get_model2101_11_period_from_clt_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxPeriodFromCLT2101.addItems(ind_list)
      self.cbxPeriodFromCLT2101.setCurrentIndex(2)
    #~~~12. Молекулярный статус (только для неплоскоклеточного рака):
    model_ftxt = self.ini_reader.get_model2101_12_molecular_status_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxMolecularStatus2101.addItems(ind_list)
      self.cbxMolecularStatus2101.setCurrentIndex(0)
    #~~~13. PD-L1 статус:
    model_ftxt = self.ini_reader.get_model2101_13_pd_l1_status_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxPD_L1Status2101.addItems(ind_list)
      self.cbxPD_L1Status2101.setCurrentIndex(0)
    #~~~14. Предпочтение пациента по ответу на терапию:
    model_ftxt = self.ini_reader.get_model2101_14_patient_preference_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxPatientPreference2101.addItems(ind_list)
      self.cbxPatientPreference2101.setCurrentIndex(0)
    #~~~ Назначить лечение:
    #~~~1. Медикамент:
    model_ftxt = self.ini_reader.get_model2101_15_expert_recommendation_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxMedication2101.addItems(ind_list)
      self.cbxMedication2101.setCurrentIndex(0)
    #~~~2. Уверенность:
    model_ftxt = self.ini_reader.get_model2101_16_18_confidence_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxConfidence2101.addItems(ind_list)
      self.cbxConfidence2101.setCurrentIndex(1)
    #~~~3. Альтернатива:
    model_ftxt = self.ini_reader.get_model2101_19_alternative_therapy50_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxAlternative2101.addItems(ind_list)
      self.cbxAlternative2101.setCurrentIndex(3)
    #~~~4. Комментарий:
    model_ftxt = self.ini_reader.get_model2101_20_comment_code_ftxt()
    ind_list = self.read_inx_list(model_ftxt)
    # print(f'[INFO]  ind_list: len: {len(ind_list)}, `{ind_list}`')
    if len(ind_list) > 0:
      self.cbxComment2101.addItems(ind_list)
      self.cbxComment2101.setCurrentIndex(1)
    #~~~~~~~
    #~ назначенное лечение отображается без возможности редактирования
    self.txtOutput.setReadOnly(True)
    #~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ отработка combobox
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.cbxStageMode.currentIndexChanged.connect(self.on_stage_mode_changed)
    self.cbxCellMode.currentIndexChanged.connect(self.on_cell_mode_changed)
    self.cbxOperableMode.currentIndexChanged.connect(self.on_operable_mode_changed)
    self.cbxTherapyMode.currentIndexChanged.connect(self.on_therapy_mode_changed)
    #~ реакция кнопок
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.btnQuit.clicked.connect(QtWidgets.QApplication.instance().quit)
    #~self.btnQuit.clicked.connect(self.on_getformsize_clicked)
    self.btnNext.clicked.connect(self.on_next_clicked)
    self.btnFaceID.clicked.connect(self.on_faceid_clicked)
    #~ подключаем обработчик тиков таймера
    self.logo_timer.timeout.connect(self.update_logo_time)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    self.show_hide_widgets()
    # устанавливаем фокус на элементе self.edtUserLogin
    self.edtUserLogin.setFocus()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Запускаем лого-таймер
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.logo_inx = 0
    self.logo_step = 1
    self.logo_timer.start()
    #~~~~~~~~~~~~~~~~~~~~~~~~

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ вызов производится при закрытии окна
  def closeEvent(self, event):
    #~ скрываем окно
    self.hide()
    #~ изменяем флаг выполнения
    #if self.lc3thread.running:
    #  self.lc3thread.running = False
    #  # Даем время, чтобы закончить
    #  self.lc3thread.wait(1000)
    #~ закрываем окно
    event.accept()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def read_inx_list(self, txt_fpath):
    inx_list = []
    with open(txt_fpath, 'r', encoding='UTF-8') as f:
      for line in f:
        data = line.strip().split('|')
        if 2 == len(data):
          list_len = len(inx_list)
          list_len_str = str(list_len)
          #~ проверяем, что txt-файл сформирован корректно
          if data[0] == list_len_str:
            inx_list.append(data[1])
          else:
            inx_list.clear()
            break
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return inx_list

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ реакция на изменения combo-box
  def on_stage_mode_changed(self, index):
    # print(f'>on_stage_mode_changed: `{index}`')
    if not 2 == index:
      QMessageBox.warning(self, "Внимание!", "Раздел находится в разработке")
      self.cbxStageMode.setCurrentIndex(2)
  #~~~
  def on_cell_mode_changed(self, index):
    if not 1 == index:
      QMessageBox.warning(self, "Внимание!", "Раздел находится в разработке")
      self.cbxCellMode.setCurrentIndex(1)
  #~~~
  def on_operable_mode_changed(self, index):
    if not 0 == index:
      QMessageBox.warning(self, "Внимание!", "Раздел находится в разработке")
      self.cbxOperableMode.setCurrentIndex(0)
  #~~~
  def on_therapy_mode_changed(self, index):
    if 0 == index:
      QMessageBox.warning(self, "Внимание!", "Раздел находится в разработке")
      self.cbxTherapyMode.setCurrentIndex(1)
    elif 1 == self.form_mode:
      #~ 2 - форма для нейронки -> модель 2100
      #~ 3 - форма для нейронки -> модель 2101
      self.form_mode = 3
      # print(f'on_therapy_mode_changed: self.form_mode: `{self.form_mode}`')
      self.show_hide_widgets()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Вызывается при нажатии на кнопку btnNext
  def on_next_clicked(self):
    # print(f'on_next_clicked: self.form_mode: `{self.form_mode}`')
    if 1 == self.form_mode:
      #~ 1 - вход в программу
      #~ Запускаем лого-таймер
      # print('[INFO] on_next_clicked: 1 -> 3...')
      self.logo_inx = 0
      self.logo_step = 1
      self.logo_timer.start()
      #~~~~~~~~~~~~~~~~~~~~~~~~
      self.btnFaceID.setEnabled(False)
      self.btnNext.setEnabled(False)
      self.lcdcthread.server_connect1(self.edtUserLogin.text(),
                                      self.edtUserPassword.text())
    elif 3 == self.form_mode:
      #~ 3 - форма для нейронки -> модель 2101
      #~~ переход к 4 - отображение результатов предсказания
      # print(f'on_next_clicked: 3 -> 4...')
      self.btnNext.setEnabled(False)
      self.lcdcthread.make_report2101(self.edtPatientFullName.text(),
                                      self.edtPatientHealthCIP.text(),
                                      self.cbxHumanRace2101.currentIndex(),
                                      self.cbxGender2101.currentIndex(),
                                      self.cbxAge2101.currentIndex(),
                                      self.cbxSmokingStatus2101.currentIndex(),
                                      self.cbxECOG2101.currentIndex(),
                                      self.cbxTumorLoad2101.currentIndex(),
                                      self.cbxCo_mutationKRAS2101.currentIndex(),
                                      self.cbxCo_mutationp532101.currentIndex(),
                                      self.cbxCo_mutationSTK112101.currentIndex(),
                                      self.cbxCo_mutationKEAP12101.currentIndex(),
                                      self.cbxPeriodFromCLT2101.currentIndex(),
                                      self.cbxMolecularStatus2101.currentIndex(),
                                      self.cbxPD_L1Status2101.currentIndex(),
                                      self.cbxPatientPreference2101.currentIndex(),
                                      self.cbxMedication2101.currentIndex(),
                                      self.cbxConfidence2101.currentIndex(),
                                      self.cbxAlternative2101.currentIndex(),
                                      self.cbxComment2101.currentIndex())
    elif 4 == self.form_mode:
      #~ 4 - отображение результатов предсказания
      #~~ переход к 2 - форма для нейронки -> модель 2100
      #~~           3 - форма для нейронки -> модель 2101
      # print(f'on_next_clicked: 4 -> 3...')
      self.form_mode = 3
      self.btnNext.setEnabled(True)
      self.btnNext.setText(' далее > ')
      self.show_hide_widgets()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ Вызывается при нажатии на кнопку btnFaceID
  def on_faceid_clicked(self):
    #~ 1 - вход в программу
    #~ Запускаем лого-таймер
    self.logo_inx = 0
    self.logo_step = 1
    self.logo_timer.start()
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.btnFaceID.setEnabled(False)
    self.btnNext.setEnabled(False)
    self.lcdcthread.server_connect2()
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ Обработчик тиков таймера
  def update_logo_time(self):
    #~~~изображения лого в виджете
    str1 = "logoa" + str(self.logo_inx) + ".png" 
    # self.lblUserPassword.setText(str1)
    str2 = os.path.join(self.logo_path, str1)
    # print(f'[INFO] logo: `{str2}`')
    self.lblLogoImg.setPixmap(QPixmap(str2))
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.logo_inx += self.logo_step
    if  1 == self.logo_step:
      if self.logo_inx > self.logo_max:
        self.logo_inx = self.logo_max-1
        self.logo_step = -1
    else:
      if self.logo_inx < 0:
        self.logo_inx = 0
        self.logo_step = 1

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def show_hide_widgets(self):
    # print(f'show_hide_widgets: self.form_mode: `{self.form_mode}`')
    #~ видимость,доступность  виджетов
    if 1 == self.form_mode:
      #~ 1 - вход в программу
      self.grbxEntrance.setVisible(True)
      self.grbxPatient.setVisible(False)
      self.grbxClassifier.setVisible(False)
      self.grbxOptions2101.setVisible(False)
      self.grbxMedication2101.setVisible(False)
      self.grbxMedReport.setVisible(False)
    elif 3 == self.form_mode:
      #~ 2 - форма для нейронки -> модель 2100
      #~ 3 - форма для нейронки -> модель 2101
      self.grbxEntrance.setVisible(False)
      self.grbxPatient.setVisible(True)
      self.grbxClassifier.setVisible(True)
      self.grbxOptions2101.setVisible(True)
      self.grbxMedication2101.setVisible(True)
      self.grbxMedReport.setVisible(False)
    elif 4 == self.form_mode:
      #~ 4 - отображение результатов предсказания
      self.grbxEntrance.setVisible(False)
      self.grbxPatient.setVisible(False)
      self.grbxClassifier.setVisible(False)
      self.grbxOptions2101.setVisible(False)
      self.grbxMedication2101.setVisible(False)
      self.grbxMedReport.setVisible(True)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def on_conn_signal(self, s):
    #~ access|FullName
    if s:
      doctor_info_lst = s.split('|')
      if '1' == doctor_info_lst[0]:
        #~ 2 - форма для нейронки -> модель 2100
        #~ 3 - форма для нейронки -> модель 2101
        self.form_mode = 3
        # print(f'> on_conn_signal: self.form_mode: `{self.form_mode}`')
      else:
        QMessageBox.warning(self, "Внимание!", doctor_info_lst[1]+" - доступ запрещен!")
    else:
      # Выводим декодированное предсказание пользователю
      QMessageBox.critical(self, "Внимание!", "Ой, а Вас нет в базе...")
    #~ оживляем кнопки
    self.btnFaceID.setEnabled(True)
    self.btnNext.setEnabled(True)
    #~ останавливаем лого-таймер
    self.logo_timer.stop()
    self.show_hide_widgets()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def on_pred2101_signal(self, s):
    lst2101 = []
    rep2101_fname = os.path.join(self.htmltemplates_dir, s)
    # print(f'rep2101_fname: `{rep2101_fname}`')
    with open(rep2101_fname, 'r', encoding='UTF-8') as f2101:
      lst2101 = f2101.readlines()
    # print(f'len: `{len(lst2101)}`')
    html_str3 = ''
    for i in range(len(lst2101)):
      html_str1 = str(lst2101[i])
      # print(f'i: {i}, html_str1: `{html_str1}`')
      # i: 28, html_str1: `    <td><img src="/static/logo.png" alt="logo" width="181" height="75"></td>
      if 28 == i: continue
      html_str2 = html_str1.replace('\n', '')
      html_str3 += html_str2
    self.txtOutput.setHtml(html_str3)
    #~ 4 - отображение результатов предсказания
    self.form_mode = 4
    # print(f'> on_pred2101_signal: self.form_mode: `{self.form_mode}`')
    self.btnNext.setEnabled(True)
    self.btnNext.setText(' < вернуться ')
    self.show_hide_widgets()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  window = LungCancerAICWindow()
  #window.setFixedWidth(992)
  #window.setFixedHeight(292)
  window.setGeometry(10, 50, 992, 292)
  window.show()
  sys.exit(app.exec())