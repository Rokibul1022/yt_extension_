# Deploy to Railway (Recommended)

## Why Railway?
- Faster than Render
- No sleep time on free tier
- Easier setup

## Steps:

1. Push code to GitHub
2. Go to https://railway.app
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repo
6. Railway auto-deploys
7. Click "Settings" → "Generate Domain"
8. Copy your URL (e.g., https://yt-downloader-production.up.railway.app)

## Update Extension:

Edit `extension/popup.js` line 17:
```javascript
const response = await fetch('https://YOUR-RAILWAY-URL.up.railway.app/download', {
```

Reload extension and test!

## Free Tier Limits:
- $5 credit/month (enough for ~500 downloads)
- No sleep time
- Fast response

## Keep Using Localhost?
If you prefer, keep using `http://localhost:5000` - works only on your PC but free forever.
