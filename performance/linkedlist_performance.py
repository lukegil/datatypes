import random
import time
from linkedlist.linkedlist import LinkedList
from plotly.offline import plot
from plotly.graph_objs import Scatter

class Timer(object):
    def start_time(self):
        self.start = time.clock()

    def stop_time(self):
        self.stop = time.clock()

    def get_elapsed(self):
        return self.stop - self.start

def get_avg(num_list):
    """ get the average of a list of numbers """
    return sum(num_list)/len(num_list)

def avg_obj(obj):
    ret = []
    for key in sorted(obj):
        ret.append([key, get_avg(obj[key])])
    return ret

def compare_append(arr_len, step, num_times, safety=10):
    LL_time = {}
    NL_time = {}

    for length in range(1, arr_len, step):
        LL_time[length] = []
        NL_time[length] = []

        for i in range(num_times):
            append_val = random.random()

            t2 = Timer()
            t2.start_time()

            LL = LinkedList()
            [LL.prepend(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            LL.append(append_val)
            t.stop_time()
            LL_time[length].append(t.get_elapsed())

            NL = []
            [NL.append(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            NL.append(append_val)
            t.stop_time()
            NL_time[length].append(t.get_elapsed())

            t2.stop_time()
            if (t2.get_elapsed() > safety):
                return [NL_time, LL_time]

    return [NL_time, LL_time]

def compare_prepend(arr_len, step, num_times, safety=10):
    LL_time = {}
    NL_time = {}

    for length in range(1, arr_len, step):
        LL_time[length] = []
        NL_time[length] = []
        for i in range(num_times):
            prepend_val = random.random()

            t2 = Timer()
            t2.start_time()

            LL = LinkedList()
            [LL.prepend(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            LL.prepend(prepend_val)
            t.stop_time()
            LL_time[length].append(t.get_elapsed())

            NL = []
            [NL.append(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            NL.insert(0, prepend_val)
            t.stop_time()
            NL_time[length].append(t.get_elapsed())

            t2.stop_time()
            if (t2.get_elapsed() > safety):
                return [NL_time, LL_time]

    return [NL_time, LL_time]

def compare_insert(arr_len, step, num_times, safety=10):
    LL_time = {}
    NL_time = {}

    for length in range(1, arr_len, step):
        LL_time[length] = []
        NL_time[length] = []

        for i in range(num_times):
            insert_val = random.random()
            insert_index = random.randint(0, length)

            t2 = Timer()
            t2.start_time()

            LL = LinkedList()
            [LL.prepend(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            LL.insert(insert_index, insert_val)
            t.stop_time()
            LL_time[length].append(t.get_elapsed())

            NL = []
            [NL.append(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            NL.insert(insert_index, insert_val)
            t.stop_time()
            NL_time[length].append(t.get_elapsed())

            t2.stop_time()
            if (t2.get_elapsed() > safety):
                return [NL_time, LL_time]

    return [NL_time, LL_time]

def insertion_sort(A):

    for indx in range(1, len(A)):
        val = A[indx]
        lft_indx = indx - 1

        while lft_indx >= 0 and A[lft_indx] > val:
            A[lft_indx + 1] = A[lft_indx]
            lft_indx -= 1
        A[lft_indx + 1] = val

    return A

def compare_insert_sort(arr_len, step, num_times, safety=10):
    LL_time = {}
    NL_time = {}

    for length in range(1, arr_len, step):
        LL_time[length] = []
        NL_time[length] = []

        for i in range(num_times):
            t2 = Timer()
            t2.start_time()

            LL = LinkedList()
            [LL.append(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            insertion_sort(LL)
            t.stop_time()
            LL_time[length].append(t.get_elapsed())

            NL = []
            [NL.append(random.random()) for x in range(length) ]

            t = Timer()
            t.start_time()
            insertion_sort(NL)
            t.stop_time()
            NL_time[length].append(t.get_elapsed())

            t2.stop_time()
            if (t2.get_elapsed() > safety):
                return [NL_time, LL_time]

    return [NL_time, LL_time]

def graph_results(test, results):

    results = {
        "Python List, {}".format(test) : avg_obj(results[0]),
        "Linked List, {}".format(test) : avg_obj(results[1])
    }

    graph_lines = []
    for name in results:

        line = Scatter(
            x = [d[0] for d in results[name]],
            y = [d[1] for d in results[name]],
            mode = 'line',
            name = name
        )
        graph_lines.append(line)

    plot(graph_lines, filename="{}_{}.html".format(test, int(time.time())))

if __name__ == "__main__":
    ar = compare_append(100001, 10000, 50)
    graph_results("append", ar)

    pr = compare_prepend(100001, 5000, 100)
    graph_results("prepend", pr)
    
    ir = compare_insert(100001, 10000, 50)
    graph_results("insert", ir)

    i_s = compare_insert_sort(100001, 10000, 50)
    graph_results("insertion_sort", i_s)
