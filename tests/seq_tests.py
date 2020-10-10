#  From https://raw.githubusercontent.com/python/cpython/master/Lib/test/seq_tests.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
"""
Tests common to tuple, list and UserList.UserList
"""

# stdlib
import pickle
import sys
from itertools import chain
from typing import List

# 3rd party
import pytest

# this package
from domdf_python_tools.testing import not_pypy
from domdf_python_tools.utils import Len


class _ALWAYS_EQ:
	"""
	Object that is equal to anything.
	"""

	def __eq__(self, other):
		return True

	def __ne__(self, other):
		return False


ALWAYS_EQ = _ALWAYS_EQ()


class _NEVER_EQ:
	"""
	Object that is not equal to anything.
	"""

	def __eq__(self, other):
		return False

	def __ne__(self, other):
		return True

	def __hash__(self):
		return 1


NEVER_EQ = _NEVER_EQ()


# Various iterables
# This is used for checking the constructor (here and in test_deque.py)
def iterfunc(seqn):
	'Regular generator'
	for i in seqn:
		yield i


class Sequence:
	"""Sequence using __getitem__"""

	def __init__(self, seqn):
		self.seqn = seqn

	def __getitem__(self, i):
		return self.seqn[i]


class IterFunc:
	"""Sequence using iterator protocol"""

	def __init__(self, seqn):
		self.seqn = seqn
		self.i = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self.i >= len(self.seqn):
			raise StopIteration
		v = self.seqn[self.i]
		self.i += 1
		return v


class IterGen:
	"""Sequence using iterator protocol defined with a generator"""

	def __init__(self, seqn):
		self.seqn = seqn
		self.i = 0

	def __iter__(self):
		for val in self.seqn:
			yield val


class IterNextOnly:
	"""Missing __getitem__ and __iter__"""

	def __init__(self, seqn):
		self.seqn = seqn
		self.i = 0

	def __next__(self):
		if self.i >= len(self.seqn):
			raise StopIteration
		v = self.seqn[self.i]
		self.i += 1
		return v


class IterNoNext:
	"""Iterator missing __next__()"""

	def __init__(self, seqn):
		self.seqn = seqn
		self.i = 0

	def __iter__(self):
		return self


class IterGenExc:
	"""Test propagation of exceptions"""

	def __init__(self, seqn):
		self.seqn = seqn
		self.i = 0

	def __iter__(self):
		return self

	def __next__(self):
		3 // 0  # pylint: disable=pointless-statement


class IterFuncStop:
	"""Test immediate stop"""

	def __init__(self, seqn):
		pass

	def __iter__(self):
		return self

	def __next__(self):
		raise StopIteration


def itermulti(seqn):
	"""Test multiple tiers of iterators"""
	return chain(map(lambda x: x, iterfunc(IterGen(Sequence(seqn)))))


class LyingTuple(tuple):

	def __iter__(self):
		yield 1


class LyingList(list):

	def __iter__(self):
		yield 1


