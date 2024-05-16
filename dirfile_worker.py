#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ import the necessary packages
#~ библиотека для вызова системных функций
import os
import shutil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class DirectoryFileWorker:
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def directory_exists(self, directory_path: str) -> bool:
    """Проверяет, существует ли директория."""
    retVal = False
    if os.path.exists(directory_path):
      if os.path.isdir(directory_path):
        retVal = True
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def remove_directory(self, directory_path: str):
    """Удаляет директорию, если она пустая."""
    if self.directory_exists(directory_path):
      try:
        shutil.rmtree(directory_path)
        # print(f'[INFO] Directory was successfully deleted: `{path}`')
      except OSError as e:
        print(f'[ERROR] Error deleting a directory: `{directory_path}`: {e.strerror}')
        return

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def create_directory(self, directory_path: str):
    """Создает директорию, если она еще не существует."""
    if not self.directory_exists(directory_path):
      os.makedirs(directory_path)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def remove_create_directory(self, directory_path: str):
    self.remove_directory(directory_path)
    self.create_directory(directory_path)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_directory_one_level_list(self, directory_path: str) -> list[str]:
    subdirectories = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]
    return subdirectories

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_image_list(self, directory_path: str) -> list[str]:
    img_lst = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    if not self.directory_exists(directory_path):
      return img_lst
    #~~~~~~~~~~~~~~~~~~~~~~~~
    for fname in os.listdir(directory_path):
      if os.path.isfile(os.path.join(directory_path, fname)):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
          img_lst.append(fname)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return img_lst

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ file_ext: 'tif'
  def get_file_list(self, directory_path: str, file_ext: str) -> list[str]:
    img_lst = []
    #~~~~~~~~~~~~~~~~~~~~~~~~
    if not self.directory_exists(directory_path):
      return img_lst
    #~~~~~~~~~~~~~~~~~~~~~~~~
    file_ext2 = '.'+file_ext
    for fname in os.listdir(directory_path):
      if os.path.isfile(os.path.join(directory_path, fname)):
        if fname.lower().endswith(file_ext2):
          img_lst.append(fname)
    #~~~~~~~~~~~~~~~~~~~~~~~~
    return img_lst

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def file_exists(self, file_path: str) -> bool:
    retVal = False
    if os.path.exists(file_path):
      if os.path.isfile(file_path):
        retVal = True
    return retVal

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def remove_file(self, file_path: str):
    if self.file_exists(file_path):
      os.remove(file_path)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def copy_file(self, file_path, destination_file_path):
    if not self.file_exists(file_path):
      print(f'[WARNING] The file was not found: `{file_path}`')
      return
    try:
      shutil.copyfile(file_path, destination_file_path)
    except FileNotFoundError:
      print(f'[ERROR] The file was not found: `{file_path}`')
    except Exception as e:
      print(f'[ERROR] {e}')

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def get_file_directory(self, file_path: str) -> str:
    #~ получение пути к директории
    directory_path = os.path.dirname(file_path)
    return directory_path

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  #~ 'DJI_0035.JPG' -> base_fname: `DJI_0035`, suffix_fname: `.JPG`
  def get_fname_base_suffix(self, file_name: str) -> tuple:
    #~ разделяем имя файла и расширение
    #~ находим индекс последней точки в строке
    last_dot_index = file_name.rfind('.')
    #~ возвращаем подстроку начиная с начала строки до последней точки включительно
    base_fname = file_name[:last_dot_index]
    #~ расширение
    suffix_fname = file_name[last_dot_index:]
    #~ возвращаем имя и расширение
    return base_fname,suffix_fname

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def format_counter(self, counter: int, digits: int):
    counter_str = str(counter)
    formatted_counter = counter_str.zfill(digits)
    return formatted_counter
