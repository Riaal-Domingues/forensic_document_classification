
import multiprocessing

class holderClass():
    def __init__(self):
        self.x = 12
        
    def increment(self,in_q,out_q):
        while in_q:
            object_class = in_q.get()
            object_class.x = object_class.x + 1
            out_q.put(object_class)

class testClass():
    def __init__(self):
        self.object = holderClass()
        self.x = self.object.x
        
    def process(self):
        #process1 = multiprocessing.Process(target=self.test1)
        #process1.start()
        #process1.join()
        process2 = multiprocessing.Process(target=self.object.increment)
        process2.start()
        process2.join()

    def pool(self):
        pool = multiprocessing.Pool(1)
        #for answer in pool.imap(increment, range(10)):
        #    print(answer)
        #print
        for answer in pool.imap(self.square, range(10)):
            print(answer)

    def test2(self):
        print("Hello, world 2")

    def square(self, x):
        return x * x
    
    def self_square(self):
        self.x = 12


def worker(x):
    return x*x

def is_even(numbers, q):
    for n in numbers:
        if n % 2 == 0:
            q.put(n)
    q.put(None)
    
def even_is(in_q,out_q):
    while in_q:
        number = in_q.get()
        if number == None:
            out_q.put(None)
        else:
            if number % 2 == 0:
                out_q.put(number)

def square(in_q,out_q):
    while in_q:
        number = in_q.get()
        if number == None:
            out_q.put(None)
        else:
            out_q.put(number*number)
            
