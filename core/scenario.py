#!/usr/bin/python
# wentong@taobao.com
# 11-1-19 11:23
#

class abstract_scenario:
    name = None
    think_time = 0
    thread_num = 1
    scenario_thread_pool = []
    run_count = None
    #for staticistis
    stat_done_count = 0
    stat_failed_count = 0
    stat_response_time = 0.0

    def get_name(self):
        if self.name:
            return self.name
        else:
            return "All"

    def init(self):
        pass

    def real_action(self):
        try:
            return self.action()
        except Exception:
            return False

    def action(self):
        pass

    def destory(self):
        pass

    def stat_info(self, rt, ret=True, count=1):
        if ret:
            self.stat_done_count += count
        else:
            self.stat_failed_count += count
        self.stat_response_time += rt

    def clear_stat_info(self):
        self.stat_done_count = 0
        self.stat_failed_count = 0
        self.stat_response_time = 0.0
