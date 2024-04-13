mainstay

Framework to easily query the OpenAI API using pre-constructed, thorough prompting.

All creadit goes to Daniel Miessler and his Fabric project - https://github.com/danielmiessler

Mainstay is an implementation without the bells and whistles Fabric provides. The patterns used there can be lifted and shifted for use as prompts for Mainstay.

Python libraries you'll likely need:
markdown
markdownify
openai
anthropic
termcolor
rich

It's hardcoded to be dropped into /opt/mainstay/ although you could change this by editing mainstay.py here:
    try:
        #Conf file hardcoded here
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            data = json.load(read_file)
    except Exception as e:
        print (colored('[x] Unable to read configuration file: ' + str(e), 'red', attrs=['bold']))
        return -1

You'll need to edit the mainstay.conf file before use:
{
    "logger": "true",
    "logroot": "",
    "promptdir": "/opt/mainstay/prompts",
    "defaultai": "chatgpt", 
    "defaultmodels": [
        {
            "openai": "gpt-4-0125-preview"
        },
        {
            "anthropic": "claude-3-haiku-20240307"
        }
    ],
    "apikeys": [
        {
            "openai": ""
        },
        {
            "anthropic": ""
        }
    ]
}

Usage: <Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help
Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize --ai chatgpt --model gpt-4-0125-preview --output /your/directory --debug
Input either pipe in or use --input - What you're to ask the AI
Required Arguments:
--prompt - Action to be sent to OpenAI to action
--ai - AI to use - chatgpt or claude
Optional Arguments:
--output - Choose where you wish the output to be directed
--listprompts - Prints a list of available prompts.
--listmodels - Prints the available LLM models to use.
--viewprompt - View the content of a specified prompt.
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.
--help - You're looking at it!
