import pytest
from fastapi import status
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/",
                                 json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/",
                                 json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == status.HTTP_409_CONFLICT


def test_vote_on_post_unauthorized_user(client, test_posts, test_user):
    res = client.put(f"/posts/{test_posts[0].id}", json={"post_id": 5000, "dir": 1})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/",
                                 json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == status.HTTP_201_CREATED


def test_vote_on_post_non_existent(authorized_client, test_posts, test_user):
    res = authorized_client.post("/vote/",
                                 json={"post_id": 5000, "dir": 1})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_on_post_non_existent(authorized_client, test_posts, test_user):
    res = authorized_client.post("/vote/",
                                 json={"post_id": 5000, "dir": 0})
    assert res.status_code == status.HTTP_404_NOT_FOUND


