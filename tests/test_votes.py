

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/{test_posts[3].id}")
    assert res.status_code == 201


# def test_delete_vote(authorized_client, test_posts):
#     res = authorized_client.post(f"/vote/{test_posts[3].id}")
#     res = authorized_client.post(f"/vote/{test_posts[3].id}")
#     assert res.status_code == 201


def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/80000")
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(f"/vote/{test_posts[3].id}")
    assert res.status_code == 401
