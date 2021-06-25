from laplace import *
from laplace.log import Log

if __name__ == '__main__':
  Laplace([
    [1, 1, 2, 3],
    [1, 0, 0, 4],
    [2, 0, 0, 5],
    [3, 4, 5, 5],
  ], [2], log='one').run()

  Laplace([
    [175 / 2, 100, 100, 100, 150 / 2],
    [75, 0, 0, 0, 50],
    [75, 0, 0, 0, 50],
    [75, 0, 0, 0, 50],
    [75 / 2, 0, 0, 0, 50 / 2],
  ], [3], 2, log='two').run()

  output = Insulation([
    [100, 100, 100, 100],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
  ], [2, 4], log='ins').run()

  HeatFluxIns(output, r=2, log='heatflux', heatflux=True).run()

  HeatFlux([
    [100, 100, 100, 100, 100],
    [75, 78.59, 76.06, 69.71, 50],
    [75, 63.21, 56.11, 52.34, 50],
    [75, 43, 33.3, 33.89, 50],
    [0, 0, 0, 0, 0],
  ], r=4, log='heattest', heatflux=True).run()
