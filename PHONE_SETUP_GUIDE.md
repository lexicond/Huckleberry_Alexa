# Complete Phone Setup Guide
## Huckleberry Alexa Integration - Do Everything From Your Phone! 📱

**Estimated Time:** 60-90 minutes
**What You'll Need:**
- Your iPhone
- Alexa device nearby
- Credit card for IFTTT Pro ($5/month)
- Huckleberry login credentials

**Important:** Keep this guide open in one browser tab while working in others!

---

## 🎯 Overview: What We're Building

By the end of this guide, you'll be able to say:
- "Alexa, log a poo" → Logs to Huckleberry ✅
- "Alexa, log a left feed" → Starts breastfeeding timer ✅
- "Alexa, log a bottle" → Logs bottle feed ✅
- "Alexa, start sleep" → Starts sleep session ✅

All hands-free, while holding baby Kai!

---

# Part 1: Deploy to Railway (20 mins)

## Step 1.1: Sign Up for Railway

**On your iPhone:**

1. **Open Safari** and go to: `https://railway.app`

2. **Tap "Login"** in the top right corner

3. **Tap "Sign in with GitHub"**
   - If you don't have a GitHub account:
     - Tap "Create an account" on GitHub
     - Use: `leila@esmails.net` or your email
     - Choose a password and save it!
     - Verify your email
     - Come back to Railway

4. **Authorize Railway**
   - GitHub will ask "Authorize Railway?"
   - Tap "Authorize Railway"

5. **You're in!** You should see the Railway dashboard

---

## Step 1.2: Create New Project from GitHub

**Still in Safari on Railway:**

1. **Tap "New Project"** (big button in the middle or top right)

2. **Tap "Deploy from GitHub repo"**

3. **If asked to configure GitHub:**
   - Tap "Configure GitHub App"
   - Select your account (lexicond)
   - Tap "Only select repositories"
   - Find and select "Huckleberry_Alexa"
   - Tap "Save"
   - Go back to Railway

4. **Select Repository:**
   - You should see "Huckleberry_Alexa" in the list
   - Tap it

5. **Railway will start deploying:**
   - You'll see "Deploying..." with logs scrolling
   - This takes 2-3 minutes
   - Keep this tab open!

---

## Step 1.3: Set Environment Variables

**Critical Step - Don't skip!**

1. **While deployment is running:**
   - Tap on your project name
   - Look for a "Variables" tab or settings icon (⚙️)
   - Tap "Variables" or "Settings" → "Variables"

2. **Add Variable #1: HUCKLEBERRY_EMAIL**
   - Tap "+ New Variable" or "Add Variable"
   - **Variable Name:** `HUCKLEBERRY_EMAIL`
   - **Value:** `leila@esmails.net`
   - Tap "Add" or "Save"

3. **Add Variable #2: HUCKLEBERRY_PASSWORD**
   - Tap "+ New Variable"
   - **Variable Name:** `HUCKLEBERRY_PASSWORD`
   - **Value:** [Your Huckleberry password - the one you use to log into the app]
   - Tap "Add" or "Save"
   - ⚠️ **IMPORTANT:** Type this carefully! Wrong password = won't work

4. **Add Variable #3: CHILD_NAME**
   - Tap "+ New Variable"
   - **Variable Name:** `CHILD_NAME`
   - **Value:** `Kai De Ville`
   - ⚠️ **MUST MATCH EXACTLY** how it appears in Huckleberry app
   - Tap "Add"

5. **Add Variable #4: WEBHOOK_SECRET**
   - Tap "+ New Variable"
   - **Variable Name:** `WEBHOOK_SECRET`
   - **Value:** Create a random secret

   **How to create a random secret:**
   - Open a new tab
   - Go to: `https://www.random.org/passwords/?num=1&len=32&format=html&rnd=new`
   - Copy the password it generates
   - Paste as the value
   - **SAVE THIS SECRET!** You'll need it for IFTTT
   - Screenshot this or email it to yourself!

   - Tap "Add"

