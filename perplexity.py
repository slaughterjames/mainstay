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
perplexity.py - Handles connecting to the Perplexity API for Mainstay v0.4

This module provides functionality to list available Perplexity LLM models and to send prompts to the Perplexity API, saving the responses to a file. It is designed to be used as part of the Mainstay framework.

Classes:
    perplexity: Handles model listing and API interaction for Perplexity.

Copyright 2025 James Slaughter. Licensed under GPL v3 or later.
"""

#python imports
import os
import sys
import json
import datetime
import requests
from io import StringIO
from collections import defaultdict
from array import *
from rich.console import Console
from rich.markdown import Markdown

#programmer generated imports
from logger import logger
from controller import controller


'''
perplexity
Class: This class is is responsible for keeping global settings available through class properties
'''
class perplexity:
    """
    The perplexity class provides methods to interact with the Perplexity AI API.
    It can list available models and execute prompts using the API.
    """
    '''
    Constructor
    '''
    def __init__(self):
        """
        Initializes the perplexity class.
        Currently, no properties are set in the constructor.
        """
        fn = ''

    '''
    ListModels()
    Function: - List all available LLM models to use
    '''
    def ListModels(self, CON, LOG):
        """
        Lists all available Perplexity LLM models and shows the default model.

        Args:
            CON: Controller object containing configuration and state.
            LOG: Logger object for colored output.

        Returns:
            int: 0 on success.
        """
        defaultmodel = ''
        perplexitymodels = ['Sonar',
                      'Sonar Pro',
                      'Sonar Reasoning',
                      'Sonar Reasoning Pro',
                      'Sonar Deep Research']

        for models in CON.defaultmodels: 
            for key, value in models.items():
                if (CON.debug == True):
                    print ('[DEBUG] AI Provider: ' + str(key) + ' | Model: ' + str(value))
                if (key == 'perplexity'):
                    print ('\r\n[*] Default model located!')
                    defaultmodel = value 

        print (LOG.colored('[*] Default Model: ', 'echoinfo', bold=True) + LOG.colored(defaultmodel, 'echolink', bold=True))
    
        print (LOG.colored('\r\n[*] Model List:', 'echoinfo', bold=True))
        for model in perplexitymodels:                    
            print ('[-] ' + model)

        print ('\n\r[-] Perplexity AI model updates are maintained at: https://docs.perplexity.ai/guides/pricing \n\r')   

        print ('\n\r[*] Use the \'--model\' CLI argument to use one of these. \n\r')      

        return 0

    '''
    Execute()
    Function: - Does the doing against a target
    '''
    def Execute(self, CON, LOG):
        """
        Sends a prompt to the Perplexity API and writes the response to a file.

        Args:
            CON: Controller object containing configuration, input, and state.
            LOG: Logger object for colored output.

        Returns:
            int: 0 on success, -1 on error (e.g., missing API key or prompt file).
        """
        # Initialize variables
        system_input = ''
        prompt_read = ''        
        promptfile = ''
        data = ''
        current_dateTime = datetime.date.today()
        apikey = ''
        output = ''      

        # Determine output file path
        if (len(CON.output) != 0):
            output = CON.output
        else:
            output = CON.logroot + '/' + str(current_dateTime) + '.md'

        # Find the Perplexity API key in the config
        for apikeys in CON.apikeys: 
            for key, value in apikeys.items():
                if (CON.debug == True):
                    print ('[DEBUG] API: ' + str(key) + ' | API Key: ' + str(value))
                if (key == 'perplexity'):
                    print ('\r\n[*] API key located!')
                    apikey = value            

        if (apikey == ''):
            # API key is required
            print (LOG.colored('\r\n[x] Unable to execute Mainstay - Perplexity apikey value not input.  Please add one to /opt/mainstay/mainstay.conf', 'echoerror', bold=True))
            return -1
        else:
            # Set API key as environment variable
            os.environ["PERPLEXITY_API_KEY"] = apikey                        

        console = Console()

        print ('[*] Model is: ' + CON.model + '\r\n')

        # Build the prompt file path
        promptfile = CON.promptdir + '/' + CON.prompt + '.md'

        # Read the prompt file
        try:
            with open(promptfile, "r+") as read_file:
                prompt_read = read_file.read()            
        except Exception as e:
            print (LOG.colored('[x] Unable to find prompt file: ' + str(e), 'echoerror', bold=True))
            return -1   

        url = "https://api.perplexity.ai/chat/completions"

        # Prepare the payload for the API request
        if (len(CON.input) != 0):
            payload = {
                "model": CON.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": prompt_read
                    },
                    {
                        "role": "user", 
                        "content": f"{CON.input}"
                    }
                ]
            }
            headers = {
                "Authorization": "Bearer " + apikey,
                "Content-Type": "application/json"
            }
        else:
            payload = {
                "model": CON.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": prompt_read
                    },
                    {
                        "role": "user", 
                        "content": f"{CON.pipe}"
                    }
                ]
            }
            headers = {
                "Authorization": "Bearer " + apikey,
                "Content-Type": "application/json"
            }

        # Send the request to the Perplexity API
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            print (LOG.colored('[*] Prompt response...\r\n', 'echoinfo', bold=True))        
        except Exception as e:
            print (LOG.colored('[x] Unable to complete task: ' + str(e), 'echoerror', bold=True))
            return -1
        
        # Parse the response JSON
        data = json.loads(response.text)

        if (CON.debug == True):
            print(json.dumps(data, indent=4))    

        # Write the response and citations to the output file
        try:          
            with open(output, "w", encoding='utf-8') as write_file:
                # Write header lines
                write_file.write("\n")  # Blank line
                write_file.write(f"URL: {CON.url}\n")  # URL line - populated with actual URL if available
                write_file.write("TAGS: \n")  # Tags line
                write_file.write("\n")  # Another blank line
                # Write citations
                for citation in data['citations']:
                    console.print(Markdown(citation))
                    write_file.write(citation + '\n')
                write_file.write("\n")  # Blank line
                console.print(Markdown(data['choices'][0]['message']['content']))
                write_file.write(data['choices'][0]['message']['content'] + '\n')                
                
            print (LOG.colored('\r\n[*] Prompt response has been written to file here: ', 'echoinfo', bold=True) + LOG.colored(output, 'echolink', bold=True))
        except Exception as e:
            print (LOG.colored('[x] Unable to complete task: ' + str(e), 'echoerror', bold=True))
            return -1

        return 0