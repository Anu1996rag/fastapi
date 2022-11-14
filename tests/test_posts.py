import pytest
from fastapi import status
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    post_map = map(validate, res.json())
    posts = list(post_map)

    assert len(test_posts) == len(posts)
    assert res.status_code == status.HTTP_200_OK


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_non_existent(authorized_client, test_posts):
    res = authorized_client.get("/posts/500000")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, title, content, published, test_user):
    res = authorized_client.post("/posts/",
                                 json={"title": title, "content": content, "published": published})
    new_post = schemas.PostResponse(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert new_post.title == title
    assert new_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/",
                                 json={"title": "arbitrary title", "content": "random content"})

    new_post = schemas.PostResponse(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert new_post.published == True
    assert new_post.owner_id == test_user["id"]


def test_create_post_unauthorized_user(client, test_user):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "random content"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_unauthorized_user(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_non_existent(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/50000")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post_unauthorized_user(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_post_non_existent(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/50000", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND
