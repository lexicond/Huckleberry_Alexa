# Huckleberry Alexa Integration

A production-ready Flask web service that receives voice commands from Alexa (via Voice Monkey webhooks) and logs baby care activities to the Huckleberry baby tracking app.

Perfect for busy parents who need hands-free tracking while their hands are full with their baby! 👶

## Features

- 🎙️ **Voice-Activated Logging** - Use Alexa to log activities hands-free
- ⏱️ **Timer Controls** - Start, stop, pause, and resume feeding and sleep timers
- 🍼 **Multiple Activity Types** - Track breastfeeding, bottles, diapers, and sleep
- 🔒 **Secure** - Webhook secret verification protects your data
- 📊 **Detailed Tracking** - Support for sizes, colors, amounts, sides, and more
- 🚀 **Easy Deployment** - Ready for Railway, Render, or Heroku
- ✅ **Well-Tested** - Comprehensive test suite included
- 📝 **Rich Documentation** - Clear setup guides and examples

## Supported Activities

### 🤱 Breastfeeding (with Timer Controls)
- **Start**: "Alexa, start a breastfeed on left" or "Alexa, start a breastfeed on right"
- **Stop**: "Alexa, stop breastfeed" (saves timed session)
- **Pause**: "Alexa, pause breastfeed" (temporarily pause timer)
- **Resume**: "Alexa, resume breastfeed" (continue paused session)
- **Switch**: "Alexa, switch feeding side" (left ↔ right)
- **Cancel**: "Alexa, cancel breastfeed" (discard without saving)

### 🍼 Bottle Feeding
- Simple: "Alexa, log a bottle" (default 120ml)
- Detailed: "Alexa, log a 150ml bottle"
- Automatic oz to ml conversion supported

### 💩 Diaper Changes
- Simple: "Alexa, log a poo" or "Alexa, log a wee"
- Combined: "Alexa, log a wee and poo"
- Detailed: "Alexa, log a big yellow poo"
- Sizes: big/large, medium, small
- Colors: yellow, brown, green, dark, black

### 😴 Sleep Tracking (with Timer Controls)
- **Start**: "Alexa, start sleep"
- **Stop**: "Alexa, stop sleep" (saves timed session)
- **Pause**: "Alexa, pause sleep" (temporarily pause)
- **Resume**: "Alexa, resume sleep" (continue paused session)
- **Cancel**: "Alexa, cancel sleep" (discard without saving)

## Quick Start (15 Minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/lexicond/Huckleberry_Alexa.git
   cd Huckleberry_Alexa
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Deploy to Railway**
   - Push to GitHub
   - Connect Railway to your GitHub repo
   - Add environment variables in Railway dashboard
   - Deploy!

4. **Set up Voice Monkey** (see [PHONE_SETUP_GUIDE.md](PHONE_SETUP_GUIDE.md) for full details)
   - Create account at https://voicemonkey.io
   - Enable Voice Monkey Alexa skill
   - Create Flows for each command with webhook POST requests
   - Create Alexa Routines to trigger Flows

5. **Test it out!**
   ```
   "Alexa, log a poo"
   ```

## Installation

### Prerequisites

- Python 3.11+
- Huckleberry account with baby profile
- Voice Monkey account (free)
- Alexa device
- Railway/Render account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/lexicond/Huckleberry_Alexa.git
   cd Huckleberry_Alexa
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your actual values:
   ```env
   HUCKLEBERRY_EMAIL=your-email@example.com
   HUCKLEBERRY_PASSWORD=YourActualPassword
   CHILD_NAME=Your Child Name
   WEBHOOK_SECRET=your-random-secret-here-32-chars-minimum
   TIMEZONE=Europe/London
   PORT=5000
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Test it's working**
   ```bash
   curl http://localhost:5000/health
   ```

## Deployment

### Railway (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Railway project**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Set environment variables**

   In Railway dashboard, add these variables:
   ```
   HUCKLEBERRY_EMAIL=your-email@example.com
   HUCKLEBERRY_PASSWORD=YourActualPassword
   CHILD_NAME=Your Child Name
   WEBHOOK_SECRET=generate-a-random-secret-here
   TIMEZONE=Europe/London
   ```

4. **Generate domain**
   - Railway automatically generates a domain like `your-app.railway.app`
   - Use this URL in your Voice Monkey webhook Flows

5. **Monitor deployment**
   - Check logs in Railway dashboard
   - Visit `https://your-app.railway.app/health` to verify

### Render (Alternative)

