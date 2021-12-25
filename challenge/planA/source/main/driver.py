

from flask import Flask, request, jsonify,Response
import requests,json
import os

from es_upload import Uploader
from es_filter import Filters

# Define the App
app = Flask(__name__)


@app.route('/')
def hello():
    """
        It Works! Test Deployment!

        PYTHON:
        --------
        import requests
        post_url = "http://localhost:7777/"
        result = requests.get(url=post_url)
        return result.json()

        CURL:
        -----
        curl -XGET http://localhost:7777/

    """
    return {200:"It Works!"}


@app.route('/api/v1.1/bmi/publish/',methods=["POST"])
def publish_bmi_stats():
    """
        Publish all Patient records into Elasticsearch databases
        Invoke module es_upload and perform all the necessary tasks.
        Send a Return code of 201 on success.
    """
    res=Uploader.parallel(os.environ['bmiUsersJsonFilePath'],os.environ['bmiCatJsonFile'],os.environ['esHost'],os.environ['esPort'],os.environ['esIndex'])
    return {200:res}


@app.route('/api/v1.1/bmi/filter/',methods=["GET"])
def filter_bmi_stats():
    """
        Publish all Patient records into Elasticsearch databases
        Invoke module es_upload and perform all the necessary tasks.
        Send a Return code of 201 on success.
    """
    esQuery=request.form.get("esQuery")
    print(esQuery)
    print(json.loads(esQuery))
    res=Filters.filter(os.environ['esHost'],os.environ['esPort'],os.environ['esIndex'],esQuery)
    return {200:res}

if __name__ == "__main__":

    # Run the Development App Server
    import os
    app.run(host=os.environ['FLASKHOSTNAME'],port=os.environ['FLASKPORT'],debug=True)
