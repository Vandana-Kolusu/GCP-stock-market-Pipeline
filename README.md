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

GCP Stock Market Project/
│
├── main.py # Core pipeline logic
├── Step-by-Step.docx # Documentation of project steps
├── Errors.docx # Known issues or troubleshooting notes
├── README.md # Project documentation (this file)
└── .gitignore # Files to ignore in version control


---

## 📡 Data Source: Alpha Vantage Stock API

This project uses the **[Alpha Vantage Stock API](https://www.alphavantage.co/)** to retrieve stock data.

- Pulls historical and real-time stock prices (daily/intraday)
- Endpoints used:
  - `TIME_SERIES_DAILY`
  - `GLOBAL_QUOTE`
- JSON responses parsed using Python
- Data stored in **GCS** and analyzed via **BigQuery**

> ⚠️ API Limit: Free tier allows 5 requests/min and 500 requests/day.

---

## 📊 Features

- ✅ Fetches live and historical stock data
- ✅ Stores raw and cleaned data in GCS
- ✅ Loads processed data into BigQuery
- ✅ Schedules updates using Cloud Scheduler
- ✅ Visualizes stock trends in Looker Studio

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Vandana-Kolusu/GCP-stock-market-Pipeline.git
cd GCP-stock-market-Pipeline
2. (Optional) Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Configure GCP
Enable these services:
BigQuery
Cloud Storage
Cloud Functions
Cloud Scheduler
Create a service account and export the credentials:
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
4. Set Up Alpha Vantage
Sign up at alphavantage.co
Get your free API key and add it to your environment or script config
📊 Looker Studio Dashboard

🔗 Access
🔗 View Dashboard
(replace with actual URL)
Includes:

Daily stock prices and volume
Volatility tracking
Ticker comparisons with filters
🚧 Limitations & Future Enhancements

API rate limits require throttling
Current support limited to selected stock tickers
Future plans: sentiment analysis, anomaly detection, predictive modeling
👩‍💻 Author

Vandana Kolusu
GitHub: @Vandana-Kolusu

📄 License

This project is licensed under the MIT License.


---

Let me know if you'd like help creating a `requirements.txt`, sample Alpha Vantage data loader, or Looker Studio embed code.
