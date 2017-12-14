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

    def log(self, message):
        with open(self.filepath, 'w') as f:
            f.write(message + '\n')

    def log_dict(self, out_dict):
        with open(self.filepath, 'w+') as f:
            out = json.dumps(out_dict)
            f.write(out)

    def log_dict_second(self, out_dict, score):
        with open(self.filepath, 'a') as f:
            out = json.dumps(out_dict)
            f.write(out + " " + str(score) + '\n')

    def readlines(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            return lines
        return None

    def readDict(self):
        
        with open(self.filepath, 'r+') as f:
            # print self.filepath
            # lines = f.readlines()
            # if not lines: return
            # #Reset to start of file
            # f.seek(0)
            in_dict = json.load(f)
            # print "In Dict", in_dict
            
        return in_dict

    # def close(self):
    #     self.log_file.close()

catan_log = Log("log.txt")


