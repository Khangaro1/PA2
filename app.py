from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import subprocess
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'cc', 'cpp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Modified to capture output
        result = subprocess.run("./compile.sh", shell=True, capture_output=True, text=True)
        output = result.stdout  # Capturing the standard output
        if result.stderr:  # Optionally handle standard error
            output += "\nErrors:\n" + result.stderr
        # Pass the output to the template
        return render_template('results.html', output=output)

    return redirect(url_for('upload_form'))

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
