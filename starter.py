#!/usr/bin/python
# wentong@taobao.com
# 11-1-20
#


from setting import *
from core.thread_manager import Thread_Manager
import os,re

class easy_runner:

    thread_manager = Thread_Manager()

    def __init__(self):
        pass

    def load_scenario(self):
        print "loading scenario!"
        test = re.compile('.py$',re.IGNORECASE)
        for s_path in SCENARIOS_PATH:
            files = filter(test.search,os.listdir(s_path))
            for file in files:
                print "loading ",os.path.join(s_path,file),
                execfile(os.path.join(s_path,file))
                exec "o=Scenario()"
                print "(name:",o.get_name(),"think time(s):",o.think_time,"thread num:",o.thread_num,")"
                self.thread_manager.add_scenario(o)


    def run(self):
        self.thread_manager.run()

    def join(self):
        self.thread_manager.join()


if __name__=='__main__':
    e=easy_runner()
    e.load_scenario()
    e.run()

    is_quit = False
    while not is_quit:
        q = raw_input("press q/Q + Enter is quit:\n")
        if q.startswith("Q") or q.startswith("q"):
            e.thread_manager.is_stop=True
            is_quit=True
    e.join()





