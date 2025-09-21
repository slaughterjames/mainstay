#! /usr/bin/env python3
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

mainstay.py - Main entry point for Mainstay v0.4

This script serves as the main controller for the Mainstay framework. It handles argument parsing, configuration loading, and dispatches tasks to the appropriate AI provider (ChatGPT, Claude, or Perplexity). It also manages prompt listing, viewing, and output handling.

Functions:
    Usage:      Prints usage instructions for the program.
    ConfRead:   Loads configuration from the mainstay.conf file.
    parse_args: Parses command-line arguments and sets up the controller.
    ListPrompts:Lists all available prompts.
    ViewPrompt: Displays the content of a specific prompt.
    Terminate:  Exits the program cleanly.
'''

#python import
import sys
import os
import glob
import json
#import datetime
import argparse
import requests
from openai import OpenAI
from collections import defaultdict
from array import *
from rich.console import Console
from rich.markdown import Markdown

#programmer generated imports
from controller import controller
from chatgpt import chatgpt
from claude import claude
from perplexity import perplexity
from logger import logger 

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    """
    Prints usage instructions for how to run the program and what arguments are available.
    """
    print ('Usage: <Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --url --listprompts --debug --help')
    print ('Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize --ai chatgpt --model gpt-4-0125-preview --output /your/directory --debug')
    print ('Input either pipe in or use --input - What you\'re to ask the AI')
    print ('Required Arguments:')
    print ('--prompt - Action to be sent to OpenAI to action')
    print ('--ai - AI to use - chatgpt, perplexity, or claude')
    print ('Optional Arguments:')
    print ('--output - Choose where you wish the output to be directed')
    print ('--url - The URL used for input when fetching content from web')
    print ('--listprompts - Prints a list of available prompts.')
    print ('--listmodels - Prints the available LLM models to use.')
    print ('--viewprompt - View the content of a specified prompt.')
    print ('--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.')
    print ('--help - You\'re looking at it!')
    sys.exit(-1)

'''
ConfRead()
Function: - Reads in the static.conf config file and assigns some of the important
            variables
