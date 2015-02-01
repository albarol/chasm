# -*- coding: utf-8 -*-


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Logger(object):

    __instance = None

    class __impl(object):

        def __init__(self):
            self.has_error = False
            self.messages = []

        def warning(self, message, *params):
            self.messages.append({'type': 'warning', 'message': bcolors.WARNING + 'WARNING: ' + message.format(*params) + bcolors.ENDC})

        def fail(self, message, *params):
            self.has_error = True
            self.messages.append({'type': 'fail', 'message': bcolors.FAIL + 'FAIL: ' + message.format(*params) + bcolors.ENDC})

        def show(self):
            for message in self.messages:
                print message['message']

        def clear(self):
            self.has_error = False
            self.messages = []

    def __init__(self):

        if not Logger.__instance:
            Logger.__instance = Logger.__impl()
        self.__dict__['_Logger__instance'] = Logger.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
