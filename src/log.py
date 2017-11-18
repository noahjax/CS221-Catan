from collections import defaultdict
import json

class Log:

    def __init__(self, filepath):
        self.filepath = filepath
        # self.log_file = open(filepath, "w+")
        # self.log_file.write("Start of log\n")
        # self.log_file.write("#####################################################################\n")
        # self.log_file.write("#####################################################################\n")
        # self.log_file.write("#####################################################################\n")

    # def log(self, message):
    #     self.log_file.write(message + '\n')

    def log_dict(self, out_dict):
        with open(self.filepath, 'w') as f:
            out = json.dumps(out_dict)
            f.write(out)

    def readlines(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            return lines
        return None

    def readDict(self):
        # lines = self.log_file.read() 
        # print lines
        # if not lines: return
        # print lines
        with open(self.filepath, 'r') as f:
            f.seek(0)
            in_dict = json.load(f)
            # print "In Dict", in_dict
        return in_dict

    # def close(self):
    #     self.log_file.close()

catan_log = Log("log.txt")
# print(catan_log.countWins())

