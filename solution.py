#!usr/bin/python
import json
import subprocess
import os



import sys
import logging

cmd = []
#verbose is set or not
verbose = False
number_of_commands = 0;


#for persistence reading
#config_file = '/tmp/db.json'
#with open(config_file, 'r') as f:
#    config = json.load(f)

#Formate Specifiers are stored by default. 
FormatUpdtDone = False
#Default log formate
log_format = '%(asctime)s *prefix* %(message)s'
#default date formate
log_date_format = '%m/%d/%Y %I:%M:%S %p' 


#Read cmdLineInput line argument as one full string then split and read different parts.
if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print "************************************************************************************"
        print "Command Usage :"
        print "docker run your_solution:final <entry-point-options> -- <command> [command-args...]" 
        print "************************************************************************************"
        sys.exit(1)
    else:
        cmdLineInput = sys.argv



# Entry point options should come first and then the command. Below code logic make sure that Entry point options are parsed before the command.
length = 1
for i in range(1, len(cmdLineInput)):
#read each word and parse the values meaningfully
    if number_of_commands ==0 and (cmdLineInput[i] == "-v" or cmdLineInput[i] == "--verbose"):
         verbose = True
    if cmdLineInput[i] == "--log-format":
         log_format = cmdLineInput[i+1]
         formatUpdate = True
    if cmdLineInput[i] == "--log-date-format":
         log_date_format = cmdLineInput[i+1]
         FormatUpdtDone = True
    if cmdLineInput[i] == "--":
        i = i + 1
        length = i
        for i in range(length, len(cmdLineInput)):
            number_of_commands+=1;
            cmd.append(cmdLineInput[i])


#Logging code.
logger = logging.getLogger("logging")
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format,  log_date_format)
stream.setFormatter(formatter)
logger.addHandler(stream)


def execute_command(cmd):
    
    stderror_in_bytes = 0
    stdout_in_bytes = 0
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # This should ideally be a Data Base like redis
    #with open(config_file, 'w') as db:
     #   db.write(json.dumps(config))
   
    logger.debug("Going to run command:" + str(cmd) +'\n') 
    
    stderror = proc.stderr.readlines()
    stdoutput = proc.stdout.readlines()
    
    for error in stderror:
        stderror_in_bytes += len(error); 
    
    for out in stdoutput:
        stdout_in_bytes += len(out); 
       
    #Hold the process to take returncode
    proc.communicate()[0]
    
    logger.debug("Command exit code:" + str(proc.returncode) + '\n')
    logger.debug("Produced " +str(stderror_in_bytes) +" bytes of stderr:" +'\n')
    
    for line in stderror:
        logger.debug(line)

    logger.debug("Produced " +str(stdout_in_bytes) +" bytes of stdout:" +'\n')
    for line in stdoutput:
        logger.debug(line)

#Execute the command only if the verbose is set and cmd is not null
if(verbose):
    if(cmd == []):
        print "************************************************************************************"
        print "Command Usage :"
        print "docker run your_solution:final <entry-point-options> -- <command> [command-args...]"
        print "************************************************************************************"
    else:
        execute_command(cmd)

sys.stdout.flush()


