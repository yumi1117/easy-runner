#!/usr/bin/python
# wentong@taobao.com
# 11-1-19 11:10
# manage thread

import time, threading

class Thread_Manager:
    scenarios = []
    thread_pool = []
    monitor_interval = 1
    is_stop = None
    statistics_info = {}
    done_count = 0
    done_lock = threading.Lock()

    def __init__(self):
        import setting

        if setting.MONITOR_INTERVAL:
            self.monitor_interval = setting.MONITOR_INTERVAL

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def run(self):
        import setting
        #reset thread_pool  and is_stop
        self.thread_pool = []
        self.is_stop = False
        self.done_count = 0

        #add thread
        self.thread_pool.append(threading.Thread(target=self.monitor))
        for scenario in self.scenarios:
            for i in xrange(scenario.thread_num):
                self.thread_pool.append(threading.Thread(target=self.run_scenario, args=(scenario,)))
        print "start run!total:", len(self.thread_pool) - 1

        if setting.THREAD_RULE and len(setting.THREAD_RULE) >= 2:
            delay_time = setting.THREAD_RULE[0]
            delay_thread = setting.THREAD_RULE[1]
            if delay_time > 0 and delay_thread > 0:
                pos = 0
                while pos < len(self.thread_pool):
                    for thread in self.thread_pool[pos:pos + delay_thread]:
                        threading.Thread.start(thread)
                    pos += delay_thread
                    time.sleep(delay_time)
        else:
            for thread in self.thread_pool:
                threading.Thread.start(thread)


    def join(self):
        for thread in self.thread_pool:
            threading.Thread.join(thread)

    def run_scenario(self, scenario):
        import copy

        tmp_scenario = copy.copy(scenario)
        run_count = 0
        tmp_scenario.init()
        while not self.is_stop:
            start = time.time()
            ret = tmp_scenario.real_action()
            scenario.stat_info(time.time() - start, ret)
            run_count += 1
            if scenario.run_count and run_count >= scenario.run_count:
                break
            if scenario.think_time > 0:
                time.sleep(scenario.think_time)
        tmp_scenario.destory()

        try:
            self.done_lock.acquire()
            self.done_count += 1
        finally:
            self.done_lock.release()

    def monitor(self):
        print "monitor start!"
        import logger, setting

        logger = logger.logger(setting.LOG_PATH_AND_FILE_NAME)
        total_count = 0
        total_failed_count = 0
        while (not self.is_stop) and (self.done_count < len(self.thread_pool) - 1):
            log_msg = ""
            for scenario in self.scenarios:
                scenario_count = (scenario.stat_done_count + scenario.stat_failed_count)
                total_failed_count += scenario.stat_failed_count
                if scenario_count == 0:
                    print scenario.get_name(), ":", (scenario_count), "(", 0, ")"
                else:
                    total_count += scenario_count
                    print scenario.get_name(), ":", (
                    scenario_count), "(", scenario.stat_response_time / scenario_count * 1000, ")"
                log_msg += ("<" + scenario.get_name() + "|" + str(scenario.stat_done_count) + "|" + str(
                        scenario.stat_failed_count) + "|" + str(scenario.stat_response_time) + ">")
                scenario.clear_stat_info()
            print "total:", total_count, " total failed:", total_failed_count
            print "---------------------------------"
            if len(log_msg) > 0:
                logger.log(log_msg)
            time.sleep(self.monitor_interval)
        print "runner is over,press q/Q + Enter for quit!"
