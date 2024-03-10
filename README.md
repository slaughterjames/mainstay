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
{
    "logger": "true",
    "logroot": "<Your preferred output location>",
    "promptdir": "/opt/mainstay/prompts", 
    "defaultmodel": "gpt-4-0125-preview",
    "apikey": "<Your OpenAI API Key>"
}


Usage: <Pipe Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help
Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize  --model gpt-4-0125-preview --output /your/directory --debug
Input either pipe in or use --input - What you're to ask the AI
Required Arguments:
--prompt - Action to be sent to OpenAI to action
Optional Arguments:
--output - Choose where you wish the output to be directed
--listprompts - Prints a list of available prompts.
--listmodels - Prints the available LLM models to use.
--viewprompt - View the content of a specified prompt.
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.
--help - You're looking at it!
