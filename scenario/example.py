#!/usr/bin/python
# wentong@taobao.com
# 11-1-20
#
import core.scenario

class Scenario(core.scenario.abstract_scenario):
    thread_num=1
    think_time = 0

#    run_count =1000

    name="update"

    socket = None

    def init(self):
        import socket

        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1',7000))
        self.socket.send('init:'+self.name+':\n')

    def action(self):
        self.socket.send('action\n')
        ret = self.socket.recv(2)
        if ret.startswith("S"):
            return True
        else:
            return False

    def destory(self):
        self.socket.send('end\n')
        self.socket.close()
