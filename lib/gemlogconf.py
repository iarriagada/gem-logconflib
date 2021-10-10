'''
Gemini Logs Configuration Resources
This is a collection of dictionaries, variables, filters and methods to manage
log configuration when using the Logging python module.
Author: Ignacio Arriagada, 2021
'''
import re
import os
import sys
import time
import logging
import threading
import datetime as dt
from logging.handlers import TimedRotatingFileHandler

# This dictionary holds the different levels handled by logging
log_level = {'DEBUG': logging.DEBUG,
             'INFO': logging.INFO,
             'WARNING': logging.WARNING,
             'ERROR': logging.ERROR,
             'CRITICAL': logging.CRITICAL}

# Filters used to parse a configuration file
cmnt_filt = re.compile(r'^[ ]*[^#]')
level_filt = re.compile(r'level=')

def set_log_level(config_file, logger):
    """
    Set the log verbosity level to a value read from a configuration file
    """
    # Start by setting the level to INFO. This is done in case that the value
    # read is not correct, or there's no value defined in the file.
    logger.setLevel(log_level['INFO'])
    try:
        with open(config_file, 'r') as f:
            # Read the file and filter out commented lines
            conf_raw = [l.strip() for l in f.readlines() if cmnt_filt.search(l)]
    except Exception as e:
        sys.exit(e)
    for l in conf_raw:
        # Search for "level". Continue with next iteration if not in the line
        if not(level_filt.search(l)):
            continue
        level = l.split('=')[1]
        # If "level" is in the line, check that is a valid option
        if level in log_level.keys():
            logger.setLevel(log_level[level])
            logger.info(f"Log level started as: {level}")
            break
        logger.critical(f"Bad option in {config_file}. "
                        f"Level: {level} is not valid")
        logger.critical(f"Level has been set to INFO")
        break
    else:
        # If this is reached, no "level" option was found in the file.
        logger.critical(f"Theres no level configuration in {config_file}")
        logger.critical(f"Level has beem set to INFO")

def log_level_thread(config_file, logger):
    '''
    Thread that reads the log config file and adjusts the log verbosity level.
    The file is read only if it has been modified.
    '''
    # Get conf file last modification time
    mod_time = os.path.getmtime(config_file)
    while True:
        # The loop sleeps at the beginning. This way this line doesn't have to
        # be repeated on every break and continue statetment
        time.sleep(0.25)
        try:
            # Get the current mod time
            curr_mtime = os.path.getmtime(config_file)
        except Exception as e:
            logger.error(f"Conflict while getting mod time for {config_file}")
            logger.error(e)
            logger.error("Retrying geting mod time...")
            continue
        # Compare curr mod time to previous mod time. If equal, file has not
        # been modified, continue next loop iteration
        comp_mtime = curr_mtime - mod_time
        if not(comp_mtime):
            continue
        mod_time = curr_mtime
        # If file has been modified, read it and search for "level"
        try:
            with open(config_file, 'r') as f:
                conf_raw = [l.strip() for l in f.readlines()
                            if cmnt_filt.search(l)]
        except Exception as e:
            logger.error(f"Conflict while modifying {config_file}")
            logger.error(e)
            logger.error("Retrying to set the log level...")
            continue
        # If level is found, check that is a valid option, and set it. Set the
        # level as INFO is option is invalid or if level is not defined in the
        # file.
        for l in conf_raw:
            if not(level_filt.search(l)):
                continue
            level = l.split('=')[1]
            if level in log_level.keys():
                logger.setLevel(log_level[level])
                logger.info(f"Log level changed to: {level}")
                break
            logger.critical(f"Bad option in {config_file}. "
                            f"Level: {level} is not valid")
            logger.setLevel(log_level['INFO'])
            logger.critical(f"Level has been set to INFO")
            break
        else:
            logger.critical(f"There is no level configuration in {config_file}")
            logger.setLevel(log_level['INFO'])
            logger.critical(f"Level has beem set to INFO")

def init_timertng_log(config_file, log_file, rot_hour):
    """
    Initialize a time rotating log. The parameters are:
        Configuration file (full path)
        Log file (full path)
        Rotation hour (integer 0-23)
    """
    logger = logging.getLogger(__name__)
    # Define log line tags as: Timestamp, level and message
    log_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # Log handler is timed rotating. It rotates at midnight plus the offset
    # defined by atTime
    log_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1,
                                        atTime=dt.time(hour=rot_hour))
    # Log file rotation suffix. The rotation time is added at the end of the
    # file name.
    log_handler.suffix = "%Y%m%dT%H%M%S"
    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)
    set_log_level(config_file, logger)
    # print(logger.handlers)
    # Start the dynamic log config manager thread
    log_conf_thread = threading.Thread(target=log_level_thread,
                                       kwargs={'config_file':config_file,
                                               'logger':logger},
                                       daemon=True)
    log_conf_thread.start()
    # Return logger object to be used by the application
    return logger
