# Voice Monkey Setup Guide

Complete phone-friendly guide for setting up Voice Monkey with Huckleberry Alexa Integration.

## What is Voice Monkey?

Voice Monkey is a free service that creates virtual smart home devices for Alexa. It allows you to trigger webhooks (HTTP requests) from Alexa voice commands via Alexa Routines.

**Why Voice Monkey?**
- ✅ Free tier with unlimited virtual devices
- ✅ Direct webhook POST requests to your Railway app
- ✅ More reliable than discontinued IFTTT integration
- ✅ Easy setup on phone or computer
- ✅ Well-documented and actively maintained

---

## Setup Overview (30 minutes)

1. Create Voice Monkey account
2. Enable Voice Monkey Alexa skill
3. Create Flows for each command
4. Create Alexa Routines
5. Test your commands

---

## Part 1: Create Voice Monkey Account (5 minutes)

### Step 1: Sign Up

1. **Open browser** on your phone
2. **Go to**: https://voicemonkey.io
3. **Click "Get Started"** or "Sign Up"
4. **Sign in with Amazon** - Use the same Amazon account linked to your Alexa device
5. **Complete signup** - You'll get a free account

### Step 2: Confirm Account

1. **Check your email** for confirmation
2. **Click the confirmation link**
3. **You're ready!**

---

## Part 2: Enable Voice Monkey Alexa Skill (5 minutes)

### Step 3: Find the Skill

1. **Open Alexa app** on your phone
2. **Tap "More"** (bottom right)
3. **Tap "Skills & Games"**
4. **Search for**: `Voice Monkey`
5. **Select**: "Voice Monkey - Smart Home + Routine Triggers + TTS"

### Step 4: Enable and Link

1. **Tap "Enable to Use"**
2. **Tap "Link Account"** when prompted
3. **Log in** with your Voice Monkey account (it will open in browser)
4. **Allow permissions**
5. **Close browser** and return to Alexa app

### Step 5: Discover Devices

1. **In Alexa app**, tap "Devices" (bottom)
2. **Tap "+" icon** (top right)
3. **Tap "Add Device"**
4. **Scroll down and tap "Other"**
5. **Tap "Discover Devices"**
6. **Wait 20-30 seconds** for discovery to complete

---

## Part 3: Create Flows (15 minutes)

Now you'll create a "Flow" in Voice Monkey for each voice command. Each Flow sends a webhook POST request to your Railway app.

### Important Information You'll Need:

**Your Railway Webhook URL:**
```
https://huckleberryalexa-production.up.railway.app/webhook
```

**Your Webhook Secret:**
```
B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt
```

### How to Create a Flow:

1. **Go to Voice Monkey website**: https://voicemonkey.io
2. **Log in** if not already
3. **Click "Flows"** in the navigation menu
4. **Click "Create New Flow"**
5. **Name the Flow** (e.g., "Log Poo")
6. **Click "Add Action"** → Select **"Web Request"**
7. **Configure the Web Request** (see specific configurations below)
8. **Save the Flow**
9. **Copy the custom action phrase** (e.g., `vm-log-poo`)

---

## Flow Configurations

For each Flow below, use these common settings:

**URL:** `https://huckleberryalexa-production.up.railway.app/webhook`
**Method:** `POST`
**Headers:** `Content-Type: application/json`

Then use the specific **Body** for each command:

### 🍼 Feeding Commands

#### Flow #1: Start Left Feed
- **Name**: `Start Left Feed`
- **Body**:
```json
{"command": "start a breastfeed on left", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```
- **Custom Action**: Copy the generated phrase (e.g., `vm-start-left-feed`)

