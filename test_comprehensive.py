"""
Comprehensive integration and edge case tests for Huckleberry Alexa Integration.

This test suite covers:
- Edge cases and error conditions
- Integration flows
- Real-world command variations
- Huckleberry API mocking
- Security scenarios
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, call
from main import app, parse_command, log_activity, init_huckleberry


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_huckleberry_api():
    """Mock Huckleberry API with all methods."""
    mock_api = MagicMock()
    mock_api.get_children.return_value = [
        {'id': 'child-123', 'name': 'Kai De Ville'}
    ]
    mock_api.start_feeding.return_value = True
    mock_api.log_bottle.return_value = True
    mock_api.log_diaper.return_value = True
    mock_api.start_sleep.return_value = True
    return mock_api


class TestCommandParsingEdgeCases:
    """Test edge cases in command parsing."""

    def test_parse_with_extra_whitespace(self):
        """Test parsing commands with extra whitespace."""
        activity_type, details = parse_command("  log a poo  ")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'

    def test_parse_with_multiple_spaces(self):
        """Test parsing commands with multiple spaces."""
        activity_type, details = parse_command("log  a  big  yellow  poo")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'
        assert details['poo_size'] == 'large'
        assert details['poo_color'] == 'yellow'

    def test_parse_mixed_case(self):
        """Test parsing with mixed case."""
        commands = [
            ("Log A Big YELLOW Poo", 'diaper', {'type': 'poo', 'poo_size': 'large', 'poo_color': 'yellow'}),
            ("LOG A LEFT FEED", 'feed', {'side': 'left'}),
            ("Start SLEEP", 'sleep', {}),
        ]
        for cmd, expected_type, expected_details in commands:
            activity_type, details = parse_command(cmd)
            assert activity_type == expected_type
            for key, value in expected_details.items():
                assert details[key] == value

    def test_parse_bottle_variations(self):
        """Test various bottle amount formats."""
        test_cases = [
            ("log a 90ml bottle", 90),
            ("log a 180ml bottle", 180),
            ("log a 3oz bottle", 88),  # ~88.72 ml
            ("log a 5oz bottle", 147),  # ~147.87 ml
            ("log a 4.5oz bottle", 133),  # ~133.08 ml
        ]
        for cmd, expected_ml in test_cases:
            activity_type, details = parse_command(cmd)
            assert activity_type == 'bottle'
            # Allow 2ml tolerance for rounding
            assert abs(details['amount_ml'] - expected_ml) <= 2

    def test_parse_poo_and_pee_variations(self):
        """Test different ways to say poo and pee."""
        variations = [
            "log a poo and pee",
            "log a poo and a pee",
            "log poo and pee",
        ]
        for cmd in variations:
            activity_type, details = parse_command(cmd)
            assert activity_type == 'diaper'
            assert details['type'] == 'both'

    def test_parse_huge_as_large(self):
        """Test that 'huge' is treated as large."""
        activity_type, details = parse_command("log a huge poo")
        assert details['poo_size'] == 'large'

    def test_parse_tiny_as_small(self):
        """Test that 'tiny' is treated as small."""
        activity_type, details = parse_command("log a tiny poo")
        assert details['poo_size'] == 'small'

    def test_parse_priority_bottle_over_feed(self):
        """Test that 'bottle feed' is recognized as bottle."""
        activity_type, details = parse_command("log a bottle feed")
        assert activity_type == 'bottle'
        assert details['amount_ml'] == 120

    def test_parse_napping_keyword(self):
        """Test 'napping' keyword for sleep."""
        activity_type, details = parse_command("baby is napping")
        assert activity_type == 'sleep'

    def test_parse_nursing_keyword(self):
        """Test 'nursing' keyword for feeding."""
        activity_type, details = parse_command("log a left nursing session")
        assert activity_type == 'feed'
        assert details['side'] == 'left'

    def test_parse_multiple_descriptors(self):
        """Test poo with size, color, and other words."""
        activity_type, details = parse_command("log a really big dark poo")
        assert activity_type == 'diaper'
        assert details['type'] == 'poo'
        assert details['poo_size'] == 'large'
        assert details['poo_color'] == 'dark'

    def test_parse_null_command(self):
        """Test None command."""
        activity_type, details = parse_command(None)
        assert activity_type is None
        assert details == {}

    def test_parse_numeric_only(self):
        """Test command with only numbers."""
        activity_type, details = parse_command("123456")
        assert activity_type is None


class TestLogActivityWithMocking:
    """Test log_activity function with mocked Huckleberry API."""

    def test_log_feed_left(self, mock_huckleberry_api):
        """Test logging left feed."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('feed', {'side': 'left'})

            assert result['success'] is True
            assert 'left' in result['message'].lower()
            mock_huckleberry_api.start_feeding.assert_called_once_with('child-123', side='left')

    def test_log_feed_right(self, mock_huckleberry_api):
        """Test logging right feed."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('feed', {'side': 'right'})

            assert result['success'] is True
            assert 'right' in result['message'].lower()
            mock_huckleberry_api.start_feeding.assert_called_once_with('child-123', side='right')

    def test_log_bottle_custom_amount(self, mock_huckleberry_api):
        """Test logging bottle with custom amount."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('bottle', {'amount_ml': 150})

            assert result['success'] is True
            assert '150' in result['message']
            mock_huckleberry_api.log_bottle.assert_called_once_with('child-123', amount_ml=150)

    def test_log_diaper_poo_only(self, mock_huckleberry_api):
        """Test logging poo-only diaper."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('diaper', {'type': 'poo'})

            assert result['success'] is True
            mock_huckleberry_api.log_diaper.assert_called_once()
            call_args = mock_huckleberry_api.log_diaper.call_args
            assert call_args.kwargs['child_id'] == 'child-123'
            assert call_args.kwargs['diaper_type'] == 'poo'

    def test_log_diaper_poo_with_details(self, mock_huckleberry_api):
        """Test logging poo with size and color."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('diaper', {
                'type': 'poo',
                'poo_size': 'large',
                'poo_color': 'yellow'
            })

            assert result['success'] is True
            assert 'large' in result['message'].lower()
            assert 'yellow' in result['message'].lower()

            call_args = mock_huckleberry_api.log_diaper.call_args
            assert call_args.kwargs['poo_consistency'] == 'large'
            assert call_args.kwargs['poo_color'] == 'yellow'

    def test_log_diaper_both(self, mock_huckleberry_api):
        """Test logging both poo and pee."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('diaper', {'type': 'both', 'pee_amount': 'large'})

            assert result['success'] is True
            call_args = mock_huckleberry_api.log_diaper.call_args
            assert call_args.kwargs['diaper_type'] == 'both'
            assert call_args.kwargs['pee_amount'] == 'large'

    def test_log_sleep(self, mock_huckleberry_api):
        """Test logging sleep."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('sleep', {})

            assert result['success'] is True
            assert 'sleep' in result['message'].lower()
            mock_huckleberry_api.start_sleep.assert_called_once_with('child-123')

    def test_log_activity_no_api(self):
        """Test log_activity when API not initialized."""
        with patch('main.huckleberry_api', None), \
             patch('main.child_id', None):
            result = log_activity('feed', {'side': 'left'})

            assert result['success'] is False
            assert 'not initialized' in result['message'].lower()

    def test_log_activity_api_exception(self, mock_huckleberry_api):
        """Test log_activity when API raises exception."""
        mock_huckleberry_api.start_feeding.side_effect = Exception("API Error")

        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('feed', {'side': 'left'})

            assert result['success'] is False
            assert 'failed' in result['message'].lower()

    def test_log_activity_unknown_type(self, mock_huckleberry_api):
        """Test log_activity with unknown activity type."""
        with patch('main.huckleberry_api', mock_huckleberry_api), \
             patch('main.child_id', 'child-123'):
            result = log_activity('unknown', {})

            assert result['success'] is False
            assert 'unknown' in result['message'].lower()


