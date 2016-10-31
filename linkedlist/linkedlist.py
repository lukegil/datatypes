#!/usr/bin/python


class LinkedList(object):
    """ Implementation of a Linked List.

        A list is comprised of LinkElements. It is initiated with a `head` which
        is always referenced by the final item.
    """

    def __init__(self):
        """ creates the head, sets length to 0 """
        self.__head = LinkElement()
        self.__head.value = -1
        self.__length = 0

    ################
    ## Properties ##
    ################
    @property
    def head(self):
        """The root of the list. It is never seen by the end user """
        return self.__head

    @head.setter
    def head(self, node):
        """ set the head to a LinkElement object """
        if (not isinstance(node, LinkElement)):
            raise TypeError("head must be type {}, you passed {}".format(LinkElement, type(node)))

        self.__head = node

    @property
    def length(self):
        """ number of LinkElements in List, excluding head """
        return self.__length

    @length.setter
    def length(self, value):

        if (not isinstance(value, int)):
            raise TypeError("head must be type {}, you passed {}".format(int, type(value)))

        self.__length = value

    ##############################
    ## Private / helper methods ##
    ##############################
    def _get_nth_el(self, indx):
        """ same as getting `indx` of a list item, but instead of following
            sequence, follows links

            indx of -1 == head
        """
        if (not isinstance(indx, int)):
            raise TypeError("index must be type {}, you passed {}".format(int, type(indx)))

        if (indx < -1 or indx >= self.length):
            raise IndexError("index out of range")


        # Q : why not use the built in __iter__ function?
        # A : for the scenario in which you want to insert between the head
        #     and the first element
        i = -1
        cur_node = self.head
        while (cur_node.next is not self.head and i < indx):
            cur_node = cur_node.next
            i += 1
        return cur_node


    def _insert_after(self, value, indx):
        """ create a ListElement with `value` and insert after indx """

        # create the new node
        new_node = LinkElement()
        new_node.value = value

        prev_node = self._get_nth_el(indx)

        # new_node takes on prev_nodes link
        new_node.next = prev_node.next

        # prev_node links to new node
        prev_node.next = new_node

        self.length += 1

    def _pop_after(self, indx):
        """ remove the ListElement at `indx` and return """
        prev_node = self._get_nth_el(indx)

        # popped node
        rm_node = prev_node.next

        # snip out prev_node.next
        prev_node.next = prev_node.next.next

        self.length -= 1

        return rm_node


    ############################
    ## Public Methods         ##
    ############################

    ### Write ###
    def append(self, value):
        """ Akin to list's append

            value - @type - any
                  - @param - creates a LinkElement with value as LinkElement.value
        """
        self._insert_after(value, self.length - 1)

    def prepend(self, value):
        """ Push to the beginning of a LinkedList

            value - @type - any
                  - @param - creates a LinkElement with value as LinkElement.value
        """
        self._insert_after(value, -1)

    def pop(self):
        """ Remove and return the final LinkElement in a list """

        l = self.length - 2 # penultimate LinkElement

        old_el = self._pop_after(l)
        return old_el

    def insert(self, value, indx):
        """ insert an element btwn LinkedList[indx - 1] and LinkedList[indx] """

        indx -= 1
        self._insert_after(value, indx)

    ### Read ###
    def get(self, indx):
        """ Same as LinkedList[indx]

            indx - @type - int
                 - @param - LinkElement to get. If < 0, get `indx`th el from the end of list

            *Performance* - this is an O(n) operation compared to standard list
                           which is O(1)
        """

        if (indx < 0):
            indx = self.length + indx

        return self._get_nth_el(indx)

    ###########################
    ### Container type methods
    ### Enables things like len() and iteration
    ### https://docs.python.org/2/reference/datamodel.html#emulating-container-types
    ###########################
    def __iter__(self):
        """ Iterate through LL following Links """
        cur_node = self.head.next # first node
        while (cur_node is not self.head):
            yield cur_node
            cur_node = cur_node.next

    def __len__(self):
        return self.length

    def __getitem__single(self, key):
        """ Returns LinkElement at position key """
        return self.get(key)

    def __getitem__slice(self, slice_k):
        """ Returns LinkedList of indices specified in slice_k, type slice """
        start = slice_k.start or 0
        stop = slice_k.stop
        step = slice_k.step or 1

        L = LinkedList() # Return List
        i = start
        prev_self = self._get_nth_el(start - 1)
        prev_L = L.head

        # iterate through remainder of list, saving every nth item to L, where n = step
        while (start < stop):

            if (i == start):
                new_el = LinkElement()
                new_el.val = prev_self.next.value
                prev_L.next = new_el
                prev_L = prev_L.next
                start += step

            prev_self = prev_self.next
            i += 1
        return L

    def __getitem__(self, key):
        """ implements self[key] evaluation

            key - @type - int or slice
                - @param - the nth item you want, or the slice of items you want
        """
        if (isinstance(key, slice)):
            return self.__getitem__slice(key)

        elif (isinstance(key, int)):
            return self.__getitem__single(key)

        else:
            raise TypeError("Type of {} was passed to __getitem__. Only {} and {} are accepted".format(type(key), slice, int))

    def __setitem__single(self, key, value):
        """ Sets self[key] to new LinkElement of value """
        prev_el = self._get_nth_el(key - 1)
        new_el = LinkElement()
        new_el.value = value
        new_el.next = prev_el.next.next
        prev_el.next = new_el

    def __setitem__slice(self, slice_k, values):
        """ Sets specified slice of self to values. Does not check that len(values) is correct

            slice_k - @type - slice
                    - @param - from slice.start up to slice.stop, set every slice.step el to value

            values - @type - iterable
                   - @param - an iterable of values to set self[indices] to

        """

        start = slice_k.start or 0
        stop = slice_k.stop
        step = slice_k.step or 1

        i = start
        j = 0
        prev_el = self._get_nth_el(i - 1)

        # from prev_el/start set every nth element to the next value, where n = step
        while (start < stop):
            if (i == start):
                new_el = LinkElement()
                new_el.value = values[j]
                new_el.next = prev_el.next.next
                prev_el.next = new_el
                start += step
                j += 1
            prev_el = prev_el.next
            i += 1

    def __setitem__(self, key, value):
        """ supports self[key] assignment.

            key - @type - slice or int
                - @param - the indices to replace

            value - @type - any or iterable
                  - @param - the indices
        """
        if (isinstance(key, int)):
            self.__setitem__single(key, value)

        elif (isinstance(key, slice) and hasattr(value, "__iter__")):
            self.__setitem__slice

        elif (isinstance(key, slice) and not hasattr(value, "__iter__")):
            raise TypeError("Tried to assign {} to slice of {}. Only iterables accepted".format(type(key), type(self)))

        else:
            raise TypeError("Type of {} was passed to __getitem__. Only {} and {} are accepted".format(type(key), slice, int))

    def __delitem__single(self, key):
        """ pop ListElement at `key` """
        prev_i = key - 1
        self._pop_after(prev_i)

    def __delitem_slice(self, slice_k):
        """ pop all ListElements spec'd by slice_k, type = slice """
        # For performance reasons, cannot use either pop or __delitem_single
        start = slice_k.start or 0
        stop = slice_k.stop
        step = slice_k.step or 1

        prev_el = self._get_nth_el(start - 1)
        i = start
        while (start < stop):
            if (i == start):
                prev_el.next = prev_el.next.next
                start += step
            prev_el = prev_el.next
            i += 1

    def __delitem__(self, key):
        """ support for `del self[key]`

            key - @type - int or slice
                - @param - a index or slice of indices to delete
        """
        if (isinstacne(key, slice)):
            self.__delitem_slice(key)

        elif (isinstance(key, int)):
            self.__delitem__single(key)

        else:
            raise TypeError("Type of {} was passed to __getitem__. Only {} and {} are accepted".format(type(key), slice, int))

    def __contains__(self, value):
        """ Is value in self[x].value for some x?
            Like a normal `list` it simply iterates through to search
            https://github.com/certik/python-2.7/blob/c360290c3c9e55fbd79d6ceacdfc7cd4f393c1eb/Objects/listobject.c#L438
        """
        for i in self:
            if (value == i.value):
                return True
        return False

    ###########################
    ### Numeric comparison type methods
    ### Enables things like > and ==
    ### https://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
    ###########################
    def __cmp__(self, cmp_w):
        """ Returns -1, 0, 1
            if self's list > cmp_w returns 1
            if self's list == cmp_w returns 0
            if self's list < cmp_w returns -1

            cmp_w - @type - LinkedList
                  - @param - is second operand in self < cmp_w for any op

            If self and cmp_w are diff types, is arbitrarily consistent.
                str(type(self)) compared to str(type(cmp_w))

            Otherwise, the first list with a smaller node is __lt__.
            if list1 is a subset of list2, list1 < list2

            See https://docs.python.org/2.7/reference/expressions.html#not-in
        """
        # diff't types, just compare type names
        if (not isinstance(cmp_w, type(self))):
            if (self < cmp_w):
                return -1
            elif (cmp_w == self):
                return 0
            else:
                return 1

        # iterate, matching item by item
        self_node = self.head.next
        other_node = cmp_w.head.next
        while (self_node is not self.head and other_node is not cmp_w.head):
            if (other_node < self_node):
                return 1
            elif (other_node > self_node):
                return -1

            self_node = self_node.next
            other_node = other_node.next

        # Still are euqal, so compare length (meaning whichever's head we got to)
        if (self_node is self.head and other_node is cmp_w.head):
            return 0
        elif (self_node is self.head):
            return -1
        elif (other_node is cmp_w.head):
            return 1

    def __gt__(self, cmp_w):
        if (self.__cmp__(cmp_w) == 1):
            return True
        else:
            return False

    def __ge__(self, cmp_w):
        if (self.__gt__(cmp_w) or self.__eq__(cmp_w)):
            return True
        else:
            return False

    def __lt__(self, cmp_w):
        if (self.__cmp__(cmp_w) == -1):
            return True
        else:
            return False
    def __le__(self, cmp_w):
        if (self.__lt__(cmp_w) or self.__eq__(cmp_w)):
            return True
        else:
            return False

    def __eq__(self, cmp_w):
        """ NB: This tests equivalence of values, not identity """
        if (self.__cmp__(cmp_w) == 0):
            return True
        else:
            return False

    def __ne__(self, cmp_w):
        if (not self.__eq__(cmp_w)):
            return True
        else:
            return False

    def __add__(self, other):
        """ Concat two LinkedLists and return a third one

            TODO : allow for LinkedList + List
        """
        if (not isinstance(other, type(self))):
            raise TypeError("can only concatenate {} (not {}) to {}".format(type(self), type(other), type(self)))

        new_list = LinkedList() # List to return
        prev_el = new_list.head # start appending to this

        for el in self:
            new_el = LinkElement()
            new_el.value = el.value
            prev_el.next = new_el
            prev_el = new_el

        for el in other:
            new_el = LinkElement()
            new_el.value = el.value
            prev_el.next = new_el
            prev_el = new_el

        new_el.next = new_list.head # close the loop by linking last el and head

        return new_list

    def __mul__(self, n):
        """ concatenate self to itself n-times. Return *new* list """
        if (not isinstance(n, int)):
            raise TypeError("can only concatenate {} (not {}) to {}".format(type(self), type(n), type(self)))

        new_list = LinkedList()
        for i in range(n):
            new_list += self
        return new_list

    def __repr__(self):
        """ __str__ falls back to this. Is what is printed in interactive env.

            Possible improvement :
                print as [[value, index of linked item in this list], ...]
                would require new __str__
        """
        ret_str = ""
        for cur_node in self:
            ret_str += "{}, ".format(cur_node.value)

        if ret_str:  ret_str = ret_str[:-2] # rm dangling ", "
        return "[" + ret_str + "]"



