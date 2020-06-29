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
        required = {"log_path":str,"name":str}
        if(self.parse_kwargs(required,kwargs)):
            self.name = kwargs['name']
            self.log_path = kwargs['log_path']
            if(not self.log_path[-1] == "/"):
                self.log_path += "/"
            if(not self.check_path(self.log_path))
                self.printer("CHECK_PATH: Failed to create desired log directory, defaulting to local directory",color="red")
                self.log_path = "./"

            logger = logging.getLogger(self.name)
            logger.setLevel(logging.DEBUG)
            try:
                formatter = kwargs['formatter']
            except KeyError:
                formatter = logging.Formatter('{} | %(levelname)s | %(message)s '.format(datetime.datetime.utcnow().replace(microsecond=0)))
            except Exception as e:
                self.printer("FORMATTER ERROR | {} | {}".format(type(e).__name__,e.args))
            filename = self.log_path+self.name+".log"

            
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
                if(not isinstance(kwargs[key],val)):
                    incorrect_type.append(key)
            except KeyError:
                missing.append(key)

        error = ""
        if(missing or incorrect_type):
            self.printer('missing = {} | incorrect type = {}'.format(missing,incorrect_type),color="red")
        else:
            return True


if __name__ == '__main__':
    prnt = color_print()
    printer = color_print().p
    for color in prnt.colors:
        printer("{}".format(color),color=color)
    x = log(log_path="./hello/world/test/",name="test")

    