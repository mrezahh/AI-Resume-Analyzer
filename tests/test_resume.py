from io import BytesIO

# ==================== Test uploading PDF or DOCX ====================
def test_upload_resume(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    files = {"file": ("test_resume.pdf", b"%PDF-1.4 test content", "application/pdf")}
    response = client.post("/resumes/upload", headers=headers, files=files)
    assert response.status_code == 200
    data = response.json()
    assert "file_name" in data
    assert data["file_name"] == "test_resume.pdf"
    assert data["user_id"] is not None
    assert data["id"] is not None
    
    
# ==================== Test uploading Invalid File ====================
def test_upload_invalid_file(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    files = {"file": ("test_resume.txt", b"Just some text content", "text/plain")}
    response = client.post("/resumes/upload", headers=headers, files=files)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid file type. Only PDF and DOCX are allowed."