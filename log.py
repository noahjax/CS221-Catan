from pieces import *
from devcards import *
from player import *

class Log:

    def __init__(self):
        self.log_file = open("catan_log.txt", "w")
        self.log_file.write("Start of log\n")
        self.log_file.write("#####################################################################\n")
        self.log_file.write("#####################################################################\n")
        self.log_file.write("#####################################################################\n")

    def log(self, message):
        self.log_file.write(message + '\n')

catan_log = Log()

