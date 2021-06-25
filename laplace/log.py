from os import mkdir
from os.path import dirname, realpath, isdir

filepath = f'{dirname(realpath(__file__))}/logs/'

class Log:
  def __init__(self, file):
    if not isdir(filepath):
      mkdir(filepath)
    self.filename = f'{filepath}{file}.log'
    self.clean()

  def clean(self):
    with open(self.filename, 'w') as f:
      f.write('')

  def pr(self, array):
    s = ''
    for i in array:
      s += '[ '
      for j in i:
        s += f'{j} '
      s += ']\n'
    s += '\n'
    return s

  def write(self, item, title=''):
    with open(self.filename, 'a') as f:
      f.write(f'~@[{title}]\n')
      f.write(item)

  def prwrite(self, arr, title=''):
    self.write(self.pr(arr), title)
