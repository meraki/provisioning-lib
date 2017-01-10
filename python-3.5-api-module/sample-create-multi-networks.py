import merakiapi as m
import time
import _thread as t
import threading as th
from vars import apikey, org


class netcreator(th.Thread):
    def __init__(self, startnet, endnet):
        self.startnet = startnet
        self.endnet = endnet
        threading.Thread.__init__(self)


    def run(self):

        while i < threadnets:
            m.addnetwork(apikey, org, 'Network #' + str(threadnum) + '-' + str(i), 'appliance', '  THREAD  ', 'UTC',
                         suppressprint=True)
            i += 1
        t.exit()




numofnets = 600
numofthreads = 6
start_time = time.time()
perthreadnets = numofnets / numofthreads

def createnets(threadnets, threadnum):
    i = 0
    while i < threadnets:
        m.addnetwork(apikey, org, 'Network #' + str(threadnum) + '-' + str(i), 'appliance', '  THREAD  ', 'UTC',
                     suppressprint=True)
        i += 1
    t.exit()


try:
    t.start_new_thread(createnets, (perthreadnets, 1,))
    t.start_new_thread(createnets, (perthreadnets, 2,))
    t.start_new_thread(createnets, (perthreadnets, 3,))
    t.start_new_thread(createnets, (perthreadnets, 4,))
    t.start_new_thread(createnets, (perthreadnets, 5,))
    t.start_new_thread(createnets, (perthreadnets, 6,))
except:
    print ("Error: unable to start thread")

while 1:
    pass

run_time = time.time() - start_time
print("{0} Networks Created".format(str(numofnets)))
print("Run time is {0} seconds".format(str(run_time)))
print("Run time is {0}".format(str(run_time/60)))