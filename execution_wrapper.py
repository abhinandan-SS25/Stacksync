import importlib.util
import sys
import json
import contextlib
import io

spec = importlib.util.spec_from_file_location("user_script", "./user_script.py")
user_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(user_module)


if not hasattr(user_module, "main"):
    print(json.dumps({
        "result": "Error: No main() function found",
        "stdout": ""
    }))
    sys.exit(1)

stdout_buffer = io.StringIO()
stderr_buffer = io.StringIO()
#capture stdout and stderr
with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
    result = user_module.main()

stdout_output = stdout_buffer.getvalue()
stderr_output = stderr_buffer.getvalue()

try:
    print(json.dumps({
        "result": result,
        "stdout": stdout_output + "\n" + stderr_output
    }))
    sys.exit(0)
except TypeError as te:
    print(json.dumps({
            "result": "Error: main() does not return a JSON object",
            "stdout": str(te)
        })
    )
    sys.exit(1)
except Exception as e:
    print(json.dumps({
            "result": "Error: Exception occurred",
            "stdout": str(e)
        })
    )
    sys.exit(1)
