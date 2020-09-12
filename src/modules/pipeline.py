import multiprocessing
from time import sleep

class Pipeline():
    
    def __init__(self):
        self.in_q = None          # Input to the pipeline
        self.out_q = None         # Output from the pipeline
        self.nr_stages = 0
        self.nr_queues = 0
        self.func_list = None     # The list of functions called in the pipeline
        self.queue_list = []      # The list of queues connecting the processes
        self.process_list = []    # The processes in order of execution connected by the queues
        
    # Create a new pipeline and start it
    def new_pipeline(self,func_list):
        self.func_list = func_list        # Store this should we like to query it later
        self.nr_stages = len(func_list)   # Extract the number of stages and store it
        self.nr_queues = self.nr_stages + 1
        
        # Create the queues we require and store them in a list
        for i in range(self.nr_queues):
            self.queue_list.append(multiprocessing.Queue())
            
        # Create the processes in order and store them in a list
        q_iter = iter(self.queue_list)
        out_q = next(q_iter)

        for func in func_list:
            in_q = out_q
            out_q = next(q_iter)
            process = multiprocessing.Process(target=func, args=(in_q, out_q))
            self.process_list.append(process)
            
        # Set the input and output to the pipeline to be the first and last queues 
        self.in_q = self.queue_list[0]
        self.out_q = self.queue_list[-1]
        
        # Start the processes
        for process in self.process_list:
            process.start()
            sleep(0.1)
            
    # Kill all running processes in the pipeline and destroy it
    def terminate_pipeline(self):
        for process in self.process_list:
            process.terminate()
            sleep(0.1)
            process.close()
            


