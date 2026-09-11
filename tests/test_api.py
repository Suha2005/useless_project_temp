import unittest
from app import create_app
from app.config import Config
from app.models import db, Analysis, Leaderboard

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class TestAPIEndpoints(unittest.TestCase):
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

    def test_random_generator_endpoint(self):
        res = self.client.post("/api/generate")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("excuse", data)
        self.assertIn("situation", data)
        self.assertTrue(len(data["excuse"]) > 5)

    def test_daily_excuse_endpoint(self):
        res = self.client.get("/api/daily")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        daily = data["daily"]
        self.assertIn("excuse", daily)
        self.assertIn("score", daily)
        self.assertIn("verdict", daily)

    def test_improve_endpoint(self):
        res = self.client.post("/api/improve", json={"excuse": "My laptop broke", "situation": "Late Assignment"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("improved_excuse", data)
        self.assertNotEqual(data["improved_excuse"], "My laptop broke")

    def test_leaderboard_flow(self):
        # Create an analysis
        analysis = Analysis(
            user_id=None,
            excuse_text="My cat reviewed my pull request and deleted production.",
            situation="Work/Internship",
            believability=40, creativity=90, originality=85, specificity=70,
            plausibility=50, desperation=60, suspiciousness=45, bullshit_level=75,
            overall_score=82, verdict="HIGHLY CONVINCING"
        )
        db.session.add(analysis)
        db.session.commit()

        # Submit to leaderboard
        submit_res = self.client.post("/api/leaderboard/submit", json={
            "analysis_id": analysis.id,
            "display_name": "SeniorCatOps"
        })
        self.assertEqual(submit_res.status_code, 200)

        # Retrieve leaderboard
        board_res = self.client.get("/api/leaderboard")
        self.assertEqual(board_res.status_code, 200)
        entries = board_res.get_json()["leaderboard"]
        self.assertTrue(any(e["display_name"] == "SeniorCatOps" for e in entries))

if __name__ == "__main__":
    unittest.main()
