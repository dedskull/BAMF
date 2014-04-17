from sys import path
import modules
import modules.common
from os.path import abspath, dirname
import threading
import time

path.append(dirname(abspath(__file__)))


def get_version():
    return "0.1.0-experimental"


def get_loaded_modules():
    l = []
    for m in modules.common.Modules.list:
        l.append(m.get_metadata())
    return l


class BruteForceCampaign(object):
    def __init__(self, module):
        self.module = module
        self.config = None
        self.queue_rlock = threading.RLock()
        self.checked = 0
        self.job_queue = []
        self.done = False

    def set_configuration(self, config):
        self.config = config

    def increment_check_count(self):
        with self.queue_rlock:
            self.checked += 1

    def thread_engine(self):
        try:
            while True:
                item = None
                with self.queue_rlock:
                    if self.done:
                        break
                    if len(self.job_queue) > 0:
                        item = self.job_queue[0]
                        del self.job_queue[0]
                if item is None:
                    time.sleep(0.1)
                    continue
                config = self.config
                config['username'] = item[0]
                config['password'] = item[1]
                if self.module.try_credentials(config):
                    print "COMPLETE: %s - %s" % (item[0], item[1])
                    with self.queue_rlock:
                        self.done = True
                self.increment_check_count()
        except Exception:
            print "exception"
        finally:
            with self.queue_rlock:
                self.done = True
                self.job_queue = []