class TestWebhookEndpointComprehensive:
    """Comprehensive webhook endpoint tests."""

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret-123'})
    @patch('main.huckleberry_api')
    @patch('main.child_id', 'child-123')
    def test_webhook_successful_poo(self, mock_api, client):
        """Test successful poo logging via webhook."""
        mock_api.log_diaper.return_value = True

        response = client.post('/webhook',
                               json={'command': 'log a big yellow poo', 'secret': 'test-secret-123'},
                               content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['activity_type'] == 'diaper'

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret-123'})
    @patch('main.huckleberry_api')
    @patch('main.child_id', 'child-123')
    def test_webhook_successful_feed(self, mock_api, client):
        """Test successful feed logging via webhook."""
        mock_api.start_feeding.return_value = True

        response = client.post('/webhook',
                               json={'command': 'log a left feed', 'secret': 'test-secret-123'},
                               content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['activity_type'] == 'feed'

    @patch.dict('os.environ', {'WEBHOOK_SECRET': ''})
    def test_webhook_empty_secret_env(self, client):
        """Test webhook with empty secret in environment."""
        response = client.post('/webhook',
                               json={'command': 'log a poo', 'secret': ''},
                               content_type='application/json')
        assert response.status_code == 401

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_case_sensitive_secret(self, client):
        """Test that webhook secret is case-sensitive."""
        response = client.post('/webhook',
                               json={'command': 'log a poo', 'secret': 'TEST-SECRET'},
                               content_type='application/json')
        assert response.status_code == 401

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_secret_with_spaces(self, client):
        """Test that webhook secret with spaces doesn't match."""
        response = client.post('/webhook',
                               json={'command': 'log a poo', 'secret': ' test-secret '},
                               content_type='application/json')
        assert response.status_code == 401

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_malformed_json(self, client):
        """Test webhook with malformed JSON."""
        response = client.post('/webhook',
                               data='not json',
                               content_type='application/json')
        assert response.status_code == 400

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'test-secret'})
    def test_webhook_json_array_instead_of_object(self, client):
        """Test webhook with JSON array instead of object."""
        response = client.post('/webhook',
                               json=['command', 'secret'],
                               content_type='application/json')
        assert response.status_code == 400


