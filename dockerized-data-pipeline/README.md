# Dockerized Data Pipeline with Airflow + MySQL

## 🚀 Project Overview
This pipeline:
1. Fetches stock data from Alpha Vantage API.
2. Parses JSON response.
3. Stores stock data in MySQL.
4. Runs hourly using Airflow inside Docker.

---

## 🛠 Setup Instructions

### 1. Install Prerequisites
- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Python 3.9+
- (Optional) MySQL Workbench or CLI

### 2. Clone Repository / Extract Project
Place all files in a folder called `dockerized-data-pipeline/`.

### 3. Add Environment Variables
Edit `.env` file and add:
```
ALPHA_VANTAGE_KEY=your_api_key_here
```

### 4. Start Pipeline
```bash
docker-compose up --build
```

### 5. Access Services
- Airflow UI → http://localhost:8080 (user: `admin`, pass: `admin`)
- MySQL DB → localhost:3306 (user: `user`, pass: `userpass`, db: `stocks`)

### 6. Verify Data
```bash
docker exec -it mysql_container mysql -uuser -puserpass -D stocks -e "SELECT * FROM stock_data LIMIT 5;"
```

### 7. Stop Services
```bash
docker-compose down
```
