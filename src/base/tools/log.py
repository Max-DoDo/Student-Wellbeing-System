from datetime import datetime
import sys

class Log:

    # ANSI Color
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    @staticmethod
    def getFormattedDate():
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def getFormattedTime():
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def _print(prefix_color, tag, *args, sep=" ", end="\n", file=sys.stdout):

        date = Log.getFormattedDate()
        time = Log.getFormattedTime()

        prefix = f"{prefix_color}[{tag}][{date} {time}]{Log.RESET}"
        message = sep.join(str(a) for a in args)

        file.write(f"{prefix} {message}{end}")

    @staticmethod
    def info(*args, **kwargs):
        Log._print(Log.BLUE, "INFO", *args, **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        Log._print(Log.YELLOW, "WARN", *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        Log._print(Log.RED, "ERROR", *args, **kwargs)

    @staticmethod
    def success(*args, **kwargs):
        Log._print(Log.GREEN, "SUCCESS", *args, **kwargs)

    @staticmethod
    def debug(*args, **kwargs):
        Log._print(Log.CYAN, "DEBUG", *args, **kwargs)