6. **Verify all 4 variables are set:**
   - HUCKLEBERRY_EMAIL ✅
   - HUCKLEBERRY_PASSWORD ✅
   - CHILD_NAME ✅
   - WEBHOOK_SECRET ✅

7. **Redeploy (if needed):**
   - If deployment already finished, tap "Deploy" again
   - Or look for "Redeploy" button
   - This picks up the new variables

---

## Step 1.4: Get Your Webhook URL

**This is your service's address on the internet:**

1. **Wait for deployment to finish:**
   - Look for "✓ Deployed" or "Success"
   - Green checkmark = good!
   - Red X = something's wrong (check logs)

2. **Find Settings tab:**
   - Tap on your service/deployment
   - Look for "Settings" tab
   - Tap it

3. **Generate Domain:**
   - Scroll to "Domains" section
   - You should see "Generate Domain" button
   - Tap "Generate Domain"
   - Railway creates a URL like: `your-app-name.railway.app`

4. **Copy Your URL:**
   - **Long press** on the generated URL
   - Tap "Copy"
   - **SAVE THIS!** You need it for IFTTT
   - Email it to yourself or save in Notes app

   **Your URL will look like:**
   ```
   https://huckleberry-alexa-production-abc123.railway.app
   ```

---

## Step 1.5: Test Your Deployment

**Let's make sure it's working!**

1. **Open new Safari tab**

2. **Test health endpoint:**
   - Type: `[YOUR_URL]/health`
   - Example: `https://your-app.railway.app/health`
   - Tap "Go"

3. **You should see JSON like this:**
   ```json
   {
     "status": "healthy",
     "huckleberry_connected": true,
     "child_name": "Kai De Ville",
     "service": "Huckleberry Alexa Integration"
   }
   ```

4. **✅ SUCCESS if you see:**
   - `"status": "healthy"`
   - `"huckleberry_connected": true`
   - `"child_name": "Kai De Ville"`

5. **❌ PROBLEM if you see:**
   - `"huckleberry_connected": false`
   - Check your Huckleberry email/password
   - Make sure CHILD_NAME matches exactly
   - Go back to Variables and fix

6. **Check Railway logs if there's an issue:**
   - Go back to Railway app
   - Tap "Deployments" or "Logs"
   - Look for error messages in red
   - Common issues:
     - Wrong password
     - Child name doesn't match
     - Email typo

---

## ✅ Part 1 Complete!

**You should have:**
- ✅ Railway project deployed
- ✅ All 4 environment variables set
- ✅ Webhook URL saved
- ✅ Webhook secret saved
- ✅ `/health` endpoint returning "healthy"

**Save these for next steps:**
- 📝 Webhook URL: `https://[your-url].railway.app`
- 🔐 Webhook Secret: `[your-32-char-secret]`

Take a screenshot or save these in your Notes app!

---

# Part 2: Set Up IFTTT (25 mins)

## Step 2.1: Sign Up for IFTTT

**Open new Safari tab:**

1. **Go to:** `https://ifttt.com`

2. **Tap "Sign up"**
   - Use email: `leila@esmails.net` or your preferred email
   - Create a password
   - Tap "Sign up"
   - Verify your email (check inbox)

3. **Skip the onboarding:**
   - IFTTT will try to show you tours
   - Keep tapping "Skip" or "Next" until you see the dashboard

---

## Step 2.2: Upgrade to IFTTT Pro

**⚠️ REQUIRED: Free tier only allows 2 applets, you need 5+**

1. **On IFTTT website:**
   - Look for "Upgrade" or "Pro" button
   - Usually in top right or banner at top

2. **Tap "Upgrade to Pro"**
   - Cost: $4.99/month
   - You need this for unlimited applets

3. **Enter payment info:**
   - Use your credit card
   - Complete the upgrade

4. **You should see "Pro" badge** on your account

**💡 Why you need Pro:**
- Free tier: 2 applets only
- You need at least 5 applets (poo, pee, feed, bottle, sleep)
- With Pro, you can create detailed commands (big yellow poo, etc.)

---

## Step 2.3: Enable Webhooks Service

**Still in IFTTT:**

1. **Tap the search icon** (magnifying glass)

