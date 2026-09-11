import unittest
from app import create_app
from app.config import Config
from app.models import db, User, Analysis

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_flow(self):
        # Successful register
        res = self.client.post("/api/auth/register", json={
            "username": "coder1",
            "email": "coder1@test.com",
            "password": "securepassword123"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["user"]["username"], "coder1")

        # Duplicate register
        res2 = self.client.post("/api/auth/register", json={
            "username": "coder1",
            "email": "coder2@test.com",
            "password": "securepassword123"
        })
        self.assertEqual(res2.status_code, 409)

    def test_registration_validation(self):
        # Short username
        res = self.client.post("/api/auth/register", json={
            "username": "ab",
            "email": "test@test.com",
            "password": "password123"
        })
        self.assertEqual(res.status_code, 400)

        # Invalid email
        res2 = self.client.post("/api/auth/register", json={
            "username": "validname",
            "email": "invalidemail",
            "password": "password123"
        })
        self.assertEqual(res2.status_code, 400)

        # Short password
        res3 = self.client.post("/api/auth/register", json={
            "username": "validname",
            "email": "test@test.com",
            "password": "123"
        })
        self.assertEqual(res3.status_code, 400)

    def test_login_and_logout(self):
        # Create user
        u = User(username="testuser", email="user@test.com")
        u.set_password("mypassword")
        db.session.add(u)
        db.session.commit()

        # Login with correct password
        res = self.client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "mypassword"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])

        # Check me
        me = self.client.get("/api/auth/me").get_json()
        self.assertTrue(me["authenticated"])

        # Logout
        self.client.post("/api/auth/logout")
        me_after = self.client.get("/api/auth/me").get_json()
        self.assertFalse(me_after["authenticated"])

        # Login with wrong password
        res_fail = self.client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(res_fail.status_code, 401)

    def test_history_authorization_isolation(self):
        # Unauthenticated access
        res = self.client.get("/api/history")
        self.assertEqual(res.status_code, 401)

        # Create two users
        u1 = User(username="user1", email="u1@test.com")
        u1.set_password("password123")
        u2 = User(username="user2", email="u2@test.com")
        u2.set_password("password123")
        db.session.add_all([u1, u2])
        db.session.commit()

        # Create private analysis for user 1
        a1 = Analysis(
            user_id=u1.id,
            excuse_text="Private excuse for user 1",
            situation="Other",
            believability=50, creativity=50, originality=50, specificity=50,
            plausibility=50, desperation=50, suspiciousness=50, bullshit_level=50,
            overall_score=50, verdict="DECENT EXCUSE", is_public=False
        )
        db.session.add(a1)
        db.session.commit()

        # User 2 logs in and tries to access user 1's analysis
        self.client.post("/api/auth/login", json={"username": "user2", "password": "password123"})
        res_forbidden = self.client.get(f"/api/analysis/{a1.id}")
        self.assertEqual(res_forbidden.status_code, 403)

if __name__ == "__main__":
    unittest.main()
