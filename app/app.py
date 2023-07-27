import os
import json
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, filename="log.txt", format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_sorted_document_files():
    """
    Get a sorted list of document files based on their last modified time
    :return: list of sorted files
    """
    try:
        data_dir = os.path.join(os.getcwd(), "..", "data")
        file_names = os.listdir(data_dir)
        file_paths = [os.path.join(data_dir, filename) for filename in file_names]
        sorted_files = sorted(file_paths, key=lambda x: os.path.getmtime(x), reverse=True)
        return sorted_files
    except Exception as e:
        logger.error(f"Error while getting document files: {e}")
        return []


def recursive_keyword_search(keyword, data):
    """
    It will search the keyword in document with all columns
    :param keyword: input key
    :param data: document content in json format
    :return: Bool based keyword match with content
    """
    if isinstance(data, int) and str(keyword) in str(data):
        return True
    elif isinstance(data, str) and str(keyword).lower() in data.lower():
        return True
    elif isinstance(data, list):
        for item in data:
            if recursive_keyword_search(keyword, item):
                return True
    elif isinstance(data, dict):
        for key, value in data.items():
            if recursive_keyword_search(keyword, value):
                return True
    return False


def keyword_search_in_document(keyword, document_path):
    """
    Search given input value in json document
    :param keyword: Input value
    :param document_path: path of document
    :return: document content or None
    """
    try:
        with open(document_path) as f:
            document = json.load(f)
            if recursive_keyword_search(keyword, document):
                return document
    except Exception as e:
        logger.error(f"Error while searching keyword in document {document_path}: {e}")
    return None


@app.route('/search', methods=['GET'])
def search_documents():
    """
    Search the given input value in each json document which are stored in data folder
    :return:  input matched document content in json format
    """
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify(error='Keyword parameter is missing'), 400

    sorted_files = get_sorted_document_files()

    for file_path in sorted_files:
        result = keyword_search_in_document(keyword, file_path)
        if result:
            return jsonify(result), 200

    return jsonify(message='No matching document found'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
