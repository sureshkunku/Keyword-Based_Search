import os
import json
import pytest
from app import app, get_sorted_document_files, recursive_keyword_search, keyword_search_in_document


@pytest.fixture
def client():
    client = app.test_client()
    yield client


@pytest.fixture
def temp_data_dir(tmpdir):
    # Create a temporary directory and add some sample JSON files for testing
    data_dir = os.path.join(os.getcwd(), "..", "data")
    yield data_dir


def test_get_sorted_document_files(temp_data_dir):
    sorted_files = get_sorted_document_files()
    assert isinstance(sorted_files, list)
    assert len(sorted_files) > 0


def test_recursive_keyword_search():
    sample_data = {
        "abstracts": [],
        "application_date": "1997-12-19",
        "assignees": [],
        "inventors": [
            {
                "first_name": "",
                "last_name": "TAMAKI SANEAKI",
                "name": ""
            },
            {
                "first_name": "",
                "last_name": "SHIMOYAMA NAOHIKO",
                "name": ""
            }
        ],
        "ipc_classes": [
            {
                "label": "G06F  12/08",
                "primary": True
            }
        ],
        "ipcr_classes": [
            {
                "label": "G06F  12/08        20060101AFI20051220RMJP"
            }
        ],
        "legal_status": "Withdrawn",
        "locarno_classes": [],
        "national_classes": [
            {
                "label": "G06F  12/08       E",
                "primary": True
            },
            {
                "label": "G06F  12/0862  100",
                "primary": False
            },
            {
                "label": "G06F  12/0895  116",
                "primary": False
            },
            {
                "label": "G06F  12/0864",
                "primary": False
            },
            {
                "label": "G06F  12/08    507A",
                "primary": False
            },
            {
                "label": "G06F  12/08    579",
                "primary": False
            },
            {
                "label": "G06F  12/08    511A",
                "primary": False
            },
            {
                "label": "G06F  12/08       G",
                "primary": False
            }
        ],
        "patent_number": "JP-H11184752-A",
        "priority_date": "1997-12-19",
        "publication_date": "1999-07-09",
        "publication_id": 143645573,
        "titles": [
            {
                "lang": "JA",
                "text": "データ処理装置及びデータ処理システム"
            },
            {
                "lang": "EN",
                "text": "DATA PROCESSOR AND SYSTEM THEREFOR"
            }
        ]
    }
    assert recursive_keyword_search(143645573, sample_data)
    assert recursive_keyword_search("SHIMOYAMA", sample_data)
    assert recursive_keyword_search("Withdrawn", sample_data)
    assert not recursive_keyword_search("Suresh", sample_data)
    assert not recursive_keyword_search("Babu", sample_data)


def test_keyword_search_in_document(temp_data_dir):
    # Test with keyword present in one of the sample files
    keyword = "US-4195341-A"
    document_path = os.path.join(temp_data_dir, 'US-4195341-A.json')
    result = keyword_search_in_document(keyword, document_path)
    assert result is not None
    assert result['patent_number'] == 'US-4195341-A'

    # Test with keyword not present in any of the sample files
    keyword = "Suresh"
    document_path = os.path.join(temp_data_dir, 'JP-H10177520-A.json')
    result = keyword_search_in_document(keyword, document_path)
    assert result is None


def test_search_documents(client, temp_data_dir):
    # Test with valid keyword
    response = client.get("/search?keyword=143280786")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['patent_number'] == 'JP-H09311786-A'

    # Test with missing keyword parameter
    response = client.get('/search')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Keyword parameter is missing'

    # Test with keyword not found in any documents
    response = client.get('/search?keyword=Suresh')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'No matching document found'
