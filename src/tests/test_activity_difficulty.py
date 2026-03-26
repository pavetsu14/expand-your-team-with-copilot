import unittest

from src.backend.routers import activities as activities_router


class FakeActivitiesCollection:
    def __init__(self, documents):
        self.documents = documents
        self.last_query = None

    def find(self, query):
        self.last_query = query
        return [document.copy() for document in self.documents]


class ActivityDifficultyTests(unittest.TestCase):
    def setUp(self):
        self.original_collection = activities_router.activities_collection

    def tearDown(self):
        activities_router.activities_collection = self.original_collection

    def test_filters_beginner_activities(self):
        fake_collection = FakeActivitiesCollection(
            [
                {
                    "_id": "Programming Class",
                    "description": "Learn programming fundamentals",
                    "difficulty": "beginner",
                    "participants": [],
                    "max_participants": 20,
                }
            ]
        )
        activities_router.activities_collection = fake_collection

        response = activities_router.get_activities(difficulty="beginner")

        self.assertEqual(
            fake_collection.last_query,
            {"difficulty": "beginner"},
        )
        self.assertIn("Programming Class", response)

    def test_filters_all_levels_activities(self):
        fake_collection = FakeActivitiesCollection(
            [
                {
                    "_id": "Debate Team",
                    "description": "Develop public speaking skills",
                    "participants": [],
                    "max_participants": 12,
                }
            ]
        )
        activities_router.activities_collection = fake_collection

        response = activities_router.get_activities(difficulty="all")

        self.assertEqual(
            fake_collection.last_query,
            {
                "$or": [
                    {"difficulty": {"$exists": False}},
                    {"difficulty": None},
                    {"difficulty": ""},
                ]
            },
        )
        self.assertIn("Debate Team", response)


if __name__ == "__main__":
    unittest.main()
