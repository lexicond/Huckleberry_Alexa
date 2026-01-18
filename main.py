"""
Huckleberry Alexa Integration
A Flask web service that receives voice commands from Alexa (via IFTTT webhooks)
and logs baby care activities to the Huckleberry baby tracking app.

Author: Alex & Leila
Date: January 2026
"""

import os
import re
import logging
import secrets
from datetime import datetime
from typing import Dict, Tuple, Optional, Any

from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
from huckleberry_api import HuckleberryAPI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
HUCKLEBERRY_EMAIL = os.getenv('HUCKLEBERRY_EMAIL')
HUCKLEBERRY_PASSWORD = os.getenv('HUCKLEBERRY_PASSWORD')
CHILD_NAME = os.getenv('CHILD_NAME')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
TIMEZONE = os.getenv('TIMEZONE', 'Europe/London')  # Default to UK timezone
PORT = int(os.getenv('PORT', 5000))

# Constants
DEFAULT_BOTTLE_ML = 120
OZ_TO_ML_CONVERSION = 29.5735
DEFAULT_FEED_SIDE = 'left'
DEFAULT_DIAPER_TYPE = 'poo'
DEFAULT_PEE_AMOUNT = 'medium'

# Global variables
huckleberry_api: Optional[HuckleberryAPI] = None
child_id: Optional[str] = None


def init_huckleberry() -> bool:
    """
    Initialize Huckleberry API connection and get child ID.

    Returns:
        bool: True if initialization successful, False otherwise
    """
    global huckleberry_api, child_id

    try:
        if not all([HUCKLEBERRY_EMAIL, HUCKLEBERRY_PASSWORD, CHILD_NAME]):
            logger.error("Missing required environment variables")
            return False

        logger.info("Initializing Huckleberry API connection...")
        logger.info(f"Using timezone: {TIMEZONE}")
        huckleberry_api = HuckleberryAPI(HUCKLEBERRY_EMAIL, HUCKLEBERRY_PASSWORD, TIMEZONE)

        # Get children and find matching child
        children = huckleberry_api.get_children()
        logger.info(f"Found {len(children)} children in Huckleberry account")

        for child in children:
            if child.get('name') == CHILD_NAME:
                child_id = child.get('id')
                logger.info(f"Found child: {CHILD_NAME} with ID: {child_id}")
                return True

        logger.error(f"Child '{CHILD_NAME}' not found in Huckleberry account")
        return False

    except Exception as e:
        logger.error(f"Failed to initialize Huckleberry API: {str(e)}", exc_info=True)
        return False


