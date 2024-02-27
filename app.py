from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os
import tempfile
import time  # for introducing delay

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.cc'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.cc') as temp:
                file.save(temp.name)
                # Ensure file is saved and closed before proceeding
                temp.close()
                compile_result = compile_and_execute(temp.name)
                # Attempt to delete the file with a delay
                time.sleep(1)  # Delay to give time for the OS to release any locks
                try:
                    os.unlink(temp.name)
                except PermissionError as e:
                    print(f"Error deleting file: {e}")
                return render_template('results.html', result=compile_result)
    return render_template('upload.html')

def compile_and_execute(filepath):
    compile_cmd = f"g++ {filepath} -o {filepath}.out"
    test_script = "./walk.cc_test.sh"
    compile_process = subprocess.run(compile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if compile_process.returncode != 0:
        return "Compilation failed."
    
    # Ensure compilation output file is generated before grading
    if os.path.exists(f"{filepath}.out"):
        grading_process = subprocess.run(test_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if grading_process.returncode == 0:
            score = grading_process.stdout.decode().strip()
            return f"Score: {score} out of 2 correct."
        else:
            return "An error occurred during grading."
    else:
        return "Compilation succeeded but executable was not created."

if __name__ == '__main__':
    app.run(debug=True)
