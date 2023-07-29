import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
from inspect import currentframe,getframeinfo

class color_print():
    def __init__(self):
        self.colors = {
            'red':'\033[31m',
            'green':'\033[32m',
            'yellow':'\033[33m',
            'blue':'\033[34m',
            'magenta':'\033[35m',
            'cyan':'\033[36m',
        }
        self.end = '\033[0m'

    def print(self,message,**kwargs):
        try:
            color = self.colors[kwargs['color'].lower()]
        except:
            color = self.end
        try:
            print(color + message + self.end)
        except Exception as e:
            header = "============================================================"
            print(self.colors['red'] + header + "\nCOLOR PRINT ERROR!\n{} | {}\n".format(type(e).__name__.replace("'",""),e.args) + header + self.end)
    
    def debug(self,message):
        self.print(message,color="green")
    def info(self,message):
        self.print(message,color="cyan")
    def warning(self,message):
        self.print(message,color="yellow")
    def error(self,message):
        self.print(message,color="magenta")
    def critical(self,message):
        self.print(message,color="red")

class Log:
    def __init__(self,**kwargs):
        self.printer = color_print()#.p
        required = {"log_path":str,"name":str,"level":int}
        if(self.parse_kwargs(required,kwargs)):
            self.log_path = kwargs['log_path']
            self.name = kwargs['name']
            self.level = kwargs['level']
            try:
                self.print_filename = kwargs['print_filename']
            except Exception as e:
                self.print_filename = False
            if(self.print_filename): self.prefix = self.name + " "
            else: self.prefix = ""

            try:
                self.create_path = kwargs['create_path']
            except KeyError:
                self.create_path = True

            if(self.create_path):
                if(not self.log_path[-1] == "/"):
                    self.log_path += "/"
                if(not self.check_path(self.log_path)):
                    self.printer.critical("CHECK_PATH: Failed to create desired log directory, defaulting to local directory")
                    self.log_path = "./"

            logger = logging.getLogger(self.name)
            logger.setLevel(self.set_level())
            try:
                formatter = logging.Formatter(kwargs['formatter'])
            except KeyError:
                formatter = logging.Formatter('{} | %(levelname)s | %(message)s '.format(datetime.datetime.utcnow().replace(microsecond=0)))
            except Exception as e:
                self.printer.critical("FORMATTER ERROR | {} | {}".format(type(e).__name__,e.args))

            filename = self.log_path+self.name+".log"
        
            fh = TimedRotatingFileHandler(filename,when='d',interval=30,backupCount=1,encoding=None,delay=False,utc=True,atTime=datetime.time(4, 0, 0))
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
            self.logger = logger

    def set_level(self):
        if(self.level == 1):
            return logging.DEBUG
        elif(self.level == 2):
            return logging.INFO
        elif(self.level == 3):
            return logging.WARNING
        elif(self.level == 4):
            return logging.ERROR
        elif(self.level == 5):
            return logging.CRITICAL
        else:
            return logging.DEBUG

    def check_path(self,path):
        try:
            x = path.split("/")
            full_path = ""
            if(x[0] == "." or x[0] == "~"):
                x[0] += "/"
                full_path += x[0]
                x.pop(0)
            for i in range(len(x)):
                if(x[i]):
                    x[i] += "/"
                    full_path += x[i]
                    if(not os.path.exists(full_path)):
                        os.mkdir(full_path)
        except Exception as e:
            self.printer.critical("CHECK_PATH: {} | {}".format(type(e).__name__,e.args))
            return False
        return True

    def parse_kwargs(self,required,kwargs):
        missing = []
        incorrect_type = []
        for key,val in required.items():
            try:
                if(isinstance(val,list)):
                    correct_type = False
                    for item in val:
                        if(isinstance(kwargs[key],item)):
                            correct_type = True
                    if(not correct_type):
                        incorrect_type.append(key)
                elif(not isinstance(kwargs[key],val)):
                    incorrect_type.append(key)
            except KeyError:
                missing.append(key)
            except Exception as e:
                self.printer.critical('PARSE_KWARGS: {} | {}'.format(type(e).__name__,e.args))
        if(missing or incorrect_type):
            self.printer.critical('missing = {} | incorrect type = {}'.format(missing,incorrect_type))
            return False
        else:
            return True

    def debug(self,message):
        self.logger.debug(message)
        self.printer.debug("DEBUG----| " + self.prefix + message)

    def info(self,message):
        self.logger.info(message)
        self.printer.info("INFO-----| " + self.prefix + message)
    
    def warning(self,message):
        self.logger.warning(message)
        self.printer.warning("WARNING--| " + self.prefix + message)
    
    def error(self,message):
        self.logger.error(message)
        self.printer.error("ERROR----| " + self.prefix + message)
    
    def critical(self,message):
        self.logger.critical(message)
        self.printer.critical("CRITICAL-| " + self.prefix + message)

    def line(self): #get line number for logging
        cf = currentframe()
        return str(cf.f_back.f_lineno)+" "