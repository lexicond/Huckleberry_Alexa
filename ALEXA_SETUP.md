# Alexa & IFTTT Setup Guide

This guide will walk you through setting up Alexa voice commands to trigger your Huckleberry logging service via IFTTT webhooks.

## Overview

The integration flow works like this:

```
Alexa → Alexa Routine → IFTTrigger Virtual Device → IFTTT Applet → Your Webhook Service → Huckleberry API
```

**Time Required:** 30-60 minutes for initial setup
**Cost:** Free (IFTTT free tier supports up to 2 applets, Pro tier supports unlimited)

## Prerequisites

Before you begin, make sure you have:

- ✅ Deployed your Huckleberry Alexa service (Railway/Render)
- ✅ Your webhook URL (e.g., `https://your-app.railway.app`)
- ✅ Your webhook secret from environment variables
- ✅ Amazon Alexa device (Echo, Echo Dot, etc.)
- ✅ Alexa app on your phone (iOS/Android)
- ✅ IFTTT account

## Part 1: IFTTT Setup

### Step 1.1: Create IFTTT Account

1. Go to [IFTTT.com](https://ifttt.com)
2. Click "Sign up" and create an account
3. Verify your email address
4. Consider upgrading to Pro for unlimited applets (optional, $5/month)

### Step 1.2: Enable Webhooks Service

1. Go to [IFTTT Webhooks](https://ifttt.com/maker_webhooks)
2. Click "Connect" to enable Webhooks service
3. Click "Documentation" to view your webhook key
4. **Save your webhook key** - you'll need it later

### Step 1.3: Create Your First Applet (Poo Logging)

Let's create an applet for logging a basic poo as an example:

1. **Go to Create Applet:**
   - Visit [IFTTT Create](https://ifttt.com/create)
   - Click "If This" (the trigger)

2. **Set up the Trigger:**
   - Search for "IFTTrigger"
   - Select "IFTTrigger"
   - Choose "Trigger a scene" (you might need to connect IFTTrigger first)
   - **Device name:** `log_poo` (use underscores, no spaces)
   - Click "Create trigger"

3. **Set up the Action:**
   - Click "Then That"
   - Search for "Webhooks"
   - Select "Webhooks"
   - Choose "Make a web request"

4. **Configure the Webhook:**
   - **URL:** `https://your-app.railway.app/webhook`
   - **Method:** `POST`
   - **Content Type:** `application/json`
   - **Body:**
     ```json
     {"command": "log a poo", "secret": "your-webhook-secret-here"}
     ```
   - Click "Create action"

5. **Finish:**
   - Review and click "Continue"
   - Give it a name: "Log poo to Huckleberry"
   - Click "Finish"

### Step 1.4: Create Additional Applets

Repeat the process above for each command you want to support. Here are recommended applets:

#### Basic Applets (Priority)

| Device Name | Command | Description |
|-------------|---------|-------------|
| `log_poo` | `log a poo` | Basic poo |
| `log_pee` | `log a pee` | Basic pee |
| `log_feed` | `log a feed` | Start left breastfeeding |
| `log_bottle` | `log a bottle` | Log 120ml bottle |
| `log_sleep` | `start sleep` | Start sleep session |

#### Detailed Applets (Optional)

| Device Name | Command | Description |
|-------------|---------|-------------|
| `log_big_poo` | `log a big poo` | Large poo |
| `log_yellow_poo` | `log a yellow poo` | Yellow poo |
| `log_big_yellow_poo` | `log a big yellow poo` | Large yellow poo |
| `log_left_feed` | `log a left feed` | Left breastfeeding |
| `log_right_feed` | `log a right feed` | Right breastfeeding |
| `log_poo_and_pee` | `log a poo and pee` | Both poo and pee |

**Pro Tip:** Start with 5-10 most common commands, then add more as needed.

### Step 1.5: Test Your Applets

Test each applet manually before connecting to Alexa:

1. Open the applet in IFTTT
2. Click "Check now" or manually trigger it
3. Check IFTTT Activity log (Settings → Activity)
4. Verify the webhook was called successfully
5. Check your Huckleberry app to see if activity was logged

## Part 2: Alexa IFTTrigger Skill Setup

### Step 2.1: Enable IFTTrigger Skill

1. **Open Alexa App:**
   - Open Alexa app on your phone
   - Tap "More" (bottom right)
   - Tap "Skills & Games"

2. **Find IFTTrigger:**
   - Search for "IFTTrigger"
   - Tap "IFTTrigger" skill by "IFTTT"
   - Tap "Enable to Use"

3. **Link Accounts:**
   - Sign in with your IFTTT account
   - Grant permissions
   - Wait for "Successfully linked" message

### Step 2.2: Discover Devices

1. **In Alexa App:**
   - Tap "More" → "Skills & Games"
   - Tap "Your Skills" → "IFTTrigger"
   - Tap "Settings"
   - Tap "Discover Devices" or say "Alexa, discover devices"

2. **Wait for Discovery:**
   - This can take 20-30 seconds
   - Alexa will say "Discovery starting..." then "I found X devices"

3. **Verify Devices:**
   - Go to "Devices" tab in Alexa app
   - You should see all your IFTTrigger devices (log_poo, log_pee, etc.)

**Troubleshooting:** If devices don't appear:
- Make sure applets are enabled in IFTTT
- Wait a few minutes and try "Discover devices" again
- Disable and re-enable the IFTTrigger skill

## Part 3: Alexa Routines Setup

Now create Alexa Routines to trigger your devices with natural voice commands.

### Step 3.1: Create First Routine (Log Poo)

1. **Open Alexa App:**
   - Tap "More" (bottom right)
   - Tap "Routines"
   - Tap "+" icon (top right) to create new routine

2. **Name Your Routine:**
   - Enter routine name: "Log a poo"
   - This is just for you, not the voice command

3. **Set When This Happens (Trigger):**
   - Tap "When this happens"
   - Select "Voice"
   - Enter: `log a poo`
   - Tap "Next"
   - **Optional:** Add variations like "log poo", "logged a poo"

4. **Set Add Action:**
   - Tap "Add action"
   - Select "Smart Home"
   - Scroll down and find your "log_poo" device
   - Select "Power" → "On"
   - Tap "Next"

5. **Choose Device (Optional):**
   - Select which Alexa device responds
   - Or leave as "All devices"

6. **Save:**
   - Tap "Save" (top right)

### Step 3.2: Test Your Routine

1. Say: **"Alexa, log a poo"**
2. Alexa should respond: "OK"
3. Check your Huckleberry app - you should see a new poo entry!

**If it doesn't work:**
- Check IFTTT Activity log for errors
- Check your webhook service logs (Railway/Render dashboard)
- Try triggering the IFTTT applet manually
- Verify webhook URL and secret are correct

### Step 3.3: Create More Routines

Create routines for each command. Here are examples:

#### Basic Routines

| Routine Name | Voice Command | IFTTrigger Device |
|--------------|---------------|-------------------|
| Log a poo | "log a poo" | log_poo |
| Log a pee | "log a pee" | log_pee |
| Log a feed | "log a feed" | log_feed |
| Log a bottle | "log a bottle" | log_bottle |
| Start sleep | "start sleep" | log_sleep |

#### Advanced Routines with Variations

For "Log a poo" you might add these variations:
- "log a poo"
- "log poo"
- "logged a poo"
- "baby pooped"

For "Log a feed" you might add:
- "log a feed"
- "log feed"
- "start a feed"
- "baby's eating"

**Pro Tip:** Keep voice commands short and distinct to avoid confusion.

## Part 4: Advanced Voice Commands

### Detailed Poo Commands

For detailed poo tracking (size and color), create separate routines:

| Voice Command | IFTTrigger Device | IFTTT Command |
|---------------|-------------------|---------------|
| "log a big poo" | log_big_poo | `log a big poo` |
| "log a small poo" | log_small_poo | `log a small poo` |
| "log a yellow poo" | log_yellow_poo | `log a yellow poo` |
| "log a big yellow poo" | log_big_yellow_poo | `log a big yellow poo` |

### Side-Specific Feeding

| Voice Command | IFTTrigger Device | IFTTT Command |
|---------------|-------------------|---------------|
| "log a left feed" | log_left_feed | `log a left feed` |
| "log a right feed" | log_right_feed | `log a right feed` |

### Bottle with Amount

| Voice Command | IFTTrigger Device | IFTTT Command |
|---------------|-------------------|---------------|
| "log a 120ml bottle" | log_120ml_bottle | `log a 120ml bottle` |
| "log a 4oz bottle" | log_4oz_bottle | `log a 4oz bottle` |

## Part 5: Testing & Verification

### Test Each Command

Go through each routine and test it:

1. **Say the command** to Alexa
2. **Listen for response** - Should say "OK"
3. **Check IFTTT Activity** - Should show triggered applet
4. **Check webhook logs** - Should show successful request
5. **Check Huckleberry** - Should show logged activity

### Common Test Commands

```
"Alexa, log a poo"
"Alexa, log a pee"
"Alexa, log a feed"
"Alexa, log a left feed"
"Alexa, log a right feed"
"Alexa, log a bottle"
"Alexa, start sleep"
"Alexa, log a big yellow poo"
```

## Part 6: Optimization & Tips

### Voice Command Best Practices

1. **Keep it short:** "log a poo" is better than "please log a poo diaper"
2. **Be distinct:** Avoid similar-sounding commands
3. **Use natural language:** Commands you'll actually remember when tired
4. **Add variations:** Include common ways you might say it

### Recommended Daily Workflows

**Morning routine:**
```
"Alexa, log a poo"
"Alexa, log a feed"
```

**After feeding:**
```
"Alexa, log a left feed"  (or right)
```

**After diaper change:**
```
"Alexa, log a big yellow poo"
```

**Before nap:**
```
"Alexa, start sleep"
```

### Multiple Users

If both parents will use this:

1. **Use same IFTTT account** - Applets work for anyone
2. **Add routines to all devices** - Set routines to work on "All devices"
3. **Share webhook URL** - Both can test endpoints

## Part 7: Troubleshooting

### "Alexa doesn't understand the command"

**Possible causes:**
- Routine not created or disabled
- Voice command doesn't match exactly
- Alexa misheard you

**Solutions:**
- Check routine is enabled in Alexa app
- Try speaking more clearly
- Add command variations
- Check Alexa app history to see what she heard

### "Alexa says OK but nothing logs"

**Possible causes:**
- IFTTT applet not triggered
- Webhook URL wrong
- Webhook secret wrong
- Service down

**Solutions:**
- Check IFTTT Activity log
- Manually trigger IFTTT applet
- Verify webhook URL and secret
- Check Railway/Render service status
- Check webhook service logs

### "IFTTT applet triggers but webhook fails"

**Possible causes:**
- Wrong webhook URL
- Wrong webhook secret
- Service down
- Network issues

**Solutions:**
- Test webhook manually with curl:
  ```bash
  curl -X POST https://your-app.railway.app/webhook \
    -H "Content-Type: application/json" \
    -d '{"command": "log a poo", "secret": "your-secret"}'
  ```
- Check Railway/Render logs
- Verify environment variables
- Check health endpoint: `https://your-app.railway.app/health`

### "IFTTrigger devices not appearing"

**Possible causes:**
- Skill not enabled
- Applets not created
- Discovery not run

**Solutions:**
- Disable and re-enable IFTTrigger skill
- Wait 5 minutes after creating applets
- Run device discovery again
- Restart Alexa app

### "Command parsing errors"

**Possible causes:**
- Unsupported command format
- Typo in IFTTT applet command

**Solutions:**
- Check `/commands` endpoint for valid formats
- Test command with `/test/<activity>` endpoint
- Verify IFTTT applet command matches expected format
- Check webhook service logs for parsing errors

## Part 8: Maintenance

### Weekly Checks

- Review IFTTT Activity log for failures
- Check webhook service health endpoint
- Verify all commands still working

### Monthly Tasks

- Review and optimize routines
- Add new commands as needed
- Check Railway/Render usage/costs
- Update webhook secret (every 3-6 months)

### When Baby's Routine Changes

Update your most-used commands:
- Add bottle commands if switching to bottles
- Add nap variations as sleep patterns change
- Update default amounts (e.g., larger bottle sizes)

## Part 9: Advanced Setups

### Using IFTTT Filters

IFTTT Pro users can use filter code to customize webhooks:

```javascript
// Example: Add timestamp to command
let command = IFTTrigger.SceneName;
let timestamp = Meta.currentUserTime.format("YYYY-MM-DD HH:mm:ss");

Webhooks.makeWebRequest.setBody(JSON.stringify({
  "command": command,
  "secret": "your-secret",
  "timestamp": timestamp
}));
```

### Creating Grouped Commands

Create routines with multiple actions:

**Example: "Bedtime Routine"**
1. Log a feed
2. Log a diaper change
3. Start sleep

This requires multiple IFTTrigger devices in sequence.

### Location-Based Triggers

IFTTT Pro supports location triggers:
- Auto-log when arriving home with baby
- Reminders based on location

## Part 10: Quick Reference

### Essential IFTTT Applets

Minimal setup (5 applets):
1. log_poo → "log a poo"
2. log_pee → "log a pee"
3. log_feed → "log a feed"
4. log_bottle → "log a bottle"
5. log_sleep → "start sleep"

### Essential Alexa Routines

Match the 5 applets above with voice commands.

### Testing Checklist

Before going live:
- [ ] All IFTTT applets created and enabled
- [ ] IFTTrigger skill enabled
- [ ] Devices discovered in Alexa app
- [ ] All routines created
- [ ] Each command tested successfully
- [ ] Webhook service healthy (check /health)
- [ ] Checked Huckleberry app for logged activities

## Support & Resources

- **Main Documentation:** [README.md](README.md)
- **IFTTT Help:** [IFTTT Support](https://help.ifttt.com)
- **Alexa Routines Help:** [Amazon Alexa Routines](https://www.amazon.com/gp/help/customer/display.html?nodeId=G202200080)
- **IFTTrigger Skill:** [Amazon Alexa Skills](https://www.amazon.com/IFTTT-IFTTrigger/dp/B08F7DY5Z4)

## Success!

Once everything is set up, you should be able to:

✅ Say "Alexa, log a poo" and have it automatically logged
✅ Track all baby activities hands-free
✅ Focus on your baby instead of your phone

**Congratulations!** You've successfully set up voice-activated baby tracking! 🎉👶

---

**Pro Tip:** Print out a cheat sheet of your most common commands and stick it on the fridge for quick reference!
