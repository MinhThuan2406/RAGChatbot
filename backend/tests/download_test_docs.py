import os
import requests

TEST_DOCS_DIR = os.path.join(os.path.dirname(__file__), "test_docs")
os.makedirs(TEST_DOCS_DIR, exist_ok=True)

files = [
    # (filename, url)
    ("sample.pdf", "https://file-examples.com/wp-content/uploads/2017/10/file-sample_150kB.pdf"),
    ("sample.docx", "https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.docx"),
    ("sample.doc", "https://file-examples.com/wp-content/uploads/2017/02/file-sample_100kB.doc"),
    ("sample.jpg", "https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB.jpg"),
    ("sample.jpeg", "https://file-examples.com/wp-content/uploads/2017/10/file_example_JPG_100kB_1.jpeg"),
    ("sample.png", "https://file-examples.com/wp-content/uploads/2017/10/file_example_PNG_100kB.png"),
    ("unsupported.txt", "https://www.w3.org/TR/PNG/iso_8859-1.txt"),
]

for fname, url in files:
    out_path = os.path.join(TEST_DOCS_DIR, fname)
    if os.path.exists(out_path):
        print(f"{fname} already exists, skipping.")
        continue
    print(f"Downloading {fname}...")
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"Saved {fname}")
    except Exception as e:
        print(f"Failed to download {fname}: {e}")