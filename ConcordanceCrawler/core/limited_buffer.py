from collections import deque

class LimitedBuffer(object):
	'''stores limited number of objects'''

	def __init__(self, maxsize=1000000):
		if maxsize < 0:
			raise ValueError("maxsize must be nonnegative integer")

		self.maxsize = maxsize
		self.size = 0

		self.deque = deque()
		self.items_set = set()

	def insert(self, item):
		if item in self.items_set:
			return
		if self.maxsize == 0:
			return

		if self.size == self.maxsize:
			r = self.deque.popleft()
			self.items_set.remove(r)
			self.size -= 1

		self.deque.append(item)
		self.items_set.add(item)
		self.size += 1

	def contains(self, item):
		return item in self.items_set


if __name__ == '__main__':
	b = LimitedBuffer(5)

	for i in range(10):
		b.insert(i)
		print(i)
		for j in range(15):
			print(b.contains(j))
		print()
