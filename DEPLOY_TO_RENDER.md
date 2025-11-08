# Deploy to Render

## Steps:

1. Push code to GitHub
2. Go to https://render.com and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Render auto-detects settings from render.yaml
6. Click "Create Web Service"
7. Wait for deployment (5-10 mins)
8. Copy your service URL (e.g., https://yt-downloader-xyz.onrender.com)

## Update Extension:

Edit `extension/popup.js` and replace:
```javascript
const response = await fetch('http://localhost:5000/download', {
```

With:
```javascript
const response = await fetch('https://YOUR-RENDER-URL.onrender.com/download', {
```

## Important:
- Free tier sleeps after 15 mins of inactivity (first request takes 30s to wake)
- Files are streamed directly to browser (no storage issues)
- Works from anywhere with internet

## Alternative: Use Locally
Keep using localhost:5000 - works only on your computer but faster and always available.
