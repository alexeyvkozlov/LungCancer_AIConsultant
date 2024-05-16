#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import configparser
import os

from dirfile_worker import DirectoryFileWorker

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SettingsReader:
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, data_path: str):
    self.is_init = False
    config_filename = os.path.join(data_path, 'settings.ini')
    # print(f'[INFO] config filename: `{config_filename}`')
    #~~~~~~~~~~~~~~~~~~~~~~~~
    dir_filer = DirectoryFileWorker()
    if not dir_filer.file_exists(config_filename):
      print(f'[WARNING] can`t find settingsfile: `{config_filename}`')
      return
    #~~~~~~~~~~~~~~~~~~~~~~~~
    self.config = configparser.ConfigParser()
    self.config.read(config_filename, encoding='utf-8')
    self.is_init = True
    # print(f'[INFO] self.is_init: `{self.is_init}`')

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_server_host(self) -> str:
    if self.is_init:
      return self.config.get('SERVER', 'host')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_server_port(self) -> int:
    if self.is_init:
      return self.config.getint('SERVER', 'port')
    else:
      return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_ucredentials(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'ucredentials')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_htmltemplatesdir(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'htmltemplates_dir')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_logodir(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'logo_dir')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_stage_mode_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'stage_mode_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_cell_mode_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'cell_mode_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_operable_mode_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'operable_mode_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_therapy_mode_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'therapy_mode_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_01_human_race_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_01_human_race_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_02_gender_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_02_gender_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_03_age_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_03_age_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_04_smoking_status_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_04_smoking_status_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_05_ecog_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_05_ecog_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_06_10_no_yes_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_06_10_no_yes_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_11_period_from_clt_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_11_period_from_clt_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_12_molecular_status_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_12_molecular_status_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_13_pd_l1_status_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_13_pd_l1_status_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_14_patient_preference_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_14_patient_preference_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_15_expert_recommendation_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_15_expert_recommendation_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_16_18_confidence_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_16_18_confidence_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_19_alternative_therapy50_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_19_alternative_therapy50_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model2101_20_comment_code_ftxt(self) -> str:
    if self.is_init:
      return self.config.get('DATA_IN', 'model2101_20_comment_code_ftxt')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model21000(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'model21000')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_expert21000(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'expert21000')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_status21000(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'status21000')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model21001(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'model21001')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_expert21001(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'expert21001')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_status21001(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'status21001')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model21002(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'model21002')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_expert21002(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'expert21002')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_status21002(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'status21002')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_model21010(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'model21010')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_expert21010(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'expert21010')
    else:
      return ''
  #~~~~~~~~~~~~~~~~~~~~~~~~
  def get_status21010(self) -> str:
    if self.is_init:
      return self.config.get('DATA_MODELS', 'status21010')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_medreportdir(self) -> str:
    if self.is_init:
      return self.config.get('DATA_REPORT', 'medreport_dir')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_trainer_fyml(self) -> str:
    if self.is_init:
      return self.config.get('FACE_ID', 'trainer_fyml')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_pseudo_camera_fmov(self) -> str:
    if self.is_init:
      return self.config.get('FACE_ID', 'pseudo_camera_fmov')
    else:
      return ''

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_fid_userid(self) -> int:
    if self.is_init:
      return self.config.getint('FACE_ID', 'user_id')
    else:
      return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_fid_faceoffsetpix(self) -> int:
    if self.is_init:
      return self.config.getint('FACE_ID', 'face_offset_pix')
    else:
      return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_fid_train_dataset(self) -> str:
    if self.is_init:
      return self.config.get('FACE_ID', 'train_dataset')
    else:
      return ''