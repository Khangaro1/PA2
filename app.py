from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import subprocess
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'cpp', 'c'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set up logging
logging.basicConfig(level=logging.INFO)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Always secure the filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            app.logger.info(f'Received file: {filename}')  # Log the received file
            result = compile_and_execute(filepath)
            return render_template('result.html', result=result)
    return render_template('upload.html')

def compile_and_execute(filepath):
    compile_cmd = f"/usr/bin/g++ {filepath}"
    run_cmd = "./compile_and_run.sh"
    try:
        # Ensure stdout and stderr are captured for decoding
        compile_process = subprocess.run(compile_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Assuming your script outputs the result to stdout
        run_process = subprocess.run(run_cmd, shell=True, capture_output=True, check=True)
        output = run_process.stdout.decode()
    except subprocess.CalledProcessError as e:
        # Safely decode stderr or stdout, checking if they are not None
        error_message = e.stderr.decode() if e.stderr else "Unknown error"
        output = f"An error occurred: {error_message}"
    return output

if __name__ == '__main__':
    app.run(debug=True)
