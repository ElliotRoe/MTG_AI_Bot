class MTGALogReader:
    USER = "Elliot Roe"
    LOG_PATH = "C:\\Users\\" + USER + "\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
    GAME_STATE_PATTERN = "GreToClientEvent"

    # follow.py
    #
    # Follow a file like tail -f.

    import time
    def follow(thefile):
        thefile.seek(0, 2)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    if __name__ == '__main__':
        logfile = open("run/foo/access-log", "r")
        loglines = follow(logfile)
        for line in loglines:
            print line,