class CommonTest:
	# The type to be tested
	type2test: type

	def assertEqual(self, left, right):
		assert left == right

	def assertNotEqual(self, left, right):
		assert left != right

	def assertRaises(self, what, func, *args):
		with pytest.raises(what):
			func(*args)

	def test_constructors(self):
		l0: List = []
		l1 = [0]
		l2 = [0, 1]

		u = self.type2test()
		u0 = self.type2test(l0)
		u1 = self.type2test(l1)
		u2 = self.type2test(l2)

		uu = self.type2test(u)
		uu0 = self.type2test(u0)
		uu1 = self.type2test(u1)
		uu2 = self.type2test(u2)

		v = self.type2test(tuple(u))

		class OtherSeq:

			def __init__(self, initseq):
				self.__data = initseq

			def __len__(self):
				return len(self.__data)

			def __getitem__(self, i):
				return self.__data[i]

		s = OtherSeq(u0)
		v0 = self.type2test(s)
		self.assertEqual(len(v0), len(s))

		s2 = "this is also a sequence"
		vv = self.type2test(s2)
		self.assertEqual(len(vv), len(s2))

		# Create from various iteratables
		for s2 in ("123", "", range(1000), ('do', 1.2), range(2000, 2200, 5)):  # type: ignore
			for g in (Sequence, IterFunc, IterGen, itermulti, iterfunc):
				self.assertEqual(self.type2test(g(s2)), self.type2test(s2))
			self.assertEqual(self.type2test(IterFuncStop(s2)), self.type2test())
			self.assertEqual(self.type2test(c for c in "123"), self.type2test("123"))
			self.assertRaises(TypeError, self.type2test, IterNextOnly(s2))
			self.assertRaises(TypeError, self.type2test, IterNoNext(s2))
			self.assertRaises(ZeroDivisionError, self.type2test, IterGenExc(s2))

		# Issue #23757
		self.assertEqual(self.type2test(LyingTuple((2, ))), self.type2test((1, )))
		self.assertEqual(self.type2test(LyingList([2])), self.type2test([1]))

	def test_truth(self):
		assert not self.type2test()
		assert self.type2test([42])

	def test_getitem(self):
		u = self.type2test([0, 1, 2, 3, 4])
		for i in Len(u):
			self.assertEqual(u[i], i)
			self.assertEqual(u[int(i)], i)
		for i in range(-len(u), -1):
			self.assertEqual(u[i], len(u) + i)
			self.assertEqual(u[int(i)], len(u) + i)
		self.assertRaises(IndexError, u.__getitem__, -len(u) - 1)
		self.assertRaises(IndexError, u.__getitem__, len(u))
		self.assertRaises(ValueError, u.__getitem__, slice(0, 10, 0))

		u = self.type2test()
		self.assertRaises(IndexError, u.__getitem__, 0)
		self.assertRaises(IndexError, u.__getitem__, -1)

		self.assertRaises(TypeError, u.__getitem__)

		a = self.type2test([10, 11])
		self.assertEqual(a[0], 10)
		self.assertEqual(a[1], 11)
		self.assertEqual(a[-2], 10)
		self.assertEqual(a[-1], 11)
		self.assertRaises(IndexError, a.__getitem__, -3)
		self.assertRaises(IndexError, a.__getitem__, 3)

	def test_getslice(self):
		l = [0, 1, 2, 3, 4]
		u = self.type2test(l)

		self.assertEqual(u[0:0], self.type2test())
		self.assertEqual(u[1:2], self.type2test([1]))
		self.assertEqual(u[-2:-1], self.type2test([3]))
		self.assertEqual(u[-1000:1000], u)
		self.assertEqual(u[1000:-1000], self.type2test([]))
		self.assertEqual(u[:], u)
		self.assertEqual(u[1:None], self.type2test([1, 2, 3, 4]))
		self.assertEqual(u[None:3], self.type2test([0, 1, 2]))

		# Extended slices
		self.assertEqual(u[::], u)
		self.assertEqual(u[::2], self.type2test([0, 2, 4]))
		self.assertEqual(u[1::2], self.type2test([1, 3]))
		self.assertEqual(u[::-1], self.type2test([4, 3, 2, 1, 0]))
		self.assertEqual(u[::-2], self.type2test([4, 2, 0]))
		self.assertEqual(u[3::-2], self.type2test([3, 1]))
		self.assertEqual(u[3:3:-2], self.type2test([]))
		self.assertEqual(u[3:2:-2], self.type2test([3]))
		self.assertEqual(u[3:1:-2], self.type2test([3]))
		self.assertEqual(u[3:0:-2], self.type2test([3, 1]))
		self.assertEqual(u[::-100], self.type2test([4]))
		self.assertEqual(u[100:-100:], self.type2test([]))
		self.assertEqual(u[-100:100:], u)
		self.assertEqual(u[100:-100:-1], u[::-1])
		self.assertEqual(u[-100:100:-1], self.type2test([]))
		self.assertEqual(u[-100:100:2], self.type2test([0, 2, 4]))

		# Test extreme cases with long ints
		a = self.type2test([0, 1, 2, 3, 4])
		self.assertEqual(a[-pow(2, 128):3], self.type2test([0, 1, 2]))
		self.assertEqual(a[3:pow(2, 145)], self.type2test([3, 4]))
		self.assertEqual(a[3::sys.maxsize], self.type2test([3]))

	def test_contains(self):
		u = self.type2test([0, 1, 2])
		for i in u:
			assert i in u
		for i in min(u) - 1, max(u) + 1:
			assert i not in u

		self.assertRaises(TypeError, u.__contains__)

	def test_contains_fake(self):
		# Sequences must use rich comparison against each item
		# (unless "is" is true, or an earlier item answered)
		# So ALWAYS_EQ must be found in all non-empty sequences.
		assert ALWAYS_EQ not in self.type2test([])
		assert ALWAYS_EQ in self.type2test([1])
		assert 1 in self.type2test([ALWAYS_EQ])
		assert NEVER_EQ not in self.type2test([])

	def test_contains_order(self):
		# Sequences must test in-order.  If a rich comparison has side
		# effects, these will be visible to tests against later members.
		# In this test, the "side effect" is a short-circuiting raise.
		class DoNotTestEq(Exception):
			pass

		class StopCompares:

			def __eq__(self, other):
				raise DoNotTestEq

		checkfirst = self.type2test([1, StopCompares()])
		assert 1 in checkfirst
		checklast = self.type2test([StopCompares(), 1])
		self.assertRaises(DoNotTestEq, checklast.__contains__, 1)

	def test_len(self):
		self.assertEqual(len(self.type2test()), 0)
		self.assertEqual(len(self.type2test([])), 0)
		self.assertEqual(len(self.type2test([0])), 1)
		self.assertEqual(len(self.type2test([0, 1, 2])), 3)

	def test_minmax(self):
		u = self.type2test([0, 1, 2])
		self.assertEqual(min(u), 0)
		self.assertEqual(max(u), 2)

	def test_addmul(self):
		u1 = self.type2test([0])
		u2 = self.type2test([0, 1])
		self.assertEqual(u1, u1 + self.type2test())
		self.assertEqual(u1, self.type2test() + u1)
		self.assertEqual(u1 + self.type2test([1]), u2)
		self.assertEqual(self.type2test([-1]) + u1, self.type2test([-1, 0]))
		self.assertEqual(self.type2test(), u2 * 0)
		self.assertEqual(self.type2test(), 0 * u2)
		self.assertEqual(self.type2test(), u2 * 0)
		self.assertEqual(self.type2test(), 0 * u2)
		self.assertEqual(u2, u2 * 1)
		self.assertEqual(u2, 1 * u2)
		self.assertEqual(u2, u2 * 1)
		self.assertEqual(u2, 1 * u2)
		self.assertEqual(u2 + u2, u2 * 2)
		self.assertEqual(u2 + u2, 2 * u2)
		self.assertEqual(u2 + u2, u2 * 2)
		self.assertEqual(u2 + u2, 2 * u2)
		self.assertEqual(u2 + u2 + u2, u2 * 3)
		self.assertEqual(u2 + u2 + u2, 3 * u2)

		class subclass(self.type2test):  # type: ignore
			pass

		u3 = subclass([0, 1])
		assert u3 == u3 * 1
		assert u3 is not u3 * 1

	def test_iadd(self):
		u = self.type2test([0, 1])
		u += self.type2test()
		self.assertEqual(u, self.type2test([0, 1]))
		u += self.type2test([2, 3])
		self.assertEqual(u, self.type2test([0, 1, 2, 3]))
		u += self.type2test([4, 5])
		self.assertEqual(u, self.type2test([0, 1, 2, 3, 4, 5]))

		u = self.type2test("spam")
		u += self.type2test("eggs")
		self.assertEqual(u, self.type2test("spameggs"))

	def test_imul(self):
		u = self.type2test([0, 1])
		u *= 3
		assert u == self.type2test([0, 1, 0, 1, 0, 1])
		u *= 0
		assert u == self.type2test([])

	def test_getitemoverwriteiter(self):
		# Verify that __getitem__ overrides are not recognized by __iter__
		class T(self.type2test):  # type: ignore

			def __getitem__(self, key):
				return str(key) + '!!!'

		assert next(iter(T((1, 2)))) == 1

	def test_repeat(self):
		for m in range(4):
			s = tuple(range(m))
			for n in range(-3, 5):
				self.assertEqual(self.type2test(s * n), self.type2test(s) * n)
			self.assertEqual(self.type2test(s) * (-4), self.type2test([]))
			self.assertEqual(id(s), id(s * 1))

	def test_bigrepeat(self):
		if sys.maxsize <= 2147483647:
			x = self.type2test([0])
			x *= 2**16
			self.assertRaises(MemoryError, x.__mul__, 2**16)
			if hasattr(x, '__imul__'):
				self.assertRaises(MemoryError, x.__imul__, 2**16)

	def test_subscript(self):
		a = self.type2test([10, 11])
		self.assertEqual(a.__getitem__(0), 10)
		self.assertEqual(a.__getitem__(1), 11)
		self.assertEqual(a.__getitem__(-2), 10)
		self.assertEqual(a.__getitem__(-1), 11)
		self.assertRaises(IndexError, a.__getitem__, -3)
		self.assertRaises(IndexError, a.__getitem__, 3)
		self.assertEqual(a.__getitem__(slice(0, 1)), self.type2test([10]))
		self.assertEqual(a.__getitem__(slice(1, 2)), self.type2test([11]))
		self.assertEqual(a.__getitem__(slice(0, 2)), self.type2test([10, 11]))
		self.assertEqual(a.__getitem__(slice(0, 3)), self.type2test([10, 11]))
		self.assertEqual(a.__getitem__(slice(3, 5)), self.type2test([]))
		self.assertRaises(ValueError, a.__getitem__, slice(0, 10, 0))
		self.assertRaises(TypeError, a.__getitem__, 'x')

	def test_count(self):
		a = self.type2test([0, 1, 2]) * 3
		self.assertEqual(a.count(0), 3)
		self.assertEqual(a.count(1), 3)
		self.assertEqual(a.count(3), 0)

		self.assertEqual(a.count(ALWAYS_EQ), 9)
		self.assertEqual(self.type2test([ALWAYS_EQ, ALWAYS_EQ]).count(1), 2)
		self.assertEqual(self.type2test([ALWAYS_EQ, ALWAYS_EQ]).count(NEVER_EQ), 2)
		self.assertEqual(self.type2test([NEVER_EQ, NEVER_EQ]).count(ALWAYS_EQ), 0)

		self.assertRaises(TypeError, a.count)

		class BadExc(Exception):
			pass

		class BadCmp:

			def __eq__(self, other):
				if other == 2:
					raise BadExc()
				return False

		self.assertRaises(BadExc, a.count, BadCmp())

	@not_pypy("Doesn't work on PyPy")
	def test_index(self):
		u = self.type2test([0, 1])
		self.assertEqual(u.index(0), 0)
		self.assertEqual(u.index(1), 1)
		self.assertRaises(ValueError, u.index, 2)

		u = self.type2test([-2, -1, 0, 0, 1, 2])
		self.assertEqual(u.count(0), 2)
		self.assertEqual(u.index(0), 2)
		self.assertEqual(u.index(0, 2), 2)
		self.assertEqual(u.index(-2, -10), 0)
		self.assertEqual(u.index(0, 3), 3)
		self.assertEqual(u.index(0, 3, 4), 3)
		self.assertRaises(ValueError, u.index, 2, 0, -10)

		self.assertEqual(u.index(ALWAYS_EQ), 0)
		self.assertEqual(self.type2test([ALWAYS_EQ, ALWAYS_EQ]).index(1), 0)
		self.assertEqual(self.type2test([ALWAYS_EQ, ALWAYS_EQ]).index(NEVER_EQ), 0)
		self.assertRaises(ValueError, self.type2test([NEVER_EQ, NEVER_EQ]).index, ALWAYS_EQ)

		self.assertRaises(TypeError, u.index)

		class BadExc(Exception):
			pass

		class BadCmp:

			def __eq__(self, other):
				if other == 2:
					raise BadExc()
				return False

		a = self.type2test([0, 1, 2, 3])
		self.assertRaises(BadExc, a.index, BadCmp())

		a = self.type2test([-2, -1, 0, 0, 1, 2])
		self.assertEqual(a.index(0), 2)
		self.assertEqual(a.index(0, 2), 2)
		self.assertEqual(a.index(0, -4), 2)
		self.assertEqual(a.index(-2, -10), 0)
		self.assertEqual(a.index(0, 3), 3)
		self.assertEqual(a.index(0, -3), 3)
		self.assertEqual(a.index(0, 3, 4), 3)
		self.assertEqual(a.index(0, -3, -2), 3)
		self.assertEqual(a.index(0, -4 * sys.maxsize, 4 * sys.maxsize), 2)
		self.assertRaises(ValueError, a.index, 0, 4 * sys.maxsize, -4 * sys.maxsize)
		self.assertRaises(ValueError, a.index, 2, 0, -10)

	def test_pickle(self):
		lst = self.type2test([4, 5, 6, 7])
		for proto in range(pickle.HIGHEST_PROTOCOL + 1):
			lst2 = pickle.loads(pickle.dumps(lst, proto))
			self.assertEqual(lst2, lst)
			self.assertNotEqual(id(lst2), id(lst))
