# mainstay

Framework to easily query the OpenAI API using pre-constructed, thorough prompting.

All creadit goes to Daniel Miessler and his Fabric project - https://github.com/danielmiessler

Mainstay is an implementation without the bells and whistles Fabric provides.  The patterns used there can be lifted and shifted for use as prompts for Mainstay.

Python libraries you'll likely need:
markdown
markdownify
openai
termcolor
rich

You'll need to edit the mainstay.conf file before use:
{\n
    "logger": "true",\n
    "logroot": "<Your preferred output location>",\n
    "promptdir": "/opt/mainstay/prompts", \n
    "defaultmodel": "gpt-4-0125-preview",\n
    "apikey": "<Your OpenAI API Key>"\n
}\n

Usage: <Pipe Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help\n
Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize  --model gpt-4-0125-preview --output /your/directory --debug\n
Input either pipe in or use --input - What you're to ask the AI\n
Required Arguments:\n
--prompt - Action to be sent to OpenAI to action\n
Optional Arguments:\n
--output - Choose where you wish the output to be directed\n
--listprompts - Prints a list of available prompts.\n
--listmodels - Prints the available LLM models to use.\n
--viewprompt - View the content of a specified prompt.\n
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.\n
--help - You're looking at it!
