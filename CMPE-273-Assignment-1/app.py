from flask import Flask
import sys
from github import Github
import base64
import os
import yaml
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from Dockerized Flask App!!"


@app.route("/v1/<filename>")
def display(filename):
    return get_config_files(sys.argv[1], filename)


def get_config_files(path, filename):
    githubDetails = path.split("github.com/")[1].split("/")
    yamlfileName = filename.split(".")[0] + ".yml"

    try:
        if not os.path.exists("v1"):
            os.makedirs("v1")

        # Read and store the contents to a local file every time in case the server is down the next time.
        content = base64.b64decode(Github().get_user(githubDetails[0]).get_repo(
            githubDetails[1]).get_file_contents(yamlfileName).content)
        outputfile = open('v1/' + yamlfileName, 'wb')
        outputfile.write(str(content))
        outputfile.close()

        if filename.endswith(".json"):
            return str(json.dumps(yaml.load(content)))
        else:
            if filename.endswith(".yml"):
                return str(content)
            else:
                # If file is not json or yml display error message.
                return "Invalid file type. Please enter .yml or .json file name."

    except Exception as ex:
        # If file not present locally or on github show error message.
        if not os.path.isfile('v1/' + yamlfileName):
            return "File not found in Github and local repository. Please enter correct file name."

        # If file not present in github (server down) get latest from local copy
        with open('v1/' + yamlfileName, 'r') as stream:
            if filename.endswith(".yml"):
                return str(stream.read())
            else:
                return str(json.dumps(yaml.load(stream)))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
