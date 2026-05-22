# Recommendation System API

A production-style recommendation engine built with FastAPI.

OmniPulse recommendation engine 
- using FastAPI, PostgreSQL, Redis, and vector similarity search 
- serving personalized recommendations with sub-150ms latency.

```text
Frontend
   |
   v
FastAPI Backend
   |
   +----------------+
   |                |
   v                v
PostgreSQL        Redis Cache
   |
   v
Recommendation Engine
   |
   v
ML Models / Embeddings
```text

## Features

- JWT Authentication
- Personalized Recommendations
- Vector Similarity Search
- Redis Caching
- PostgreSQL
- Dockerized Setup

## Run

```bash
docker-compose up --build
```

Visit:

- http://localhost:8000/docs