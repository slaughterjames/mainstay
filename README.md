mainstay

Framework to easily query the OpenAI API using pre-constructed, thorough prompting.<br>

All creadit goes to Daniel Miessler and his Fabric project - https://github.com/danielmiessler<br>

Mainstay is an implementation without the bells and whistles Fabric provides. The patterns used there can be lifted and shifted for use as prompts for Mainstay.<br>

Python libraries you'll likely need:<br>
markdown<br>
markdownify<br>
openai<br>
anthropic<br>
termcolor<br>
rich<br>

It's hardcoded to be dropped into /opt/mainstay/ although you could change this by editing mainstay.py here:<br>
    try:<br>
        #Conf file hardcoded here<br>
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:<br>
            data = json.load(read_file)<br>
    except Exception as e:<br>
        print (colored('[x] Unable to read configuration file: ' + str(e), 'red', attrs=['bold']))<br>
        return -1<br>

You'll need to edit the mainstay.conf file before use:<br>
{<br>
    "logger": "true",<br>
    "logroot": "",<br>
    "promptdir": "/opt/mainstay/prompts",<br>
    "defaultai": "chatgpt", <br>
    "defaultmodels": [<br>
        {<br>
            "openai": "gpt-4-0125-preview"<br>
        },<br>
        {<br>
            "anthropic": "claude-3-haiku-20240307"<br>
        }<br>
    ],<br>
    "apikeys": [<br>
        {<br>
            "openai": ""<br>
        },<br>
        {<br>
            "anthropic": ""<br>
        }<br>
    ]<br>
}<br>

Usage: <Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help<br>
Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize --ai chatgpt --model gpt-4-0125-preview --output /your/directory --debug<br>
Input either pipe in or use --input - What you're to ask the AI<br>
Required Arguments:<br>
--prompt - Action to be sent to OpenAI to action<br>
--ai - AI to use - chatgpt or claude<br>
Optional Arguments:<br>
--output - Choose where you wish the output to be directed<br>
--listprompts - Prints a list of available prompts.<br>
--listmodels - Prints the available LLM models to use.<br>
--viewprompt - View the content of a specified prompt.<br>
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.<br>
--help - You're looking at it!<br>

Changelog for 0.2:<br>
Added support for Anthropic's Claude3
