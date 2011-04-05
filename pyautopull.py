import json
import subprocess
from flask import Flask, request

app = Flask(__name__)
app.config.from_object('config')

@app.route("/", methods=["POST"])
def autodeploy():
    try:
        with open("./last_commit", "r") as f:
            before = f.read()
        after = json.loads(request.form["payload"])["after"]
        if before != after:
            subprocess.call(["/bin/bash", "-c", app.config["CMD"]])
            with open("./last_commit", "w") as f:
                f.write(after)
    except Exception as e:
        with open("/tmp/pyautopull_err", "w") as f:
            f.write("exception: " + repr(e) + "\n")
    finally:
        return "thanks github, <3!\n"

if __name__ == "__main__":
    app.run()