2. **Search for:** `Webhooks`

3. **Tap "Webhooks"** (by IFTTT, with webhook icon)

4. **Tap "Connect"**
   - Authorizes Webhooks for your account

5. **Tap Settings icon** (⚙️) or "Documentation"
   - You'll see "Your key is: XXXXXXXXXXXX"
   - You don't need to save this, but it's there if needed

---

## Step 2.4: Create Your First Applet (Log a Poo)

**Let's create the most important one first!**

1. **Tap "Create"** (top right, or + button)

2. **Set up the "If This" trigger:**

   a. **Tap "If This"** (the first part)

   b. **Search for:** `IFTTrigger`

   c. **Tap "IFTTrigger"** (virtual device skill)

   d. **If not connected:**
      - Tap "Connect"
      - Follow prompts to link to Alexa account
      - Login with same Amazon account as your Alexa

   e. **Choose trigger:** "Trigger a scene"

   f. **Device name:** Type `log_poo`
      - ⚠️ Use underscores, not spaces!
      - Must be all lowercase
      - No special characters except underscore

   g. **Tap "Create trigger"**

3. **Set up the "Then That" action:**

   a. **Tap "Then That"** (the second part)

   b. **Search for:** `Webhooks`

   c. **Tap "Webhooks"**

   d. **Choose action:** "Make a web request"

   e. **Fill in the webhook details:**

   **URL:**
   ```
   https://[YOUR-RAILWAY-URL]/webhook
   ```
   Replace `[YOUR-RAILWAY-URL]` with your actual Railway URL from Part 1

   Example:
   ```
   https://huckleberry-alexa-production-abc123.railway.app/webhook
   ```

   **Method:** Select `POST`

   **Content Type:** Select `application/json`

   **Body:** Copy this exactly, but replace YOUR_SECRET:
   ```json
   {"command": "log a poo", "secret": "YOUR_SECRET_HERE"}
   ```

   Replace `YOUR_SECRET_HERE` with your actual webhook secret from Part 1

   Example:
   ```json
   {"command": "log a poo", "secret": "abc123def456ghi789jkl012mno345pq"}
   ```

   ⚠️ **CRITICAL:**
   - Keep the quotes around the secret
   - No extra spaces
   - Must be exactly as shown

   f. **Tap "Create action"**

4. **Review and Finish:**
   - **Title:** "Log poo to Huckleberry" (or whatever you want)
   - **Tap "Finish"**

5. **✅ Your first applet is created!**

---

## Step 2.5: Create More Essential Applets

**Repeat the same process for these commands:**

### Applet #2: Log a Pee

**If This:**
- IFTTrigger → Device name: `log_pee`

**Then That:**
- Webhooks → URL: `https://[YOUR-URL]/webhook`
- Method: POST
- Content Type: application/json
- Body: `{"command": "log a pee", "secret": "YOUR_SECRET"}`

---

### Applet #3: Log a Feed

**If This:**
- IFTTrigger → Device name: `log_feed`

**Then That:**
- Webhooks → URL: `https://[YOUR-URL]/webhook`
- Method: POST
- Content Type: application/json
- Body: `{"command": "log a feed", "secret": "YOUR_SECRET"}`

---

### Applet #4: Log a Bottle

**If This:**
- IFTTrigger → Device name: `log_bottle`

**Then That:**
- Webhooks → URL: `https://[YOUR-URL]/webhook`
- Method: POST
- Content Type: application/json
- Body: `{"command": "log a bottle", "secret": "YOUR_SECRET"}`

---

### Applet #5: Start Sleep

**If This:**
- IFTTrigger → Device name: `log_sleep`

**Then That:**
- Webhooks → URL: `https://[YOUR-URL]/webhook`
- Method: POST
- Content Type: application/json
- Body: `{"command": "start sleep", "secret": "YOUR_SECRET"}`

---

## Step 2.6: Create Detailed Applets (Optional but Recommended)

**These let you say detailed commands:**

### Log a Big Poo

- Device: `log_big_poo`
- Command: `log a big poo`

### Log a Yellow Poo

- Device: `log_yellow_poo`
- Command: `log a yellow poo`

