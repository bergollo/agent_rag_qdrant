"""Tests for the vector store upload endpoint."""

from __future__ import annotations

from pathlib import Path


def test_vector_upload_success(api_client, tmp_path: Path):
    client, stub = api_client

    sample_file = tmp_path / "sample.txt"
    sample_content = b"hello embeddings"
    sample_file.write_bytes(sample_content)

    with sample_file.open("rb") as fh:
        files = {"file": (sample_file.name, fh, "text/plain")}
        resp = client.post("/v1/vectorstore/upload", files=files)

    assert resp.status_code == 200
    assert resp.json() == {"id": "stub-doc", "status": "uploaded"}
    assert stub.uploaded_files == [
        {"filename": sample_file.name, "size": len(sample_content)}
    ]
