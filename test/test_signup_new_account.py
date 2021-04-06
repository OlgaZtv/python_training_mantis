
def test_singup_new_account(app):
    username = "user1"
    password = "test"
    app.james.ensure_user_exist(username, password)
    