class LinkElement(object):
    """ Elements of a Linked List. Include a value and a reference to the next
        item in the LinkedList
    """

    def __init__(self):
        self.__next = self #reference to the next object
        self.__value = None #value of head object is None

    ################
    ## Properties ##
    ################
    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, LinkElement_obj):
        if (not isinstance(LinkElement_obj, LinkElement)):
            raise TypeError("set_next takes a {} object. You added a {}".format(self, type(LinkElement_obj)))
        self.__next = LinkElement_obj

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


    ###########################
    ### Numeric comparison type methods
    ### Enables things like > and ==
    ### https://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
    ###########################
    def __cmp__(self, cmp_w):
        """ Returns -1, 0, 1
            if self.value > cmp_w.value: returns 1
            if self.value == cmp_w.value: returns 0
            if self.value < cmp_w.value: returns -1

            cmp_w - @type - LinkElement
                  - @param - is second operand in self < cmp_w for any op

            If self and cmp_w are diff types, is arbitrarily consistent.
                str(type(self)) compared to str(type(cmp_w))

            Otherwise, relies on Python's defaults

            See https://docs.python.org/2.7/reference/expressions.html#not-in
        """
        if (not isinstance(cmp_w, type(self))):
            if (str(type(self)) < str(type(cmp_w))):
                return -1
            elif (str(type(cmp_w)) == str(type(self))):
                return 0
            else:
                return 1

        else:

            if ( self.value < cmp_w.value):
                return -1
            elif (cmp_w.value == self.value):
                return 0
            else:
                return 1

    def __gt__(self, cmp_w):
        if (self.__cmp__(cmp_w) == 1):
            return True
        else:
            return False

    def __ge__(self, cmp_w):
        if (self.__gt__(cmp_w) or self.__eq__(cmp_w)):
            return True
        else:
            return False

    def __lt__(self, cmp_w):
        if (self.__cmp__(cmp_w) == -1):
            return True
        else:
            return False
    def __le__(self, cmp_w):
        if (self.__lt__(cmp_w) or self.__eq__(cmp_w)):
            return True
        else:
            return False

    def __eq__(self, cmp_w):
        """ NB : this is equivalence of value field, not identity use `self is cmp_w` for that """
        if (self.__cmp__(cmp_w) == 0):
            return True
        else:
            return False

    def __ne__(self, cmp_w):
        if (not self.__eq__(cmp_w)):
            return True
        else:
            return False


    ##############################
    ## End-user representation  ##
    ##############################
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
