import os
from datetime import datetime

'''
A class for recording program execution logs and providing diverse console output.
This class provides different console output methods, each with a corresponding color.

It also provides a toggleable function to record all console output from the current run to the file system.

@Author: Max great_maxwell@outlook.com
@LastUpdateDate: 2025-11-27
'''
class Log:

    # ANSI Color
    RESET   = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"

    #  Will the log written into file
    write_to_file = False

    # log folder path
    log_path = "log"

    '''
    This method provide the toogle for whether written down the console output to file system.

    @param: enabled: bool 
        When this parameter set to true. All the log information will be written down to 'log_path/[Date][Time].log'
    '''
    @staticmethod
    def isFileLogging(enabled: bool):
        Log.write_to_file = enabled
        if enabled and not os.path.exists(Log.log_path):
            os.makedirs(Log.log_path)

    '''
    Get current Date. Formatted by YYYY-MM-DD
    This method return the system date 
    '''
    @staticmethod
    def getDate():
        return datetime.now().strftime("%Y-%m-%d")

    '''
    Get current Time. Formatted by HH:MM:SS
    This method return the system time
    '''
    @staticmethod
    def getTime():
        return datetime.now().strftime("%H:%M:%S")
    
    '''
    Get current Time. Formatted by HH-MM-SS
    This method return the system time
    Only calling this method When your system does not allow special characters ':'
    '''
    @staticmethod
    def getTimeForFile():
        return datetime.now().strftime("%H-%M-%S")

    '''
    private class

    '''
    @staticmethod
    def _toFile(prefix: str, message: str):
        if not Log.write_to_file:
            return
        
        log_file = os.path.join(Log.log_path, f"{Log.getDate()} {Log.getTimeForFile()}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{prefix} {message}\n")

    '''
    private class

    '''
    @staticmethod
    def _log(color: str, level: str, *args):
        timestamp = f"{Log.getDate()} {Log.getTime()}"
        message = " ".join(str(a) for a in args)
        prefix = f"[{level}][{timestamp}]"

        print(f"{color}{prefix}{Log.RESET} {message}")

        Log._toFile(prefix, message)

    @staticmethod
    def info(*args):
        Log._log(Log.BLUE, "INFO", *args)

    @staticmethod
    def warn(*args):
        Log._log(Log.YELLOW, "WARN", *args)

    @staticmethod
    def error(*args):
        Log._log(Log.RED, "ERROR", *args)

    @staticmethod
    def success(*args):
        Log._log(Log.GREEN, "SUCCESS", *args)

    @staticmethod
    def debug(*args):
        Log._log(Log.MAGENTA, "DEBUG", *args)