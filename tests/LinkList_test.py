import sys, os, unittest
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())
from linkedlist.linkedlist import LinkedList, LinkElement


class LinkList_base(unittest.TestCase):
    def setUp(self):
        self.L = LinkedList()

class LL_init(LinkList_base):
    def test_length(self):
        """ Length of an empty list should be 0 """
        self.assertEqual(self.L.length, 0)

    def test_head_type(self):
        """ Head of a list should be a LinkElement type"""
        self.assertIsInstance(self.L.head, LinkElement)

    def test_head_value(self):
        """ Default Head value should be -1 """
        self.assertEqual(self.L.head.value, -1)

    def test_head_next(self):
        """ The head of a list should link to itself """
        self.assertIs(self.L.head, self.L.head.next)

class LL_head(LinkList_base):
    def test_head_getterType(self):
        """ The head should be of type LinkElement """
        self.assertIsInstance(self.L.head, LinkElement)

    def test_head_getterValue(self):
        """ the head should have a value of -1 """
        self.assertEqual(self.L.head.value, -1)

    def test_head_setterType(self):
        """ The Head should not be anything but type LinkElement """
        with self.assertRaises(TypeError):
            self.L.head = 9

    def test_head_setterValue(self):
        """ The head should have the value you set it to """
        self.L.head.value = "huh"
        self.assertEqual(self.L.head.value, "huh")

class LL_length(LinkList_base):
    def test_length_getterType(self):
        """ The length should be an integer """
        self.assertIsInstance(self.L.length, int)

    def test_length_getterValue(self):
        """ The length of an empty list should be 0 """
        self.assertEqual(self.L.length, 0)

    def test_length_setterType(self):
        """ The length should only be set to an int """
        with self.assertRaises(TypeError):
            self.L.length = {}

    def test_length_setterValue(self):
        """ The length should have the value you set it to """
        self.L.length = 5
        self.assertEqual(self.L.length, 5)

class LinkedList_w_els(LinkList_base):
    def setUp(self):
        self.L = LinkedList()

        new_el = LinkElement()
        new_el.value = 7
        self.L.head.next = new_el
        self.L.head.next.next = self.L.head

        new_el = LinkElement()
        new_el.value = 8
        self.L.head.next.next = new_el
        self.L.head.next.next.next = self.L.head

        self.L.length = 2

class LL_get_nth_el(LinkedList_w_els):

    def test_getNth_indexError_over(self):
        """ You should receive an error if you request an item >= length """
        i = 3
        with self.assertRaises(IndexError):
            self.L._get_nth_el(i)

    def test_getNth_indexError_under(self):
        """ You should receive an error if you request an item < -1 """
        i = -3
        with self.assertRaises(IndexError):
            self.L._get_nth_el(i)

    def test_getNth_typeError(self):
        """ Indices should only be integers """
        i = "L"
        with self.assertRaises(TypeError):
            self.L._get_nth_el(i)

    def test_getNth_head(self):
        """ requesting index -1 should give you the head """
        i = -1
        self.assertIs(self.L._get_nth_el(i), self.L.head)

    def test_getNth_first(self):
        """ requesting indx '0' should give you the element ref'd by the Head """
        i = 0
        self.assertIs(self.L._get_nth_el(i), self.L.head.next)

    def test_getNth_second(self):
        """ requesting index '1' should give you the second element """
        i = 1
        self.assertIs(self.L._get_nth_el(i), self.L.head.next.next)

    def test_getNth_cacheNode(self):
        """ requesting indx '0' should give you the element ref'd by the Head """
        i = 0
        self.L._get_nth_el(i)
        self.assertIs(self.L.cache_node, self.L.head.next)
        self.assertEqual(self.L.cache_index, i)

class LL_insert_after(LinkedList_w_els):

    def test_insertAfter_Head(self):
        """ Inserting after -1 should create a LinkElement ref'd by Head """
        self.L._insert_after("tester", -1)
        self.assertEqual(self.L.head.next.value, "tester")

        self.assertEqual(self.L.length, 3)

    def test_insertAfter_Middle(self):
        """ Inserting after indx 0 should create a LinkElement ref'd by '0' """
        self.L._insert_after("tester2", 0)
        self.assertEqual(self.L.head.next.next.value, "tester2")

        self.assertEqual(self.L.length, 3)

    def test_insertAfter_End(self):
        """ Inserting at end of list should create a LinkElement that refs Head """
        self.L._insert_after("tester3", 1)
        self.assertEqual(self.L.head.next.next.next.value, "tester3")
        self.assertIs(self.L.head, self.L.head.next.next.next.next)
        self.assertEqual(self.L.length, 3)

