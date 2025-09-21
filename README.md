mainstay

Framework to easily query the OpenAI API, Anthropic API, or Perplexity API using pre-constructed, thorough prompting.

All credit goes to Daniel Miessler and his Fabric project - https://github.com/danielmiessler

Mainstay is an implementation without the bells and whistles Fabric provides. The patterns used there can be lifted and shifted for use as prompts for Mainstay.

Python libraries you'll likely need:
- markdown
- markdownify
- openai
- anthropic
- rich
- requests

It's hardcoded to be dropped into /opt/mainstay/ although you could change this by editing mainstay.py here:
    try:
        #Conf file hardcoded here
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            data = json.load(read_file)
    except Exception as e:
        print (colored('[x] Unable to read configuration file: ' + str(e), 'red', attrs=['bold']))
        return -1

You'll need to edit the mainstay.conf file before use. Here is an example including all supported providers:
```
{
    "logger": "true",
    "logroot": "/home/scalp/mainstaylogs",
    "promptdir": "/home/scalp/mainstay3/prompts",
    "defaultai": "chatgpt", 
    "defaultmodels": [
        {
            "openai": "gpt-4o"
        },
        {
            "perplexity": "sonar"
        },
        {
            "anthropic": "claude-3-5-haiku-20241022"
        }
    ],
    "apikeys": [
        {
            "openai": "your-openai-api-key"
        },
        {
            "perplexity": "your-perplexity-api-key"
        },
        {
            "anthropic": "your-anthropic-api-key"
        }
    ]
}
```

## What is Perplexity?
Perplexity is an AI provider, similar to OpenAI and Anthropic, that offers its own large language models (LLMs). You can use it by selecting `--ai perplexity` and providing your Perplexity API key in the config file.

## Usage
You can provide input either by piping it in or using the `--input` argument:

```
Usage: <Input for AI> | OR --input [required] --prompt [optional] --model --output --listprompts --debug --help
```

### Example (using Perplexity):
```
cat text.txt | /opt/mainstay/mainstay.py --prompt summarize --ai perplexity --model sonar-pro --output /your/directory --debug
```

### Example (using OpenAI):
```
cat text.txt | /opt/mainstay/mainstay.py --prompt summarize --ai chatgpt --model gpt-4o --output /your/directory --debug
```

### Example (using Anthropic):
```
cat text.txt | /opt/mainstay/mainstay.py --prompt summarize --ai claude --model claude-3-5-haiku-20241022 --output /your/directory --debug
```

### Arguments
- `--prompt`      : Action to be sent to the AI to perform
- `--ai`          : AI to use - `chatgpt`, `perplexity`, or `claude`
- `--model`       : (Optional) Specify the LLM model to use (see `--listmodels`)
- `--output`      : (Optional) Choose where you wish the output to be directed
- `--url`         : (Optional) The URL used for input when fetching content from web
- `--listprompts` : Prints a list of available prompts
- `--listmodels`  : Prints the available LLM models to use for the selected AI
- `--viewprompt`  : View the content of a specified prompt
- `--debug`       : Prints verbose logging to the screen to troubleshoot issues
- `--help`        : Shows usage information

## How to Add Your Perplexity API Key
In your `mainstay.conf` file, under `"apikeys"`, add your Perplexity API key like this:
```
{
    "perplexity": "your-perplexity-api-key"
}
```

## How to Choose a Model
Each provider (OpenAI, Anthropic, Perplexity) has different models. For Perplexity, you can use models like `sonar`, `sonar-pro`, etc. Use the `--model` argument to pick one. Use `--listmodels` to see available models for your selected AI.

---

If you have any questions or need help, feel free to ask!
