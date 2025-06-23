# 📈 GCP Stock Market Pipeline

A data pipeline project built using **Google Cloud Platform (GCP)** to fetch, process, and analyze stock market data — visualized using **Looker Studio** for insights and dashboards.

---

## 🚀 Project Overview

This project automates the collection and analysis of stock market data using GCP services. It ingests data from the Alpha Vantage API, stores it securely, processes it with Python, and visualizes insights through Looker Studio.

---

## 🛠️ Tech Stack

- **Alpha Vantage API** – for stock market data
- **Google Cloud Storage (GCS)** – stores raw and cleaned data
- **Cloud Functions / Cloud Scheduler** – automation and orchestration
- **BigQuery** – scalable data warehousing and SQL analysis
- **Looker Studio** – interactive dashboards for data visualization
- **Python** – data collection and transformation

---

## 📂 Project Structure


```
![Final drawio](https://github.com/user-attachments/assets/fb40c9bf-cf82-4180-9d74-f9234f79cd50)


GCP Stock Market Project/
├── main.py              # Core script to extract and load stock data
├── Step-by-Step.docx    # Setup documentation
├── Errors.docx          # Known issues & resolutions
├── README.md            # Project overview and documentation
└── .gitignore           # Git ignore rules

````

---

## 📡 Data Source: Alpha Vantage API

This project uses the **Alpha Vantage API** to fetch real-time and historical stock data.

- Endpoints used:
  - `TIME_SERIES_DAILY`
  - `GLOBAL_QUOTE`
- Supports symbols like `AAPL`, `GOOGL`, `TSLA`, etc.
- Response format: JSON

📌 **Note:** Free tier allows **5 requests/min** and **500 requests/day**.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Vandana-Kolusu/GCP-stock-market-Pipeline.git
cd GCP-stock-market-Pipeline
````

### 2. Create a Virtual Environment (Optional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure GCP

1. Enable the following APIs:

   * BigQuery API
   * Cloud Storage API
   * Cloud Functions API
   * Cloud Scheduler API

2. Create a service account with access to:

   * BigQuery Admin
   * Storage Admin
   * Cloud Functions Developer

3. Export your service account credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"
```

### 4. Add Your Alpha Vantage API Key

Store your key securely (e.g., using environment variables or a config file):

```bash
export ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

---

## 🧠 Core Features

* ✅ Automated data ingestion from Alpha Vantage
* ✅ Cloud Function to run scheduled updates
* ✅ Clean and upload data to BigQuery
* ✅ Create dashboards in Looker Studio

---

## 📊 Looker Studio Dashboard

> [🔗 View Dashboard](https://lookerstudio.google.com/s/ssWD6aPU8dw)


### Dashboard Highlights:

* Daily stock prices and volume
* Historical trends and moving averages
* Compare multiple tickers
* Filter by date range and ticker symbol

---

## 🚧 Limitations & Future Improvements

* Current implementation limited by Alpha Vantage's free-tier rate limits
* Only selected tickers are processed
* Future additions:

  * Intraday support
  * Sentiment analysis using news APIs
  * Predictive modeling (e.g., using Vertex AI)

---

## 👩‍💻 Author

**Vandana Kolusu**
GitHub: [@Vandana-Kolusu](https://github.com/Vandana-Kolusu)

---

## 🙋‍♀️ Questions?

Feel free to open an [issue](https://github.com/Vandana-Kolusu/GCP-stock-market-Pipeline/issues) or contact me via GitHub!

```

---

Let me know if you want me to save this as a file, auto-create the `requirements.txt`, or generate visual diagrams for your architecture.
```
