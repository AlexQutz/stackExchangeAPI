import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import app

class TestStackStatsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('main.requests.get')
    def test_stack_stats_endpoint(self, mock_get):
        # Mock the response from the Stack Exchange API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {"answer_id": 1, "is_accepted": True, "score": 5, "question_id": 1},
                {"answer_id": 2, "is_accepted": False, "score": 3, "question_id": 1},
            ]
        }
        mock_get.return_value = mock_response

        # Make a request to the /api/v1/stackstats endpoint
        response = self.app.get('/api/v1/stackstats?since=2022-01-01 00:00:00&until=2022-01-31 23:59:59')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        data = response.json

        # Define the expected response data
        expected_data = {
            "total_accepted_answers": 1,
            "average_score_accepted_answers": 5.0,
            "average_answer_count_per_question": 2.0,
            "top_10_comments_count": {'1': 2, '2': 2}  #this occurs because both responses include the items tag.
        }

    
        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()