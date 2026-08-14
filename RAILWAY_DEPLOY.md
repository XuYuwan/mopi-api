# 🚀 MOPI API - Quick Deploy to Railway

## Step-by-Step (2 minutes!)

### 1. Open Railway
Go to: **https://railway.app**

### 2. Sign In
Click "Login" → "Sign in with GitHub"

### 3. New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose: **`XuYuwan/mopi-api`**

### 4. Wait for Deploy
Railway will:
- ✅ Detect Python
- ✅ Install dependencies from `requirements.txt`
- ✅ Run `uvicorn main:app --host 0.0.0.0 --port $PORT`
- ✅ Deploy! (~2 minutes)

### 5. Get Your URL
- Click on your deployment
- Go to **"Settings"** → **"Generate Domain"**
- Copy your URL: `https://mopi-api-production-XXXX.up.railway.app`

---

## ✅ Test Your Live API

Once deployed, test it:

```bash
# Health check
curl https://YOUR-RAILWAY-URL.up.railway.app/

# Search test
curl "https://YOUR-RAILWAY-URL.up.railway.app/search?q=dua+lipa&limit=3"
```

---

## 📱 Then Update MOPI Android App

I'll update `MusicApi.kt` to use your live Railway URL!

---

**Ready?** Open Railway and deploy, then tell me your URL! 🚀

Or if you want, I can guide you through a different platform (Render, Fly.io, etc.)
