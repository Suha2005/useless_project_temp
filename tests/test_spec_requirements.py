import unittest
from app import create_app
from app.config import Config
from app.models import db

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class TestSpecRequirements(unittest.TestCase):
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

    def test_roast_advice_request(self):
        """Testing advice request: Should I text my ex?"""
        res = self.client.post("/api/roast", json={
            "prompt": "Should I text my ex at 3 AM?"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("roast", data)
        self.assertIn("ragebait_advice", data)
        self.assertGreaterEqual(data["emotional_damage"], 70)

    def test_roast_excuse_submission(self):
        """Testing excuse submission: My alarm didn't ring."""
        res = self.client.post("/api/roast", json={
            "prompt": "Sir, I couldn't come to class because my alarm didn't ring."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("roast", data)
        self.assertIn("ragebait_advice", data)

    def test_roast_career_streamer_dilemma(self):
        """Testing career dilemma: Quit job to stream."""
        res = self.client.post("/api/roast", json={
            "prompt": "I want to quit my job and stream full-time."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(bool(data.get("diagnosis_tag")))

    def test_special_characters_and_emojis(self):
        """Emojis and special characters handled cleanly."""
        prompt = "Should I text my ex? 😭💔💀 <script>alert(1)</script>"
        res = self.client.post("/api/roast", json={"prompt": prompt})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

if __name__ == "__main__":
    unittest.main()
