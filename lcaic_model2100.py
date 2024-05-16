#~~~ модель 2100
#~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ библиотека для вызова системных функций
import os
#~ библиотека для работы с массивами данных
import numpy as np
from datetime import datetime
#~~~~~~~
#~ tensorflow загрузка, сохраненной модели
#~ import tensorflow as tf
from tensorflow.keras.models import load_model
#~~~~~~~
#~ импорт библиотеки TFLite
# import tensorflow.lite as lite

from settings_reader import SettingsReader
from dirfile_worker import DirectoryFileWorker


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ объект для работы с моделью
#~~~~~~~~~~~~~~~~~~~~~~~~
class Model2100Worker:
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, prog_path: str):
    self.prog_path = prog_path
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(self.prog_path)
    model21000_path = self.ini_reader.get_model21000()
    self.expert21000 = self.ini_reader.get_expert21000()
    self.status21000 = self.ini_reader.get_status21000()
    model21001_path = self.ini_reader.get_model21001()
    self.expert21001 = self.ini_reader.get_expert21001()
    self.status21001 = self.ini_reader.get_status21001()
    model21002_path = self.ini_reader.get_model21002()
    self.expert21002 = self.ini_reader.get_expert21002()
    self.status21002 = self.ini_reader.get_status21002()
    self.htmltemplates_dir = self.ini_reader.get_htmltemplatesdir()
    self.medreport_dir = self.ini_reader.get_medreportdir()
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаем директорию для результатов
    self.dir_filer = DirectoryFileWorker()
    # self.dir_filer.remove_create_directory(self.report_dir)
    self.dir_filer.create_directory(self.medreport_dir)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    print('[INFO] Model2100Worker:')
    print(f'[INFO]  program path: `{self.prog_path}`')
    print(f'[INFO]  model21000: `{model21000_path}`')
    print(f'[INFO]  expert21000: `{self.expert21000}`')
    print(f'[INFO]  status21000: `{self.status21000}`')
    print(f'[INFO]  model21001: `{model21001_path}`')
    print(f'[INFO]  expert21001: `{self.expert21001}`')
    print(f'[INFO]  status21001: `{self.status21001}`')
    print(f'[INFO]  model21002: `{model21002_path}`')
    print(f'[INFO]  expert21002: `{self.expert21002}`')
    print(f'[INFO]  status21002: `{self.status21002}`')
    print(f'[INFO]  htmltemplates_dir: `{self.htmltemplates_dir}`')
    print(f'[INFO]  medreport_dir: `{self.medreport_dir}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21000.h5 0|Лактионов Константин Константинович|заведующий отделением, профессор, д.м.н.
    #~~~ отсортированный список по возрастанию conclusion_lst
    self.conclusion_lst0 = [111116, 111125, 111127, 111132, 111155, 111175, 112255, 112311, 112314, 112327, 112411, 112447, 112555, 112567, 223311, 223443]
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ загрузка модели нейронной сети Deep Neural Network
    #~ путь к tensorflow файлу-модели
    self.model21000 = load_model(model21000_path)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # model_fname0 = os.path.join(model_path, FLMODELH5_21000)
    # self.model21000 = lite.Interpreter(model_path=model_fname0)
    # self.model21000.allocate_tensors()
    # self.input_details0 = self.model21000.get_input_details()
    # self.output_details0 = self.model21000.get_output_details()
    # self.input_shape0 = self.input_details0[0]['shape']
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21001.h5 1|Денисова Елена Сергеевна|онколог
    self.conclusion_lst1 = [111222, 111232, 111322, 111323, 111332, 111333, 111432, 111433, 112323, 112333, 112432, 112433, 223111, 323111, 412433, 542222, 542232, 642432, 712323, 712333, 811342, 933323, 933333]
    self.model21001 = load_model(model21001_path)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # model_fname1 = os.path.join(model_path, FLMODELH5_21001)
    # self.model21001 = lite.Interpreter(model_path=model_fname1)
    # self.model21001.allocate_tensors()
    # self.input_details1 = self.model21001.get_input_details()
    # self.output_details1 = self.model21001.get_output_details()
    # self.input_shape1 = self.input_details1[0]['shape']
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21002.h5 2|Савченко Илья Вячеславович|онколог, химиотерапевт
    self.conclusion_lst2 = [111222, 111232, 111322, 111323, 111332, 111333, 111432, 111433, 112323, 112333, 112432, 112433, 223111, 323111, 412433, 542222, 542232, 642432, 712323, 712333, 811342, 933323, 933333]
    self.model21002 = load_model(model21002_path)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # model_fname2 = os.path.join(model_path, FLMODELH5_21002)
    # self.model21002 = lite.Interpreter(model_path=model_fname2)
    # self.model21002.allocate_tensors()
    # self.input_details2 = self.model21002.get_input_details()
    # self.output_details2 = self.model21002.get_output_details()
    # self.input_shape2 = self.input_details2[0]['shape']
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.report_counter = 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ кодирование x-вектора
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def onehot_encoder(self, num: int, digit_count: int): 
    '''
    Числовое кодирование one-hot-encoding
    Args:
      num - число для кодирования
      digit_count - число разрядов
    Returns:
      num в виде списка one-hot-encoding
    '''
    #~~~~~~~~~~~~~~~~~~~~~~~~
    retVal = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(digit_count):
      if i == num:
        retVal.append(1)
      else:
        retVal.append(0)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getXLstVector(self, inxStage,inxHistology,inxECOG,inxAge,inxGender,inxMolecularStatus,
                    inxPD_L1Status,inxSmokingStatus,inxContraindicationsRT,inxPatientPreference):
    '''
    Числовое кодирование X-вектора
    Args:
      inxStage...inxPatientPreference - числовые индексы из списка возможных
    Returns:
      массив числовых кодов
    '''
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # print(f"2100> 1. 'Стадия': `{inxStage}`")
    # print(f"2100> 2. 'Гистология': `{inxHistology}`")
    # print(f"2100> 3. 'ECOG': `{inxECOG}`")
    # print(f"2100> 4. 'Возраст': `{inxAge}`")
    # print(f"2100> 5. 'Пол': `{inxGender}`")
    # print(f"2100> 6. 'Молекулярный статус (только для неплоскоклеточного рака)': `{inxMolecularStatus}`")
    # print(f"2100> 7. 'PD-L1 статус': `{inxPD_L1Status}`")
    # print(f"2100> 8. 'Статус курения': `{inxSmokingStatus}`")
    # print(f"2100> 9. 'Относительные противопоказания к ЛТ': `{inxContraindicationsRT}`")
    # print(f"2100> 10. 'Предпочтение пациента по ответу на терапию': `{inxPatientPreference}`")
    #~~~~~~~~~~~~~~~~~~~~~~~~
    retVal = []
    #~~~1. 'Стадия'
    retVal.append(inxStage)
    #~~~2. 'Гистология': one-hot-encoding
    ohe_lst2 = self.onehot_encoder(inxHistology, 3)
    retVal.extend(ohe_lst2)
    #~~~3. 'ECOG'
    ohe_lst3 = self.onehot_encoder(inxECOG, 3)
    retVal.extend(ohe_lst3)
    #~~~4. 'Возраст'
    retVal.append(inxAge)
    #~~~5. 'Пол'
    retVal.append(inxGender)
    #~~~6. 'Молекулярный статус (только для неплоскоклеточного рака)'
    ohe_lst6 = self.onehot_encoder(inxMolecularStatus, 16)
    retVal.extend(ohe_lst6)
    #~~~7. 'PD-L1 статус'
    ohe_lst7 = self.onehot_encoder(inxPD_L1Status, 4)
    retVal.extend(ohe_lst7)
    #~~~8. 'Статус курения'
    ohe_lst8 = self.onehot_encoder(inxSmokingStatus, 4)
    retVal.extend(ohe_lst8)
    #~~~9. 'Относительные противопоказания к ЛТ'
    retVal.append(inxContraindicationsRT)
    #~~~10. 'Предпочтение пациента по ответу на терапию'
    retVal.append(inxPatientPreference)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    del ohe_lst2
    del ohe_lst3
    del ohe_lst6
    del ohe_lst7
    del ohe_lst8
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # print(f' >retVal: len: {len(retVal)}: {retVal}')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ получение реверсивных значений
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseExpertRecommendationCode(self, num):
    '''
    Получение текстового значения `Ответ эксперта (Лактионов)` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = 'лучевая терапия'
    elif 2 == num:
      retVal = 'монохимиотерапия'
    elif 3 == num:
      retVal = 'ПХТ'
    elif 4 == num:
      retVal = 'симптоматическая терапия'
    elif 5 == num:
      retVal = 'одномоментная ХЛТ'
    elif 6 == num:
      retVal = 'переход на вариант лечения IV стадии'
    elif 7 == num:
      retVal = 'последовательная ХЛТ'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseExpertRecommendationCode12(self, num):
    '''
    Получение текстового значения `Ответ эксперта (Денисова,Савченко)` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = 'симптоматическая терапия'
    elif 2 == num:
      retVal = 'одномоментная ХЛТ'
    elif 3 == num:
      retVal = 'последовательная ХЛТ'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseChemotherapyVariantCode(self, num):
    '''
    Получение текстового значения `Вариант ХТ` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'Паклитаксел+Карбоплатин'
    elif 3 == num:
      retVal = 'Пеметрексед'
    elif 4 == num:
      retVal = 'Пеметрексед+Цисплатин'
    elif 5 == num:
      retVal = 'Этопозид Карбоплатин'
    elif 6 == num:
      retVal = 'Этопозид монорежим'
    elif 7 == num:
      retVal = 'Этопозид+Цисплатин'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseChemotherapyVariantCode12(self, num):
    '''
    Получение текстового значения `Вариант ХТ` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'Пеметрексед+цисплатин'
    elif 3 == num:
      retVal = 'Этопозид+цисплатин'
    elif 4 == num:
      retVal = 'Этопозид цисплатин/карбоплатин Дурвалумаб'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseAlternativeChemotherapyVariantCode(self, num):
    '''
    Получение текстового значения `Альтернативный выбор ХТ (как компонента ХЛТ)` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'еженедельный Паклитаксел'
    elif 3 == num:
      retVal = 'Паклитаксел'
    elif 4 == num:
      retVal = 'Пеметрексед'
    elif 5 == num:
      retVal = 'Этопозид монорежим'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseAlternativeChemotherapyVariantCode12(self, num):
    '''
    Получение текстового значения `Альтернативный выбор ХТ (как компонента ХЛТ)` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'еженедельный Паклитаксел+карбоплатин'
    elif 3 == num:
      retVal = 'Паклитаксел+карбоплатин'
    elif 4 == num:
      retVal = 'Этопозид карбоплатин'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseConfidence1007550Code(self, num):
    '''
    Получение числового значения `Поставьте галочку, если уверены на 100%`,`Если 75%`,`Если 50%`
    по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      числового значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = 'уверенность 100%'
    elif 2 == num:
      retVal = 'уверенность 75%'
    elif 3 == num:
      retVal = 'уверенность 50%'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseAlternativeTherapy50Code(self, num):
    '''
    Получение текстового значения `Альтернатива, если 50% - обязательно` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'вариант лечения IV стадии'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseAlternativeTherapy50Code12(self, num):
    '''
    Получение текстового значения `Альтернатива, если 50% - обязательно` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'Лучевая терапия в монорежиме'
    elif 3 == num:
      retVal = 'Симпоматическая терапия'
    elif 4 == num:
      retVal = 'последовательная ХЛТ'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseCommentCode(self, num):
    '''
    Получение текстового значения `Комментарий` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'Большая вероятность инкурабельности больного.'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseCommentCode12(self, num):
    '''
    Получение текстового значения `Комментарий` по категориальному значению
    Args:
      num - числовое категориальное значение
    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num:
      retVal = '0'
    elif 2 == num:
      retVal = 'Большая вероятность инкурабельности больного. Детально оценить общесоматический статус для решения вопроса о возможности проведения монохимиотерапии или проведение ЛТ в монорежиме.'
    elif 3 == num:
      retVal = 'Возможно рассмотреть вопрос ЛТ в монорежиме.'
    elif 4 == num:
      retVal = 'Наиболее часто при мелкоклеточном раке статус по шкале ECOG3 связан с основным заболеванием. И требует скорейшего начала химиотерапии.'
    elif 5 == num:
      retVal = 'Необходима более детальная оценка сопутствующей патологии и чем именно обусловлен статус по шкале ECOG 2. Если основным заболеванием, то предпочтение отдаем одновременной ХЛТ, если все-таки тяжесть состояния обусловлена сопутсвующей патологией, то возможно выбрать последовательный вариант ХЛТ. При выборе одновременной ХЛТ, лучше рассмотреть вариант еженедельного введения химиотерапии.'
    elif 6 == num:
      retVal = 'Необходима детальная оценка статуса по шкале ECOG. При мелкоклеточном раке чаще всего статус определяет основное заболевание, следовательно возможно начало одновременной ХЛТ, если все таки статус ECOG обусловлен сопуствующей патологией, то возможно отдать предпочтение последовательному варианту ХЛТ.'
    elif 7 == num:
      retVal = 'Необходима консультация хирурга для решения вопроса о возможной санации, в случае улучшения общего состояния пациента, возможно рассмотреть вариант проведения последовательной ХЛТ.'
    elif 8 == num:
      retVal = 'Необходима консультация хирурга на предмет возможного удаления паренхиматозного очага распада. Если невозможно - тщательная оценка риска кровотечения перед началом лучевой терапии.'
    elif 9 == num:
      retVal = 'Требуется дополнительная оценка статуса пациента, консультация хирурга для решения вопроса о возможной санации с последующим решением вопроса о химиотерапии. При невозможности коррекции общего состояния, рассмотреть вопрос о симптоматической терапии.'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def reverse_conclusion(self, num):
    '''
    Реверсирование кода заключения и перевод чисел в слова
    Args:
      num - числовой код заключения
    Returns:
      список значений
    '''
    retVal = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    digits = []
    while num > 0:
      digits.append(num % 10)
      num //= 10
    # print(f'digits: len: {len(digits)}: {digits}')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ 13 - N1 - 'Ответ эксперта (Лактионов)'
    retVal.append(self.getReverseExpertRecommendationCode(digits[0]))
    #~~~ 14 - N1 - 'Вариант ХТ'
    retVal.append(self.getReverseChemotherapyVariantCode(digits[1]))
    #~~~ 15 - N1 - 'Альтернативный выбор ХТ (как компонента ХЛТ)'
    retVal.append(self.getReverseAlternativeChemotherapyVariantCode(digits[2]))
    #~~~ 16 - N1 - 'Поставьте галочку, если уверены на 100%'
    #~~~ 17 - N1 - 'Если 75%'
    #~~~ 18 - N1 - 'Если 50%'
    retVal.append(self.getReverseConfidence1007550Code(digits[3]))
    #~~~ 19 - N1 - 'Альтернатива, если 50% - обязательно'
    retVal.append(self.getReverseAlternativeTherapy50Code(digits[4]))
    #~~~ 20 - N1 - 'Комментарий'
    retVal.append(self.getReverseCommentCode(digits[5]))
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def reverse_conclusion12(self, num):
    '''
    Реверсирование кода заключения и перевод чисел в слова
    Args:
      num - числовой код заключения
    Returns:
      список значений
    '''
    retVal = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    digits = []
    while num > 0:
      digits.append(num % 10)
      num //= 10
    # print(f'digits: len: {len(digits)}: {digits}')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ 11 - L1 - 'Ответ эксперта (Лактионов)'
    retVal.append(self.getReverseExpertRecommendationCode12(digits[0]))
    #~~~ 12 - L1 - 'Вариант ХТ'
    retVal.append(self.getReverseChemotherapyVariantCode12(digits[1]))
    #~~~ 13 - L1 - 'Альтернативный выбор ХТ (как компонента ХЛТ)'
    retVal.append(self.getReverseAlternativeChemotherapyVariantCode12(digits[2]))
    #~~~ 14 - L1 - 'Поставьте галочку, если уверены на 100%'
    #~~~ 15 - L1 - 'Если 75%'
    #~~~ 16 - L1 - 'Если 50%'
    retVal.append(self.getReverseConfidence1007550Code(digits[3]))
    #~~~ 17 - L1 - 'Альтернатива, если 50% - обязательно'
    retVal.append(self.getReverseAlternativeTherapy50Code12(digits[4]))
    #~~~ 18 - L1 - 'Комментарий'
    retVal.append(self.getReverseCommentCode12(digits[5]))
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseStage(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'IIIаI'
    elif 1 == num:
      retVal = 'IIIб'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseHistology(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'плоскоклеточный'
    elif 1 == num:
      retVal = 'неплоскоклеточный'
    elif 2 == num:
      retVal = 'мелкоклеточный'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseEcog(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0-1'
    elif 1 == num:
      retVal = '2'
    elif 2 == num:
      retVal = '3+'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseAge(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'до 70'
    elif 1 == num:
      retVal = '>70'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseGender(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'мужской'
    elif 1 == num:
      retVal = 'женский'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseMolecularStatus(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'не исследовались'
    elif 1 == num:
      retVal = 'нет мутаций'
    elif 2 == num:
      retVal = 'ALK'
    elif 3 == num:
      retVal = 'BRAF'
    elif 4 == num:
      retVal = 'EGFR (G719X, L816Q, S768I)'
    elif 5 == num:
      retVal = 'EGFR T790M'
    elif 6 == num:
      retVal = 'EGFR ex18'
    elif 7 == num:
      retVal = 'EGFR ex19'
    elif 8 == num:
      retVal = 'EGFR ex20'
    elif 9 == num:
      retVal = 'EGFR ex21'
    elif 10 == num:
      retVal = 'HER2'
    elif 11 == num:
      retVal = 'KRAS G12C'
    elif 12 == num:
      retVal = 'MET 14ex'
    elif 13 == num:
      retVal = 'NTRK'
    elif 14 == num:
      retVal = 'RET'
    elif 15 == num:
      retVal = 'ROS1'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReversePD_L1Status(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'не исследовался'
    elif 1 == num:
      retVal = '1 %'
    elif 2 == num:
      retVal = '1–49 %'
    elif 3 == num:
      retVal = '≥50 %'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseSmokingStatus(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'в настоящее время'
    elif 1 == num:
      retVal = 'курение в прошлом (бросил более 1 месяца до 1 года)'
    elif 2 == num:
      retVal = 'курение в прошлом (бросил более 1 года)'
    elif 3 == num:
      retVal = 'никогда не курил'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseContraindicationsRT(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'нет'
    elif 1 == num:
      retVal = 'да'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReversePatientPreference(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'результативность лечения'
    elif 1 == num:
      retVal = 'сохранение качества жизни'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorExpertRecommendation(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'лучевая терапия'
    elif 1 == num:
      retVal = 'монохимиотерапия'
    elif 2 == num:
      retVal = 'ПХТ' 
    elif 3 == num:
      retVal = 'симптоматическая терапия' 
    elif 4 == num:
      retVal = 'одномоментная ХЛТ' 
    elif 5 == num:
      retVal = 'переход на вариант лечения IV стадии' 
    elif 6 == num:
      retVal = 'последовательная ХЛТ' 
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorChemotherapyVariant(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0'
    elif 1 == num:
      retVal = 'Паклитаксел+Карбоплатин'
    elif 2 == num:
      retVal = 'Пеметрексед'
    elif 3 == num:
      retVal = 'Пеметрексед+Цисплатин'
    elif 4 == num:
      retVal = 'Этопозид Карбоплатин'
    elif 5 == num:
      retVal = 'Этопозид монорежим'
    elif 6 == num:
      retVal = 'Этопозид+Цисплатин'
    elif 7 == num:
      retVal = 'Этопозид цисплатин/карбоплатин Дурвалумаб'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorAltChemotherapyVariant(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0'
    elif 1 == num:
      retVal = 'еженедельный Паклитаксел'
    elif 2 == num:
      retVal = 'Паклитаксел'
    elif 3 == num:
      retVal = 'Пеметрексед'
    elif 4 == num:
      retVal = 'Этопозид монорежим'
    elif 5 == num:
      retVal = 'еженедельный Паклитаксел+карбоплатин'
    elif 6 == num:
      retVal = 'Паклитаксел+карбоплатин'
    elif 7 == num:
      retVal = 'Этопозид карбоплатин'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorConfidence1007550(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '100%'
    elif 1 == num:
      retVal = '75%'
    elif 2 == num:
      retVal = '50%' 
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorAlternativeTherapy50(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0'
    elif 1 == num:
      retVal = 'вариант лечения IV стадии'
    elif 2 == num:
      retVal = 'Лучевая терапия в монорежиме'
    elif 3 == num:
      retVal = 'Симпоматическая терапия'
    elif 4 == num:
      retVal = 'последовательная ХЛТ'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorComment(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0'
    elif 1 == num:
      retVal = 'Большая вероятность инкурабельности больного.'
    elif 2 == num:
      retVal = 'Большая вероятность инкурабельности больного. Детально оценить общесоматический статус для решения вопроса о возможности проведения монохимиотерапии или проведение ЛТ в монорежиме.'
    elif 3 == num:
      retVal = 'Возможно рассмотреть вопрос ЛТ в монорежиме.'
    elif 4 == num:
      retVal = 'Наиболее часто при мелкоклеточном раке статус по шкале ECOG3 связан с основным заболеванием. И требует скорейшего начала химиотерапии.'
    elif 5 == num:
      retVal = 'Необходима более детальная оценка сопутствующей патологии и чем именно обусловлен статус по шкале ECOG 2. Если основным заболеванием, то предпочтение отдаем одновременной ХЛТ, если все-таки тяжесть состояния обусловлена сопутсвующей патологией, то возможно выбрать последовательный вариант ХЛТ. При выборе одновременной ХЛТ, лучше рассмотреть вариант еженедельного введения химиотерапии.'
    elif 6 == num:
      retVal = 'Необходима детальная оценка статуса по шкале ECOG. При мелкоклеточном раке чаще всего статус определяет основное заболевание, следовательно возможно начало одновременной ХЛТ, если все таки статус ECOG обусловлен сопуствующей патологией, то возможно отдать предпочтение последовательному варианту ХЛТ.'
    elif 7 == num:
      retVal = 'Необходима консультация хирурга для решения вопроса о возможной санации, в случае улучшения общего состояния пациента, возможно рассмотреть вариант проведения последовательной ХЛТ.'
    elif 8 == num:
      retVal = 'Необходима консультация хирурга на предмет возможного удаления паренхиматозного очага распада. Если невозможно - тщательная оценка риска кровотечения перед началом лучевой терапии.'
    elif 9 == num:
      retVal = 'Требуется дополнительная оценка статуса пациента, консультация хирурга для решения вопроса о возможной санации с последующим решением вопроса о химиотерапии. При невозможности коррекции общего состояния, рассмотреть вопрос о симптоматической терапии.'
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ строковые интерпретации данных
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_patient_lst(self, patient_name: str, patient_health_cip: str):
    retVal = []
    retVal.append('Пациент:')
    retVal.append('  1. Фамилия, имя, отчество: ' + patient_name)
    retVal.append('  2. Полис ОМС: ' + patient_health_cip)
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_patient_discharge_lst(self, inxStage,inxHistology,inxECOG,inxAge,
                                inxGender,inxMolecularStatus,inxPD_L1Status,
                                inxSmokingStatus,inxContraindicationsRT,inxPatientPreference):
    retVal = []
    retVal.append('Выписка пациента:')
    str_n = self.getReverseStage(inxStage)
    retVal.append('  1. Стадия: ' + str_n)
    str_n = self.getReverseHistology(inxHistology)
    retVal.append('  2. Гистология: ' + str_n)
    str_n = self.getReverseEcog(inxECOG)
    retVal.append('  3. ECOG: ' + str_n)
    str_n = self.getReverseAge(inxAge)
    retVal.append('  4. Возраст: ' + str_n)
    str_n = self.getReverseGender(inxGender)
    retVal.append('  5. Пол: ' + str_n)
    str_n = self.getReverseMolecularStatus(inxMolecularStatus)
    retVal.append('  6. Молекулярный статус (только для неплоскоклеточного рака): ' + str_n)
    str_n = self.getReversePD_L1Status(inxPD_L1Status)
    retVal.append('  7. PD-L1 статус: ' + str_n)
    str_n = self.getReverseSmokingStatus(inxSmokingStatus)
    retVal.append('  8. Статус курения: ' + str_n)
    str_n = self.getReverseContraindicationsRT(inxContraindicationsRT)
    retVal.append('  9. Относительные противопоказания к ЛТ: ' + str_n)
    str_n = self.getReversePatientPreference(inxPatientPreference)
    retVal.append('  10. Предпочтение пациента по ответу на терапию: ' + str_n)
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_ai_expert_conclusion_lst(self, expert_index: str, 
                                   expert_medication: str, expert_chemotherapy_variant: str, 
                                   expert_altchemotherapy_variant: str, expert_confidence: str,
                                   expert_alternative: str, expert_comment: str):
    retVal = []
    retVal.append('Рекомендация ии-эксперта "№' + expert_index + ':')
    retVal.append('  1. Терапия: ' + expert_medication)
    retVal.append('  2. Вариант ХТ: ' + expert_chemotherapy_variant)
    retVal.append('  3. Альтернативный выбор ХТ (как компонента ХЛТ): ' + expert_altchemotherapy_variant)
    retVal.append('  4. Уверенность: ' + expert_confidence)
    retVal.append('  5. Альтернатива, если 50% - обязательно: ' + expert_alternative)
    retVal.append('  6. Комментарий: ' + expert_comment)
    #~~~
    if '1' == expert_index:
      retVal.append('  7. Фамилия, имя, отчество ии-эксперта: ' + self.expert21000)
      retVal.append('  8. Статус ии-эксперта: ' + self.status21000)
    elif '2' == expert_index:
      retVal.append('  7. Фамилия, имя, отчество ии-эксперта: ' + self.expert21001)
      retVal.append('  8. Статус ии-эксперта: ' + self.status21001)
    elif '3' == expert_index:
      retVal.append('  7. Фамилия, имя, отчество ии-эксперта: ' + self.expert21002)
      retVal.append('  8. Статус ии-эксперта: ' + self.status21002)
    #~~~
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_doctor_conclusion_lst(self, doctor_name: str, doctor_status: str,
                                inxMedication: int, inxChemotherapyVariant: int, inxAltChemotherapyVariant: int,
                                inxConfidence: int, inxAlternative: int, inxComment: int):
    retVal = []
    retVal.append('Заключение лечащего врача:')
    str_n = self.getReverseDoctorExpertRecommendation(inxMedication)
    retVal.append('  1. Терапия: ' + str_n)
    str_n = self.getReverseDoctorChemotherapyVariant(inxChemotherapyVariant)
    retVal.append('  2. Вариант ХТ: ' + str_n)
    str_n = self.getReverseDoctorAltChemotherapyVariant(inxAltChemotherapyVariant)
    retVal.append('  3. Альтернативный выбор ХТ (как компонента ХЛТ): ' + str_n)
    str_n = self.getReverseDoctorConfidence1007550(inxConfidence)
    retVal.append('  4. Уверенность: ' + str_n)
    str_n = self.getReverseDoctorAlternativeTherapy50(inxAlternative)
    retVal.append('  5. Альтернатива, если 50% - обязательно: ' + str_n)
    str_n = self.getReverseDoctorComment(inxComment)
    retVal.append('  6. Комментарий: ' + str_n)
    #~~~
    retVal.append('  7. Фамилия, имя, отчество врача: ' + doctor_name)
    retVal.append('  8. Статус врача: ' + doctor_status)
    #~~~ дата, время: 
    now_dt = datetime.now()
    str_n = now_dt.strftime("%Y.%m.%d %H:%M")
    retVal.append('  9. Дата, время: ' + str_n)
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~
  def patch_html_str(self, str_val: str):
    str1 = str_val.replace('>', '&gt;')
    retVal = str1.replace('<', '&lt;')
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ заключение-отчет на основании модели 2100
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def make_report(self, doctor_id: int, doctor_name: str, doctor_status: str,
                  patient_name: str, patient_health_cip: str,
                  inxStage: int, inxHistology: int, inxECOG, inxAge: int,
                  inxGender: int, inxMolecularStatus: int, inxPD_L1Status: int,
                  inxSmokingStatus: int, inxContraindicationsRT: int, inxPatientPreference: int,
                  inxMedication: int, inxChemotherapyVariant: int, inxAltChemotherapyVariant: int,
                  inxConfidence: int, inxAlternative: int, inxComment: int):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21000.h5 0|Лактионов Константин Константинович|заведующий отделением, профессор, д.м.н.
    x_row_lst0 = self.getXLstVector(inxStage,inxHistology,inxECOG,inxAge,inxGender,inxMolecularStatus,
                                    inxPD_L1Status,inxSmokingStatus,inxContraindicationsRT,inxPatientPreference)
    x_row_arr0 = np.array(x_row_lst0, dtype=np.float32).reshape(1, len(x_row_lst0))
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~ tensorflow
    pred0 = self.model21000.predict(x_row_arr0)
    #~~~~~~~ tensorflow-light
    # #~ установка входного тензора в модель
    # self.model21000.set_tensor(self.input_details0[0]['index'], x_row_arr0)
    # #~ выполнение интерпретации модели на входных данных
    # self.model21000.invoke()
    # #~ получение выходного тензора из модели
    # pred0 = self.model21000.get_tensor(self.output_details0[0]['index'])
    #~~~~~~~
    pred0_inx_max = np.argmax(pred0[0,:])
    conclusion_code0 = self.conclusion_lst0[pred0_inx_max]
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ akozlov hard-code 2023.11.20
    # conclusion_code0 = 223443
    rev_conclusion_lst0 = self.reverse_conclusion(conclusion_code0)
    print(f'[INFO]  >conclusion_code0: {conclusion_code0}')
    print(f'[INFO]  >rev_conclusion_lst0: {rev_conclusion_lst0}')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21001.h5 1|Денисова Елена Сергеевна|онколог
    x_row_lst1 = self.getXLstVector(inxStage,inxHistology,inxECOG,inxAge,inxGender,inxMolecularStatus,
                                    inxPD_L1Status,inxSmokingStatus,inxContraindicationsRT,inxPatientPreference)
    x_row_arr1 = np.array(x_row_lst1, dtype=np.float32).reshape(1, len(x_row_lst1))
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~ tensorflow
    pred1 = self.model21001.predict(x_row_arr1)
    #~~~~~~~ tensorflow-light
    # self.model21001.set_tensor(self.input_details1[0]['index'], x_row_arr1)
    # self.model21001.invoke()
    # pred1 = self.model21001.get_tensor(self.output_details1[0]['index'])
    #~~~~~~~
    pred1_inx_max = np.argmax(pred1[0,:])
    conclusion_code1 = self.conclusion_lst1[pred1_inx_max]
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ akozlov hard-code 2023.11.20
    # conclusion_code1 = 223111
    rev_conclusion_lst1 = self.reverse_conclusion12(conclusion_code1)
    print(f'[INFO]  >conclusion_code1: {conclusion_code1}')
    print(f'[INFO]  >rev_conclusion_lst1: {rev_conclusion_lst1}')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21002.h5 2|Савченко Илья Вячеславович|онколог, химиотерапевт
    x_row_lst2 = self.getXLstVector(inxStage,inxHistology,inxECOG,inxAge,inxGender,inxMolecularStatus,
                                    inxPD_L1Status,inxSmokingStatus,inxContraindicationsRT,inxPatientPreference)
    x_row_arr2 = np.array(x_row_lst2, dtype=np.float32).reshape(1, len(x_row_lst2))
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~ tensorflow
    pred2 = self.model21002.predict(x_row_arr2)
    #~~~~~~~ tensorflow-light
    # self.model21002.set_tensor(self.input_details2[0]['index'], x_row_arr2)
    # self.model21002.invoke()
    # pred2 = self.model21002.get_tensor(self.output_details2[0]['index'])
    #~~~~~~~
    pred2_inx_max = np.argmax(pred2[0,:])
    conclusion_code2 = self.conclusion_lst2[pred2_inx_max]
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ akozlov hard-code 2023.11.20
    # conclusion_code2 = 223111
    rev_conclusion_lst2 = self.reverse_conclusion12(conclusion_code2)
    print(f'[INFO] >conclusion_code2: {conclusion_code2}')
    print(f'[INFO] >rev_conclusion_lst2: {rev_conclusion_lst2}')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ формирование отчета-заключения
    #~~~~~~~~~~~~~~~~~~~~~~~~
    patient_lst = self.get_patient_lst(patient_name, patient_health_cip)
    patient_discharge_lst = self.get_patient_discharge_lst(inxStage,inxHistology,inxECOG,inxAge,
                                                          inxGender,inxMolecularStatus,inxPD_L1Status,
                                                          inxSmokingStatus,inxContraindicationsRT,inxPatientPreference)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    ai_expert0_conclusion_lst = self.get_ai_expert_conclusion_lst('1',
                                                                  rev_conclusion_lst0[0], rev_conclusion_lst0[1],
                                                                  rev_conclusion_lst0[2], rev_conclusion_lst0[3],
                                                                  rev_conclusion_lst0[4], rev_conclusion_lst0[5])
    ai_expert1_conclusion_lst = self.get_ai_expert_conclusion_lst('2',
                                                                  rev_conclusion_lst1[0], rev_conclusion_lst1[1],
                                                                  rev_conclusion_lst1[2], rev_conclusion_lst1[3],
                                                                  rev_conclusion_lst1[4], rev_conclusion_lst1[5])
    ai_expert2_conclusion_lst = self.get_ai_expert_conclusion_lst('3',
                                                                  rev_conclusion_lst2[0], rev_conclusion_lst2[1],
                                                                  rev_conclusion_lst2[2], rev_conclusion_lst2[3],
                                                                  rev_conclusion_lst2[4], rev_conclusion_lst2[5])
    #~~~~~~~~~~~~~~~~~~~~~~~~
    doctor_conclusion_lst = self.get_doctor_conclusion_lst(doctor_name, doctor_status,
                                                          inxMedication, inxChemotherapyVariant, inxAltChemotherapyVariant,
                                                          inxConfidence, inxAlternative, inxComment)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ после того как списки сформированы, записывает текстовый файл отчета
    #~~~~~~~~~~~~~~~~~~~~~~~~
    now_dt = datetime.now()
    dt_str = now_dt.strftime("%Y%m%d%H%M%S")
    patient_name2 = patient_name.replace(' ', '')
    str_n = dt_str + '_' + patient_name2 + '.txt'
    medreport_fname = os.path.join(self.medreport_dir, str_n)
    with open(medreport_fname, 'w', encoding='UTF-8') as f0:
      f0.write('Химиолучевая терапия. Медицинское заключение.\n\n')
      for str_n in patient_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in patient_discharge_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in ai_expert0_conclusion_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in ai_expert1_conclusion_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in ai_expert2_conclusion_lst:
        f0.write(str_n + '\n')
      f0.write('\n\n')
      f0.write('-'*70)
      f0.write('\n')
      for str_n in doctor_conclusion_lst:
        f0.write(str_n + '\n')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ и финальное - формируем html-документ для отображения результата
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ формируем маркер создаваемого html-файла
    self.report_counter += 1
    if self.report_counter > 1000000:
      self.report_counter = 0
    dt_str = now_dt.strftime("%Y%m%d%H%M%S")
    #~ 'rm2100_' ->  r - report, m - model
    report_marker = 'rm2100_' + dt_str + str(self.report_counter) + '.html'
    #~ открываю html-шаблон-отчета
    #~ 'page210rh.html' -> r - report, h - head
    fname1 = os.path.join(self.htmltemplates_dir, 'page210rh.html')
    fname2 = os.path.join(self.htmltemplates_dir, report_marker)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    line1_lst = []
    with open(fname1, 'r', encoding='UTF-8') as f1:
      line1_lst = f1.readlines()
    line1_lst.append('<h4><span style="color:#e53f31;">Химиолучевая терапия. Медицинское заключение.</span></h4>')
    # print(f'2100> line1_lst: len: {len(line1_lst)}: {line1_lst}')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    line_html = ''
    with open(fname2, 'w', encoding='UTF-8') as f2:
      #~~~~~~~
      for i in range(len(line1_lst)):
        f2.write(line1_lst[i])
      #~~~ пациент
      for i in range(len(patient_lst)):
        line_html = self.patch_html_str(patient_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~ выписка пациента
      for i in range(len(patient_discharge_lst)):
        line_html = self.patch_html_str(patient_discharge_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~ рекомендация ии-эксперта №1
      for i in range(len(ai_expert0_conclusion_lst)):
        line_html = self.patch_html_str(ai_expert0_conclusion_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~ рекомендация ии-эксперта №2
      for i in range(len(ai_expert1_conclusion_lst)):
        line_html = self.patch_html_str(ai_expert1_conclusion_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~ рекомендация ии-эксперта №3
      for i in range(len(ai_expert2_conclusion_lst)):
        line_html = self.patch_html_str(ai_expert2_conclusion_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~ заключение лечащего врача
      for i in range(len(doctor_conclusion_lst)):
        line_html = self.patch_html_str(doctor_conclusion_lst[i])
        if 0 == i:
          f2.write('<span style="color: blue;">'+line_html+'</span><br>'+'\n')
        else:
          f2.write(line_html+'<br>'+'\n')
      f2.write('<br>'+'\n')
      #~~~~~~~
      f2.write('\n')
      f2.write('</td></tr></table></body></html>')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return report_marker