import unittest
from linkedlist.linkedlist import LinkElement

class LinkEl_base(unittest.TestCase):
    def setUp(self):
        self.el = LinkElement()
        self.el2 = LinkElement()

class LinkEl_init(LinkEl_base):
    def test_value(self):
        self.assertIsNone(self.el.value)

    def test_next(self):
        e = self.el
        n = self.el.next
        self.assertIs(e, n)

class LinkEl_next(LinkEl_base):

    def test_getter(self):
        self.assertIs(self.el.next, self.el)

    def test_setter_basecase(self):
        self.el.next = self.el2
        self.assertIs(self.el.next, self.el2)

    def test_setter_typecheck(self):
        with self.assertRaises(TypeError):
            self.el.next = 9

class LinkEl_value(LinkEl_base):
    def test_getter_basecase(self):
        self.assertIsNone(self.el.value)

    def test_setter_int(self):
        self.el.value = 7
        self.assertEqual(self.el.value, 7)

    def test_setter_iterable(self):
        self.el.value = [1,2,3]
        self.assertEqual(self.el.value, [1,2,3])

class LinkEl__cmp__(LinkEl_base):

    def test_diffType_lt(self):
        # Nonetype > LinkElement
        larger = None
        self.assertEqual(self.el.__cmp__(larger), -1)

    def test_diffType_gt(self):
        # class A < class Li...
        class A(object):
            pass

        smaller = A()
        self.assertEqual(self.el.__cmp__(smaller), 1)

    def test_sameType_lt(self):
        self.el.value = 7
        self.el2.value = 9

        self.assertEqual(self.el.__cmp__(self.el2), -1)

    def test_sameType_eq(self):
        self.el.value = 9
        self.el2.value = 9

        self.assertEqual(self.el.__cmp__(self.el2), 0)

    def test_sameType_gt(self):
        self.el.value = 10
        self.el2.value = 9

        self.assertEqual(self.el.__cmp__(self.el2), 1)

class LinkEl_comparisons(LinkEl_base):
    def test_diffType_lt(self):
        larger = None
        self.assertTrue(self.el < larger)

    def test_diffType_gt(self):
        class A(object):
            pass
        smaller = A()
        self.assertTrue(self.el > smaller)

    def test_sameType_lt(self):
        self.el.value = 9
        self.el2.value = 10
        self.assertTrue(self.el < self.el2)

    def test_sameType_lte_lt(self):
        self.el.value = 9
        self.el2.value = 10
        self.assertTrue(self.el <= self.el2)

    def test_sameType_lte_eq(self):
        self.el.value = 10
        self.el2.value = 10
        self.assertTrue(self.el <= self.el2)

    def test_sameType_gt(self):
        self.el.value = 11
        self.el2.value = 10
        self.assertTrue(self.el > self.el2)

    def test_sameType_gte_gt(self):
        self.el.value = 11
        self.el2.value = 10
        self.assertTrue(self.el >= self.el2)

    def test_sameType_gte_eq(self):
        self.el.value = 11
        self.el2.value = 11
        self.assertTrue(self.el >= self.el2)

    def test_sameType_eq(self):
        self.el.value = 11
        self.el2.value = 11
        self.assertTrue(self.el == self.el2)

    def test_sameType_ne(self):
        self.el.value = 10
        self.el2.value = 11
        self.assertTrue(self.el != self.el2)



if __name__ == '__main__':
    unittest.main()
