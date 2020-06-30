import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import os
import sys
        
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

    def p(self,message,**kwargs):
        try:
            color = self.colors[kwargs['color'].lower()]
        except:
            color = self.end
        try:
            print(color + message + self.end)
        except Exception as e:
            header = "============================================================"
            print(self.colors['red'] + header + "\nCOLOR PRINT ERROR!\n{} | {}\n".format(type(e).__name__.replace("'",""),e.args) + header + self.end)

class log:
    def __init__(self,**kwargs):
        self.printer = color_print().p
        required = {"log_path":str,"name":str,"level":[str,int]}
        if(self.parse_kwargs(required,kwargs)):
            self.log_path = kwargs['log_path']
            self.name = kwargs['name']
            self.level = kwargs['level']
            
            if(not self.log_path[-1] == "/"):
                self.log_path += "/"
            if(not self.check_path(self.log_path)):
                self.printer("CHECK_PATH: Failed to create desired log directory, defaulting to local directory",color="red")
                self.log_path = "./"

            logger = logging.getLogger(self.name)
            logger.setLevel(self.set_level())
            
            try:
                formatter = kwargs['formatter']
            except KeyError:
                formatter = logging.Formatter('{} | %(levelname)s | %(message)s '.format(datetime.datetime.utcnow().replace(microsecond=0)))
            except Exception as e:
                self.printer("FORMATTER ERROR | {} | {}".format(type(e).__name__,e.args))

            filename = self.log_path+self.name+".log"

            fh = TimedRotatingFileHandler(filename,when='d',interval=30,backupCount=1,encoding=None,delay=False,utc=True,atTime=datetime.time(4, 0, 0))
            fh.setLevel(self.set_level())
            fh.setFormatter(formatter)
            logger.addHandler(fh)
    
            self.logger = logger

    def set_level(self):
        try:
            level = self.level.lower()
        except TypeError:
            pass
        if(level == "debug" or level == 1):
            return logging.DEBUG
        elif(level == "info" or level == 2):
            return logging.INFO
        elif(level == "warning" or level == 3):
            return logging.WARNING
        elif(level == "error" or level == 4):
            return logging.ERROR
        elif(level == "critical" or level == 5):
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
            self.printer("CHECK_PATH: {} | {}".format(type(e).__name__,e.args),color="red")
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
                else:
                    return False
            except KeyError:
                missing.append(key)

        if(missing or incorrect_type):
            self.printer('missing = {} | incorrect type = {}'.format(missing,incorrect_type),color="red")
        else:
            return True
              
    def log(self,message,level):
        #debug = green
        if(level == 1):
            self.logger.debug(message)
            if(debug): printer("DEBUG | " + self.name + " " + message,color="green")
        #info = cyan
        elif(level == 2):
            self.logger.info(message)
            printer("INFO | " + self.name + " " + message,color="cyan")
        #warning = yellow
        elif(level == 3):
            self.logger.warning(message)
            printer("WARNING | " + self.name + " " + message,color="yellow")
        #error = magenta
        elif(level == 4):
            self.logger.error(message)
            printer("ERROR | " + self.name + " " + message,color="magenta")
        #critical = red
        elif(level == 5):
            self.logger.critical(message)
            printer("CRITICAL | " + self.name + " " + message,color="red")

def test():
    a = logger(name="testLog")
    a.log("this is my message from 1",1)
    a.log("this is my message from 1",2)
    a.log("this is my message from 1",3)
    a.log("this is my message from 1",4)
    a.log("this is my message from 1",5)
    time.sleep(2)
    a.log("this is my message from 2",1)
    a.log("this is my message from 2",2)
    a.log("this is my message from 2",3)
    a.log("this is my message from 2",4)
    a.log("this is my message from 2",5)
    time.sleep(2)
    a.log("this is my message from 3",1)
    a.log("this is my message from 3",2)
    a.log("this is my message from 3",3)
    a.log("this is my message from 3",4)
    a.log("this is my message from 3",5)
    time.sleep(2)
    a.log("this is my message from 4",1)
    a.log("this is my message from 4",2)
    a.log("this is my message from 4",3)
    a.log("this is my message from 4",4)
    a.log("this is my message from 4",5)

if __name__ == '__main__':
    prnt = color_print()
    printer = color_print().p
    for color in prnt.colors:
        printer("{}".format(color),color=color)
    x = log(log_path="./hello/world/test/",name="test")

    