class LL_pop_after(LinkedList_w_els):

    def test_popAfter_Head(self):
        """ popping after -1 should remove the first element """
        pre_pop = self.L.head.next
        new_val = self.L.head.next.next
        post_pop = self.L._pop_after(-1)

        self.assertIs(pre_pop, post_pop)
        self.assertIs(new_val, self.L.head.next)
        self.assertIsNot(post_pop, self.L.head.next)

    def test_popAfter_middle(self):
        new_el = LinkElement()

        new_el.value = 4
        new_el.next = self.L.head
        self.L.head.next.next.next = new_el

        pre_pop = self.L.head.next.next
        new_val = self.L.head.next.next.next
        post_pop = self.L._pop_after(0)

        self.assertIs(pre_pop, post_pop)
        self.assertIs(new_val, self.L.head.next.next)
        self.assertIsNot(post_pop, self.L.head.next.next)

    def test_popAfter_last(self):
        """ popping after length - 2 should connect length - 2 to the head """
        pre_pop = self.L.head.next.next
        new_val = self.L.head
        post_pop = self.L._pop_after(0)

        self.assertIs(pre_pop, post_pop)
        self.assertIs(new_val, self.L.head.next.next)
        self.assertIsNot(post_pop, self.L.head.next.next)

class LL_append(LinkList_base):

    def test_append_newList(self):
        """ append to an empty list should update length to 1, add a LinkElement after head,
            and that LE should link to Head
        """
        self.L.append(8)
        self.assertEqual(self.L.head.next.value, 8)
        self.assertEqual(self.L.length, 1)
        self.assertIs(self.L.head, self.L.head.next.next)

    def test_append_again(self):
        """ appending to a non-empty list should add to last el, increase length,
            and reset the link to head
        """
        new_el = LinkElement()
        new_el.value = "tester"
        new_el.next = self.L.head
        self.L.head.next = new_el
        self.L.length = 1

        self.L.append("tester2")

        self.assertEqual("tester2", self.L.head.next.next.value)
        self.assertEqual(self.L.length, 2)
        self.assertIs(self.L.head, self.L.head.next.next.next)

class LL_prepend(LinkList_base):

    def test_prepend_newList(self):
        """ prepend to an empty list should update length to 1, add a LinkElement after head,
            and that LE should link to Head
        """
        self.L.prepend(8)
        self.assertEqual(self.L.head.next.value, 8)
        self.assertEqual(self.L.length, 1)
        self.assertIs(self.L.head, self.L.head.next.next)

    def test_prepend_again(self):
        """ prepending to a non-empty list should add before last el, and increase length
        """
        new_el = LinkElement()
        new_el.value = "tester"
        new_el.next = self.L.head
        self.L.head.next = new_el
        self.L.length = 1

        self.L.prepend("tester2")

        self.assertEqual("tester2", self.L.head.next.value)
        self.assertEqual(self.L.length, 2)
        self.assertIs(self.L.head.next.next, new_el)


class LL_pop(LinkedList_w_els):

    def test_pop_empty(self):
        """ popping an empty list should lead to index error """
        L = LinkedList()
        with self.assertRaises(IndexError):
            L.pop()

    def test_pop_normal(self):
        """ popping should remove last item, update links, and update length """
        pre_pop = self.L.head.next.next
        old_length = self.L.length
        post_pop = self.L.pop()

        self.assertIs(pre_pop, post_pop)
        self.assertEqual(self.L.length, old_length - 1)
        self.assertIs(self.L.head, self.L.head.next.next)

class LL_insert(LinkedList_w_els):

    def test_insert_empty(self):
        """ inserting at '0' in empty list should add an element after head, and increase len by 1 """
        L = LinkedList()

        L.insert(0, "tester")
        self.assertEqual(L.head.next.value, "tester")
        self.assertEqual(L.length, 1)
        self.assertIs(L.head, L.head.next.next)

    def test_insert_middle(self):
        """ insert at `indx` should add an element between `indx` - 1 and `indx` """
        old_1 = self.L.head.next
        old_2 = self.L.head.next.next
        old_length = self.L.length
        self.L.insert(1, "tester2")
        self.assertIs(self.L.head.next, old_1)
        self.assertEqual(self.L.head.next.next.value, "tester2")
        self.assertIs(self.L.head.next.next.next, old_2)
        self.assertEqual(self.L.length, old_length + 1)

    def test_insert_IndexError(self):
        """ trying to insert at an index > length should raise an IndexError """
        with self.assertRaises(IndexError):
            self.L.insert(8, "tester3")


class LL_get(LinkedList_w_els):

    def test_get(self):
        """ requesting get(n) should give you the nth element """
        el = self.L.get(1)
        self.assertIs(el, self.L.head.next.next)

    def test_get_IndexError(self):
        """ requesting get(n) where n >= length should error """
        with self.assertRaises(IndexError):
            self.L.get(self.L.length)

class LL_iter(LinkedList_w_els):

    def test_iter(self):
        i = 0
        for el in self.L:
            self.assertIs(el, self.L.get(i))
            i += 1

class LL_len(LinkedList_w_els):

    def test__len__(self):
        self.assertEqual(len(self.L), self.L.length)


class LL_getItemSingle(LinkedList_w_els):

    def test_getitem_single_base(self):
        """ L[n] should return the n'th element """
        self.assertIs(self.L._getitem__single(0), self.L.head.next)

    def test_getitem_single_negative(self):
        """ L[-n] should return n elements from the end of the list """
        self.assertIs(self.L._getitem__single(-2), self.L.head.next)





if __name__ == '__main__':
    unittest.main()
