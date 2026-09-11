import unittest
from app.scoring import (
    generate_fallback_roast,
    get_double_down_roast,
    detect_category,
    DAMAGE_TIERS
)

class TestRagebaitScoring(unittest.TestCase):
    def test_category_detection(self):
        self.assertEqual(detect_category("Should I text my ex at 3 AM?"), "ex")
        self.assertEqual(detect_category("I want to quit my 9-5 to stream on Twitch"), "career")
        self.assertEqual(detect_category("I spent all my rent money on DoorDash and crypto"), "money")
        self.assertEqual(detect_category("My alarm didn't ring and I overslept"), "late_excuse")
        self.assertEqual(detect_category("I haven't been to the gym in 14 months"), "gym_health")
        self.assertEqual(detect_category("Why is the sky blue?"), "general")

    def test_roast_generation_and_damage_ranges(self):
        res = generate_fallback_roast("Should I text my ex?")
        self.assertIn("roast", res)
        self.assertIn("ragebait_advice", res)
        self.assertIn("damage_tier", res)
        self.assertIn("diagnosis_tag", res)

        self.assertTrue(70 <= res["emotional_damage"] <= 100)
        self.assertTrue(70 <= res["delusion_index"] <= 100)
        self.assertTrue(70 <= res["copium_level"] <= 100)
        self.assertTrue(len(res["roast"]) > 20)
        self.assertTrue(len(res["ragebait_advice"]) > 20)

    def test_damage_tier_validity(self):
        tier_names = [t[2] for t in DAMAGE_TIERS]
        for _ in range(10):
            res = generate_fallback_roast("I skipped work today")
            self.assertIn(res["damage_tier"], tier_names)

    def test_double_down_roast(self):
        orig = "You are financially illiterate."
        doubled = get_double_down_roast(orig, "I bought crypto")
        self.assertTrue(len(doubled) > 20)
        self.assertNotEqual(orig, doubled)

if __name__ == "__main__":
    unittest.main()
