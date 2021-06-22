import threading
import time


class LogReader:
    LOG_UPDATE_SPEED = 0.1

    def __init__(self, patterns, log_path="/Users/Elliot Roe/AppData/LocalLow/Wizards Of The Coast/MTGA/Player.log",
                 player_id="LE3ZCMCJZBHUDGATTY2EJLUEIM"):
        self.__player = player_id
        self.__log_path = log_path
        self.__lines_containing_pattern = {}
        self.__has_new_line = {}
        for pattern in patterns:
            self.__lines_containing_pattern[pattern] = ""
            self.__has_new_line[pattern] = False

        self.__log_monitor_thread = None
        self.__stop_monitor = False

    def __follow(self, the_file):
        the_file.seek(0)
        while not self.__stop_monitor:
            line = the_file.readline()
            if not line:
                time.sleep(self.LOG_UPDATE_SPEED)
                continue
            yield line

    def __monitor_log_file(self):
        print(self.__log_path)
        log_file = open(self.__log_path, "r")
        log_lines = self.__follow(log_file)
        for line in log_lines:
            if self.__stop_monitor:
                return
            for pattern in self.__lines_containing_pattern:
                if pattern in line:
                    self.__has_new_line[pattern] = True
                    self.__lines_containing_pattern[pattern] = line

    def start_log_monitor(self):
        self.__stop_monitor = False
        self.__log_monitor_thread = threading.Thread(target=self.__monitor_log_file)
        self.__log_monitor_thread.start()

    def stop_log_monitor(self):
        self.__stop_monitor = True
        self.__log_monitor_thread.join()

    def is_monitoring(self):
        return self.__log_monitor_thread is not None and self.__log_monitor_thread.is_alive()

    def get_latest_line_containing_pattern(self, pattern):
        self.__has_new_line[pattern] = False
        return self.__lines_containing_pattern[pattern]

    def has_new_line(self, pattern):
        return self.__has_new_line[pattern]
