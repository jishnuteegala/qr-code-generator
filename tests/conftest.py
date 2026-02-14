import pytest
import tempfile
import os
from pathlib import Path
import pandas as pd
from io import BytesIO


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_excel_file(temp_dir):
    data = {
        'Phone': ['+441234567890', '+442345678901', '+443456789012'],
        'Name': ['John Smith', 'Alice Johnson', 'Bob Brown'],
        'Email': ['john@example.com', 'alice@example.com', 'bob@example.com'],
    }
    df = pd.DataFrame(data)
    filepath = temp_dir / "contacts.xlsx"
    df.to_excel(filepath, index=False)
    return filepath


@pytest.fixture
def sample_excel_with_duplicates(temp_dir):
    data = {
        'Phone': ['+441234567890', '+441234567890', '+442345678901'],
        'Name': ['John Smith', 'John Smith', 'Alice Johnson'],
    }
    df = pd.DataFrame(data)
    filepath = temp_dir / "contacts_dup.xlsx"
    df.to_excel(filepath, index=False)
    return filepath


@pytest.fixture
def sample_excel_with_invalid(temp_dir):
    data = {
        'Phone': ['+441234567890', '', None, '+442345678901'],
        'Name': ['John Smith', 'Alice Johnson', 'Bob Brown', 'Eve'],
    }
    df = pd.DataFrame(data)
    filepath = temp_dir / "contacts_invalid.xlsx"
    df.to_excel(filepath, index=False)
    return filepath


@pytest.fixture
def sample_csv_file(temp_dir):
    data = {
        'Phone': ['+441234567890', '+442345678901'],
        'Name': ['John Smith', 'Alice Johnson'],
    }
    df = pd.DataFrame(data)
    filepath = temp_dir / "contacts.csv"
    df.to_csv(filepath, index=False)
    return filepath


@pytest.fixture
def mock_excel_bytes():
    df = pd.DataFrame({
        'Phone': ['+441234567890'],
        'Name': ['Test User'],
    })
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()


@pytest.fixture
def sample_payload_data():
    return {
        'Phone': '+441234567890',
        'Name': 'John Smith',
        'Email': 'john@example.com',
    }
