#~~~ модель 2101
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
class Model2101Worker:
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, prog_path: str):
    self.prog_path = prog_path
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.ini_reader = SettingsReader(self.prog_path)
    model21010_path = self.ini_reader.get_model21010()
    self.expert21010 = self.ini_reader.get_expert21010()
    self.status21010 = self.ini_reader.get_status21010()
    self.htmltemplates_dir = self.ini_reader.get_htmltemplatesdir()
    self.medreport_dir = self.ini_reader.get_medreportdir()
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ создаем директорию для результатов
    self.dir_filer = DirectoryFileWorker()
    # self.dir_filer.remove_create_directory(self.report_dir)
    self.dir_filer.create_directory(self.medreport_dir)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    print('[INFO] Model2101Worker:')
    print(f'[INFO]  program path: `{self.prog_path}`')
    print(f'[INFO]  model21010: `{model21010_path}`')
    print(f'[INFO]  expert21010: `{self.expert21010}`')
    print(f'[INFO]  status21010: `{self.status21010}`')
    print(f'[INFO]  htmltemplates_dir: `{self.htmltemplates_dir}`')
    print(f'[INFO]  medreport_dir: `{self.medreport_dir}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21010.h5 0|Лактионов Константин Константинович|заведующий отделением, профессор, д.м.н.
    #~~~ отсортированный список по возрастанию conclusion_lst
    self.conclusion_lst0 = [1111, 1113, 1223, 2111, 2121, 2421, 2431, 3123, 3223, 3233, 4111, 4224, 4234, 4531, 5224, 5234, 5521, 5531, 6232, 6321, 6333, 6432, 7223, 7233, 7421, 8223, 8421, 9111, 9223, 9421, 10121, 10223, 20121, 20233]
    #~~~ загрузка модели нейронной сети Deep Neural Network
    #~ путь к tensorflow файлу-модели
    self.model21010 = load_model(model21010_path)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # #~ путь к tensorflow-light файлу-модели
    # model_fname0 = os.path.join(model_path, FLMODELH5_21010)
    # #~ загрузка модели TFLite
    # self.model21010 = lite.Interpreter(model_path=model_fname0)
    # #~ выделение памяти для тензоров модели
    # self.model21010.allocate_tensors()
    # #~ получение информации о входных и выходных слоях модели (тензорах)
    # self.input_details0 = self.model21010.get_input_details()
    # self.output_details0 = self.model21010.get_output_details()
    # #~ определение формы входного тензора на основе информации о модели
    # self.input_shape0 = self.input_details0[0]['shape']
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
  def getXLstVector(self, inxHumanRace,inxGender,inxAge,inxSmokingStatus,inxECOG,
                    inxTumorLoad,inxCo_mutationKRAS,inxCo_mutationp53,inxCo_mutationSTK11,
                    inxCo_mutationKEAP1,inxPeriodFromCLT,inxMolecularStatus,
                    inxPD_L1Status,inxPatientPreference):
    '''
    Числовое кодирование X-вектора
    Args:
      inxExpert...inxPatientPreference - числовые индексыиз списка возможных
    Returns:
      массив числовых кодов
    '''
    #~~~~~~~~~~~~~~~~~~~~~~~~
    # print(f'2101> Раса: {inxHumanRace}')
    # print(f'2101> Пол: {inxGender}')
    # print(f'2101> Возраст: {inxAge}')
    # print(f'2101> Статус курения: {inxSmokingStatus}')
    # print(f'2101> ECOG: {inxECOG}')
    # print(f'2101> Есть опухолевая нагрузка? (симптомная опухоль): {inxTumorLoad}')
    # print(f'2101> Ко-мутации KRAS: {inxCo_mutationKRAS}')
    # print(f'2101> Ко-мутации p53.: {inxCo_mutationp53}')
    # print(f'2101> Ко-мутации STK11: {inxCo_mutationSTK11}')
    # print(f'2101> Ко-мутации KEAP1: {inxCo_mutationKEAP1}')
    # print(f'2101> Срок от окончания ХЛТ: {inxPeriodFromCLT}')
    # print(f'2101> Молекулярный статус (только для неплоскоклеточного рака): {inxMolecularStatus}')
    # print(f'2101> PD-L1 статус: {inxPD_L1Status}')
    # print(f'2101> Предпочтение пациента по ответу на терапию: {inxPatientPreference}')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    retVal = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~1. Раса: one-hot-encoding
    #~ utils – модуль с полезными инструментами для подготовки данных
    #~ используем для to_categoricall
    #~ from tensorflow.keras import utils
    #~#~ohe_arr2 = utils.to_categorical(inxHumanRace, 3)
    #~ ohe_lst2 = ohe_arr2.astype(int).tolist()
    ohe_lst1 = self.onehot_encoder(inxHumanRace, 3) 
    retVal.extend(ohe_lst1)
    #~~~2. Пол:
    retVal.append(inxGender)
    #~~~3. Возраст:
    retVal.append(inxAge)
    #~~~4. Статус курения:
    ohe_lst4 = self.onehot_encoder(inxSmokingStatus, 3)
    retVal.extend(ohe_lst4)
    #~~~5. ECOG:
    retVal.append(inxECOG)
    #~~~6. Есть опухолевая нагрузка? (симптомная опухоль):
    retVal.append(inxTumorLoad)
    #~~~7. Ко-мутации KRAS:
    retVal.append(inxCo_mutationKRAS)
    #~~~8. Ко-мутации p53.:
    retVal.append(inxCo_mutationp53)
    #~~~9. Ко-мутации STK11:
    retVal.append(inxCo_mutationSTK11)
    #~~~10. Ко-мутации KEAP1:
    retVal.append(inxCo_mutationKEAP1)
    #~~~11. Срок от окончания ХЛТ:
    ohe_lst11 = self.onehot_encoder(inxPeriodFromCLT, 3)
    retVal.extend(ohe_lst11)
    #~~~12. Молекулярный статус (только для неплоскоклеточного рака):
    ohe_lst12 = self.onehot_encoder(inxMolecularStatus, 6)
    retVal.extend(ohe_lst12)
    #~~~13. PD-L1 статус:
    ohe_lst13 = self.onehot_encoder(inxPD_L1Status, 3)
    retVal.extend(ohe_lst13)
    #~~~14. Предпочтение пациента по ответу на терапию:
    retVal.append(inxPatientPreference)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    del ohe_lst1
    del ohe_lst4
    del ohe_lst11
    del ohe_lst12
    del ohe_lst13
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
      retVal = 'наблюдение'
    elif 2 == num:
      retVal = 'Алектиниб'
    elif 3 == num:
      retVal = 'Дурвалумаб'
    elif 4 == num:
      retVal = 'Осимертиниб'
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
      retVal = '100%'
    elif 2 == num:
      retVal = '75%'
    elif 3 == num:
      retVal = '50%'
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
      retVal = 'наблюдение'
    elif 3 == num:
      retVal = 'Алектиниб'
    elif 4 == num:
      retVal = 'Дурвалумаб'
    elif 5 == num:
      retVal = 'Осимертиниб'
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseCommentCode(self, num4, num5):
    '''
    Получение текстового значения `Комментарий` по категориальным значениям 5-го и 6-го разрядов

    Args:
      num5 - числовое категориальное значение пятого разряда
      num6 - числовое категориальное значение шестого разряда

    Returns:
      текстовое значение
    '''
    retVal = '-'
    if 1 == num4:
      retVal = '0'
    elif 2 == num4:
      retVal = 'нет доказательной базы для назначения после перерыва >61 дня после ХЛТ'
    elif 3 == num4:
      retVal = 'возможно есть мутации и эффективность Дурвалумаба будет низкой'
    elif 4 == num4:
      retVal = 'возможна низкая эффективность Дурвалумаба, Осимертиниб без доказательной базы'
    elif 5 == num4:
      retVal = 'возможна низкая эффективность Дурвалумаба, Осимертиниб без доказательной базы, эффективность Осимертиниба ниже при 21 экзоне'
    elif 6 == num4:
      retVal = 'возможна низкая эффективность Дурвалумаба, Алектиниб без доказательной базы'
    elif 7 == num4:
      retVal = 'возможна низкая эффективность Дурвалумаба при PD-1 < 1%'
    elif 8 == num4:
      retVal = 'возможна низкая эффективность Дурвалумаба при PD-1 < 1%, возможно есть активирующие мутации'
    elif 9 == num4:
      retVal = 'вероятность 45% PD-L1 < 1% с потенциально низкой эффективностью Дурвалумаба'
    elif 1 == num5:
      retVal = 'возможно есть мутации и эффективность Дурвалумаба будет низкой, вероятность 45% PD-L1 < 1% с потенциально низкой эффективностью Дурвалумаба'
    elif 2 == num5:
      retVal = 'возможно есть мутации и эффективность Дурвалумаба будет низкой, возможна низкая эффективность Дурвалумаба при PD-1 < 1%'
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
    #~~~15: 'Ответ эксперта (Лактионов)' -> 'Наблюдение'
    retVal.append(self.getReverseExpertRecommendationCode(digits[0]))
    #~~~ 16 - N1 - 'Поставьте галочку, если уверены на 100%'
    #~~~ 17 - N1 - 'Если 75%'
    #~~~ 18 - N1 - 'Если 50%'
    retVal.append(self.getReverseConfidence1007550Code(digits[1]))
    #~~~19: 'Альтернатива, если 50% - обязательно' -> 'Дурвалумаб'
    retVal.append(self.getReverseAlternativeTherapy50Code(digits[2]))
    #~~~20: 'Комментарий' -> 'Нет доказательной базы для назначения после перерыва >61 дня после ХЛТ'
    #~ getCommentCode(elem_str1)
    comment_digit4 = digits[3]
    comment_digit5 = 0
    if 5 == len(digits):
      comment_digit5 = digits[4]
    retVal.append(self.getReverseCommentCode(comment_digit4, comment_digit5))
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseHumanRace(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'азиатская'
    elif 1 == num:
      retVal = 'европейская'
    elif 2 == num:
      retVal = 'другая' 
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
  def getReverseAge(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'до 70'
    elif 1 == num:
      retVal = '>70'
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
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseEcog(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0-1'
    elif 1 == num:
      retVal = '2'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseNoYes(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'нет'
    elif 1 == num:
      retVal = 'да'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseFinishChemoRadioTherapy(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'до 42 дней'
    elif 1 == num:
      retVal = 'от 43 до 60 дней'
    elif 2 == num:
      retVal = 'более 61 дня'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseMolecularStatus(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'нет мутаций'
    elif 1 == num:
      retVal = 'не исследовались'
    elif 2 == num:
      retVal = 'ALK позитивный'
    elif 3 == num:
      retVal = 'EGFR редкий вариант'
    elif 4 == num:
      retVal = 'EGFR ex19'
    elif 5 == num:
      retVal = 'EGFR ex21'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReversePDL1Status(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'не исследовался'
    elif 1 == num:
      retVal = 'менее 1%'
    elif 2 == num:
      retVal = 'более 1%'
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReversePatientPreference(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'результативность лечения'
    elif 1 == num:
      retVal = 'сохранение качества жизни'
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorExpertRecommendation(self, num):
    retVal = '-'
    if 0 == num:
      retVal = 'наблюдение'
    elif 1 == num:
      retVal = 'Алектиниб'
    elif 2 == num:
      retVal = 'Дурвалумаб' 
    elif 3 == num:
      retVal = 'Осимертиниб' 
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
      retVal = 'наблюдение'
    elif 2 == num:
      retVal = 'Алектиниб' 
    elif 3 == num:
      retVal = 'Дурвалумаб' 
    elif 4 == num:
      retVal = 'Осимертиниб' 
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def getReverseDoctorComment(self, num):
    retVal = '-'
    if 0 == num:
      retVal = '0'
    elif 1 == num:
      retVal = 'нет доказательной базы для назначения после перерыва >61 дня после хлт'
    elif 2 == num:
      retVal = 'возможно есть мутации и эффективность дурвалумаба будет низкой' 
    elif 3 == num:
      retVal = 'возможна низкая эффективность дурвалумаба, осимертиниб без доказательной базы' 
    elif 4 == num:
      retVal = 'возможна низкая эффективность дурвалумаба, осимертиниб без доказательной базы, эффективность осимертиниба ниже при 21 экзоне' 
    elif 5 == num:
      retVal = 'возможна низкая эффективность дурвалумаба, алектиниб без доказательной базы' 
    elif 6 == num:
      retVal = 'возможна низкая эффективность дурвалумаба при pd-1 < 1%' 
    elif 7 == num:
      retVal = 'возможна низкая эффективность дурвалумаба при pd-1 < 1%, возможно есть активирующие мутации' 
    elif 8 == num:
      retVal = 'вероятность 45% pd-l1 < 1% с потенциально низкой эффективностью дурвалумаба' 
    elif 9 == num:
      retVal = 'возможно есть мутации и эффективность дурвалумаба будет низкой, вероятность 45% pd-l1 < 1% с потенциально низкой эффективностью дурвалумаба' 
    elif 10 == num:
      retVal = 'возможно есть мутации и эффективность дурвалумаба будет низкой, возможна низкая эффективность дурвалумаба при pd-1 < 1%' 
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
  def get_patient_discharge_lst(self, inxHumanRace, inxGender, inxAge,
                                inxSmokingStatus, inxECOG, inxTumorLoad,
                                inxCo_mutationKRAS, inxCo_mutationp53, inxCo_mutationSTK11,
                                inxCo_mutationKEAP1, inxPeriodFromCLT, inxMolecularStatus,
                                inxPD_L1Status, inxPatientPreference):
    retVal = []
    retVal.append('Выписка пациента:')
    str_n = self.getReverseHumanRace(inxHumanRace)
    retVal.append('  1. Раса: ' + str_n)
    str_n = self.getReverseGender(inxGender)
    retVal.append('  2. Пол: ' + str_n)
    str_n = self.getReverseAge(inxAge)
    retVal.append('  3. Возраст: ' + str_n)
    str_n = self.getReverseSmokingStatus(inxSmokingStatus)
    retVal.append('  4. Статус курения: ' + str_n)
    str_n = self.getReverseEcog(inxECOG)
    retVal.append('  5. ECOG: ' + str_n)
    str_n = self.getReverseNoYes(inxTumorLoad)
    retVal.append('  6. Есть опухолевая нагрузка? (симптомная опухоль): ' + str_n)
    str_n = self.getReverseNoYes(inxCo_mutationKRAS)
    retVal.append('  7. Ко-мутации KRAS: ' + str_n)
    str_n = self.getReverseNoYes(inxCo_mutationp53)
    retVal.append('  8. Ко-мутации p53.: ' + str_n)
    str_n = self.getReverseNoYes(inxCo_mutationSTK11)
    retVal.append('  9. Ко-мутации STK11: ' + str_n)
    str_n = self.getReverseNoYes(inxCo_mutationKEAP1)
    retVal.append('  10. Ко-мутации KEAP1: ' + str_n)
    str_n = self.getReverseFinishChemoRadioTherapy(inxPeriodFromCLT)
    retVal.append('  11. Срок от окончания ХЛТ: ' + str_n)
    str_n = self.getReverseMolecularStatus(inxMolecularStatus)
    retVal.append('  12. Молекулярный статус (только для неплоскоклеточного рака): ' + str_n)
    str_n = self.getReversePDL1Status(inxPD_L1Status)
    retVal.append('  13. PD-L1 статус: ' + str_n)
    str_n = self.getReversePatientPreference(inxPatientPreference)
    retVal.append('  14. Предпочтение пациента по ответу на терапию: ' + str_n)
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_ai_expert_conclusion_lst(self, expert_index: str, 
                                    expert_medication: str, expert_confidence: str,
                                    expert_alternative: str, expert_comment: str):
    retVal = []
    retVal.append('Рекомендация ии-эксперта "№' + expert_index + ':')
    retVal.append('  1. Лечение: ' + expert_medication)
    retVal.append('  2. Уверенность: ' + expert_confidence)
    retVal.append('  3. Альтернатива, если 50% - обязательно: ' + expert_alternative)
    retVal.append('  4. Комментарий: ' + expert_comment)
    #~~~
    if '1' == expert_index:
      retVal.append('  5. Фамилия, имя, отчество ии-эксперта: ' + self.expert21010)
      retVal.append('  6. Статус ии-эксперта: ' + self.status21010)
    #~~~
    return retVal
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_doctor_conclusion_lst(self, doctor_name: str, doctor_status: str,
                                inxMedication: int, inxConfidence: int, inxAlternative: int, inxComment: int):
    retVal = []
    retVal.append('Заключение лечащего врача:')
    str_n = self.getReverseDoctorExpertRecommendation(inxMedication)
    retVal.append('  1. Лечение: ' + str_n)
    str_n = self.getReverseDoctorConfidence1007550(inxConfidence)
    retVal.append('  2. Уверенность: ' + str_n)
    str_n = self.getReverseDoctorAlternativeTherapy50(inxAlternative)
    retVal.append('  3. Альтернатива, если 50% - обязательно: ' + str_n)
    str_n = self.getReverseDoctorComment(inxComment)
    retVal.append('  4. Комментарий: ' + str_n)
    #~~~
    retVal.append('  5. Фамилия, имя, отчество врача: ' + doctor_name)
    retVal.append('  6. Статус врача: ' + doctor_status)
    #~~~ дата, время: 
    now_dt = datetime.now()
    str_n = now_dt.strftime("%Y.%m.%d %H:%M")
    retVal.append('  7. Дата, время: ' + str_n)
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~
  def patch_html_str(self, str_val: str):
    str1 = str_val.replace('>', '&gt;')
    retVal = str1.replace('<', '&lt;')
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~ заключение-отчет на основании модели 2101
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def make_report(self, doctor_id: int, doctor_name: str, doctor_status: str,
                  patient_name: str, patient_health_cip: str,
                  inxHumanRace: int, inxGender: int, inxAge: int,
                  inxSmokingStatus: int, inxECOG: int, inxTumorLoad: int,
                  inxCo_mutationKRAS: int, inxCo_mutationp53: int, inxCo_mutationSTK11: int,
                  inxCo_mutationKEAP1: int, inxPeriodFromCLT: int, inxMolecularStatus: int,
                  inxPD_L1Status: int, inxPatientPreference: int, 
                  inxMedication: int, inxConfidence: int, inxAlternative: int, inxComment: int):
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~ model21010.h5 0|Лактионов Константин Константинович|заведующий отделением, профессор, д.м.н.
    x_row_lst0 = self.getXLstVector(inxHumanRace,inxGender,inxAge,inxSmokingStatus,inxECOG,
                                    inxTumorLoad,inxCo_mutationKRAS,inxCo_mutationp53,inxCo_mutationSTK11,
                                    inxCo_mutationKEAP1,inxPeriodFromCLT,inxMolecularStatus,
                                    inxPD_L1Status,inxPatientPreference)
    x_row_arr0 = np.array(x_row_lst0, dtype=np.float32).reshape(1, len(x_row_lst0))
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~ tensorflow
    pred0 = self.model21010.predict(x_row_arr0)
    #~~~~~~~ tensorflow-light
    # #~ установка входного тензора в модель
    # self.model21010.set_tensor(self.input_details0[0]['index'], x_row_arr0)
    # #~ выполнение интерпретации модели на входных данных
    # self.model21010.invoke()
    # #~ получение выходного тензора из модели
    # pred0 = self.model21010.get_tensor(self.output_details0[0]['index'])
    #~~~~~~~
    pred0_inx_max = np.argmax(pred0[0,:])
    conclusion_code0 = self.conclusion_lst0[pred0_inx_max]
    #~~~~~~~~~~~~~~~~~~~~~~~~
    #~ akozlov hard-code 2023.11.20
    # conclusion_code0 = 2421
    rev_conclusion_lst0 = self.reverse_conclusion(conclusion_code0)
    # print(f' >conclusion_code0: {conclusion_code0}')
    # print(f' >rev_conclusion_lst0: {rev_conclusion_lst0}')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ формирование отчета-заключения
    #~~~~~~~~~~~~~~~~~~~~~~~~
    patient_lst = self.get_patient_lst(patient_name, patient_health_cip)
    patient_discharge_lst = self.get_patient_discharge_lst(inxHumanRace, inxGender, inxAge,
                                                          inxSmokingStatus, inxECOG, inxTumorLoad,
                                                          inxCo_mutationKRAS, inxCo_mutationp53, inxCo_mutationSTK11,
                                                          inxCo_mutationKEAP1, inxPeriodFromCLT, inxMolecularStatus,
                                                          inxPD_L1Status, inxPatientPreference)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    ai_expert0_conclusion_lst = self.get_ai_expert_conclusion_lst('1',
                                                                  rev_conclusion_lst0[0], rev_conclusion_lst0[1],
                                                                  rev_conclusion_lst0[2], rev_conclusion_lst0[3])
    #~~~~~~~~~~~~~~~~~~~~~~~~
    doctor_conclusion_lst = self.get_doctor_conclusion_lst(doctor_name, doctor_status,
                                                          inxMedication, inxConfidence, inxAlternative, inxComment)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ после того как списки сформированы, записывает текстовый файл отчета
    #~~~~~~~~~~~~~~~~~~~~~~~~
    now_dt = datetime.now()
    dt_str = now_dt.strftime("%Y%m%d%H%M%S")
    patient_name2 = patient_name.replace(' ', '')
    str_n = dt_str + '_' + patient_name2 + '.txt'
    medreport_fname = os.path.join(self.medreport_dir, str_n)
    with open(medreport_fname, 'w', encoding='UTF-8') as f0:
      f0.write('Иммунотерапия. Медицинское заключение.\n\n')
      for str_n in patient_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in patient_discharge_lst:
        f0.write(str_n + '\n')
      f0.write('\n')
      for str_n in ai_expert0_conclusion_lst:
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
    #~ 'rm2101_' ->  r - report, m - model
    report_marker = 'rm2101_' + dt_str + str(self.report_counter) + '.html'
    #~ открываю html-шаблон-отчета
    #~ 'page210rh.html' -> r - report, h - head
    fname1 = os.path.join(self.htmltemplates_dir, 'page210rh.html')
    fname2 = os.path.join(self.htmltemplates_dir, report_marker)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    line1_lst = []
    with open(fname1, 'r', encoding='UTF-8') as f1:
      line1_lst = f1.readlines()
    line1_lst.append('<h4><span style="color:#e53f31;">Иммунотерапия. Медицинское заключение.</span></h4>')
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