### Log a Big Yellow Poo

- Device: `log_big_yellow_poo`
- Command: `log a big yellow poo`

### Log a Left Feed

- Device: `log_left_feed`
- Command: `log a left feed`

### Log a Right Feed

- Device: `log_right_feed`
- Command: `log a right feed`

**💡 Tip:** You can create as many as you want with Pro!

---

## Step 2.7: Test an Applet Manually

**Let's make sure one works before moving on:**

1. **Go to "My Applets"** in IFTTT

2. **Tap on "Log poo to Huckleberry"** (or your first applet)

3. **Look for "Check now" or test button**
   - Some versions have a play button ▶️
   - Or tap the applet and look for "Run"

4. **Manually trigger it**
   - IFTTT will send the webhook

5. **Check your Huckleberry app:**
   - Open Huckleberry on your phone
   - Look for a new poo entry
   - Should appear with current timestamp

6. **✅ If it worked:**
   - You'll see a poo in Huckleberry!
   - Move to next part

7. **❌ If it didn't work:**
   - Check IFTTT Activity log:
     - Tap your profile icon
     - Tap "Activity"
     - Look for the applet run
     - See if there's an error
   - Check Railway logs for errors
   - Verify your webhook secret matches
   - Verify your webhook URL is correct

---

## ✅ Part 2 Complete!

**You should have:**
- ✅ IFTTT Pro subscription
- ✅ 5+ applets created
- ✅ Webhooks connected to Railway
- ✅ At least one test succeeded

**IFTTrigger devices created:**
- log_poo ✅
- log_pee ✅
- log_feed ✅
- log_bottle ✅
- log_sleep ✅
- Plus any detailed ones you added

---

# Part 3: Set Up Alexa (20 mins)

## Step 3.1: Enable IFTTrigger Skill

**Open the Alexa app on your iPhone:**

1. **Open Alexa app**
   - Blue app with white circle

2. **Tap "More"** (bottom right, three horizontal lines)

3. **Tap "Skills & Games"**

4. **Tap the search icon** (magnifying glass)

5. **Search for:** `IFTTrigger`

6. **Tap "IFTTrigger"**
   - Should say "by IFTTT"
   - Has an orange/white icon

7. **Tap "Enable To Use"**

8. **Link Accounts:**
   - Alexa will ask you to link IFTTT
   - Login with your IFTTT credentials
   - Email: `leila@esmails.net` (or whatever you used)
   - Tap "Authorize"

9. **Success message:**
   - "IFTTrigger has been successfully linked"
   - Tap "Done" or "Close"

---

## Step 3.2: Discover Devices

**This is how Alexa finds your virtual devices:**

1. **Option A: Use Voice**
   - Say to your Alexa: **"Alexa, discover devices"**
   - Wait 20-30 seconds
   - Alexa will say: "Starting discovery... I found X devices"

2. **Option B: Use App**
   - In Alexa app, tap "Devices" (bottom bar, house icon)
   - Tap the + icon (top right)
   - Tap "Add Device"
   - Scroll down to "Other"
   - Tap "Discover Devices"
   - Wait 20-30 seconds

3. **Check discovered devices:**
   - Tap "Devices" tab
   - Scroll through "All Devices"
   - You should see:
     - log_poo
     - log_pee
     - log_feed
     - log_bottle
     - log_sleep
     - (Plus any detailed ones)

4. **✅ If you see all devices:** Great! Move on!

5. **❌ If devices missing:**
   - Wait 5 minutes and try discovery again
   - Make sure IFTTT applets are enabled
   - Try disabling and re-enabling IFTTrigger skill
   - Restart Alexa app

---

## Step 3.3: Create Alexa Routine #1 (Log a Poo)

**Now we connect your voice to the devices:**

1. **In Alexa app, tap "More"** (bottom right)

2. **Tap "Routines"**

3. **Tap the + icon** (top right)

4. **Set routine name:**
   - **Enter name:** "Log a poo"
   - This is just for you, not the voice command
   - Tap "Next" or go back

