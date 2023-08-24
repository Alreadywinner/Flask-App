#import functions_framework
#un comment this when deploying the code on google cloud functions
from flask import Flask, request, jsonify
import base64
import io
import docx2txt

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
#@functions_framework.http
#pass request as a argument in this handle_request method
def handle_request():
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        if request_json and 'rawDocument' in request_json:
            print(f"Received request_json: {request_json}")
            raw_document = request_json['rawDocument']
            mimeType = raw_document['mimeType']
            base64_file = raw_document['content']
            print(f"Received base64_file: {base64_file[:100]}...")

            # Decode base64 file
            docx_bytes = base64.b64decode(base64_file)
            file_like_object = io.BytesIO(docx_bytes)

            # Extract text using docx2txt
            text = docx2txt.process(file_like_object)

            return jsonify({"message": "OK", "text": text})
        else:
            print(f"Invalid request: {request_json}")
            return jsonify({"error": "Invalid request"}), 400
    elif request.method == 'GET':
        # Handle the "GET" request for the root URL (optional)
        return "Hello, this is the Flask app!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
