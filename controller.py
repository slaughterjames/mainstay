'''
Mainstay v0.1
'''

'''
controller.py - This file is responsible for keeping global settings available through class properties
'''

#python imports
import imp
import sys
from array import *

#programmer generated imports
#from logger import logger

'''
controller
Class: This class is is responsible for keeping global settings available through class properties
'''
class controller:
    '''
    Constructor
    '''
    def __init__(self):

        self.debug = False#Boolean value, if set to true, debug lines will print to the console.
        self.defaultmodel = ''#value read from the conf file.
        self.model = ''#input from the --model cmd line flag.
        self.file = ''#data you want to query.
        self.apikey = ''#list of apikeys stored centrally.
        self.history = ''#conversational history file
        self.conversational_history = []
        self.template = ''#The custom template to prompt the LLM
        self.template_text = ''
        self.questions = ''#File containing questions you want to ask the data
        self.questions_list = []
        self.output = ''#input from the --output cmd line flag.
        self.logroot = ''#Directory name read from the config file "logroot" line.  Root directory for all logs.
        self.CWP = ''#Current working directory. 
        self.logdir = ''#Full log path where program output will be deposited.
        self.logger = ''#Boolean value read from the config file "logger" line.
        self.logging = False#Boolean value when True allows logging output.
        self.listprompts = False#Boolean input from the --listprompts cmd line flag
        self.listmodels = False#Boolean input from the --listmodels cmd line flag
        self.viewprompt = False#Boolean input from the --viewprompts cmd line flag
        self.promptdir = ''#Location of all promptfiles
        self.prompts = []
        self.prompt = ''
        self.input = ''
        self.pipe = ''
        self.openaiconstruct = ''
