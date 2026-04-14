# Vendor Risk Assessment Dashboard

A Streamlit dashboard for visualising third-party cyber risk assessment (TPCRA) results.

## Repo structure

```
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Theme + server config
└── README.md
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**.
4. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
5. Click **Deploy** — live in ~60 seconds.

Every `git push` to `main` automatically redeploys the app.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Updating data

- **Default view**: the bundled sample data loads automatically.
- **Upload your own**: use the sidebar file uploader to load any JSON that follows the same schema.
- **Hardcode new data**: replace `DEFAULT_DATA` in `app.py` and push to GitHub.
