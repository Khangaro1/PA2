from flask import Flask, request, redirect, url_for, render_template, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'cc', 'cpp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
            filename = 'walk.cc'  # Static name for simplicity
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = compile_and_execute(filepath)
            return render_template('result.html', result=result)
    return render_template('upload.html')

def compile_and_execute(filepath):
    compile_cmd = f"/usr/bin/g++ {filepath}"
    run_cmd = "./compile_and_run.sh"  # Your script to run the compiled program
    try:
        # Compile the C++ program
        compile_process = subprocess.run(compile_cmd, shell=True, check=True)
        # Execute your script
        run_process = subprocess.run(run_cmd, shell=True, capture_output=True, check=True)
        output = run_process.stdout.decode()
    except subprocess.CalledProcessError as e:
        output = f"An error occurred: {e.output.decode()}"
    return output

if __name__ == '__main__':
    app.run(debug=True)
