# Huckleberry Alexa Integration

A production-ready Flask web service that receives voice commands from Alexa (via IFTTT webhooks) and logs baby care activities to the Huckleberry baby tracking app.

Perfect for busy parents who need hands-free tracking while their hands are full with their baby! 👶

## Features

- 🎙️ **Voice-Activated Logging** - Use Alexa to log activities hands-free
- 🍼 **Multiple Activity Types** - Track breastfeeding, bottles, diapers, and sleep
- 🔒 **Secure** - Webhook secret verification protects your data
- 📊 **Detailed Tracking** - Support for sizes, colors, amounts, and more
- 🚀 **Easy Deployment** - Ready for Railway, Render, or Heroku
- ✅ **Well-Tested** - Comprehensive test suite included
- 📝 **Rich Documentation** - Clear setup guides and examples

## Supported Activities

### 🤱 Breastfeeding
- Simple: "Alexa, log a feed"
- Detailed: "Alexa, log a left feed" or "Alexa, log a right feed"
- Default: Left side if not specified

### 🍼 Bottle Feeding
- Simple: "Alexa, log a bottle"
- Detailed: "Alexa, log a 120ml bottle" or "Alexa, log a 4oz bottle"
- Default: 120ml if not specified
- Automatic oz to ml conversion (1 oz = 29.5735 ml)

### 💩 Diaper Changes
- Simple: "Alexa, log a poo" or "Alexa, log a pee"
- Combined: "Alexa, log a poo and pee"
- Detailed: "Alexa, log a big yellow poo"
- Sizes: big/large, medium, small
- Colors: yellow, brown, green, dark, black

### 😴 Sleep Tracking
- Simple: "Alexa, start sleep" or "Alexa, log a nap"

## Quick Start (5 Minutes)

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

3. **Deploy to Railway** (or skip to Local Development)
   - Push to GitHub
   - Connect Railway to your GitHub repo
   - Add environment variables in Railway dashboard
   - Deploy!

4. **Set up IFTTT** (see [ALEXA_SETUP.md](ALEXA_SETUP.md) for details)
   - Enable IFTTrigger skill in Alexa
   - Create IFTTT applets for each command
   - Create Alexa routines for voice phrases

5. **Test it out!**
   ```
   "Alexa, log a poo"
   ```

## Installation

### Prerequisites

- Python 3.11+
- Huckleberry account with baby profile
- IFTTT account
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
   HUCKLEBERRY_EMAIL=leila@esmails.net
   HUCKLEBERRY_PASSWORD=YourActualPassword
   CHILD_NAME=Kai De Ville
   WEBHOOK_SECRET=your-random-secret-here-32-chars-minimum
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
   HUCKLEBERRY_EMAIL=leila@esmails.net
   HUCKLEBERRY_PASSWORD=YourActualPassword
   CHILD_NAME=Kai De Ville
   WEBHOOK_SECRET=generate-a-random-secret-here
   ```

4. **Generate domain**
   - Railway automatically generates a domain like `your-app.railway.app`
   - Use this URL in your IFTTT webhooks

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
   - Use generated URL in IFTTT webhooks

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `HUCKLEBERRY_EMAIL` | Yes | Your Huckleberry account email | `leila@esmails.net` |
| `HUCKLEBERRY_PASSWORD` | Yes | Your Huckleberry account password | `YourPassword123` |
| `CHILD_NAME` | Yes | Child's name as shown in Huckleberry | `Kai De Ville` |
| `WEBHOOK_SECRET` | Yes | Random secret for webhook security | `abc123xyz...` (32+ chars) |
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

## API Documentation

### GET /health

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-18T10:30:00.000Z",
  "huckleberry_connected": true,
  "child_name": "Kai De Ville",
  "service": "Huckleberry Alexa Integration"
}
```

**Status Codes:**
- `200` - Service healthy and Huckleberry connected
- `503` - Service degraded (Huckleberry not connected)

### POST /webhook