def parse_command(command: str) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Parse voice command to identify activity type and details.

    Args:
        command: Raw voice command string from Alexa

    Returns:
        Tuple of (activity_type, details_dict) or (None, {}) if unable to parse

    Examples:
        "log a poo" -> ('diaper', {'type': 'poo'})
        "log a big yellow poo" -> ('diaper', {'type': 'poo', 'poo_size': 'large', 'poo_color': 'yellow'})
        "log a left feed" -> ('feed', {'side': 'left'})
        "log a 120ml bottle" -> ('bottle', {'amount_ml': 120})
    """
    if not command:
        return None, {}

    # Normalize command
    cmd = command.lower().strip()
    logger.info(f"Parsing command: {cmd}")

    # Activity type detection (in priority order)
    activity_type = None
    details: Dict[str, Any] = {}

    # 1. Check for bottle feeding
    bottle_keywords = ['bottle']
    if any(keyword in cmd for keyword in bottle_keywords):
        activity_type = 'bottle'

        # Extract amount (ml or oz)
        ml_match = re.search(r'(\d+)\s*ml', cmd)
        oz_match = re.search(r'(\d+(?:\.\d+)?)\s*oz', cmd)

        if ml_match:
            details['amount_ml'] = int(ml_match.group(1))
        elif oz_match:
            # Convert oz to ml
            oz_amount = float(oz_match.group(1))
            details['amount_ml'] = int(oz_amount * OZ_TO_ML_CONVERSION)
        else:
            # Default to 120ml
            details['amount_ml'] = DEFAULT_BOTTLE_ML

    # 2. Check for breastfeeding
    feed_keywords = ['feed', 'feeding', 'breast', 'nurse', 'nursing']
    if not activity_type and any(keyword in cmd for keyword in feed_keywords):
        activity_type = 'feed'

        # Determine side (left or right)
        if 'right' in cmd:
            details['side'] = 'right'
        elif 'left' in cmd:
            details['side'] = 'left'
        else:
            # Default to left
            details['side'] = DEFAULT_FEED_SIDE

    # 3. Check for sleep
    sleep_keywords = ['sleep', 'nap', 'sleeping', 'napping']
    if not activity_type and any(keyword in cmd for keyword in sleep_keywords):
        activity_type = 'sleep'

    # 4. Check for diaper (poo/pee)
    diaper_keywords = ['diaper', 'poo', 'poop', 'pee', 'wee', 'wet']
    if not activity_type and any(keyword in cmd for keyword in diaper_keywords):
        activity_type = 'diaper'

        # Determine diaper type
        has_poo = any(word in cmd for word in ['poo', 'poop'])
        has_pee = any(word in cmd for word in ['pee', 'wee', 'wet'])

        if has_poo and has_pee:
            details['type'] = 'both'
        elif has_poo:
            details['type'] = 'poo'
        elif has_pee:
            details['type'] = 'pee'
        else:
            # Default to poo if just "diaper" mentioned
            details['type'] = DEFAULT_DIAPER_TYPE

        # Extract poo details if applicable
        if details['type'] in ['poo', 'both']:
            # Size descriptors
            if any(word in cmd for word in ['big', 'large', 'huge']):
                details['poo_size'] = 'large'
            elif any(word in cmd for word in ['small', 'tiny', 'little']):
                details['poo_size'] = 'small'
            elif 'medium' in cmd:
                details['poo_size'] = 'medium'

            # Color descriptors
            if 'yellow' in cmd:
                details['poo_color'] = 'yellow'
            elif 'brown' in cmd:
                details['poo_color'] = 'brown'
            elif 'green' in cmd:
                details['poo_color'] = 'green'
            elif 'dark' in cmd:
                details['poo_color'] = 'dark'
            elif 'black' in cmd:
                details['poo_color'] = 'black'

        # Extract pee details if applicable
        if details['type'] in ['pee', 'both']:
            if any(word in cmd for word in ['big', 'large', 'huge']):
                details['pee_amount'] = 'large'
            elif any(word in cmd for word in ['small', 'tiny', 'little']):
                details['pee_amount'] = 'small'
            else:
                details['pee_amount'] = DEFAULT_PEE_AMOUNT

    if activity_type:
        logger.info(f"Parsed command -> Activity: {activity_type}, Details: {details}")
        return activity_type, details
    else:
        logger.warning(f"Unable to parse command: {cmd}")
        return None, {}


def log_activity(activity_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Log activity to Huckleberry using the API.

    Args:
        activity_type: Type of activity ('feed', 'bottle', 'diaper', 'sleep')
        details: Dictionary containing activity-specific details

    Returns:
        Dictionary with success status and message
    """
    global huckleberry_api, child_id

    if not huckleberry_api or not child_id:
        logger.error("Huckleberry API not initialized")
        return {
            'success': False,
            'message': 'Huckleberry API not initialized',
            'error': 'API connection not available'
        }

    try:
        logger.info(f"Logging {activity_type} activity with details: {details}")

        if activity_type == 'feed':
            # Start breastfeeding session
            side = details.get('side', DEFAULT_FEED_SIDE)
            huckleberry_api.start_feeding(child_id, side=side)
            message = f"Started {side} breastfeeding session"

        elif activity_type == 'bottle':
            # Log bottle feeding
            amount_ml = details.get('amount_ml', DEFAULT_BOTTLE_ML)
            huckleberry_api.log_bottle(child_id, amount_ml=amount_ml)
            message = f"Logged {amount_ml}ml bottle feed"

        elif activity_type == 'diaper':
            # Log diaper change
            diaper_type = details.get('type', DEFAULT_DIAPER_TYPE)

            # Prepare parameters based on type
            params = {'child_id': child_id, 'diaper_type': diaper_type}

            if diaper_type in ['poo', 'both']:
                if 'poo_size' in details:
                    params['poo_consistency'] = details['poo_size']
                if 'poo_color' in details:
                    params['poo_color'] = details['poo_color']

            if diaper_type in ['pee', 'both']:
                params['pee_amount'] = details.get('pee_amount', DEFAULT_PEE_AMOUNT)

            huckleberry_api.log_diaper(**params)

            # Build descriptive message
            desc = []
            if 'poo_size' in details:
                desc.append(details['poo_size'])
            if 'poo_color' in details:
                desc.append(details['poo_color'])
            desc.append(diaper_type)
            message = f"Logged {' '.join(desc)} diaper change"

        elif activity_type == 'sleep':
            # Start sleep session
            huckleberry_api.start_sleep(child_id)
            message = "Started sleep session"

        else:
            logger.error(f"Unknown activity type: {activity_type}")
            return {
                'success': False,
                'message': f'Unknown activity type: {activity_type}',
                'error': 'Invalid activity type'
            }

        logger.info(f"Successfully logged activity: {message}")
        return {
            'success': True,
            'message': message,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error logging activity: {str(e)}", exc_info=True)
        return {
            'success': False,
            'message': 'Failed to log activity to Huckleberry',
            'error': str(e)
        }


@app.route('/health', methods=['GET'])
def health_check() -> Response:
    """
    Health check endpoint for monitoring services.

    Returns:
        JSON response with status, timestamp, and Huckleberry connection status
    """
    huckleberry_connected = huckleberry_api is not None and child_id is not None

    response = {
        'status': 'healthy' if huckleberry_connected else 'degraded',
        'timestamp': datetime.utcnow().isoformat(),
        'huckleberry_connected': huckleberry_connected,
        'child_name': CHILD_NAME if huckleberry_connected else None,
        'service': 'Huckleberry Alexa Integration'
    }

    status_code = 200 if huckleberry_connected else 503
    return jsonify(response), status_code


@app.route('/webhook', methods=['POST'])
def webhook() -> Response:
    """
    Main webhook endpoint for IFTTT requests.

    Expected JSON body:
        {
            "command": "log a poo",
            "secret": "your-webhook-secret"
        }

    Returns:
        JSON response indicating success or failure
    """
    try:
        # Get request data
        data = request.get_json()

        if not data:
            logger.warning("Webhook called with no JSON data")
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Verify webhook secret (using constant-time comparison)
        provided_secret = data.get('secret')
        if not provided_secret or not secrets.compare_digest(
            provided_secret, WEBHOOK_SECRET or ""
        ):
            logger.warning(f"Webhook called with invalid secret from IP: {request.remote_addr}")
            return jsonify({
                'success': False,
                'message': 'Invalid webhook secret'
            }), 401

        # Get command
        command = data.get('command')
        if not command:
            logger.warning("Webhook called with no command")
            return jsonify({
                'success': False,
                'message': 'No command provided'
            }), 400

        logger.info(f"Webhook received command: {command}")

        # Parse command
        activity_type, details = parse_command(command)

        if not activity_type:
            logger.warning(f"Unable to parse command: {command}")
            return jsonify({
                'success': False,
                'message': 'Unable to parse command',
                'command': command
            }), 400

        # Log activity
        result = log_activity(activity_type, details)

        status_code = 200 if result.get('success') else 500
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


@app.route('/commands', methods=['GET'])
def list_commands() -> Response:
    """
    List all available voice commands.

    Returns:
        JSON response with command examples organized by category
    """
    commands = {
        'breastfeeding': {
            'simple': [
                'log a feed',
                'log a feeding'
            ],
            'detailed': [
                'log a left feed',
                'log a right feed',
                'log a left nursing session'
            ]
        },
        'bottle': {
            'simple': [
                'log a bottle'
            ],
            'detailed': [
                'log a 120ml bottle',
                'log a 4oz bottle',
                'log a 150ml bottle'
            ]
        },
        'diaper': {
            'simple': [
                'log a poo',
                'log a pee',
                'log a diaper',
                'log a poo and pee'
            ],
            'detailed': [
                'log a big poo',
                'log a yellow poo',
                'log a big yellow poo',
                'log a small brown poo',
                'log a medium green poo'
            ],
            'sizes': ['big', 'medium', 'small'],
            'colors': ['yellow', 'brown', 'green', 'dark', 'black']
        },
        'sleep': {
            'simple': [
                'start sleep',
                'log a nap',
                'start sleeping'
            ]
        },
        'notes': [
            'Commands are case-insensitive',
            'Default side for feeding is left',
            'Default amount for bottle is 120ml',
            'Default type for diaper is poo',
            'Sizes and colors are optional for diapers'
        ]
    }

    return jsonify({
        'service': 'Huckleberry Alexa Integration',
        'commands': commands,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@app.route('/test/<activity>', methods=['GET'])
def test_activity(activity: str) -> Response:
    """
    Manual testing endpoint for development.

    Args:
        activity: Activity type to test (feed, bottle, diaper, sleep, poo, pee)

    Query parameters:
        - For feed: side=left|right
        - For bottle: amount=120 (ml)
        - For diaper/poo: size=big|medium|small, color=yellow|brown|green|dark|black
        - For pee: size=big|medium|small

    Examples:
        /test/feed?side=left
        /test/bottle?amount=120
        /test/poo?size=big&color=yellow
        /test/sleep

    Returns:
        JSON response with test results
    """
    logger.info(f"Test endpoint called for activity: {activity}")

    # Build details from query parameters
    details: Dict[str, Any] = {}

    # Map common activity names
    activity_map = {
        'poo': 'diaper',
        'pee': 'diaper',
        'feed': 'feed',
        'feeding': 'feed',
        'bottle': 'bottle',
        'sleep': 'sleep',
        'nap': 'sleep'
    }

    activity_type = activity_map.get(activity.lower())

    if not activity_type:
        return jsonify({
            'success': False,
            'message': f'Unknown activity type: {activity}',
            'valid_types': list(activity_map.keys())
        }), 400

    # Extract query parameters based on activity type
    if activity_type == 'feed':
        details['side'] = request.args.get('side', DEFAULT_FEED_SIDE)

    elif activity_type == 'bottle':
        amount = request.args.get('amount', str(DEFAULT_BOTTLE_ML))
        try:
            details['amount_ml'] = int(amount)
        except ValueError:
            logger.warning(f"Invalid bottle amount '{amount}', using default {DEFAULT_BOTTLE_ML}ml")
            details['amount_ml'] = DEFAULT_BOTTLE_ML

    elif activity_type == 'diaper':
        # Determine type based on original activity name
        if activity.lower() == 'poo':
            details['type'] = 'poo'
        elif activity.lower() == 'pee':
            details['type'] = 'pee'
        else:
            details['type'] = request.args.get('type', DEFAULT_DIAPER_TYPE)

        # Get size and color if provided
        if 'size' in request.args:
            if details['type'] in ['poo', 'both']:
                details['poo_size'] = request.args.get('size')
            if details['type'] in ['pee', 'both']:
                details['pee_amount'] = request.args.get('size')

        if 'color' in request.args and details['type'] in ['poo', 'both']:
            details['poo_color'] = request.args.get('color')

    # Log the activity
    result = log_activity(activity_type, details)

    status_code = 200 if result.get('success') else 500
    return jsonify({
        **result,
        'test_mode': True,
        'original_activity': activity,
        'mapped_activity': activity_type
    }), status_code


@app.errorhandler(404)
def not_found(error) -> Response:
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found',
        'available_endpoints': ['/health', '/webhook', '/commands', '/test/<activity>']
    }), 404


@app.errorhandler(500)
def internal_error(error) -> Response:
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


# Initialize Huckleberry on startup
@app.before_request
def ensure_huckleberry_initialized():
    """Ensure Huckleberry API is initialized before handling requests."""
    global huckleberry_api, child_id

    # Skip initialization for health check to avoid startup delays
    if request.path == '/health':
        return

    if not huckleberry_api or not child_id:
        logger.info("Huckleberry API not initialized, attempting initialization...")
        if not init_huckleberry():
            logger.error("Failed to initialize Huckleberry API")
            return jsonify({
                'success': False,
                'message': 'Service unavailable - Huckleberry API initialization failed',
                'error': 'Could not connect to Huckleberry'
            }), 503


if __name__ == '__main__':
    logger.info("Starting Huckleberry Alexa Integration service...")
    logger.info(f"Port: {PORT}")
    logger.info(f"Child Name: {CHILD_NAME}")
    logger.info(f"Environment variables loaded: {all([HUCKLEBERRY_EMAIL, HUCKLEBERRY_PASSWORD, CHILD_NAME, WEBHOOK_SECRET])}")

    # Initialize Huckleberry on startup
    init_huckleberry()

    # Run Flask app
    app.run(host='0.0.0.0', port=PORT, debug=False)
