import os
import subprocess
from flask import Flask, json, request, jsonify

app = Flask(__name__)

command = [
    "nsjail",
    "--config", "./run.python3.config.proto",
    "--",
    "python3",
    "execution_wrapper.py"
]

@app.route("/execute", methods=["POST"])
def execute_code():
    '''Execute user-submitted Python code'''
    if not request.json:
        return jsonify({
            "result": "Invalid JSON",
            "stdout": ""
        }), 400

    data = request.json
    code = data.get("script", "")

    if type(code) is not str or not code.strip():
        return jsonify({
            "result": "Invalid script",
            "stdout": ""
        }), 400

    # write the code to a temporary file
    # we may set up a temp file per user to avoid conflicts and improve parallelism
    with open("user_script.py", "w", encoding="utf-8") as f:
        f.write(code.strip())

    # execute the script as a subprocess
    writer = subprocess.run(command, capture_output=True, text=True, check=False)
    stderr_str = writer.stderr
    stdout_str = writer.stdout
    result = writer.returncode

    if result != 0:
        if stdout_str:
            return json.loads(stdout_str), 400
        return jsonify({
            "result": "Error executing script",
            "stdout": stderr_str,
        }), 400

    #remove temp file
    os.remove("./user_script.py")

    return json.loads(stdout_str), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
