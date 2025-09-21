'''
Mainstay v0.4 - Copyright 2025 James Slaughter,
This file is part of Mainstay v0.4.

Mainstay v0.4 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mainstay v0.4 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Mainstay v0.4.  If not, see <http://www.gnu.org/licenses/>.
'''

"""
chatgpt.py - Handles connecting to the OpenAI API for Mainstay v0.4

This module provides functionality to list available OpenAI LLM models and to send prompts to the OpenAI API, saving the responses to a file. It is designed to be used as part of the Mainstay framework.

Classes:
    chatgpt: Handles model listing and API interaction for OpenAI.

Copyright 2025 James Slaughter. Licensed under GPL v3 or later.
"""

#python imports
import os
import json
import datetime
import requests
from openai import OpenAI
from collections import defaultdict
from array import *
from rich.console import Console
from rich.markdown import Markdown

#programmer generated imports
from controller import controller

'''
chatgpt
Class: This class is is responsible for keeping global settings available through class properties
'''
class chatgpt:
    """
    The chatgpt class provides methods to interact with the OpenAI API.
    It can list available models and execute prompts using the API.
    """
    '''
    Constructor
    '''
    def __init__(self):
        """
        Initializes the chatgpt class.
        Currently, no properties are set in the constructor.
        """
        fn = ''

    '''
    ListModels()
    Function: - List all available LLM models to use
    '''
    def ListModels(self, CON, LOG):
        """
        Lists all available OpenAI LLM models and shows the default model.

        Args:
            CON: Controller object containing configuration and state.
            LOG: Logger object for colored output.

        Returns:
            int: 0 on success, -1 on error (e.g., missing API key or failed request).
        """
        apikey = '' 
        defaultmodel = ''

        for models in CON.defaultmodels: 
            for key, value in models.items():
                if (CON.debug == True):
                    print ('[DEBUG] AI Provider: ' + str(key) + ' | Model: ' + str(value))
                if (key == 'openai'):
                    print ('\r\n[*] Default model located!')
                    defaultmodel = value 

        for apikeys in CON.apikeys: 
            for key, value in apikeys.items():
                if (CON.debug == True):
                    print ('[DEBUG] API: ' + str(key) + ' | API Key: ' + str(value))
                if (key == 'openai'):
                    print ('\r\n[*] API key located!')
                    apikey = value

        openai_url = 'https://api.openai.com/v1/models'

        print ('[*] Retrieving List...\n\r')

        session_headers = {
            "Authorization": f"Bearer {apikey}"
            }
    
        try:
            response = requests.get(openai_url, headers=session_headers)
        except Exception as e:
            print (LOG.colored('[x] OpenAI exception raised...' + str(e), 'echoerror', bold=True))
            return -1
    
        if (response.status_code == 200):
            print ('[*] Response 200 from server...\n\r')
            result = response.json()
            result = json.dumps(result, sort_keys=False, indent=4)
            result = json.loads(result)        
            if (CON.debug == True):
                print (result)
        else:
            print ('[-] OpenAI response HTTP status code: ' + str(response.status_code))
            print (LOG.colored('[-] Unable to retrieve model list...', 'echowarning', bold=True))
            return -1

        print (LOG.colored('[*] Default Model: ', 'echoinfo', bold=True) + LOG.colored(defaultmodel, 'echolink', bold=True))
    
        print (LOG.colored('\r\n[*] Model List:', 'echoinfo', bold=True))
        for model in result['data']:
            if ('gpt-' in model['id']):            
                print ('[-] ' + model['id'])   

        print ('\n\r[*] Use the \'--model\' CLI argument to use one of these. \n\r')      

        return 0

    '''
    Execute()
    Function: - Does the doing against a target
    '''
    def Execute(self, CON, LOG):
        """
        Sends a prompt to the OpenAI API and writes the response to a file.

        Args:
            CON: Controller object containing configuration, input, and state.
            LOG: Logger object for colored output.

        Returns:
            int: 0 on success, -1 on error (e.g., missing API key or prompt file).
        """
        user_input = ''
        system_input = ''
        prompt_read = ''        
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
                if (key == 'openai'):
                    print ('\r\n[*] API key located!')
                    apikey = value            

        if (apikey == ''):
            print (LOG.colored('\r\n[x] Unable to execute Mainstay - OpenAI apikey value not input.  Please add one to /opt/mainstay/mainstay.conf', 'echoerror', bold=True))
            return -1        
        else:
            os.environ["OPENAI_API_KEY"] = apikey       
            CON.openaiconstruct = OpenAI()

        console = Console()

        print ('[*] Model is: ' + CON.model + '\r\n')

        if (len(CON.input) != 0):
            user_input = {"role": "user", "content": f"{CON.input}"}
        else:
            user_input = {"role": "user", "content": f"{CON.pipe}"}

        promptfile = CON.promptdir + '/' + CON.prompt + '.md'

        try:
            with open(promptfile, "r+") as read_file:
                prompt_read = read_file.read()            
                system_input = {"role": "system", "content": prompt_read}  
        except Exception as e:
            print (LOG.colored('[x] Unable to find prompt file: ' + str(e), 'echoerror', bold=True))
            return -1   
    
        sendpackage = [system_input, user_input]

        if (CON.debug == True):
            print ('[DEBUG] sendpackage: ' + sendpackage)    

        try:
            response = CON.openaiconstruct.chat.completions.create(
            model=CON.model,
            messages=sendpackage,
            temperature=0.0,
            top_p=1,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            )
            print (LOG.colored('[*] Prompt response...\r\n', 'echoinfo', bold=True))
            console.print(Markdown(response.choices[0].message.content))        
        except Exception as e:
            print (LOG.colored('[x] Unable to complete task: ' + str(e), 'echoerror', bold=True))
            return -1

        try:
            with open(output, "w") as write_file:
                # Write header lines
                write_file.write("\n")  # Blank line
                write_file.write(f"URL: {CON.url}\n")  # URL line - populated with actual URL if available
                write_file.write("TAGS: \n")  # Tags line
                write_file.write("\n")  # Another blank line
                # Write the actual content
                write_file.write(response.choices[0].message.content)
            print (LOG.colored('\r\n[*] Prompt response has been written to file here: ', 'echoinfo', bold=True) + LOG.colored(output, 'echolink', bold=True))
        except Exception as e:
            print (LOG.colored('[x] Unable to complete task: ' + str(e), 'echoerror', bold=True))
            return -1

        return 0
