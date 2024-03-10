# mainstay

Framework to easily query the OpenAI API using pre-constructed, thorough prompting.

All creadit goes to Daniel Miessler and his Fabric project - https://github.com/danielmiessler

Mainstay is an implementation without the bells and whistles Fabric provides.  The patterns used there can be lifted and shifted for use as prompts for Mainstay.

Python libraries you'll likely need:<br/>
markdown<br/>
markdownify<br/>
openai<br/>
termcolor<br/>
rich<br/>

You'll need to edit the mainstay.conf file before use:<br/><br/>
{<br/><br/>
    "logger": "true",<br/><br/>
    "logroot": "<Your preferred output location>",<br/><br/>
    "promptdir": "/opt/mainstay/prompts", <br/><br/>
    "defaultmodel": "gpt-4-0125-preview",<br/><br/>
    "apikey": "<Your OpenAI API Key>"<br/><br/>
}<br/><br/>

Usage: <Pipe Input for OpenAI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help<br/><br/>
Example: cat text.txt | /opt/mainstay/mainstay.py --prompt summerize  --model gpt-4-0125-preview --output /your/directory --debug<br/><br/>
Input either pipe in or use --input - What you're to ask the AI<br/><br/>
Required Arguments:<br/><br/>
--prompt - Action to be sent to OpenAI to action<br/><br/>
Optional Arguments:<br/><br/>
--output - Choose where you wish the output to be directed<br/><br/>
--listprompts - Prints a list of available prompts.<br/><br/>
--listmodels - Prints the available LLM models to use.<br/><br/>
--viewprompt - View the content of a specified prompt.<br/><br/>
--debug - Prints verbose logging to the screen to troubleshoot issues with a recon installation.<br/><br/>
--help - You're looking at it!<br/><br/>
