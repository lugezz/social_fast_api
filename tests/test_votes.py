import pytest

from app import models


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/{test_posts[3].id}")
    assert res.status_code == 201


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(f"/vote/{test_posts[3].id}")
    assert res.status_code == 201
    assert res.json()['message'] == 'Vote removed successfully'


def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/80000")
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(f"/vote/{test_posts[3].id}")
    assert res.status_code == 401
