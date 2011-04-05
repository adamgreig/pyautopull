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
            rtn = subprocess.call(app.config["CMD"])
            if rtn == 0:
                with open("./last_commit", "w") as f:
                    f.write(after)
    except Exception as e:
        pass
    finally:
        return "thanks github, <3!\n"

if __name__ == "__main__":
    app.run()
