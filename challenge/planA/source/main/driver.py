

from flask import Flask, request, jsonify,Response
import requests,json
import os

from es_upload import Uploader

# Define the App
app = Flask(__name__)


@app.route('/')
def hello():
    """
        It Works! Test Deployment!

        PYTHON:
        --------
        import requests
        post_url = "http://10.162.4.94:5000/"
        result = requests.get(url=post_url)
        return result.json()

        CURL:
        -----
        curl -XGET http://10.162.4.94:5000/

    """
    return {200:"It Works!"}


@app.route('/api/v1.1/bmi/publish/',methods=["POST"])
def publish_bmi_stats():
    """
        Publish all Patient records into Elasticsearch databases
        Invoke module es_upload and perform all the necessary tasks.
        Send a Return code of 201 on success.
    """
    res=Uploader.upload(os.environ['bmiUsersJsonFile'],os.environ['bmiCatJsonFile'],os.environ['esHost'],os.environ['esPort'],os.environ['esIndex'])
    return {200:res}

if __name__ == "__main__":

    # Run the Development App Server
    import os
    app.run(host=os.environ['FLASKHOSTNAME'],port=os.environ['FLASKPORT'],debug=True)