5. **Set "When this happens" (the trigger):**

   a. **Tap "When this happens"** (with + icon)

   b. **Tap "Voice"**

   c. **Type:** `log a poo`
      - This is what you'll say to Alexa
      - All lowercase is fine

   d. **Tap "Next"**

   e. **Optional: Add variations**
      - Tap "+" to add more phrases
      - Examples:
        - "log poo"
        - "logged a poo"
        - "baby pooped"
      - These are alternatives that work too

   f. **Tap back arrow** when done

6. **Set "Add action" (what happens):**

   a. **Tap "Add action"** (with + icon)

   b. **Scroll down and tap "Smart Home"**

   c. **Tap "Control device"**

   d. **Select device:**
      - Find and tap "log_poo" in the list
      - If you don't see it, tap "All Devices" first

   e. **Select action:**
      - Tap "Power"
      - Select "On" (turn device on)
      - This is what triggers IFTTT

   f. **Tap "Next"**

7. **From (which device responds):**
   - Choose which Alexa responds
   - Or select "All devices"
   - Tap "Next"

8. **Review and Save:**
   - You should see:
     - When: Voice - "log a poo"
     - Action: log_poo turns On
   - **Tap "Save"** (top right)

9. **✅ Your first routine is created!**

---

## Step 3.4: Create More Routines

**Repeat the process above for each command:**

### Routine #2: Log a Pee
- **When:** Voice - "log a pee"
- **Action:** log_pee turns On
- **Variations:** "log pee", "logged a pee", "baby peed"

### Routine #3: Log a Feed
- **When:** Voice - "log a feed"
- **Action:** log_feed turns On
- **Variations:** "log feed", "start a feed", "baby's eating"

### Routine #4: Log a Bottle
- **When:** Voice - "log a bottle"
- **Action:** log_bottle turns On
- **Variations:** "log bottle", "logged a bottle"

### Routine #5: Start Sleep
- **When:** Voice - "start sleep"
- **Action:** log_sleep turns On
- **Variations:** "log sleep", "baby's sleeping", "nap time"

### Optional Detailed Routines:

**Log a Big Poo:**
- When: "log a big poo"
- Action: log_big_poo turns On

**Log a Yellow Poo:**
- When: "log a yellow poo"
- Action: log_yellow_poo turns On

**Log a Left Feed:**
- When: "log a left feed"
- Action: log_left_feed turns On

**Log a Right Feed:**
- When: "log a right feed"
- Action: log_right_feed turns On

---

## ✅ Part 3 Complete!

**You should have:**
- ✅ IFTTrigger skill enabled
- ✅ All devices discovered in Alexa
- ✅ 5+ routines created
- ✅ Each routine linked to correct virtual device

---

# Part 4: Test Everything! (15 mins)

## Step 4.1: Test Your First Voice Command

**The moment of truth!**

1. **Make sure you're near your Alexa device**

2. **Say clearly:** **"Alexa, log a poo"**

3. **Alexa should respond:** "OK"
   - If she says "I don't know that", check your routine name
   - If she says nothing, check Alexa app for issues

4. **Wait 3-5 seconds**

5. **Open Huckleberry app on your phone:**
   - Look at timeline
   - You should see a new poo entry
   - Timestamp should be current

6. **✅ SUCCESS!** If you see it logged!

7. **❌ TROUBLESHOOTING if it didn't work:**

---

## Step 4.2: Troubleshooting Guide

### Issue: Alexa says "I don't know that" or "I'm not sure"

**Fix:**
- Check your routine is enabled (in Alexa app → Routines)
- Check the voice phrase matches what you said exactly
- Try adding the variation to the routine
- Try saying it slower and clearer

### Issue: Alexa says "OK" but nothing logs

**Fix:**

1. **Check IFTTT Activity:**
   - Open IFTTT app or website
   - Tap your profile → Activity
   - Look for recent trigger
   - If you see an error, read it

2. **Check Railway logs:**
   - Open Railway in Safari
   - Go to your project → Deployments → View Logs
   - Look for webhook requests
   - Check for errors in red

3. **Check Alexa app:**
   - Go to Activity (in More menu)
   - See if command was heard correctly
   - See what Alexa thought you said

