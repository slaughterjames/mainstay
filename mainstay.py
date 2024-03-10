#! /usr/bin/env python3
'''
Mainstay v0.1 - Copyright 2024 James Slaughter,
This file is part of Mainstay v0.1.

Mainstay v0.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Mainstay v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Mainstay v0.1.  If not, see <http://www.gnu.org/licenses/>.
'''

#python import
import sys
import os
import glob
import json
import datetime
import argparse
import requests
import markdown
import markdownify
from openai import OpenAI
from collections import defaultdict
from array import *
from termcolor import colored
from rich.console import Console
from rich.markdown import Markdown

#programmer generated imports
from controller import controller
#from logger import logger 

'''
Usage()
Function: Display the usage parameters when called
'''
def Usage():
    print ('Usage: <Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help')
    print ('Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize  --model gpt-4-0125-preview --output /your/directory --debug')
    print ('Input either pipe in or use --input - What you\'re to ask the AI')
    print ('Required Arguments:')
    print ('--prompt - Action to be sent to OpenAI to action')
    print ('Optional Arguments:')
    print ('--output - Choose where you wish the output to be directed')
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
    
    data = ''
    temp = ''  

    try:
        #Conf file hardcoded here
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            data = json.load(read_file)
    except Exception as e:
        print (colored('[x] Unable to read configuration file: ' + str(e), 'red', attrs=['bold']))
        return -1

    CON.logger = data['logger']
    CON.logroot = data['logroot']
    CON.defaultmodel = data['defaultmodel']
    CON.apikey = data['apikey']    
    CON.promptdir = data['promptdir']
  
    if (CON.debug == True):
        print ('[DEBUG] data: ', data)
        print ('[DEBUG] CON.logger: ' + str(CON.logger))
        print ('[DEBUG] CON.logroot: ' + str(CON.logroot))
        print ('[DEBUG] CON.defaultmodel: ' + str(CON.defaultmodel))
        print ('[DEBUG] CON.apikey: ' + str(CON.apikey))
        print ('[DEBUG] CON.promptdir: ' + str(CON.promptdir))

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

    parser = argparse.ArgumentParser(description='Process some program arguments.')

    parser.add_argument('--input', help='The text to send to the AI')
    parser.add_argument('--prompt', help='The pattern to call')
    parser.add_argument('--model', help='Specify an LLM model to use, or use the default.')
    parser.add_argument('--output', help='The output location')
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
                print (colored('[x] output must be a viable location.', 'red', attrs=['bold']))
                print ('')
                return -1

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
            print (colored('[x] prompt is a required argument.', 'red', attrs=['bold']))
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
            print (colored('[x] Insufficient input has been entered! Use --input OR pipe input in from the CLI.', 'red', attrs=['bold']))
            return -1
    elif ((len(CON.input) < 10) and (CON.listprompts == False) and (CON.listmodels == False) and (CON.viewprompt == False)):
        if (len(CON.pipe) < 20):
            print (colored('[x] Insufficient input has been entered! Use --input OR pipe input in from the CLI.', 'red', attrs=['bold']))
            return -1
    else:
        if ((CON.listprompts == False) and (CON.listmodels == False) and (CON.viewprompt == False)):
            print (colored('[x] Something has gone wrong with the input. Try again...', 'red', attrs=['bold']))
            return -1              

    return args

'''
ListModels()
Function: - List all available LLM models to use
'''
def ListModels():

    openai_url = 'https://api.openai.com/v1/models'

    print ('[*] Retrieving List...\n\r')

    session_headers = {
            "Authorization": f"Bearer {CON.apikey}"
        }
    
    try:
        response = requests.get(openai_url, headers=session_headers)
    except Exception as e:
        print (colored('[x] OpenAI exception raised...' + str(e), 'red', attrs=['bold']))
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
        print (colored('[-] Unable to retrieve model list...', 'yellow', attrs=['bold']))
        return -1

    print (colored('[*] Default Model: ', 'green', attrs=['bold']) + colored(CON.defaultmodel, 'blue', attrs=['bold']))
    
    print (colored('\r\n[*] Model List:', 'green', attrs=['bold']))
    for model in result['data']:
        if ('gpt-' in model['id']):            
            print ('[-] ' + model['id'])   

    print ('\n\r[*] Use the \'--model\' CLI argument to use one of these. \n\r')      

    return 0


