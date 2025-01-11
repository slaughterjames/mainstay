#! /usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json
import shlex
from termcolor import colored

app = Flask(__name__)

# Load configuration
def load_config():
    try:
        with open('/opt/mainstay/mainstay.conf', 'r') as read_file:
            return json.load(read_file)
    except Exception as e:
        print(colored(f'[x] Unable to read configuration file: {str(e)}', 'red', attrs=['bold']))
        return None

config = load_config()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Debug: Print all form data
            print("Form data received:", request.form)
            print("Form files:", request.files)
            
            # Get all form data with default values
            pasted_input = request.form.get('pastedInput', '')
            prompts = request.form.getlist('prompt')
            ai = request.form.get('ai', '')
            model = request.form.get('model', '')
            output_path = request.form.get('output', '')  # This contains full path with filename
            base_filename = request.form.get('filename', '')

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
                        output=prompt_output
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

def run_mainstay(input_text, prompt, ai, model, output):
    command = [
        'python3', '/opt/mainstay/mainstay.py',
        '--prompt', prompt,
        '--ai', ai,
        '--model', model,
        '--output', output
    ]
    
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
    # This function should return a list of available output paths
    # You may want to customize this based on your specific requirements
    return ['/path/to/output1', '/path/to/output2', '/path/to/output3']

def get_prompts():
    prompt_dir = config.get('promptdir', '/opt/mainstay/prompts')
    prompts = []
    for file in os.listdir(prompt_dir):
        if file.endswith('.md'):
            prompts.append(file[:-3])  # Remove the .md extension
    return prompts

@app.route('/list_prompts')
def list_prompts():
    prompts = get_prompts()
    return jsonify(prompts=prompts)

@app.route('/view_prompt/<prompt_name>')
def view_prompt(prompt_name):
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
    models = config.get('defaultmodels', [])
    return jsonify(models=models)

if __name__ == '__main__':
    app.run(debug=True)
