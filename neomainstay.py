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
'''

"""
neomainstay.py - Flask Web Interface for Mainstay v0.4

This module provides a web-based interface for the Mainstay framework using Flask. It allows users to submit prompts, select AI models, and save results to files through a browser. The backend handles validation, runs the mainstay engine, and manages prompt/model selection.

Key Features:
    - Web form for submitting input and selecting prompts/models
    - Validates output paths and filenames
    - Runs the mainstay engine and saves results
    - Lists available prompts and models
    - Views prompt content

Copyright 2025 James Slaughter. Licensed under GPL v3 or later.
"""

from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json
import shlex
import requests
from urllib.parse import urlparse
from termcolor import colored

app = Flask(__name__)

# Load configuration
def load_config():
    """
    Loads the configuration file for Mainstay.
    Returns:
        dict: Configuration data if successful, None otherwise.
    """
    try:
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            return json.load(read_file)
    except Exception as e:
        print(colored(f'[x] Unable to read configuration file: {str(e)}', 'red', attrs=['bold']))
        return None

config = load_config()

def fetch_url_content(url):
    """
    Fetches content from a URL using requests library.
    Args:
        url (str): The URL to fetch content from.
    Returns:
        tuple: (content, error_message) - content is the fetched text or None if error
    """
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return None, "Invalid URL format. Please include http:// or https://"
        
        # Set headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the URL with timeout
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Check if content is text-based
        content_type = response.headers.get('content-type', '').lower()
        if 'text' not in content_type and 'html' not in content_type:
            return None, f"URL content is not text-based (content-type: {content_type})"
        
        # Return the text content
        return response.text, None
        
    except requests.exceptions.Timeout:
        return None, "Request timed out. The URL took too long to respond."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Could not reach the URL."
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP error: {e.response.status_code} - {e.response.reason}"
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route for the web interface. Handles GET (show form) and POST (process form) requests.
    On POST, validates input, runs mainstay, and returns results as JSON.
    On GET, renders the main form.
    """
    if request.method == 'POST':
        try:
            # Debug: Print all form data
            print("Form data received:", request.form)
            print("Form files:", request.files)
            
            # Get all form data with default values
            pasted_input = request.form.get('pastedInput', '')
            url_input = request.form.get('urlInput', '')
            use_url = request.form.get('use_url') == 'true'
            prompts = request.form.getlist('prompt')
            ai = request.form.get('ai', '')
            model = request.form.get('model', '')
            output_path = request.form.get('output', '')  # This contains full path with filename
            base_filename = request.form.get('filename', '')
            
            # Handle URL input if checkbox is checked
            if use_url and url_input:
                print(f"Fetching content from URL: {url_input}")
                url_content, url_error = fetch_url_content(url_input)
                if url_error:
                    print(f"URL fetch error: {url_error}")
                    return jsonify(error=f"Failed to fetch URL content: {url_error}"), 400
                pasted_input = url_content
                print(f"Successfully fetched {len(pasted_input)} characters from URL")
            elif use_url and not url_input:
                return jsonify(error="URL input is required when URL mode is selected"), 400

            # Extract directory path from the full path
            output_dir = os.path.dirname(output_path)
            print(f"Extracted directory path: {output_dir}")

            # Validation checks with detailed logging
            if not output_dir:
                print("Validation failed: Output directory is empty")
                return jsonify(error="Output directory is empty"), 400
                
            print(f"Checking if directory exists: {output_dir}")
            if not os.path.exists(output_dir):
                print(f"Validation failed: Directory does not exist: {output_dir}")
                return jsonify(error=f"Output directory does not exist: {output_dir}"), 400
                
            if not os.path.isdir(output_dir):
                print(f"Validation failed: Not a directory: {output_dir}")
                return jsonify(error=f"Path exists but is not a directory: {output_dir}"), 400
                
            if not os.access(output_dir, os.W_OK):
                print(f"Validation failed: Directory not writable: {output_dir}")
                return jsonify(error=f"Output directory is not writable: {output_dir}"), 400

            if not base_filename:
                print("Validation failed: Filename is empty")
                return jsonify(error="Filename cannot be empty"), 400
                
            if not prompts:
                print("Validation failed: No prompts selected")
                return jsonify(error="Please select at least one prompt"), 400
                
            if not pasted_input and not use_url:
                print("Validation failed: No input text provided")
                return jsonify(error="Please provide input text or select URL mode"), 400

            print("All validation checks passed!")
            
            # Split filename and extension
            filename_parts = base_filename.rsplit('.', 1)
            base_name = filename_parts[0]
            extension = filename_parts[1] if len(filename_parts) > 1 else ''
            
            results = []
            errors = []
            
            for prompt in prompts:
                try:
                    # Create unique filename for each prompt
                    prompt_filename = f"{base_name}_{prompt}.{extension}"
                    prompt_output = os.path.join(output_dir, prompt_filename)
                    
                    # Check if file already exists
                    if os.path.exists(prompt_output):
                        warning = f"Warning: File {prompt_filename} already exists and will be overwritten."
                        results.append(warning)
                    
                    # Run mainstay and capture result
                    result = run_mainstay(
                        input_text=pasted_input,
                        prompt=prompt,
                        ai=ai,
                        model=model,
                        output=prompt_output,
                        url=url_input if use_url else ''
                    )
                    
                    # Verify file was created
                    if os.path.exists(prompt_output):
                        file_size = os.path.getsize(prompt_output)
                        status = (
                            f"✓ Successfully saved to {prompt_filename} "
                            f"(Size: {file_size/1024:.1f} KB)"
                        )
                    else:
                        status = f"⚠ Warning: File {prompt_filename} was not created"
                    
                    results.append(f"Results for '{prompt}':\n{status}\n{result}")
                    
                except Exception as e:
                    error_msg = f"❌ Error processing prompt '{prompt}': {str(e)}"
                    errors.append(error_msg)
                    continue
            
            # Combine results and errors
            all_messages = results + errors
            combined_result = "\n\n=== Next Prompt Results ===\n\n".join(all_messages)
            
            if errors:
                return jsonify(result=combined_result, has_errors=True)
            return jsonify(result=combined_result, has_errors=False)

        except Exception as e:
            return jsonify(error=f"Fatal error: {str(e)}"), 500

    prompts = get_prompts()
    return render_template('index.html', prompts=prompts)

def run_mainstay(input_text, prompt, ai, model, output, url=''):
    """
    Runs the mainstay engine with the given parameters and input text.
    Args:
        input_text (str): The text to send as input.
        prompt (str): The prompt to use.
        ai (str): The AI provider.
        model (str): The model to use.
        output (str): The output file path.
        url (str): The URL used for input (optional).
    Returns:
        str: The output or error message from mainstay.
    """
    command = [
        'python3', '/opt/mainstay/mainstay.py',
        '--prompt', prompt,
        '--ai', ai,
        '--model', model,
        '--output', output
    ]
    
    # Add URL parameter if provided
    if url:
        command.extend(['--url', url])
    
    # Use shlex.join to properly escape the command arguments
    cmd_str = shlex.join(command)
    
    # Use shell=True to allow piping, and pass the command as a string
    process = subprocess.Popen(cmd_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Send the input_text to stdin and get the output
    stdout, stderr = process.communicate(input=input_text)
    
    if process.returncode != 0:
        # If there was an error, include stderr in the result
        return f"Error: {stderr}"
    
    return stdout

def get_output_paths():
    """
    Returns a list of available output paths. Customize as needed.
    Returns:
        list: List of output path strings.
    """
    return ['/path/to/output1', '/path/to/output2', '/path/to/output3']

def get_prompts():
    """
    Lists available prompt files (without .md extension).
    Returns:
        list: List of prompt names.
    """
    prompt_dir = config.get('promptdir', '/opt/mainstay/prompts')
    prompts = []
    for file in os.listdir(prompt_dir):
        if file.endswith('.md'):
            prompts.append(file[:-3])  # Remove the .md extension
    return prompts

@app.route('/list_prompts')
def list_prompts():
    """
    API endpoint to list available prompts.
    Returns:
        JSON: List of prompt names.
    """
    prompts = get_prompts()
    return jsonify(prompts=prompts)

@app.route('/view_prompt/<prompt_name>')
def view_prompt(prompt_name):
    """
    API endpoint to view the content of a specific prompt file.
    Args:
        prompt_name (str): The name of the prompt (without .md).
    Returns:
        JSON: Content of the prompt file or error message.
    """
    prompt_dir = config.get('promptdir', '/opt/mainstay/prompts')
    prompt_file = os.path.join(prompt_dir, f"{prompt_name}.md")
    try:
        with open(prompt_file, 'r') as file:
            content = file.read()
        return jsonify(content=content)
    except Exception as e:
        return jsonify(error=f"Unable to read prompt file: {str(e)}"), 404

@app.route('/list_models')
def list_models():
    """
    API endpoint to list available AI models from the config.
    Returns:
        JSON: List of model names.
    """
    models = config.get('defaultmodels', [])
    return jsonify(models=models)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
