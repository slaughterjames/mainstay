'''
Logger v0.1 - Copyright 2025 James Slaughter,
This file is part of Logger v0.1.

Logger v0.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Logger v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Logger v0.1.  If not, see <http://www.gnu.org/license>.
'''

'''
logger.py - This file is responsible for providing a mechanism to write 
log files to the hard drive and read in the static.conf file


logger
Class: This class is responsible for providing a mechanism to write
       log files to the hard drive and read in the static.conf file
       - Uncomment commented lines in the event troubleshooting is required
        
'''

#python imports
import sys
import os
import datetime

#programmer generated imports
from fileio import fileio

class logger:
    
    '''
    Constructor
    '''
    def __init__(self):
        
        self.startdatetime = ''

    def colored (self, message, echo, bold):
        # Regular colors
        RC = "\033[0;31m"  # Red
        GC = "\033[0;32m"  # Green
        YC = "\033[0;33m"  # Yellow
        BC = "\033[0;34m"  # Blue
        WC = "\033[0;37m"  # White        
    
        # Bold colors
        BRC = "\033[1;31m"  # Bold Red
        BGC = "\033[1;32m"  # Bold Green
        BYC = "\033[1;33m"  # Bold Yellow
        BBC = "\033[1;34m"  # Bold Blue
        BWC = "\033[1;37m"  # Bold White
    
        EC = "\033[0m"     # End color

        # Choose regular or bold version of the color
        if echo == 'echoerror':
            color = BRC if bold else RC
        elif echo == 'echoinfo':
            color = BGC if bold else GC
        elif echo == 'echowarn':
            color = BYC if bold else YC
        elif echo == 'echolink':
            color = BBC if bold else BC
        elif echo == 'echowhite':  # Added white option
            color = BWC if bold else WC            
        else:
            return message

        return f"{color}{message}{EC}"    

    '''
    ReportCreate()
    Function: - Creates a new log file based on the target
              - Adds a header to the log 
    '''     
    def ReportCreate(self, logdir, targetlist):  
        logroot = logdir + 'logroot.html'
        FLog = fileio()
        
        self.startdatetime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        filename = logroot

        data = '<html>\n'
        data += '\n--------------------------------------------------------------------------------'
        data += '---------------------------------------<br/>'
        data += '<head>\n<title>'+ '</title>\n'
        data += '\n<strong>Starting Analysis On Targetlist: ' + str(targetlist) + '</strong>' + '\n' 
        data += '\n<br/><strong>Date/Time: </strong>' + self.startdatetime + '<br/>\n'
        data += '--------------------------------------------------------------------------------'
        data += '---------------------------------------<br/>\n</head>\n'
        data += '<link rel=\"stylesheet\" href=\"/opt/static/static.css\">\n<body>\n'
        FLog.WriteNewLogFile(filename, data)
   
        return 0 

    '''

    ReportFooter()
    Function: - Adds a footer to close out the log file created in the function above
              - 
              -  
    '''     
    def ReportFooter(self, logdir):  
        FLog = fileio()        
        filename = logdir + 'logroot.html'        
        data = '<strong>END OF FILE</strong><br/>'
        data += '--------------------------------------------------------------------------------'
        data += '---------------------------------------\n<br/>'
        data += 'Processed by Static v0.3\n<br/>'
        data += '--------------------------------------------------------------------------------'
        data += '---------------------------------------\n<br/>'
        data += '\n</body>\n</html>\n'
        FLog.WriteLogFile(filename, data)
        print ('\n')
        print ('[*] Report file written to: ' + filename)
           
        return 0


    '''    
    WriteReport()
    Function: - Writes to the current log file            
              - Returns to the caller
    '''    
    def WriteReport(self, logdir, newlogline):  
        FLog = fileio()
        filename = logdir + 'logroot.html'
        data = str(newlogline) #+ '\n<br/>'
        FLog.WriteLogFile(filename, data)
           
        return 0 

    '''
    LogCreate()
    Function: - Creates a new summary log file based on the target
              - Adds a header to the log                
    '''     
    def SummaryCreate(self, logdir, target):  
        logroot = logdir + 'logroot.html'
        FLog = fileio()
        
        self.startdatetime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        filename = logdir + target + '.html'
        data = '<html>\n'
        data += '\n--------------------------------------------------------------------------------'
        data += '---------------------------------------<br/>'
        data += '<head>\n<title>' + filename + '</title>\n'
        data += '\n<strong>Analysis Target: ' + target + '</strong>' + '\n' 
        data += '\n<br/><strong>Date/Time: </strong>' + self.startdatetime + '<br/>\n'
        data += '--------------------------------------------------------------------------------'
        data += '---------------------------------------<br/>\n</head>\n'
        data += '<link rel=\"stylesheet\" href=\"/opt/static/static.css\">\n<body>\n'
        FLog.WriteNewLogFile(filename, data)
           
        return 0   
    
    '''
    LogFooter()
    Function: - Adds a footer to close out the summary log file created in the function above
    '''     
    def SummaryFooter(self, logdir, target):  
        FLog = fileio()        
        filename = logdir + target + '.html'        
        data = '--------------------------------------------------------------------------------'
        data += '---------------------------------------\n<br/>'
        data += 'Processed by Static v0.3\n<br/>'
        data += '--------------------------------------------------------------------------------'
        data += '---------------------------------------\n<br/>'
        data += '\n</body>\n</html>\n'
        FLog.WriteLogFile(filename, data)
        print ('\n[*] Summary file written to: ' + filename)
           
        return 0       
   
    '''    
    WriteStrongLog()

    Function: - Writes a bolded line the current summary log file            
              - Returns to the caller
    '''    
    def WriteStrongLog(self, logdir, target, newlogline):  
        FLog = fileio()
        filename = logdir + target + '.html'
        data = '<strong>' + newlogline + '</strong>\n<br/>'
        FLog.WriteLogFile(filename, data)
           
        return 0

    '''    
    WriteSubLog()
    Function: - Writes a subsection line to the current summary log file
              - e.g. |-----------------> <Your Line>           
              - Returns to the caller
    '''    
    def WriteSubLog(self, logdir, target, newlogline):  
        FLog = fileio()
        filename = logdir + target + '.html'
        data = '|--------> ' + newlogline + '\n<br/>'
        FLog.WriteLogFile(filename, data)
           
        return 0 

    '''    
    WriteStrongSubLog()
    Function: - Writes a bolded subsection line to the current summary log file
              - e.g. |-----------------> <Your Line>           
              - Returns to the caller
    '''    
    def WriteStrongSubLog(self, logdir, target, newlogline):  
        FLog = fileio()
        filename = logdir + target + '.html'
        data = '|--------> <strong>' + newlogline + '</strong>\n<br/>'
        FLog.WriteLogFile(filename, data)
           
        return 0 

    '''    
    WriteLog()
    Function: - Writes a plain line to the current summary log file            
              - Returns to the caller
    '''    
    def WriteSummary(self, logdir, target, newlogline):  
        FLog = fileio()
        filename = logdir + target + '.html'
        data = newlogline + '\n<br/>'
        FLog.WriteLogFile(filename, data)
           
        return 0 

     
    '''    
    WriteConsoleLog()
    Function: - Writes a log of print() entries displayed on the console to the current log file            
              - Returns to the caller
    '''    
    def WriteConsoleLog(self, logdir, target, newlogline):  
        FLog = fileio()
        filename = logdir + target + '.log'
        data = newlogline + '\n'
        FLog.WriteLogFile(filename, data)
           
        return 0 
