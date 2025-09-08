# 🚀 NOVA Assistant - Streamlit Cloud Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - You need a GitHub account
2. **Streamlit Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **OpenAI API Key** - Your existing API key
4. **Assistant ID** - Your assistant ID: `asst_XTd5ExJ9KUTLyrFkzkzPZa2f`

## 🛠️ Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Create a new GitHub repository** (or use existing one)
2. **Upload all files** to your repository:
   - `streamlit_app.py`
   - `nova_client.py`
   - `config.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`

### Step 2: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select your repository** from the dropdown
5. **Choose the branch** (usually `main` or `master`)
6. **Set the main file path** to `streamlit_app.py`
7. **Click "Deploy!"**

### Step 3: Configure Secrets

1. **After deployment**, go to your app's dashboard
2. **Click "Settings"** (gear icon)
3. **Go to "Secrets"** tab
4. **Add your secrets**:

```toml
OPENAI_API_KEY = "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"
OPENAI_ASSISTANT_ID = "asst_XTd5ExJ9KUTLyrFkzkzPZa2f"
```

5. **Click "Save"**

### Step 4: Test Your Deployment

1. **Go to your app URL** (provided by Streamlit Cloud)
2. **Test the chat functionality**
3. **Verify your assistant is working**

## 🔧 Troubleshooting

### Common Issues:

1. **"OpenAI API key is required" error**
   - Check that your secrets are properly configured
   - Make sure the secret names match exactly

2. **App won't start**
   - Check the logs in Streamlit Cloud dashboard
   - Verify all dependencies are in `requirements.txt`

3. **Assistant not responding**
   - Verify your assistant ID is correct
   - Check that your OpenAI API key has access to assistants

### Debug Steps:

1. **Check logs** in Streamlit Cloud dashboard
2. **Test locally** first with `streamlit run streamlit_app.py`
3. **Verify secrets** are properly set
4. **Check GitHub repository** has all required files

## 📁 Required Files Structure

```
your-repo/
├── streamlit_app.py          # Main Streamlit app
├── nova_client.py            # NOVA client class
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── .gitignore               # Git ignore file
└── .streamlit/
    └── secrets.toml         # Local secrets (optional)
```

## 🌐 Your App URL

Once deployed, your app will be available at:
`https://your-app-name.streamlit.app`

## 🔄 Updates

To update your app:
1. **Push changes** to your GitHub repository
2. **Streamlit Cloud will automatically redeploy**
3. **Your app will be updated** in a few minutes

## 📞 Support

If you encounter issues:
1. Check the Streamlit Cloud logs
2. Verify all files are uploaded correctly
3. Ensure secrets are properly configured
4. Test locally first

---

**🎉 Congratulations!** Your NOVA Assistant is now live on Streamlit Cloud!