#### Flow #2: Start Right Feed
- **Name**: `Start Right Feed`
- **Body**:
```json
{"command": "start a breastfeed on right", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #3: Stop Breastfeed
- **Name**: `Stop Breastfeed`
- **Body**:
```json
{"command": "stop breastfeed", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #4: Pause Breastfeed
- **Name**: `Pause Breastfeed`
- **Body**:
```json
{"command": "pause breastfeed", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #5: Resume Breastfeed
- **Name**: `Resume Breastfeed`
- **Body**:
```json
{"command": "resume breastfeed", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #6: Switch Feeding Side
- **Name**: `Switch Feeding Side`
- **Body**:
```json
{"command": "switch feeding side", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

### 💩 Diaper Commands

#### Flow #7: Log Poo
- **Name**: `Log Poo`
- **Body**:
```json
{"command": "log a poo", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #8: Log Wee
- **Name**: `Log Wee`
- **Body**:
```json
{"command": "log a wee", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #9: Log Wee and Poo
- **Name**: `Log Wee and Poo`
- **Body**:
```json
{"command": "log a wee and poo", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

### 😴 Sleep Commands

#### Flow #10: Start Sleep
- **Name**: `Start Sleep`
- **Body**:
```json
{"command": "start sleep", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #11: Stop Sleep
- **Name**: `Stop Sleep`
- **Body**:
```json
{"command": "stop sleep", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #12: Pause Sleep
- **Name**: `Pause Sleep`
- **Body**:
```json
{"command": "pause sleep", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

#### Flow #13: Resume Sleep
- **Name**: `Resume Sleep`
- **Body**:
```json
{"command": "resume sleep", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

### 🍼 Bottle Command

#### Flow #14: Log Bottle
- **Name**: `Log Bottle`
- **Body**:
```json
{"command": "log a bottle", "secret": "B72yvGFuT6xmJxHMqJvqwknxA7RDb8Lt"}
```

---

## Part 4: Create Alexa Routines (10 minutes)

Now link your voice commands to the Flows you created.

### How to Create an Alexa Routine:

1. **Open Alexa app**
2. **Tap "More"** (bottom right)
3. **Tap "Routines"**
4. **Tap "+" icon** (top right)
5. **Tap "When this happens"** → Select **"Voice"**
6. **Enter your voice phrase** (e.g., "log a poo")
7. **Tap "Next"**
8. **Tap "Add action"**
9. **Scroll down and tap "Custom"**
10. **Enter the custom action phrase** from your Voice Monkey Flow (e.g., `vm-log-poo`)
11. **Tap "Next"**
12. **Tap "Save"** at the top right

### Recommended Routines:

#### Routine #1: Log Poo
- **When**: Voice → `log a poo`
- **Action**: Custom → `vm-log-poo` (or whatever your Flow's custom action is)

#### Routine #2: Log Wee
- **When**: Voice → `log a wee`
- **Action**: Custom → `vm-log-wee`

#### Routine #3: Log Wee and Poo
- **When**: Voice → `log a wee and poo`
- **Action**: Custom → `vm-log-wee-and-poo`

#### Routine #4: Start Left Feed
- **When**: Voice → `start a breastfeed on left`
- **Action**: Custom → `vm-start-left-feed`

#### Routine #5: Start Right Feed
- **When**: Voice → `start a breastfeed on right`
- **Action**: Custom → `vm-start-right-feed`

#### Routine #6: Stop Breastfeed
- **When**: Voice → `stop breastfeed`
- **Action**: Custom → `vm-stop-breastfeed`

#### Routine #7: Pause Breastfeed
- **When**: Voice → `pause breastfeed`
- **Action**: Custom → `vm-pause-breastfeed`

#### Routine #8: Resume Breastfeed
- **When**: Voice → `resume breastfeed`
- **Action**: Custom → `vm-resume-breastfeed`

#### Routine #9: Switch Feeding Side
- **When**: Voice → `switch feeding side`
- **Action**: Custom → `vm-switch-feeding-side`

#### Routine #10: Start Sleep
- **When**: Voice → `start sleep`
- **Action**: Custom → `vm-start-sleep`

#### Routine #11: Stop Sleep
- **When**: Voice → `stop sleep`
- **Action**: Custom → `vm-stop-sleep`

#### Routine #12: Pause Sleep
- **When**: Voice → `pause sleep`
- **Action**: Custom → `vm-pause-sleep`

#### Routine #13: Resume Sleep
- **When**: Voice → `resume sleep`
- **Action**: Custom → `vm-resume-sleep`

#### Routine #14: Log Bottle
- **When**: Voice → `log a bottle`
- **Action**: Custom → `vm-log-bottle`

---

## Part 5: Test Your Setup (5 minutes)

### Test Each Command:

1. **Say to Alexa**: "Alexa, log a poo"
2. **Check Railway logs**:
   - Open Railway dashboard on your phone
   - Tap your project
   - Tap "Deployments"
   - Tap "View Logs"
   - Look for: `Webhook received command: log a poo`
   - Should see: `Successfully logged activity`
3. **Check Huckleberry app** - Verify the activity appears

### If it doesn't work:

1. **Check Railway logs** for errors
2. **Test the Flow** manually in Voice Monkey dashboard
3. **Verify webhook secret** matches in both Railway and Voice Monkey
4. **Check Alexa routine** uses correct custom action phrase
5. **Try saying command again** clearly

---

## Quick Reference: Voice Commands

Once set up, you can say:

### Feeding
- "Alexa, start a breastfeed on left"
- "Alexa, start a breastfeed on right"
- "Alexa, stop breastfeed"
- "Alexa, pause breastfeed"
- "Alexa, resume breastfeed"
- "Alexa, switch feeding side"

### Diapers
- "Alexa, log a poo"
- "Alexa, log a wee"
- "Alexa, log a wee and poo"

### Sleep
- "Alexa, start sleep"
- "Alexa, stop sleep"
- "Alexa, pause sleep"
- "Alexa, resume sleep"

### Bottle
- "Alexa, log a bottle"

---

## Troubleshooting

### Alexa says "I don't know that"
- Check the Alexa Routine is enabled
- Verify you're saying the exact trigger phrase
- Try saying it more slowly and clearly

### Command triggers but nothing logs
- Check Railway logs for errors
- Verify webhook secret matches
- Test the Flow manually in Voice Monkey
- Check Huckleberry connection at `/health` endpoint

### 401 Unauthorized error in logs
- Webhook secret doesn't match
- Check both Railway environment variable and Voice Monkey Flow Body
- Make sure secret is in JSON body, not headers

### Flow doesn't appear in Voice Monkey
- Refresh the page
- Make sure you saved the Flow
- Check you're logged into the correct account

---

## Tips for Parents

### Suggested Minimum Setup:

If you don't want to set up all 14 commands, start with these essentials:

1. **Log Poo** - Most frequently needed
2. **Log Wee** - Second most common
3. **Start Left Feed** - For timing feeds
4. **Stop Breastfeed** - To save the timed feed
5. **Start Sleep** - For naps and bedtime
6. **Stop Sleep** - To save sleep duration

You can always add more commands later!

### Pro Tips:

- **Start simple**: Set up 2-3 commands first, test them, then add more
- **Use while feeding**: Keep hands free by using voice only
- **Set up both sides**: Even if you prefer one side, set up both left and right feeds
- **Timer control**: Use stop (not cancel) to save your sessions
- **Check app**: Always verify in Huckleberry app that it logged correctly

---

## Cost

- **Voice Monkey**: FREE (unlimited flows and devices)
- **Railway**: $5/month (already set up for the backend)
- **Total**: $5/month

---

## Support

If you have issues:

1. **Check Railway logs** first
2. **Test Flow manually** in Voice Monkey dashboard
3. **Verify all environment variables** are set correctly in Railway
4. **Check** `/health` endpoint shows Huckleberry connected
5. **Create an issue** on GitHub if problem persists

---

## Next Steps

Once everything is working:

1. ✅ Test all your most-used commands
2. ✅ Add more commands as needed
3. ✅ Bookmark Railway dashboard for checking logs
4. ✅ Enjoy hands-free baby tracking!

---

**Made with ❤️ for sleep-deprived parents**