'''
ListPrompts()
Function: - List all available prompts and their descriptions
'''
def ListPrompts():
    
    print (colored('[*] Prompt List:', 'green', attrs=['bold']))
    for prompt in CON.prompts:     
        print ('[-] ' + prompt.strip('.md'))             

    return 0

'''
ViewPrompt()
Function: - List all available prompts and their descriptions
'''
def ViewPrompt():
    promptfile = ''
    markdown_string = ''
    print (colored('[*] Prompt Content: \r\n', 'green', attrs=['bold']))

    promptfile = CON.promptdir + '/' + CON.prompt + '.md'
    console = Console()

    try:
        with open(promptfile, 'r+') as read_file:            
            #data = markdown.markdown(read_file.read())
            #markdown_string = markdownify.markdownify(data)
            console.print(Markdown(read_file.read()))

    except Exception as e:
        print (colored('[x] Unable to find prompt file: ' + str(e), 'red', attrs=['bold']))
        return -1

    print (markdown_string)

    return 0


'''
Execute()
Function: - Does the doing against a target
'''
def Execute():

    user_input = ''
    system_input = ''
    prompt_read = ''
    data = ''
    promptfile = ''
    sendpackage = []
    current_dateTime = datetime.date.today()
    output = ''
    if (len(CON.output) != 0):
        output = CON.output
    else:
        output = CON.logroot + '/' + str(current_dateTime) + '.md'

    if (CON.apikey == ''):
        print (colored('\r\n[x] Unable to execute Mainstay - OpenAI apikey value not input.  Please add one to /opt/mainstay/mainstay.conf', 'red', attrs=['bold']))
        return -1        
    else:
        print ('[*] API key located!')
        if (CON.debug == True):
            print ('[DEBUG] API Key: ' + CON.apikey) 
        os.environ["OPENAI_API_KEY"] = CON.apikey       
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
        print (colored('[x] Unable to find prompt file: ' + str(e), 'red', attrs=['bold']))
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
        print (colored('[*] Prompt response...\r\n', 'green', attrs=['bold']))
        console.print(Markdown(response.choices[0].message.content))        
    except Exception as e:
        print (colored('[x] Unable to complete task: ' + str(e), 'red', attrs=['bold']))
        return -1

    try:
        with open(output, "w") as write_file:
            write_file.write(response.choices[0].message.content)
        print (colored('\r\n[*] Prompt response has been written to file here: ', 'green', attrs=['bold']) + colored(output, 'blue', attrs=['bold']))
    except Exception as e:
        print (colored('[x] Unable to complete task: ' + str(e), 'red', attrs=['bold']))
        return -1

    return 0

'''
Terminate()
Function: - Attempts to exit the program cleanly when called  
'''
     
def Terminate(exitcode):
    sys.exit(exitcode)

'''
This is the mainline section of the program and makes calls to the 
various other sections of the code
'''

if __name__ == '__main__':
    
    ret = 0

    Table_Data = ()

    CON = controller()
                   
    ret = parse_args()

    if (ret == -1):
        Usage()
        Terminate(ret) 

    ret = ConfRead()        

    if (ret == -1):
        print ('[x] Terminated reading the configuration file...')
        Terminate(ret)

    if (not CON.model):
        CON.model = CON.defaultmodel

    if (CON.listprompts == True):
        ListPrompts()
        Terminate(0)

    if (CON.listmodels == True):
        ListModels()
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

    print ('[*] Executing...\r')

    Execute()                

    print ('')
    print (colored('[*] Program Complete', 'green', attrs=['bold']))

    Terminate(0)
'''
END OF LINE
'''
