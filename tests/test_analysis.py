import unittest
from app import create_app
from app.config import Config
from app.models import db

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class TestAnalysisAPI(unittest.TestCase):
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

    def test_empty_input_validation(self):
        res = self.client.post("/api/roast", json={"prompt": ""})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])

        res2 = self.client.post("/api/roast", json={"prompt": "   "})
        self.assertEqual(res2.status_code, 400)
        data2 = res2.get_json()
        self.assertFalse(data2["success"])

    def test_short_input_validation(self):
        res = self.client.post("/api/roast", json={"prompt": "H"})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])

    def test_successful_roast_schema(self):
        payload = {
            "prompt": "Should I text my ex? It's 2 AM and I miss them.",
            "tone": "brutal"
        }
        res = self.client.post("/api/roast", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

        self.assertIn("roast", data)
        self.assertIn("ragebait_advice", data)
        self.assertIn("emotional_damage", data)
        self.assertIn("delusion_index", data)
        self.assertIn("copium_level", data)
        self.assertIn("damage_tier", data)
        self.assertIn("diagnosis_tag", data)

        self.assertTrue(70 <= data["emotional_damage"] <= 100)
        self.assertTrue(len(data["roast"]) > 10)
        self.assertTrue(len(data["ragebait_advice"]) > 10)

    def test_double_down_endpoint(self):
        res = self.client.post("/api/double-down", json={
            "prompt": "I spent all my rent on crypto.",
            "original_roast": "You are financially illiterate."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("double_down_roast", data)

if __name__ == "__main__":
    unittest.main()
