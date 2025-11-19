# Weather Analytics Cloud Pipeline 

A cloud-based REST API for collecting, storing, and analyzing real-time weather data from multiple international cities using FastAPI, PostgreSQL, and AWS RDS.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue)
![AWS](https://img.shields.io/badge/AWS-RDS-orange)


## Features

### Core Functionality
- **Real-time Data Collection**: Automated weather data retrieval from 10 international cities
- **RESTful API**: 8 FastAPI endpoints for data access and analytics
- **Cloud Database**: PostgreSQL deployed on AWS RDS with automated backups
- **Analytics Engine**: 4 specialized endpoints for weather pattern analysis
- **Automated Scheduling**: Cron-based collection every 6 hours

### Analytics Features
- **Average Temperature Analysis**: Calculate temperature statistics over customizable time periods
- **Multi-City Comparison**: Compare current weather conditions across multiple cities
- **Temperature Rankings**: Identify hottest and coldest cities based on latest data
- **Weather Alerts**: Automated detection of extreme weather conditions with threshold-based alerting


## Tech Stack

**Backend:** Python 3.10, FastAPI, Uvicorn, SQLAlchemy, Pydantic  
**Database:** PostgreSQL 14, AWS RDS, psycopg2  
**APIs:** OpenWeatherMap  


## Architecture
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
│  (Python Script) │      │     (Pydantic)   │
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

## API Endpoints

The API provides 8 endpoints for weather data operations:

- **Health Check**: `GET /` - API status
- **Data Collection**: `POST /collect/{city}` - Collect weather for a city
- **Data Retrieval**: `GET /weather/{city}`, `GET /weather/` - Query historical data
- **Analytics**: 
  - `GET /analytics/average-temp/{city}` - Temperature statistics
  - `GET /analytics/compare` - Compare multiple cities
  - `GET /analytics/hottest` - Hottest/coldest rankings
  - `GET /analytics/alerts` - Extreme weather detection

