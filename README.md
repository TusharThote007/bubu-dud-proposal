# bubu & dud — Web Proposal (Streamlit)

A cute two-choice proposal app for the web: **Yes** or **Think again**. The "Think again" button keeps shuffling, and when she chooses **Yes**, confetti/balloons appear.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (two easy options)

### Option A — Streamlit Community Cloud
1. Push these files to a public GitHub repo.
2. Go to https://share.streamlit.io (Streamlit Community Cloud) → **New app**.
3. Select your repo and pick `app.py`. Deploy.
4. Share your public URL (ends with `.streamlit.app`).

### Option B — Hugging Face Spaces
1. Create a new **Space** and choose **Streamlit** as the SDK.
2. Upload `app.py` and `requirements.txt`.
3. Click **Run**. Your app will be live at `https://huggingface.co/spaces/<you>/<space-name>`.