class TestInitHuckleberry:
    """Test Huckleberry API initialization."""

    @patch.dict('os.environ', {
        'HUCKLEBERRY_EMAIL': 'test@example.com',
        'HUCKLEBERRY_PASSWORD': 'password123',
        'CHILD_NAME': 'Test Child'
    })
    @patch('main.HuckleberryAPI')
    def test_init_success(self, mock_huckleberry_class):
        """Test successful Huckleberry initialization."""
        mock_api = MagicMock()
        mock_api.get_children.return_value = [
            {'id': 'child-123', 'name': 'Test Child'}
        ]
        mock_huckleberry_class.return_value = mock_api

        # Import to reset globals
        from main import init_huckleberry
        result = init_huckleberry()

        assert result is True
        mock_huckleberry_class.assert_called_once_with('test@example.com', 'password123')

    @patch.dict('os.environ', {
        'HUCKLEBERRY_EMAIL': 'test@example.com',
        'HUCKLEBERRY_PASSWORD': 'password123',
        'CHILD_NAME': 'Nonexistent Child'
    })
    @patch('main.HuckleberryAPI')
    def test_init_child_not_found(self, mock_huckleberry_class):
        """Test initialization when child not found."""
        mock_api = MagicMock()
        mock_api.get_children.return_value = [
            {'id': 'child-456', 'name': 'Different Child'}
        ]
        mock_huckleberry_class.return_value = mock_api

        from main import init_huckleberry
        result = init_huckleberry()

        assert result is False

    @patch.dict('os.environ', {
        'HUCKLEBERRY_EMAIL': '',
        'HUCKLEBERRY_PASSWORD': 'password123',
        'CHILD_NAME': 'Test Child'
    })
    def test_init_missing_email(self):
        """Test initialization with missing email."""
        from main import init_huckleberry
        result = init_huckleberry()

        assert result is False

    @patch.dict('os.environ', {
        'HUCKLEBERRY_EMAIL': 'test@example.com',
        'HUCKLEBERRY_PASSWORD': 'password123',
        'CHILD_NAME': 'Test Child'
    })
    @patch('main.HuckleberryAPI')
    def test_init_api_exception(self, mock_huckleberry_class):
        """Test initialization when API raises exception."""
        mock_huckleberry_class.side_effect = Exception("Connection failed")

        from main import init_huckleberry
        result = init_huckleberry()

        assert result is False


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_common_voice_commands(self):
        """Test commands as they might come from Alexa."""
        common_commands = [
            ("log a poo", 'diaper', 'poo'),
            ("log a pee", 'diaper', 'pee'),
            ("log a feed", 'feed', 'left'),
            ("log a bottle", 'bottle', 120),
            ("start sleep", 'sleep', None),
            ("log a big yellow poo", 'diaper', 'poo'),
            ("log a left feed", 'feed', 'left'),
            ("log a right feed", 'feed', 'right'),
        ]

        for cmd, expected_type, expected_detail in common_commands:
            activity_type, details = parse_command(cmd)
            assert activity_type == expected_type, f"Failed for command: {cmd}"

    @patch.dict('os.environ', {'WEBHOOK_SECRET': 'my-secret-key'})
    @patch('main.huckleberry_api')
    @patch('main.child_id', 'child-123')
    def test_multiple_webhooks_sequence(self, mock_api, client):
        """Test multiple webhook calls in sequence."""
        mock_api.log_diaper.return_value = True
        mock_api.start_feeding.return_value = True
        mock_api.log_bottle.return_value = True

        commands = [
            'log a poo',
            'log a feed',
            'log a bottle',
        ]

        for cmd in commands:
            response = client.post('/webhook',
                                   json={'command': cmd, 'secret': 'my-secret-key'},
                                   content_type='application/json')
            assert response.status_code == 200, f"Failed for command: {cmd}"


class TestEndpointAccessibility:
    """Test that all endpoints are accessible."""

    def test_health_endpoint_accessible(self, client):
        """Test health endpoint is accessible without auth."""
        response = client.get('/health')
        assert response.status_code in [200, 503]  # Either healthy or degraded is fine

    def test_commands_endpoint_accessible(self, client):
        """Test commands endpoint is accessible without auth."""
        response = client.get('/commands')
        assert response.status_code == 200

    def test_webhook_requires_auth(self, client):
        """Test webhook requires authentication."""
        response = client.post('/webhook', json={})
        assert response.status_code in [400, 401]  # Either missing data or auth

    def test_cors_not_enabled(self, client):
        """Test that CORS is not enabled (security)."""
        response = client.get('/health')
        assert 'Access-Control-Allow-Origin' not in response.headers


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
