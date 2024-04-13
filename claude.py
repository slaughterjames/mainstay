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
claude.py - This file is responsible for connecting to the Anthropic API
'''

#python imports
import os
import datetime
#import markdown
#import markdownify
#from anthropic import Anthropic
import anthropic
from collections import defaultdict
from array import *
from termcolor import colored
from rich.console import Console
from rich.markdown import Markdown

#programmer generated imports
from controller import controller

'''
claude
Class: This class is is responsible for keeping global settings available through class properties
'''
class claude:
    '''
    Constructor
    '''
    def __init__(self):
        fn = ''

    '''
    ListModels()
    Function: - List all available LLM models to use
    '''
    def ListModels(self, CON):
        
        defaultmodel = ''
        anthropicmodels = ['claude-3-opus-20240229',
                      'claude-3-sonnet-20240229',
                      'claude-3-haiku-20240307',
                      'claude-2.1']

        for models in CON.defaultmodels: 
            for key, value in models.items():
                if (CON.debug == True):
                    print ('[DEBUG] AI Provider: ' + str(key) + ' | Model: ' + str(value))
                if (key == 'anthropic'):
                    print ('\r\n[*] Default model located!')
                    defaultmodel = value 

        print (colored('[*] Default Model: ', 'green', attrs=['bold']) + colored(defaultmodel, 'blue', attrs=['bold']))
    
        print (colored('\r\n[*] Model List:', 'green', attrs=['bold']))
        for model in anthropicmodels:                    
            print ('[-] ' + model)

        print ('\n\r[-] Anthropic AI model updates are maintained at: https://docs.anthropic.com/claude/docs/models-overview \n\r')   

        print ('\n\r[*] Use the \'--model\' CLI argument to use one of these. \n\r')      

        return 0
    
    '''
    Execute()
    Function: - Does the doing against a target
    '''
    def Execute(self, CON):

        user_input = ''
        system_input = ''
        promptfile = ''
        sendpackage = []
        current_dateTime = datetime.date.today()
        apikey = ''
        output = ''

        if (len(CON.output) != 0):
            output = CON.output
        else:
            output = CON.logroot + '/' + str(current_dateTime) + '.md'

        for apikeys in CON.apikeys: 
            for key, value in apikeys.items():
                if (CON.debug == True):
                    print ('[DEBUG] API: ' + str(key) + ' | API Key: ' + str(value))
                if (key == 'anthropic'):
                    print ('\r\n[*] API key located!')
                    apikey = value         

        if (apikey == ''):
            print (colored('\r\n[x] Unable to execute Mainstay - Anthropic apikey value not input.  Please add one to /opt/mainstay/mainstay.conf', 'red', attrs=['bold']))
            return -1        
        else:
            os.environ["ANTHROPIC_API_KEY"] = apikey            
            client = anthropic.Anthropic(api_key=apikey,)
            
        console = Console()

        print ('[*] Model is: ' + CON.model + '\r\n')

        if (len(CON.input) != 0):
            user_input = {"role": "user", "content": f"{CON.input}"}
        else:
            user_input = {"role": "user", "content": f"{CON.pipe}"}

        promptfile = CON.promptdir + '/' + CON.prompt + '.md'

        try:
            with open(promptfile, "r+") as read_file:
                system_input = read_file.read()            
        except Exception as e:
            print (colored('[x] Unable to find prompt file: ' + str(e), 'red', attrs=['bold']))
            return -1 

        sendpackage = [system_input, user_input]

        if (CON.debug == True):
            print ('[DEBUG] sendpackage: ' + str(sendpackage))

        try:            
            response = client.messages.create(
            model=CON.model,
            max_tokens=4096,
            system=system_input,            
            messages=[user_input],            
            temperature=1.0,
            top_p=1,
            )
            print (colored('[*] Prompt response...\r\n', 'green', attrs=['bold']))                        
            console.print(Markdown(response.content[0].text))        
        except Exception as e:
            print (colored('[x] Unable to complete task: ' + str(e), 'red', attrs=['bold']))
            return -1

        try:
            with open(output, "w") as write_file:                
                write_file.write(response.content[0].text)
            print (colored('\r\n[*] Prompt response has been written to file here: ', 'green', attrs=['bold']) + colored(output, 'blue', attrs=['bold']))
        except Exception as e:
            print (colored('[x] Unable to complete task: ' + str(e), 'red', attrs=['bold']))
            return -1            

        return 0                    