# Overview
## Description
* Logging can be a little daunting. This makes things a little easier.
## Features
* Simple logger set up
* Automatically print log levels to terminal in color for easier debugging
* Promotes logging DURING development, not after! Reduce your tech debt.

# Log Levels
* 1 = DEBUG (green)
* 2 = INFO (cyan)
* 3 = WARNING (yellow)
* 4 = ERROR (magenta)
* 5 = CRITICAL (red)

# Syntax
```python
from logg3r import Log

#initialize logger
#OPTIONAL! this initializes the file handler format, it defaults to a simple TIME | LEVEL | MESSAGE format
#formatter='{} | %(levelname)s | %(message)s '.format(datetime.datetime.utcnow().replace(microsecond=0))
#rotation=filename,when='d',interval=30,backupCount=1,encoding=None,delay=False,utc=True,atTime=datetime.time(4, 0, 0)

logger = Log(log_path="./path/to/logs/",	#REQUIRED: sets the path of the log file
			#REQUIRED: sets the name of the log file
			name="test_log",				
			#REQUIRED: sets log level to be stored in file and printed to console
			level=1	
			#OPTIONAL: defaults to above format, any valid logger format is accepted
			#,formatter=formatter,
			#OPTIONAL: defaults to 30 days of retention with (1) log overflow file (log.1)
			#rotation=rotation
			)				

logger.log("test DEBUG message",1)
logger.log("test INFO message",2)
logger.log("test WARNING message",3)
logger.log("test ERROR message",4)
logger.log("test CRITICAL message",5)
```

# References
* https://docs.python.org/3.8/library/logging.handlers.html#timedrotatingfilehandler