1. **Create Render account**
   - Go to [Render](https://render.com)
   - Sign up with GitHub

2. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure service**
   - Name: `huckleberry-alexa`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`

4. **Set environment variables**
   - Add all variables from `.env.example`

5. **Deploy**
   - Render will automatically deploy
   - Use generated URL in Voice Monkey webhooks

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `HUCKLEBERRY_EMAIL` | Yes | Your Huckleberry account email | `your-email@example.com` |
| `HUCKLEBERRY_PASSWORD` | Yes | Your Huckleberry account password | `YourPassword123` |
| `CHILD_NAME` | Yes | Child's name as shown in Huckleberry | `Your Child Name` |
| `WEBHOOK_SECRET` | Yes | Random secret for webhook security | `abc123xyz...` (32+ chars) |
| `TIMEZONE` | Yes | Your timezone for Huckleberry API | `Europe/London`, `America/New_York` |
| `PORT` | No | Server port (Railway sets automatically) | `5000` |

### Generating Webhook Secret

Generate a secure random secret:

```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# Or use any password generator for 32+ characters
```

## Voice Monkey Setup

See [PHONE_SETUP_GUIDE.md](PHONE_SETUP_GUIDE.md) for detailed phone-friendly instructions.

### Quick Summary:

1. **Create Voice Monkey account** at https://voicemonkey.io
2. **Enable Alexa skill** - Search for "Voice Monkey" in Alexa app
3. **Create Flows** - One for each command you want to use
4. **Configure webhook** in each Flow:
   - URL: `https://your-app.railway.app/webhook`
   - Method: `POST`
   - Headers: `Content-Type: application/json`
   - Body: `{"command": "log a poo", "secret": "your-webhook-secret"}`
5. **Create Alexa Routines** - Link your voice phrases to Voice Monkey custom actions

## API Documentation

### GET /health

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-18T10:30:00.000Z",
  "huckleberry_connected": true,
  "child_name": "Your Child Name",
  "service": "Huckleberry Alexa Integration"
}
```

**Status Codes:**
- `200` - Service healthy and Huckleberry connected
- `503` - Service degraded (Huckleberry not connected)

### POST /webhook

Main webhook endpoint for Voice Monkey requests.

**Request:**
```json
{
  "command": "log a big yellow poo",
  "secret": "your-webhook-secret"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Logged large yellow poo diaper change",
  "activity_type": "diaper",
  "details": {
    "type": "poo",
    "poo_size": "large",
    "poo_color": "yellow"
  },
  "timestamp": "2026-01-18T10:30:00.000Z"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Unable to parse command",
  "command": "invalid command"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (invalid command, missing parameters)
- `401` - Unauthorized (invalid secret)
- `500` - Server error (Huckleberry API failure)

### GET /commands

List all available voice commands.

**Response:**
```json
{
  "service": "Huckleberry Alexa Integration",
  "commands": {
    "breastfeeding": {
      "start": ["start a breastfeed on left", "start a breastfeed on right"],
      "control": ["stop breastfeed", "pause breastfeed", "resume breastfeed", "switch feeding side", "cancel breastfeed"]
    },
    "bottle": {
      "simple": ["log a bottle"],
      "detailed": ["log a 120ml bottle", "log a 150ml bottle"]
    },
    "diaper": {
      "simple": ["log a poo", "log a wee", "log a wee and poo"],
      "detailed": ["log a big yellow poo"]
    },
    "sleep": {
      "start": ["start sleep"],
      "control": ["stop sleep", "pause sleep", "resume sleep", "cancel sleep"]
    }
  },
  "timestamp": "2026-01-18T10:30:00.000Z"
}
```

### GET /test/&lt;activity&gt;

Manual testing endpoint for development.

**Examples:**

Test breastfeeding:
```bash
curl "http://localhost:5000/test/feed?side=left"
```

Test bottle:
```bash
curl "http://localhost:5000/test/bottle?amount=120"
```

Test diaper:
```bash
curl "http://localhost:5000/test/poo?size=big&color=yellow"
```

Test sleep:
```bash
curl "http://localhost:5000/test/sleep"
```

## Voice Commands Reference

### Breastfeeding Commands

**Starting a Feed:**
```
"Alexa, start a breastfeed on left"  → Start left breastfeeding timer
"Alexa, start a breastfeed on right" → Start right breastfeeding timer
```

**Controlling the Timer:**
```
"Alexa, stop breastfeed"          → Save and complete the feeding session
"Alexa, pause breastfeed"         → Pause the timer temporarily
"Alexa, resume breastfeed"        → Resume paused feeding
"Alexa, switch feeding side"      → Switch between left and right
"Alexa, cancel breastfeed"        → Discard session without saving
```

### Bottle Feeding Commands

```
"Alexa, log a bottle"            → Log 120ml bottle (default)
"Alexa, log a 120ml bottle"      → Log 120ml bottle
"Alexa, log a 150ml bottle"      → Log 150ml bottle
```

### Diaper Commands

```
"Alexa, log a poo"              → Log basic poo
"Alexa, log a wee"              → Log basic wee/pee
"Alexa, log a pee"              → Log basic pee
"Alexa, log a wee and poo"      → Log both

"Alexa, log a big poo"          → Log large poo
"Alexa, log a small poo"        → Log small poo
"Alexa, log a yellow poo"       → Log yellow poo
"Alexa, log a big yellow poo"   → Log large yellow poo
```

### Sleep Commands

**Starting Sleep:**
```
"Alexa, start sleep"            → Start sleep timer
```

**Controlling the Timer:**
```
"Alexa, stop sleep"            → Save and complete the sleep session
"Alexa, pause sleep"           → Pause the timer temporarily
"Alexa, resume sleep"          → Resume paused sleep
"Alexa, cancel sleep"          → Discard session without saving
```

## Complete Voice Monkey Flow Configurations

For each command, create a Flow in Voice Monkey with these settings:

**URL:** `https://your-app.railway.app/webhook`
**Method:** `POST`
**Headers:** `Content-Type: application/json`

### Breastfeeding Flows

**Start Left Feed:**
```json
{"command": "start a breastfeed on left", "secret": "your-webhook-secret"}
```

**Start Right Feed:**
```json
{"command": "start a breastfeed on right", "secret": "your-webhook-secret"}
```

**Stop Breastfeed:**
```json
{"command": "stop breastfeed", "secret": "your-webhook-secret"}
```

**Pause Breastfeed:**
```json
{"command": "pause breastfeed", "secret": "your-webhook-secret"}
```

**Resume Breastfeed:**
```json
{"command": "resume breastfeed", "secret": "your-webhook-secret"}
```

**Switch Feeding Side:**
```json
{"command": "switch feeding side", "secret": "your-webhook-secret"}
```

### Diaper Flows

**Log Poo:**
```json
{"command": "log a poo", "secret": "your-webhook-secret"}
```

**Log Wee:**
```json
{"command": "log a wee", "secret": "your-webhook-secret"}
```

**Log Wee and Poo:**
```json
{"command": "log a wee and poo", "secret": "your-webhook-secret"}
```

### Sleep Flows

**Start Sleep:**
```json
{"command": "start sleep", "secret": "your-webhook-secret"}
```

**Stop Sleep:**
```json
{"command": "stop sleep", "secret": "your-webhook-secret"}
```

**Pause Sleep:**
```json
{"command": "pause sleep", "secret": "your-webhook-secret"}
```

**Resume Sleep:**
```json
{"command": "resume sleep", "secret": "your-webhook-secret"}
```

### Bottle Flow

**Log Bottle:**
```json
{"command": "log a bottle", "secret": "your-webhook-secret"}
```

## Testing

### Run Unit Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest test_main.py -v

# Run specific test
pytest test_main.py::TestCommandParsing::test_parse_simple_poo -v

# Run with coverage
pytest test_main.py --cov=main --cov-report=html
```

### Manual Testing with cURL

**Health check:**
```bash
curl https://your-app.railway.app/health
```

**List commands:**
```bash
curl https://your-app.railway.app/commands
```

**Test webhook (replace secret):**
```bash
curl -X POST https://your-app.railway.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"command": "log a poo", "secret": "your-webhook-secret"}'
```

**Test specific activity:**
```bash
curl "https://your-app.railway.app/test/poo?size=big&color=yellow"
```

## Troubleshooting

### Huckleberry Connection Issues

**Problem:** Health check shows `huckleberry_connected: false`

**Solutions:**
- Check `HUCKLEBERRY_EMAIL` and `HUCKLEBERRY_PASSWORD` are correct
- Verify `CHILD_NAME` exactly matches name in Huckleberry app (case-sensitive!)
- Ensure `TIMEZONE` is set correctly (e.g., `Europe/London`, `America/New_York`)
- Check Railway/Render logs for error messages
- Try logging into Huckleberry web app to verify credentials

### Webhook Secret Errors

**Problem:** Receiving 401 Unauthorized errors

**Solutions:**
- Verify `WEBHOOK_SECRET` in Railway matches secret in Voice Monkey Flows
- Ensure no extra spaces or quotes in secret
- Secret must be in the JSON body, not headers
- Check Voice Monkey Flow configuration

### Command Not Parsing

**Problem:** Commands not being recognized

**Solutions:**
- Check exact voice command in Railway logs
- Compare with examples in `/commands` endpoint
- Test similar command using `/test/<activity>` endpoint
- Check logs for parsing errors
- Verify JSON body format in Voice Monkey Flow

### Voice Monkey Not Triggering

**Problem:** Alexa command not triggering Voice Monkey

**Solutions:**
- Verify Voice Monkey Alexa skill is enabled
- Check Flow is enabled in Voice Monkey dashboard
- Test Flow manually in Voice Monkey
- Verify Alexa routine uses correct custom action phrase
- Check Voice Monkey logs for triggers

### Deployment Issues

**Problem:** Railway/Render deployment failing

**Solutions:**
- Check all environment variables are set
- Verify `requirements.txt` is in repository
- Check deployment logs for specific errors
- Ensure Python version is 3.11+
- Verify `Procfile` exists and is correct

## Security Notes

⚠️ **Important Security Practices:**

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use strong webhook secret** - Minimum 32 characters
3. **Use HTTPS in production** - Railway/Render provide this automatically
4. **Rotate secrets periodically** - Change webhook secret every few months
5. **Monitor logs** - Watch for invalid secret attempts
6. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`

## Development

### Project Structure

```
Huckleberry_Alexa/
├── main.py                  # Main Flask application
├── test_parsing.py          # Command parsing tests
├── test_comprehensive.py    # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── Procfile                # Deployment configuration
├── runtime.txt             # Python version
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── PHONE_SETUP_GUIDE.md    # Phone-friendly setup guide
├── TECHNICAL_REVIEW.md     # Code review and analysis
└── LICENSE                 # License file
```

### Code Quality

The codebase follows these best practices:

- ✅ Type hints for all functions
- ✅ Docstrings with examples
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Security best practices (constant-time secret comparison)
- ✅ DRY principle (no duplication)
- ✅ Separation of concerns
- ✅ Comprehensive test coverage

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest -v`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Monitoring

### Health Monitoring

Set up monitoring to check `/health` endpoint:

- **Uptime Robot**: Free monitoring service
- **Pingdom**: Advanced monitoring
- **Railway/Render**: Built-in health checks

Configure health check:
- URL: `https://your-app.railway.app/health`
- Interval: 5 minutes
- Expected: HTTP 200 status
- Alert if: Status not 200 for 2 consecutive checks

### Log Monitoring

View logs in real-time:

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and view logs
railway login
railway logs
```

**Render:**
- View logs in Render dashboard
- Real-time log streaming available

## FAQ

**Q: How much does this cost?**
A: Railway/Render offer free tiers perfect for this application. Voice Monkey has a free tier with unlimited virtual devices.

**Q: Can I track multiple children?**
A: Currently supports one child. Multi-child support is planned for future updates.

**Q: How do I stop a feeding or sleep session?**
A: Use voice commands like "Alexa, stop breastfeed" or "Alexa, stop sleep" to save and complete the timed session.

**Q: What's the difference between stop and cancel?**
A: "Stop" saves the timed session to Huckleberry. "Cancel" discards it without saving.

**Q: What if I say the command wrong?**
A: The service will return an error but won't log anything. Check the logs to see what was received.

**Q: Can I use this without Alexa?**
A: Yes! You can use the test endpoints or call the webhook directly from any HTTP client.

**Q: Is my data secure?**
A: Yes. All credentials are encrypted in Railway/Render. Webhook requests require a secret. Communication uses HTTPS.

**Q: Can I self-host this?**
A: Absolutely! Deploy to any platform that supports Python Flask apps.

**Q: What happened to IFTTT support?**
A: Amazon discontinued the Alexa IFTTT integration in October 2023. Voice Monkey is the modern replacement with better features.

## Roadmap

### Future Features

- [ ] Query recent activities ("Alexa, when was the last feed?")
- [ ] Multiple children support
- [ ] Voice confirmation via Alexa TTS
- [ ] Natural language improvements
- [ ] Web dashboard for monitoring
- [ ] Custom activity types
- [ ] Activity templates
- [ ] Pumping/expressing milk tracking

## Support

- 📧 Issues: [GitHub Issues](https://github.com/lexicond/Huckleberry_Alexa/issues)
- 📖 Documentation: See [PHONE_SETUP_GUIDE.md](PHONE_SETUP_GUIDE.md)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/lexicond/Huckleberry_Alexa/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ for Alex, Leila, and baby Kai
- Uses the excellent [py-huckleberry-api](https://github.com/Woyken/py-huckleberry-api) library
- Powered by Flask, Voice Monkey, and Alexa

---

Made with ☕ and 😴 by sleep-deprived parents