Main webhook endpoint for IFTTT requests.

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
      "simple": ["log a feed", "log a feeding"],
      "detailed": ["log a left feed", "log a right feed"]
    },
    "bottle": {
      "simple": ["log a bottle"],
      "detailed": ["log a 120ml bottle", "log a 4oz bottle"]
    },
    "diaper": {
      "simple": ["log a poo", "log a pee", "log a poo and pee"],
      "detailed": ["log a big yellow poo", "log a small brown poo"]
    },
    "sleep": {
      "simple": ["start sleep", "log a nap"]
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

**Query Parameters:**

| Activity | Parameters | Values |
|----------|------------|--------|
| feed | `side` | `left`, `right` |
| bottle | `amount` | Number in ml (e.g., `120`) |
| poo | `size`, `color` | Size: `big`, `medium`, `small`<br>Color: `yellow`, `brown`, `green`, `dark`, `black` |
| pee | `size` | `big`, `medium`, `small` |
| sleep | None | - |

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

## Voice Commands Reference

### Breastfeeding Commands

```
"Alexa, log a feed"              → Start left breastfeeding
"Alexa, log a left feed"         → Start left breastfeeding
"Alexa, log a right feed"        → Start right breastfeeding
"Alexa, log a nursing session"  → Start left breastfeeding
```

### Bottle Feeding Commands

```
"Alexa, log a bottle"            → Log 120ml bottle (default)
"Alexa, log a 120ml bottle"     → Log 120ml bottle
"Alexa, log a 4oz bottle"       → Log 4oz bottle (~118ml)
"Alexa, log a 150ml bottle"     → Log 150ml bottle
```

### Diaper Commands

```
"Alexa, log a poo"              → Log basic poo
"Alexa, log a pee"              → Log basic pee
"Alexa, log a diaper"           → Log basic poo (default)
"Alexa, log a poo and pee"      → Log both

"Alexa, log a big poo"          → Log large poo
"Alexa, log a small poo"        → Log small poo
"Alexa, log a medium poo"       → Log medium poo

"Alexa, log a yellow poo"       → Log yellow poo
"Alexa, log a brown poo"        → Log brown poo
"Alexa, log a green poo"        → Log green poo

"Alexa, log a big yellow poo"   → Log large yellow poo
"Alexa, log a small brown poo"  → Log small brown poo
```

### Sleep Commands

```
"Alexa, start sleep"            → Start sleep session
"Alexa, log a nap"              → Start sleep session
"Alexa, start sleeping"         → Start sleep session
```

## Troubleshooting

### Huckleberry Connection Issues

**Problem:** Health check shows `huckleberry_connected: false`

**Solutions:**
- Check `HUCKLEBERRY_EMAIL` and `HUCKLEBERRY_PASSWORD` are correct
- Verify `CHILD_NAME` exactly matches name in Huckleberry app
- Check Railway/Render logs for error messages
- Try logging into Huckleberry web app to verify credentials

### Webhook Secret Errors

**Problem:** Receiving 401 Unauthorized errors

**Solutions:**
- Verify `WEBHOOK_SECRET` in Railway matches secret in IFTTT
- Ensure no extra spaces or quotes in secret
- Regenerate secret if needed
- Check IFTTT webhook URL includes correct secret

### Command Not Parsing

**Problem:** Commands not being recognized

**Solutions:**
- Check exact voice command in IFTTT applet history
- Compare with examples in `/commands` endpoint
- Test similar command using `/test/<activity>` endpoint
- Check logs for parsing errors

### IFTTT Webhook Not Triggering

**Problem:** Alexa command not triggering IFTTT

**Solutions:**
- Verify IFTTrigger device is discovered in Alexa app
- Check IFTTT applet is enabled
- Test applet manually in IFTTT app
- Verify Alexa routine is set up correctly
- Check IFTTT activity log for triggers

### Deployment Issues

**Problem:** Railway/Render deployment failing

**Solutions:**
- Check all environment variables are set
- Verify `requirements.txt` is in repository
- Check deployment logs for specific errors
- Ensure Python version is 3.11+
- Verify `Procfile` exists and is correct

### Railway Port Issues

**Problem:** Application not responding after deployment

**Solutions:**
- Don't set PORT variable in Railway (it sets automatically)
- Ensure app binds to `0.0.0.0` not `localhost`
- Check Railway logs for startup errors

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
├── main.py              # Main Flask application
├── test_main.py         # Unit and integration tests
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment configuration
├── runtime.txt         # Python version
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── ALEXA_SETUP.md      # Alexa/IFTTT setup guide
└── LICENSE             # License file
```

### Code Quality

The codebase follows these best practices:

- ✅ Type hints for all functions
- ✅ Docstrings with examples
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Security best practices
- ✅ DRY principle (no duplication)
- ✅ Separation of concerns
- ✅ Comprehensive test coverage

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest test_main.py -v`)
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
A: Railway/Render offer free tiers that are perfect for this application. IFTTT has a free tier with limited applets.

**Q: Can I track multiple children?**
A: Currently supports one child. Multi-child support is planned for Phase 2.

**Q: How do I stop a feeding session?**
A: Currently you need to stop it manually in the Huckleberry app. Voice-based completion is planned for Phase 2.

**Q: What if I say the command wrong?**
A: The service will return an error but won't log anything. Check the logs to see what was received.

**Q: Can I use this without Alexa?**
A: Yes! You can use the test endpoints or call the webhook directly from any HTTP client.

**Q: Is my data secure?**
A: Yes. All credentials are encrypted in Railway/Render. Webhook requests require a secret. Communication uses HTTPS.

**Q: Can I self-host this?**
A: Absolutely! Deploy to any platform that supports Python Flask apps.

## Roadmap

### Phase 2 Features (Planned)

- [ ] Stop/complete ongoing activities ("Alexa, stop feeding")
- [ ] Query recent activities ("Alexa, when was the last feed?")
- [ ] Multiple children support
- [ ] Voice confirmation via Alexa TTS
- [ ] Natural language improvements
- [ ] Web dashboard for monitoring
- [ ] Custom activity types
- [ ] Activity templates

## Support

- 📧 Email: [Create an issue](https://github.com/lexicond/Huckleberry_Alexa/issues)
- 📖 Documentation: See [ALEXA_SETUP.md](ALEXA_SETUP.md)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/lexicond/Huckleberry_Alexa/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ for Alex, Leila, and baby Kai
- Uses the excellent [huckleberry-api](https://github.com/basnijholt/huckleberry-api) library
- Powered by Flask, IFTTT, and Alexa

---

Made with ☕ and 😴 by sleep-deprived parents
