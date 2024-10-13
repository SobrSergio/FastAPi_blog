import pytest

def test_create_post(client):
    
    response = client.post("/posts", json={"title": "Test Title", "content": "Test Content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"
    assert response.json()["content"] == "Test Content"

def test_update_post(client, test_post):
    
    response = client.put(f"/posts/{test_post['id']}", json={"title": "Updated Title", "content": "Updated Content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["content"] == "Updated Content"

def test_read_post(client, test_post):
    
    response = client.get(f"/posts/{test_post['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"  
    assert response.json()["content"] == "Updated Content"

def test_delete_post(client, test_post):
    
    response = client.delete(f"/posts/{test_post['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"  

def test_read_posts(client):
    
    response = client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