4. **Common issues:**
   - Webhook secret doesn't match
   - Webhook URL wrong
   - IFTTT applet disabled
   - Railway app crashed

### Issue: Wrong activity logged

**Fix:**
- Alexa misheard you
- Check Alexa Activity to see what she heard
- Delete the wrong entry in Huckleberry
- Try again with clearer pronunciation
- Add variation to routine

---

## Step 4.3: Test All Commands

**Go through each one:**

| Say This | Should Log |
|----------|------------|
| "Alexa, log a poo" | Poo diaper change |
| "Alexa, log a pee" | Pee diaper change |
| "Alexa, log a feed" | Left breastfeeding session (timer starts) |
| "Alexa, log a bottle" | 120ml bottle feed |
| "Alexa, start sleep" | Sleep session (timer starts) |

**For each command:**
1. Say it to Alexa
2. Wait for "OK"
3. Check Huckleberry app
4. Verify correct activity logged
5. ✅ Check off if working
6. ❌ Note if not working and troubleshoot

---

## Step 4.4: Test Detailed Commands (If You Created Them)

**Try these if you set them up:**

- "Alexa, log a big poo"
- "Alexa, log a yellow poo"
- "Alexa, log a big yellow poo"
- "Alexa, log a left feed"
- "Alexa, log a right feed"

**Check Huckleberry shows:**
- Size details (big, medium, small)
- Color details (yellow, brown, etc.)
- Correct side for feeding

---

## Step 4.5: Real-World Test

**Simulate actual usage:**

1. **During next diaper change:**
   - While changing Kai
   - Say "Alexa, log a poo"
   - Continue changing diaper
   - Hands stay free!
   - Check later that it logged

2. **During next feeding:**
   - While Kai is latching
   - Say "Alexa, log a left feed" (or right)
   - Timer starts in Huckleberry
   - When done, manually stop timer in app

3. **During next bottle:**
   - After feeding bottle
   - Say "Alexa, log a bottle"
   - Logs 120ml (you can edit amount in app if different)

---

## ✅ Part 4 Complete!

**You should have:**
- ✅ All voice commands working
- ✅ Activities logging to Huckleberry correctly
- ✅ Tested during real baby care activities
- ✅ Troubleshot any issues

---

# 🎉 Setup Complete!

## What You've Accomplished

You've successfully built a complete voice-activated baby tracking system!

**You can now:**
- ✅ Log any activity hands-free
- ✅ Track while holding Kai
- ✅ Keep Huckleberry updated without touching your phone
- ✅ Record details (size, color, side, amount)

---

## Daily Usage Tips

### Best Practices

1. **Keep it simple:** Use basic commands most of the time
   - "Alexa, log a poo" is faster than details
   - Add details in app later if needed

2. **Speak clearly:** Alexa needs clear pronunciation
   - Say "log a poo" not "loga poo"
   - Pause slightly between words

3. **Check occasionally:** Verify it logged correctly
   - Alexa might mishear sometimes
   - Just delete and retry if wrong

4. **Edit in app:** You can always add details later
   - Log quickly with voice
   - Add notes/times in Huckleberry app when convenient

### Common Commands You'll Use

**Most frequently used:**
```
"Alexa, log a poo"          → After every diaper change
"Alexa, log a feed"         → When starting breastfeeding
"Alexa, log a bottle"       → After bottle feeding
"Alexa, start sleep"        → When putting Kai down
```

**Less frequent but useful:**
```
"Alexa, log a big poo"      → For notable diapers
"Alexa, log a left feed"    → Track which side
"Alexa, log a pee"          → Pee-only diapers
```

---

## When Things Go Wrong

### Quick Fixes

**Alexa doesn't respond:**
- Check Alexa has power and WiFi
- Try "Alexa" wake word louder
- Check Alexa app for issues

**Logs wrong activity:**
- Delete in Huckleberry app
- Try saying command slower
- Check what Alexa heard in Activity

**Nothing logs at all:**
1. Check Railway app is still deployed (green)
2. Check IFTTT applets are enabled
3. Test `/health` endpoint in browser
4. Check Railway logs for errors

