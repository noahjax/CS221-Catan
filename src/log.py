from collections import defaultdict

class Log:

    def __init__(self, filepath):
        self.log_file = open(filepath, 'w+')
        # self.log_file.write("Start of log\n")
        # self.log_file.write("#####################################################################\n")
        # self.log_file.write("#####################################################################\n")
        # self.log_file.write("#####################################################################\n")

    def log(self, message):
        # self.log_file.write(message + "\n")
        self.log_file.write(message)

    #Writes keys and values to a file
    def log_dict(self, dict):
        for key, val in dict.items():
            self.log_file.write(str(key) +","+str(val) +'\n')

    #Probably useless but something like this could be valuable later
    def countWins(self):
        read_in = self.log_file.readlines()
        print read_in
        counts = defaultdict(int)
        for line in read_in:
            counts[line] += 1

        return dict(counts)

    def readlines(self):
        return self.log_file.readlines()

catan_log = Log("log.txt")
# print(catan_log.countWins())

