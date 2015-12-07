'''
Inspired by:
  https://gist.github.com/kylebgorman/8064310
'''

class Triangle(object):
	'''
	Sparse representation of upper diagonal triangular matrix.
	'''

	def __init__(self, edge_size, iterable):
		self.n = edge_size
		n_elements = (edge_size * (edge_size + 1)) // 2
		l = list(iterable)
		if len(l) < n_elements:
			n_missing = n_elements - len(l)
			l = l + [0] * n_missing
		elif len(l) > n_elements:
			l = l[:n_elements]
		self.values = l

	def _get_1d_index(self, indices):
		(row, col) = indices
		if col < row:
			raise IndexError('Index ({}, {}) is in lower triangle'.format(
				row, col))
		if row >= self.n or col >= self.n:
			raise IndexError('Index ({}, {}) is out of range'.format(row, col))
		return row * self.n - ((row - 1) * ((row - 1) + 1)) // 2 + col - row

	def __repr__(self):
		return '{0}({1} x {1})'.format(self.__class__.__name__, self.n)

	def __getitem__(self, indices):
		return self.values[self._get_1d_index(indices)]

	def __setitem__(self, indices, value):
		self.values[self._get_1d_index(indices)] = value
