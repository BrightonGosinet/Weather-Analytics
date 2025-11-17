# Weather Analytics Cloud Pipeline ☁️

A cloud-based REST API for collecting, storing, and analyzing real-time weather data from multiple international cities using FastAPI, PostgreSQL, and AWS RDS.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
![AWS](https://img.shields.io/badge/AWS-RDS-orange)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)
- [Cloud Deployment](#cloud-deployment)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)

## Features

### Core Functionality
- **Real-time Data Collection**: Automated weather data retrieval from 10 international cities
- **RESTful API**: 8 FastAPI endpoints for data access and analytics
- **Cloud Database**: PostgreSQL deployed on AWS RDS with automated backups
- **Analytics Engine**: 4 specialized endpoints for weather pattern analysis
- **Automated Scheduling**: Cron-based collection every 6 hours
- **Error Handling**: Comprehensive logging and retry logic

### Analytics Features
- **Average Temperature Analysis**: Calculate temperature statistics over customizable time periods
- **Multi-City Comparison**: Compare current weather conditions across multiple cities
- **Temperature Rankings**: Identify hottest and coldest cities based on latest data
- **Weather Alerts**: Automated detection of extreme weather conditions with threshold-based alerting


## 🛠️ Tech Stack

### Backend
- **Python 3.10** - Core programming language
- **FastAPI** - Modern, high-performance web framework
- **Uvicorn** - ASGI server for FastAPI
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation and settings management

### Database
- **PostgreSQL 14** - Relational database for time-series data
- **AWS RDS** - Managed database service with automated backups
- **psycopg2** - PostgreSQL adapter for Python

### External APIs
- **OpenWeatherMap API** - Real-time weather data source

### DevOps & Tools
- **Git/GitHub** - Version control
- **Cron** - Task scheduling for automated collection
- **DBeaver** - Database management and visualization
- **AWS** - Cloud infrastructure


## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     Weather Analytics                   │
│                    Cloud Architecture                   │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐
│  OpenWeatherMap  │
│       API        │
└────────┬─────────┘
         │ HTTPS
         ↓
┌──────────────────┐      ┌──────────────────┐
│  Data Collector  │─────→│  Data Processor  │
│  (Python Script) │      │     (Pandas)     │
└──────────────────┘      └────────┬─────────┘
         ↑                         │
         │                         ↓
    ┌────┴────┐           ┌──────────────────┐
    │  Cron   │           │   FastAPI App    │
    │  Job    │           │  (8 Endpoints)   │
    └─────────┘           └────────┬─────────┘
                                   │
                                   ↓
                          ┌──────────────────┐
                          │   AWS RDS        │
                          │  PostgreSQL 14   │
                          │  (Cloud Database)│
                          └──────────────────┘
```

### Data Flow
1. **Cron Job** triggers collection script every 6 hours
2. **Data Collector** fetches weather data from OpenWeatherMap API
3. **Data Processor** validates and transforms raw API responses
4. **Database Layer** stores processed data in AWS RDS PostgreSQL
5. **FastAPI** serves data through RESTful endpoints
6. **Analytics Engine** processes queries and returns insights

## 📡 API Endpoints

### Health Check
- `GET /` - API status and information

### Data Collection
- `POST /collect/{city}` - Manually trigger weather data collection for a specific city

### Data Retrieval
- `GET /weather/{city}` - Get weather history for a specific city
- `GET /weather/` - Get recent weather data for all cities

### Analytics
- `GET /analytics/average-temp/{city}` - Calculate average temperature over N days
- `GET /analytics/compare` - Compare current weather across multiple cities
- `GET /analytics/hottest` - Get hottest or coldest cities rankings
- `GET /analytics/alerts` - Detect cities with extreme weather conditions

### Interactive Documentation
- `GET /docs` - Swagger UI (interactive API documentation)
- `GET /redoc` - ReDoc (alternative documentation)


#### Prerequisites
- AWS account with billing alerts configured
- MFA enabled for security
- AWS CLI installed (optional)

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/BrightonGosinet/weather-analytics-pipeline.git
cd weather-analytics-pipeline
```

#### 2. Create Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/weather_analytics

# OpenWeatherMap API Key
WEATHER_API_KEY=your_api_key_here
```

Get your free API key at [OpenWeatherMap](https://openweathermap.org/api)

#### 5. Create PostgreSQL Database
```bash
createdb weather_analytics
```

#### 6. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

#### 7. Access API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

## ☁️ Cloud Deployment
### AWS RDS Setup

#### 1. Create RDS Instance

**Configuration:**
- **Engine:** PostgreSQL 14
- **Instance Class:** db.t3.micro (free tier eligible)
- **Storage:** 20 GB General Purpose SSD (gp3)
- **Public Access:** Yes (for development)
- **Backup Retention:** 7 days

#### 2. Configure Security Group

**Inbound Rules:**
- **Type:** PostgreSQL
- **Port:** 5432
- **Source:** Your IP address

#### 3. Update Environment Variables

Create `.env.aws` for cloud configuration:
```bash
DATABASE_URL=postgresql://postgres:PASSWORD@your-rds-endpoint.us-west-2.rds.amazonaws.com:5432/weather_analytics
WEATHER_API_KEY=your_api_key_here
```

#### 4. Migrate Data to Cloud
```bash
# Export from local
pg_dump weather_analytics > backup.sql

# Import to AWS RDS
psql -h your-rds-endpoint.us-west-2.rds.amazonaws.com -U postgres -d weather_analytics < backup.sql
```

#### 5. Switch to Cloud Database
```bash
cp .env.aws .env
```

