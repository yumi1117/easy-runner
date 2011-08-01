#!/usr/bin/python
# wentong@taobao.com
# 11-1-21
#

class logger:
    logger = None

    def __init__(self, log_file_name):
        import os
        if os.path.exists(log_file_name):
            import time
            old_log_file_name = log_file_name+"."+time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            if os.path.exists(old_log_file_name):
                os.remove(old_log_file_name)
            os.rename(log_file_name, old_log_file_name)

        import logging
        import logging.handlers
        self.logger = logging.getLogger()
        hdlr = logging.FileHandler(filename=log_file_name)
        formatter = logging.Formatter("%(asctime)s : %(message)s")
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.NOTSET)

    def log(self,msg):
        self.logger.info(msg)