'''
def ConfRead():
    """
    Reads the mainstay.conf configuration file and loads important settings into the controller (CON).
    Returns 0 on success, -1 on failure.
    """
    
    data = ''
    temp = ''  

    try:
        #Conf file hardcoded here
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            data = json.load(read_file)
    except Exception as e:
        print (LOG.colored('[x] Unable to read configuration file: ' + str(e), 'echoerror', bold=True))
        return -1

    CON.logger = data['logger']
    CON.logroot = data['logroot']
    CON.defaultmodels = data['defaultmodels']
    CON.defaultai = data['defaultai']
    CON.apikeys = data['apikeys'] 
    CON.promptdir = data['promptdir']
  
    if (CON.debug == True):
        print ('[DEBUG] data: ', data)
        print ('[DEBUG] CON.logger: ' + str(CON.logger))
        print ('[DEBUG] CON.logroot: ' + str(CON.logroot))              
        print ('[DEBUG] CON.promptdir: ' + str(CON.promptdir))

        for a_apikeys in CON.apikeys:             
            for key, value in a_apikeys.items():
                print ('[DEBUG] CON.apikeys key: ' + key + ' value: ' + value)

        for a_defaults in CON.defaultmodels:             
            for key, value in a_defaults.items():
                print ('[DEBUG] CON.default models: ' + key + ' value: ' + value)                       

    #Load prompt collection
    for file in glob.glob(CON.promptdir + '/*'):
        temp = file.rsplit("/", 3)
        CON.prompts.append(temp[3])
        temp = ''            
            
    if (CON.debug == True):
       print ('[*] Finished configuration.')
       print ('')

    return 0
            
'''
Parse() - Parses program arguments
'''
def parse_args():        
    """
    Parses command-line arguments and sets up the controller (CON) with the provided options.
    Returns the parsed arguments object, or -1 on error.
    """

    parser = argparse.ArgumentParser(description='Process some program arguments.')

    parser.add_argument('--input', help='The text to send to the AI')
    parser.add_argument('--prompt', help='The pattern to call')
    parser.add_argument('--ai', help='chatgpt, perplexity, or claude')
    parser.add_argument('--model', help='Specify an LLM model to use, or use the default.')
    parser.add_argument('--output', help='The output location')
    parser.add_argument('--url', help='The URL used for input when fetching content from web')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--listprompts', action='store_true', help='List prompts and exit')
    parser.add_argument('--listmodels', action='store_true', help='List available LLM models to use')
    parser.add_argument('--viewprompt', action='store_true', help='View a specified prompt and exit')
    parser.add_argument('--usage', action='store_true', help='Display program usage.')

    args = parser.parse_args()

    print ('[*] Arguments: ')
 
                
    if args.usage:
        return -1                                   

    if args.input:        
        CON.input = args.input
        if (CON.debug == True):
            print ('[-] input: ', CON.input)

    if args.prompt:        
        CON.prompt = args.prompt
        print ('[-] prompt: ', CON.prompt)

    if args.ai:        
        CON.ai = args.ai
        print ('[-] ai: ', CON.ai)        

    if args.model:
        #This is an optional param and needs to be checked at read time       
        CON.model = args.model
        print ('[-] model: ', CON.model)        
            
    if args.output:
        #This is an optional param and needs to be checked at read time
        CON.output = args.output
        print ('[-] output: ', CON.output)
        if len(CON.output) < 3:
            if not (CON.output == '<>'):
                print (LOG.colored('[x] output must be a viable location.', 'echoerror', bold=True))
                print ('')
                return -1

    if args.url:
        # Store the URL used for input
        CON.url = args.url
        print ('[-] url: ', CON.url)

    if args.debug:
        CON.debug = True
        print('[-] debug: ', CON.debug)

    if args.viewprompt:
        CON.viewprompt = True
        print ('[-] viewprompt: ', str(CON.viewprompt))
        print ('')       

    if (CON.debug == True):
        print ('[DEBUG] LEN CON.input: ' + str(len(CON.input))) 
    
    if (not CON.prompt):
        #listprompts and listmodels will cause all other params to be ignored    
        if args.listprompts:
            CON.listprompts = True
            print ('[-] listprompts: ', str(CON.listprompts))
            print ('') 
        elif args.listmodels:
            CON.listmodels = True
            print ('[-] listmodels: ', str(CON.listmodels))
            print ('')               
        else:            
            print (LOG.colored('[x] prompt is a required argument.', 'echoerror', bold=True))
            return -1
        
    if (not CON.ai):
        print (LOG.colored('[-] Default AI ' + CON.defaultai + ' will be used...', 'echowarning', bold=True))
        CON.ai = CON.defaultai
        if ((CON.ai != 'chatgpt') and (CON.ai != 'claude')):           
            print (LOG.colored('[x] ai must be either \'chatgpt\' OR \'claude\'.', 'echoerror', bold=True))
            return -1         

    if ((not CON.input) and (CON.listprompts == False) and (CON.listmodels == False) and (CON.viewprompt == False)):
        while True:
            try:
                CON.pipe += input()
            except EOFError:
                # no more information
                break                
        if (CON.debug == True):
            print ('[DEBUG]: ' + CON.pipe)

        if (len(CON.pipe) < 20):
            print (LOG.colored('[x] Insufficient input has been entered! Use --input OR pipe input in from the CLI.', 'echoerror', bold=True))
            return -1
    elif ((len(CON.input) < 10) and (CON.listprompts == False) and (CON.listmodels == False) and (CON.viewprompt == False)):
        if (len(CON.pipe) < 20):
            print (LOG.colored('[x] Insufficient input has been entered! Use --input OR pipe input in from the CLI.', 'echoerror', bold=True))
            return -1
    else:
        if ((CON.listprompts == False) and (CON.listmodels == False) and (CON.viewprompt == False)):
            print (LOG.colored('[x] Something has gone wrong with the input. Try again...', 'echoerror', bold=True))
            return -1              

    return args

'''
ListPrompts()
Function: - List all available prompts and their descriptions
'''
def ListPrompts():
    """
    Prints a list of all available prompt files found in the prompt directory.
    """
    print (LOG.colored('[*] Prompt List:', 'echoinfo', bold=True))
    for prompt in CON.prompts:     
        print ('[-] ' + prompt.strip('.md'))             

    return 0

'''
ViewPrompt()
Function: - List all available prompts and their descriptions
'''
def ViewPrompt():
    """
    Displays the content of a specific prompt file in markdown format.
    """
    promptfile = ''
    markdown_string = ''
    print (LOG.colored('[*] Prompt Content: \r\n', 'echoinfo', bold=True))

    promptfile = CON.promptdir + '/' + CON.prompt + '.md'
    console = Console()

    try:
        with open(promptfile, 'r+') as read_file:            
            #data = markdown.markdown(read_file.read())
            #markdown_string = markdownify.markdownify(data)
            console.print(Markdown(read_file.read()))

    except Exception as e:
        print (LOG.colored('[x] Unable to find prompt file: ' + str(e), 'echoerror', bold=True))
        return -1

    print (markdown_string)

    return 0

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''
     
def Terminate(exitcode):
    """
    Exits the program with the provided exit code.
    """
    sys.exit(exitcode)

'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''

if __name__ == '__main__':
    
    ret = 0

    Table_Data = ()

    CON = controller()

    LOG = logger()

    CGPT = chatgpt()

    CLD = claude()

    PPLX = perplexity()
                   
    ret = parse_args()

    if (ret == -1):
        Usage()
        Terminate(ret) 

    ret = ConfRead()        

    if (ret == -1):        
        print (LOG.colored('[x] Terminated reading the configuration file...', 'echoerror', bold=True))
        Terminate(ret)

    if (not CON.model):        
        if (CON.ai == 'chatgpt'):
            for models in CON.defaultmodels: 
                for key, value in models.items():            
                    if (key == 'openai'):
                        print ('\r\n[*] Default model located!')
                        CON.model = value
        elif (CON.ai == 'perplexity'):
            for models in CON.defaultmodels: 
                for key, value in models.items():            
                    if (key == 'perplexity'):
                        print ('\r\n[*] Default model located!')
                        CON.model = value
        else:
            for models in CON.defaultmodels: 
                for key, value in models.items():                
                    if (key == 'anthropic'):
                        print ('\r\n[*] Default model located!')
                        CON.model = value

        if (CON.model == ''):            
            print (LOG.colored('[x] Something has gone wrong determining the AI model. Terminating...', 'echoerror', bold=True))
            Terminate(-1)


    if (CON.listprompts == True):
        ListPrompts()
        Terminate(0)

    if (CON.listmodels == True):
        if (CON.ai == 'chatgpt'):
            CGPT.ListModels(CON, LOG)
            Terminate(0)
        elif (CON.ai == 'perplexity'):
            PPLX.ListModels(CON, LOG)
            Terminate(0)
        else:
            CLD.ListModels(CON, LOG)
            Terminate(0)

    if (CON.viewprompt == True):        
        ViewPrompt()
        Terminate(0)            

    CON.CWP = os.getcwd()
    print ('[*] Current working directory is: ' + CON.CWP)

    #if (CON.logger.strip() == 'true'): 
    #    CON.logging = True
    #    print ('[*] Logger is active')
    #else:
    #    print ('[-] Logger not active')#    

    if (CON.ai == 'chatgpt'):
        print ('[*] Executing with ChatGPT...\r')
        CGPT.Execute(CON, LOG)
    elif (CON.ai == 'perplexity'):
        print ('[*] Executing with Perplexity...\r')
        PPLX.Execute(CON, LOG)
    else:
        print ('[*] Executing with Claude...\r')
        CLD.Execute(CON, LOG)                         

    print ('')
    print (LOG.colored('[*] Program Complete', 'echoinfo', bold=True))

    Terminate(0)
'''
END OF LINE
'''