**Delays logging (10-30 seconds):**
- Normal IFTTT behavior
- Just wait, it will appear
- If over 2 minutes, something's wrong

---

## Maintenance

### Weekly
- Check Railway is still running (should be automatic)
- Verify commands still working

### Monthly
- Update Railway if prompted
- Check IFTTT subscription is active
- Review which commands you use most

### When Kai Grows
- Add new commands as needed
- Adjust bottle amounts (edit IFTTT applet body)
- Add solid food tracking (Phase 2!)

---

## Cost Summary

**Ongoing costs:**
- Railway Hobby Plan: $5/month
- IFTTT Pro: $5/month
- **Total: $10/month**

**Free alternatives:**
- Railway Free Tier (with limits)
- IFTTT Free Tier (only 2 applets)
- Total: $0/month but very limited

**Worth it?**
- Saves countless phone touches per day
- Keeps accurate tracking even when exhausted
- Peace of mind during those 2am changes
- **YES! 💯**

---

## Getting Help

### If Something Breaks

1. **Check Railway:**
   - Open Railway app
   - Check deployment status
   - View logs for errors

2. **Check IFTTT:**
   - Open IFTTT Activity
   - See if applets are triggering
   - Check for error messages

3. **Check Huckleberry:**
   - Make sure you can login
   - Try logging manually
   - Verify Kai's name in settings

4. **Restart everything:**
   - Redeploy in Railway
   - Disable/enable IFTTT applets
   - Restart Alexa device

### Support Resources

- **Railway docs:** railway.app/docs
- **IFTTT help:** help.ifttt.com
- **Alexa help:** amazon.com/alexahelp
- **Technical review:** See `TECHNICAL_REVIEW.md` in repo

---

## Phase 2 Ideas (Future)

**Things you might want later:**

1. **Stop activities by voice:**
   - "Alexa, stop feeding" → End timer
   - "Alexa, wake up" → End sleep session

2. **Query recent activities:**
   - "Alexa, when was last feed?" → Tells you time
   - "Alexa, how long did Kai sleep?" → Duration

3. **Voice confirmations:**
   - Alexa says "Logged poo at 2:30 PM"
   - Confirms it worked

4. **Multiple children:**
   - "Alexa, log poo for Kai"
   - When baby #2 arrives!

5. **More activity types:**
   - Medicine tracking
   - Pumping tracking
   - Solid food when ready

**These can be added later without breaking current setup!**

---

## Celebration! 🎉

Congratulations! You've successfully set up a sophisticated voice-activated baby tracking system, all from your phone!

**What you built:**
- ✅ Cloud-hosted Flask application
- ✅ Secure webhook system
- ✅ IFTTT automation platform
- ✅ Alexa voice integration
- ✅ Real-time Huckleberry logging

**This wasn't easy, but you did it!**

Now go enjoy hands-free tracking with baby Kai! 👶🍼

---

## Quick Reference Card

**Print or screenshot this:**

```
═══════════════════════════════════════════
        ALEXA COMMANDS CHEAT SHEET
═══════════════════════════════════════════

🚼 DIAPER:
"Alexa, log a poo"
"Alexa, log a pee"
"Alexa, log a big poo"
"Alexa, log a yellow poo"

🤱 FEEDING:
"Alexa, log a feed"
"Alexa, log a left feed"
"Alexa, log a right feed"

🍼 BOTTLE:
"Alexa, log a bottle"

😴 SLEEP:
"Alexa, start sleep"

═══════════════════════════════════════════
        TROUBLESHOOTING
═══════════════════════════════════════════

Not working?
1. Check Railway app (should be green)
2. Check IFTTT Activity for errors
3. Check Alexa app heard you correctly
4. Delete wrong entry and retry

Slow to log?
- Normal! IFTTT can take 10-30 seconds

Wrong activity?
- Delete in Huckleberry app
- Try speaking more clearly

═══════════════════════════════════════════
```

**Save this screenshot for quick reference!**

---

**Setup Guide Complete! Now go log some baby activities! 🎉👶📱**
