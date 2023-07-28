from flask import Flask, request, jsonify
from docx import Document
import base64
import io

app = Flask(__name__)


def process_docx(base64_encoded_docx):
    # decode base64 file
    docx_bytes = base64.b64decode(base64_encoded_docx)

    # create a file-like object from the decoded bytes
    file_like_object = io.BytesIO(docx_bytes)

    # load file with python-docx
    doc = Document(file_like_object)

    # extract text
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)

    return ' '.join(full_text)


@app.route('/', methods=['GET', 'POST'])

def handle_request():
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        if request_json and 'rawDocument' in request_json:
            print(f"Received request_json: {request_json}"
                  )  # Add this line to log the received JSON
            raw_document = request_json['rawDocument']
            mimeType = raw_document['mimeType']
            base64_file = raw_document['content']
            print(f"Received base64_file: {base64_file[:100]}..."
                  )  # Add this line to log the start of the received base64 string
            text = process_docx(base64_file)
            return jsonify({"message": "OK", "text": text})
        else:
            print(
                f"Invalid request: {request_json}"
            )  # Add this line to log the received data when the request is considered invalid
            return jsonify({"error": "Invalid request"}), 400
    elif request.method == 'GET':
        # Handle the "GET" request for the root URL (optional)
        return "Hello, this is the Flask app!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# Right now I do not know if app.yaml file is necessary or not but I have created it in google cloud functions
# any ways following is the code for app.yaml file:
# runtime: python37
