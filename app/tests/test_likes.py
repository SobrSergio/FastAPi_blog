import pytest

def test_like_post(client, test_post):
    response = client.post(f"/posts/{test_post['id']}/likes")
    assert response.status_code == 200
    assert response.json() == {"message": "Пост лайкнут"}

def test_unlike_post(client, test_post):
    client.post(f"/posts/{test_post['id']}/likes")
    response = client.delete(f"/posts/{test_post['id']}/likes")
    assert response.status_code == 200
    assert response.json() == {"message": "Лайк убран"}
