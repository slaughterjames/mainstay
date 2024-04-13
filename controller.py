'''
Mainstay v0.2 - Copyright 2024 James Slaughter,
This file is part of Mainstay v0.2.

Mainstay v0.2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mainstay v0.2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Mainstay v0.2.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
controller.py - This file is responsible for keeping global settings available through class properties
'''

#python imports
from array import *

#programmer generated imports
#none

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
        self.defaultmodels = []#value read from the conf file.
        self.model = ''#input from the --model cmd line flag.
        self.file = ''#data you want to query.
        self.apikeys = []#list of apikeys stored centrally.
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
        self.defaultai = ''#default AI model to use to keep from using the --ai flag in every prompt
        self.prompts = []
        self.prompt = ''
        self.ai = ''
        self.input = ''
        self.pipe = ''
        self.openaiconstruct = ''