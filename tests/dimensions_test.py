"""Test dimension library."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from absl.testing import parameterized

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simplefermi import utils as u
from simplefermi import dimensions as d

class DimensionsTest(parameterized.TestCase):


  @parameterized.parameters(
    ({"a": 1, "b": 2}, "a", {"a": 2, "b": 2}),
    ({"a": -1, "b": 2}, "a", {"a": 0, "b": 2}),
    ({"b": 2}, "a", {"a": 1, "b": 2}))
  def test_inc(self, starting, key, expected):
    self.assertEqual(d._inc(starting, key), expected)

  @parameterized.parameters(
    ({"a": 2, "b": 2}, "a", {"a": 1, "b": 2}),
    ({"a": 1, "b": 2}, "a", {"a": 0, "b": 2}),
    ({"b": 2}, "a", {"a": -1, "b": 2}))
  def test_dec(self, starting, key, expected):
    self.assertEqual(d._dec(starting, key), expected)

  def test_symbol_name(self):
    a = d.Symbol('a')
    self.assertEqual(a.name, 'a')

  def test_symbols(self):
    a = d.Symbol('a')
    b = d.Symbol('b')

    self.assertEqual(dict(a*b), {a: 1, b: 1})
    self.assertEqual(dict(a/b), {a: 1, b: -1})
    self.assertEqual(dict(a/b*b), {a: 1})
    self.assertEqual(dict(a**2), {a: 2})
    self.assertEqual(dict(1/a), {a: -1})
    self.assertFalse((a*b).dimensionless)
    self.assertTrue((b/b).dimensionless)
    self.assertTrue((a**2/b /a *b/a).dimensionless)

    with self.assertRaises(TypeError):
      2 / a
    with self.assertRaises(TypeError):
      2. / a
    with self.assertRaises(TypeError):
      a / 2
    with self.assertRaises(TypeError):
      a / 2.
    with self.assertRaises(TypeError):
      2 * a
    with self.assertRaises(TypeError):
      a * 2

  def test_symbol_eq(self):
    self.assertEqual(d.Symbol('a'), d.Symbol('a'))

  def test_as_dimension(self):
    a = d.Symbol('a')
    q = a * a
    self.assertEqual(d.as_dimension(a), q / a)
    self.assertEqual(d.as_dimension(q), q)

    with self.assertRaises(TypeError):
      d.as_dimension('string')

  def test_dimensions(self):
    a = d.Symbol('a')
    b = d.Symbol('b')
    q1 = a * b
    q2 = a / b

    self.assertEqual(q1 * q2, q1 ** 2 / q2 / q1 * q2**2)
    self.assertEqual(hash(q1 * q2), hash(q1 ** 2 / q2 / q1 * q2**2))
    self.assertEqual(a / q1, a / a / b)
    self.assertEqual(1 / q2, b / a)
    self.assertTrue(isinstance(repr(a), str))
    self.assertTrue(isinstance(repr(a**2), str))
    self.assertTrue(isinstance(repr(q1), str))
    self.assertTrue(isinstance(repr(q1/q1), str))
    with self.assertRaises(TypeError):
      2 / q1
    with self.assertRaises(TypeError):
      2. / q1
    with self.assertRaises(TypeError):
      q1 / 2
    with self.assertRaises(TypeError):
      q1 / 2.
    with self.assertRaises(TypeError):
      2 * q1
    with self.assertRaises(TypeError):
      q1 * 2

  def test_dimension_eq(self):
    a = d.Symbol('a')
    a2 = d.Symbol('a')
    b = d.Symbol('b')
    self.assertEqual(a * b, a2 * b)

if __name__ == '__main__':
  absltest.main()
