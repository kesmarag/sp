import numpy as np
import pywt
from pywt._thresholding import hard, soft


class SWPT(object):

  def __init__(self, wavelet='db4', max_level=3):
    self._wavelet = wavelet
    self._max_level = max_level
    self._coeff_dict = {}
    self._energy_dict = {}
    self._entropy_dict = {}

  def decompose(self, signal):
    pth = ['']
    self._coeff_dict[''] = np.squeeze(signal)
    for l in range(self._max_level):
      pth_new = []
      for p in pth:
        coeff = pywt.swt(
            self._coeff_dict[p],
            wavelet=self._wavelet,
            level=self._max_level - len(p),
            start_level=len(p))
        p_run = p
        for i, C in enumerate(coeff[::-1]):
          self._coeff_dict[p_run + 'A'] = C[0]
          self._energy_dict[p_run + 'A'] = np.linalg.norm(C[0]) ** 2
          self._coeff_dict[p_run + 'D'] = C[1]
          self._energy_dict[p_run + 'D'] = np.linalg.norm(C[1]) ** 2
          self._entropy_dict[p_run + 'A'] = 0.0
          self._entropy_dict[p_run + 'D'] = 0.0
          for c in C[0]:
            self._entropy_dict[p_run + 'A'] += -100.0 * np.log(c ** 2 / np.linalg.norm(signal, ord=2) ** 2 ) * c ** 2 / np.linalg.norm(signal, ord=2) ** 2
          self._entropy_dict[p_run + 'A'] = self._entropy_dict[p_run + 'A'] / 2 ** (len(p_run) + 2.0)
          for c in C[1]:
            self._entropy_dict[p_run + 'D'] += -100.0 * np.log(c ** 2 / np.linalg.norm(signal, ord=2) ** 2 ) * c ** 2 / np.linalg.norm(signal, ord=2) ** 2
          self._entropy_dict[p_run + 'D'] = self._entropy_dict[p_run + 'D'] / 2 ** (len(p_run) + 2.0)
          if i < len(coeff) - 1 and len(p_run) < self._max_level - 1:
            pth_new.append(p_run + 'D')
            p_run = p_run + 'A'
      pth = list(pth_new)
    energies = self._get_energies()
    for k in self._coeff_dict:
      if len(k) > 0:
        self._energy_dict[k] = self._energy_dict[k] / energies[len(k) - 1]

  def get_level(self, level, order='freq', thresholding=None, threshold=None, energies=False):
    assert order in ['natural', 'freq']
    r = []
    result_coeffs = []
    result_energies = []
    for k in self._coeff_dict:
      if len(k) == level:
        r.append(k)
    if order == 'freq':
      graycode_order = self._get_graycode_order(level)
      for p in graycode_order:
        if p in r:
          result_coeffs.append(self._coeff_dict[p])
          result_energies.append(self._energy_dict[p])
    else:
      print('The natural order is not supported yet.')
      exit(1)
    # apply the thressholding
    if thresholding in ['hard', 'soft']:
      if isinstance(threshold, (int, float)):
        if thresholding == 'hard':
          result_coeffs = hard(result_coeffs, threshold)
        else:
          result_coeffs = soft(result_coeffs, threshold)
      else:
        print('Threshold must be an integer or float number')
        exit(1)
    if energies:
      return result_coeffs, result_energies
    else:
      return result_coeffs

  def _get_energies(self):
      res = [0] * self._max_level
      for k in self._coeff_dict:
        if len(k) > 0:
          res[len(k) - 1] += self._energy_dict[k]
      return res

  def get_coefficient_vector(self, name):
    return self._coeff_dict[name]

  def get_energy(self, name):
    return self._energy_dict[name]

  def _get_graycode_order(self, level, x='A', y='D'):
    graycode_order = [x, y]
    for i in range(level - 1):
      graycode_order = [x + path for path in graycode_order] + \
                       [y + path for path in graycode_order[::-1]]
    return graycode_order


if __name__ == '__main__':
  x = np.random.randn(2048)
  swpt = SWPT(max_level=5)
  swpt.decompose(x)
  wp4, en = swpt.get_level(5, energies=True)
  print(swpt._get_graycode_order(3))
