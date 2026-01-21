"""
Unit and integration tests for Huckleberry Alexa Integration.

Run tests with: pytest test_main.py -v
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from main import app, parse_command, log_activity, init_huckleberry


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_huckleberry():
    """Mock Huckleberry API for testing."""
    with patch('main.huckleberry_api') as mock_api:
        mock_api.get_children.return_value = [{'id': 'test-child-id', 'name': 'Test Child'}]
        yield mock_api


class TestCommandParsing:
    """Test suite for command parsing logic."""

    def test_parse_simple_poo(self):
        """Test parsing simple poo command."""
        activity_type, details = parse_command("log a poo")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'

    def test_parse_detailed_poo(self):
        """Test parsing detailed poo command with size and color."""
        activity_type, details = parse_command("log a big yellow poo")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'
        assert details['poo_size'] == 'large'
        assert details['poo_color'] == 'yellow'

    def test_parse_poo_and_pee(self):
        """Test parsing combined poo and pee command."""
        activity_type, details = parse_command("log a poo and pee")
        assert activity_type == 'diaper'
        assert details['type'] == 'both'

    def test_parse_poo_sizes(self):
        """Test parsing different poo sizes."""
        # Big/Large
        _, details = parse_command("log a big poo")
        assert details['poo_size'] == 'large'

        # Small
        _, details = parse_command("log a small poo")
        assert details['poo_size'] == 'small'

        # Medium
        _, details = parse_command("log a medium poo")
        assert details['poo_size'] == 'medium'

    def test_parse_poo_colors(self):
        """Test parsing different poo colors."""
        colors = ['yellow', 'brown', 'green', 'dark', 'black']
        for color in colors:
            _, details = parse_command(f"log a {color} poo")
            assert details['poo_color'] == color

    def test_parse_pee(self):
        """Test parsing pee command."""
        activity_type, details = parse_command("log a pee")
        assert activity_type == 'diaper'
        assert details['type'] == 'pee'

    def test_parse_left_feed(self):
        """Test parsing left breastfeeding command."""
        activity_type, details = parse_command("log a left feed")
        assert activity_type == 'feed'
        assert details['side'] == 'left'

    def test_parse_right_feed(self):
        """Test parsing right breastfeeding command."""
        activity_type, details = parse_command("log a right feed")
        assert activity_type == 'feed'
        assert details['side'] == 'right'

    def test_parse_default_feed(self):
        """Test parsing feed command defaults to left."""
        activity_type, details = parse_command("log a feed")
        assert activity_type == 'feed'
        assert details['side'] == 'left'

    def test_parse_bottle_with_ml(self):
        """Test parsing bottle command with ml amount."""
        activity_type, details = parse_command("log a 120ml bottle")
        assert activity_type == 'bottle'
        assert details['amount_ml'] == 120

    def test_parse_bottle_with_oz(self):
        """Test parsing bottle command with oz amount."""
        activity_type, details = parse_command("log a 4oz bottle")
        assert activity_type == 'bottle'
        # 4 oz = 118.294 ml, should round to 118
        assert 115 <= details['amount_ml'] <= 120

    def test_parse_bottle_default(self):
        """Test parsing bottle command defaults to 120ml."""
        activity_type, details = parse_command("log a bottle")
        assert activity_type == 'bottle'
        assert details['amount_ml'] == 120

    def test_parse_sleep(self):
        """Test parsing sleep command."""
        activity_type, details = parse_command("start sleep")
        assert activity_type == 'sleep'

    def test_parse_nap(self):
        """Test parsing nap command."""
        activity_type, details = parse_command("log a nap")
        assert activity_type == 'sleep'

    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive."""
        commands = [
            "LOG A POO",
            "Log A Poo",
            "log a poo",
            "LoG a PoO"
        ]
        for cmd in commands:
            activity_type, details = parse_command(cmd)
            assert activity_type == 'diaper'
            assert details['type'] == 'poo'

    def test_parse_empty_command(self):
        """Test parsing empty command returns None."""
        activity_type, details = parse_command("")
        assert activity_type is None
        assert details == {}

    def test_parse_invalid_command(self):
        """Test parsing invalid command returns None."""
        activity_type, details = parse_command("invalid command xyz")
        assert activity_type is None
        assert details == {}

    def test_parse_complex_poo_command(self):
        """Test parsing complex poo command with multiple details."""
        activity_type, details = parse_command("log a small brown poo")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'
        assert details['poo_size'] == 'small'
        assert details['poo_color'] == 'brown'


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_check_returns_json(self, client):
        """Test that health check returns JSON response."""
        response = client.get('/health')
        assert response.content_type == 'application/json'

    def test_health_check_contains_status(self, client):
        """Test that health check contains status field."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] in ['healthy', 'degraded']

    def test_health_check_contains_timestamp(self, client):
        """Test that health check contains timestamp."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'timestamp' in data

    def test_health_check_contains_huckleberry_status(self, client):
        """Test that health check contains Huckleberry connection status."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'huckleberry_connected' in data


class TestWebhookEndpoint:
    """Test suite for /webhook endpoint."""

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_requires_secret(self, client):
        """Test that webhook requires valid secret."""
        response = client.post('/webhook',
                               json={'command': 'log a poo'},
                               content_type='application/json')
        assert response.status_code == 401

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_invalid_secret(self, client):
        """Test that webhook rejects invalid secret."""
        response = client.post('/webhook',
                               json={'command': 'log a poo', 'secret': 'wrong-secret'},
                               content_type='application/json')
        assert response.status_code == 401

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_no_command(self, client):
        """Test that webhook requires command parameter."""
        response = client.post('/webhook',
                               json={'secret': 'test-secret'},
                               content_type='application/json')
        assert response.status_code == 400

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_no_json(self, client):
        """Test that webhook requires JSON data."""
        response = client.post('/webhook')
        assert response.status_code == 400

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    @patch('main.huckleberry_api')
    @patch('main.child_id', 'test-child-id')
    def test_webhook_invalid_command(self, mock_api, client):
        """Test that webhook handles invalid commands."""
        response = client.post('/webhook',
                               json={'command': 'invalid xyz', 'secret': 'test-secret'},
                               content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False


class TestCommandsEndpoint:
    """Test suite for /commands endpoint."""

    def test_commands_returns_json(self, client):
        """Test that commands endpoint returns JSON."""
        response = client.get('/commands')
        assert response.content_type == 'application/json'
        assert response.status_code == 200

    def test_commands_contains_categories(self, client):
        """Test that commands endpoint contains all activity categories."""
        response = client.get('/commands')
        data = json.loads(response.data)
        assert 'commands' in data
        commands = data['commands']
        assert 'breastfeeding' in commands
        assert 'bottle' in commands
        assert 'diaper' in commands
        assert 'sleep' in commands

    def test_commands_contains_examples(self, client):
        """Test that commands endpoint contains command examples."""
        response = client.get('/commands')
        data = json.loads(response.data)
        commands = data['commands']
        assert len(commands['breastfeeding']['simple']) > 0
        assert len(commands['bottle']['simple']) > 0
        assert len(commands['diaper']['simple']) > 0
        assert len(commands['sleep']['simple']) > 0


class TestTestEndpoint:
    """Test suite for /test/<activity> endpoint."""

    def test_test_endpoint_invalid_activity(self, client):
        """Test that test endpoint rejects invalid activity types."""
        response = client.get('/test/invalid')
        assert response.status_code == 400

    def test_test_endpoint_feed(self, client):
        """Test that test endpoint accepts feed activity."""
        response = client.get('/test/feed?side=left')
        data = json.loads(response.data)
        assert 'test_mode' in data
        assert data['test_mode'] is True

    def test_test_endpoint_bottle(self, client):
        """Test that test endpoint accepts bottle activity."""
        response = client.get('/test/bottle?amount=120')
        data = json.loads(response.data)
        assert 'test_mode' in data

    def test_test_endpoint_poo(self, client):
        """Test that test endpoint accepts poo activity."""
        response = client.get('/test/poo?size=big&color=yellow')
        data = json.loads(response.data)
        assert 'test_mode' in data

    def test_test_endpoint_sleep(self, client):
        """Test that test endpoint accepts sleep activity."""
        response = client.get('/test/sleep')
        data = json.loads(response.data)
        assert 'test_mode' in data


class TestErrorHandlers:
    """Test suite for error handlers."""

    def test_404_handler(self, client):
        """Test that 404 errors are handled properly."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is False
        assert 'available_endpoints' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
