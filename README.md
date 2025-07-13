# 🕵️‍♀️ Info Klepto

**Info Klepto** is a minimalist Python-based web scraping tool that leverages **Selenium** and **BeautifulSoup** to extract information from web pages, with an interactive **Streamlit** UI to control the scraping process and view results in real-time.

> Built for those who want fast, no-fuss scraping with a clean interface.

---

## 📌 Key Features

- 🔍 Scrape dynamic websites using Selenium  
- 🧼 Clean HTML parsing with BeautifulSoup  
- 🎛️ Intuitive Streamlit UI — no code changes needed  
- ✂️ Element selection via tag and class name  
- 🧾 Real-time preview of scraped data

---

## 🧰 Tech Stack

- **Python 3**
- **Selenium**
- **BeautifulSoup (bs4)**
- **Streamlit**

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/02-davinci-01/info_klepto.git
cd info_klepto
```

### 2. Install Requirements

We recommend using a virtual environment.

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 🧪 How It Works

1. **Input the URL** you want to scrape  
2. **Specify the tag and class name** of the HTML elements you’re targeting  
3. Click **"Scrape"** to extract the data  
4. View the **results in the UI**, ready for copy or export

---

## 📂 File Overview

```
info_klepto/
│
├── app.py               # Streamlit UI and control flow
├── scraper.py           # Core logic for scraping via Selenium & BS4
├── requirements.txt     # List of Python dependencies
└── README.md            # Project documentation
```

---



## 🧠 Future Enhancements

- Export to CSV/JSON  
- Add support for scraping by XPath  
- Headless browser mode  
- Error handling and retry logic  

---

