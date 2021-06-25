from math import sqrt, atan, pi, degrees
from .log import Log

class Laplace:
  def __init__(self, array, l=None, r=None, log=None, heatflux=False):
    if l is None:
      l = [len(array) // 2] * 2

    if r is None:
      r = 4

    if log is None:
      log = 'output'

    self.array = array
    self.l = l
    self.r = r
    self.log = Log(log)
    self.heatflux = heatflux
    self.internal()

  def internal(self):
    self.start = [[1, 1]] * 2

    self.errors = []
    self.old = []
    self.error = 1

    for _ in range(self.l[0]):
      self.errors.append([0] * self.l[0])
      self.old.append([0] * self.l[0])

  def update(self, i, j):
    self.old[i - 1][j - 1] = self.array[i][j]

    self.array[i][j] = round((
      self.array[i - 1][j] +
      self.array[i + 1][j] +
      self.array[i][j - 1] +
      self.array[i][j + 1]
    ) / 4, self.r)

    self.errors[i - 1][j - 1] = round((
      self.array[i][j] -
      self.old[i - 1][j - 1]
    ) / self.array[i][j], 4)

  def loop(self):
    for i in range(self.start[0][0], len(self.array) - self.start[0][1]):
      for j in range(self.start[1][0], len(self.array[i]) - self.start[1][1]):
        self.update(i, j)

      if not self.heatflux:
        self.error = max([item for sublist in self.errors for item in sublist])

  def print(self):
    if self.heatflux:
      self.log.prwrite(self.values, 'Values] #[qn, theta')
      return

    self.log.prwrite(self.array, 'Array')
    self.log.prwrite(self.old, 'Old values')
    self.log.prwrite(self.errors, 'Errors')
    self.log.write(f'{self.error}\n\n', 'Error')

  def run(self):
    while not self.error <= 0.0001:
      self.loop()
      self.print()

    return self.array

class Insulation(Laplace):
  def internal(self):
    self.start = [[1, 1], [0, 0]]

    self.errors = []
    self.old = []
    self.error = 1

    for _ in range(self.l[0]):
      self.errors.append([0] * self.l[1])
      self.old.append([0] * self.l[1])

  def update(self, i, j):
    self.old[i - 1][j] = self.array[i][j]

    i1 = self.array[i - 1][j]
    i2 = self.array[i + 1][j]
    j1 = -1 if j - 1 < 0 else self.array[i][j - 1]
    j2 = -1 if len(self.array[i]) <= j + 1 else self.array[i][j + 1]

    self.array[i][j] = round((
      i1 + i2 +
      (2 * j2 if j1 == -1 else 2 * j1 if j2 == -1 else j1 + j2)
    ) / 4, self.r)

    self.errors[i - 1][j] = round((
      self.array[i][j] -
      self.old[i - 1][j]
    ) / self.array[i][j], 4)

class HeatFlux(Laplace):
  kprime = 0.49

  def internal(self):
    self.start = [[1, 1]] * 2
    self.values = []
    self.h = 100
    self.error = 1

  def update(self, i, j):
    i1 = -1 if j - 1 < 0 else self.array[i][j - 1]
    i2 = -1 if len(self.array[i]) <= j + 1 else self.array[i][j + 1]
    j1 = self.array[i - 1][j]
    j2 = self.array[i + 1][j]

    qx = 0 if i1 == -1 or i2 == -1 else \
      -self.kprime * (i2 - i1) / (2 * self.h)
    qy = -self.kprime * (j2 - j1) / (2 * self.h)

    qn = round(sqrt(pow(qx, 2) + pow(qy, 2)), 3)
    theta = atan(qy / qx) if qx < 0 \
      else atan(qy / qx) + pi if qx > 0 \
      else pi / 2 if qy > 0 \
      else 3 * pi / 2

    self.values.append([qn, round(degrees(theta), self.r)])
    self.error -= 1

class HeatFluxIns(HeatFlux):
  def internal(self):
    self.start = [[1, 1], [0, 0]]
    self.values = []
    self.h = 100
    self.error = 1
