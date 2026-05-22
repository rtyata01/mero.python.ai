# Recommendation System API MVP using FastAPI

## Project Overview

Build a production-style Recommendation System backend using:

- FastAPI
- PostgreSQL
- Redis
- Scikit-learn
- Docker
- JWT Authentication
- Vector Similarity Search
- Background Jobs
- Async APIs

This project is strong for:

- Backend Engineering resumes
- AI/ML Engineering resumes
- Full-stack AI applications
- System Design interviews
- Production ML discussions

---

# What This Project Does

Users can:

- Create accounts
- Browse products/movies/articles
- Get personalized recommendations
- Receive similar-item recommendations
- Track interactions
- Search items
- Save favorites
- Receive trending recommendations

The recommendation engine supports:

1. Content-based filtering
2. Collaborative filtering
3. Hybrid recommendations
4. Popularity-based fallback
5. Embedding similarity search

---

# Example Resume Bullets

## Backend + ML Resume Bullet

> Built a scalable recommendation engine using FastAPI, PostgreSQL, Redis, and vector similarity search serving personalized recommendations with sub-150ms latency.

## Advanced Resume Bullet

> Designed a hybrid recommendation system combining collaborative filtering and content-based ranking using cosine similarity and user interaction embeddings.

## Infra Resume Bullet

> Containerized ML microservices with Docker and implemented Redis caching, JWT authentication, and asynchronous recommendation pipelines.

---

# MVP Architecture

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
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| ML | Scikit-learn |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT |
| Deployment | Docker |
| Async Server | Uvicorn |
| Background Tasks | Celery or FastAPI Tasks |
| Vector Similarity | NumPy / FAISS |

---

# Recommended Project Structure

```text
recommendation-system/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── items.py
│   │   ├── recommendations.py
│   │   └── interactions.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── interaction.py
│   │   └── favorite.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── item.py
│   │   └── recommendation.py
│   │
│   ├── services/
│   │   ├── recommendation_service.py
│   │   ├── embedding_service.py
│   │   ├── ranking_service.py
│   │   └── cache_service.py
│   │
│   ├── ml/
│   │   ├── train_model.py
│   │   ├── similarity.py
│   │   └── embeddings.py
│   │
│   └── utils/
│       ├── auth.py
│       └── logger.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Database Design

## Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Items Table

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    embedding VECTOR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Interactions Table

```sql
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    item_id INTEGER REFERENCES items(id),
    interaction_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

Interaction types:

- view
- click
- like
- purchase
- save

---

# Core Recommendation Strategies

# 1. Content-Based Filtering

Recommend similar items using embeddings.

Example:

- User likes Sci-Fi movies
- Recommend more Sci-Fi movies

## Example Implementation

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_similar_items(item_embedding, item_embeddings):

    similarities = cosine_similarity(
        [item_embedding],
        item_embeddings
    )[0]

    ranked = np.argsort(similarities)[::-1]

    return ranked[:10]
```

---

# 2. Collaborative Filtering

Recommend items based on similar users.

Example:

- Users who liked Item A also liked Item B

## User-Item Matrix

```text
        Item1 Item2 Item3
User1     1     0     1
User2     1     1     0
User3     0     1     1
```

## Matrix Factorization Example

```python
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=20)
latent_matrix = svd.fit_transform(user_item_matrix)
```

---

# 3. Hybrid Recommendation System

Combine:

- Content similarity
- Collaborative filtering
- Popularity score
- User preferences

## Ranking Formula

Use weighted scoring:

genui{"math_block_widget_always_prefetch_v2": {"content": "Score = 0.5(ContentSimilarity) + 0.3(CollaborativeScore) + 0.2(Popularity)"}}

---

# API Endpoints

# Authentication APIs

## Register User

```http
POST /auth/register
```

Request:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

---

## Login

```http
POST /auth/login
```

Returns JWT token.

---

# Item APIs

## Create Item

```http
POST /items
```

## List Items

```http
GET /items
```

## Search Items

```http
GET /items/search?q=scifi
```

---

# Interaction APIs

## Record Interaction

```http
POST /interactions
```

Request:

```json
{
  "item_id": 42,
  "interaction_type": "click"
}
```

---

# Recommendation APIs

## Personalized Recommendations

```http
GET /recommendations
```

Response:

```json
[
  {
    "item_id": 15,
    "score": 0.94
  },
  {
    "item_id": 9,
    "score": 0.91
  }
]
```

---

## Similar Items

```http
GET /recommendations/similar/{item_id}
```

---

# Authentication Implementation

## JWT Setup

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(hours=24)

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

---

# SQLAlchemy Models

## User Model

```python
from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
```

---

# Pydantic Schemas

```python
from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: int
    title: str
    category: str

    class Config:
        orm_mode = True
```

---

# Recommendation Service

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RecommendationService:

    def recommend(self, user_embedding, item_embeddings):

        similarities = cosine_similarity(
            [user_embedding],
            item_embeddings
        )[0]

        top_indices = np.argsort(similarities)[::-1]

        return top_indices[:10]
```

---

# Redis Caching

Cache recommendations to reduce latency.

## Example

```python
import redis
import json

redis_client = redis.Redis(host="redis", port=6379)


def cache_recommendations(user_id, recommendations):

    redis_client.setex(
        f"recommendations:{user_id}",
        3600,
        json.dumps(recommendations)
    )
```

---

# Async Background Tasks

Use background jobs to:

- Recompute embeddings
- Retrain models
- Generate recommendations
- Sync analytics

## FastAPI Background Task Example

```python
from fastapi import BackgroundTasks


@app.post("/train")
def train_model(background_tasks: BackgroundTasks):

    background_tasks.add_task(retrain_model)

    return {"message": "Training started"}
```

---

# Embedding Generation

## Using Sentence Transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    return model.encode(text)
```

---

# Vector Search

## FAISS Integration

```python
import faiss
import numpy as np

index = faiss.IndexFlatL2(384)

vectors = np.array(item_embeddings).astype("float32")

index.add(vectors)

D, I = index.search(query_vector, 10)
```

---

# Docker Setup

## Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# Docker Compose

```yaml
version: '3.9'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: recommendations

  redis:
    image: redis:7
```

---

# Performance Optimizations

## 1. Recommendation Caching

Use Redis.

## 2. Batch Inference

Process multiple users simultaneously.

## 3. Async APIs

Use async endpoints.

## 4. Vector Databases

Use:

- Pinecone
- Weaviate
- Qdrant
- pgvector

## 5. Precomputed Recommendations

Generate nightly recommendation batches.

---

# Production Improvements

# Monitoring

Add:

- Prometheus
- Grafana
- Structured logging

---

# Security

Add:

- JWT auth
- Rate limiting
- API keys
- HTTPS
- Input validation

---

# Scaling

Use:

- Kubernetes
- Load balancers
- Horizontal scaling
- GPU inference

---

# Advanced Features

# 1. Real-Time Recommendations

Stream user events with:

- Kafka
- Redis Streams

---

# 2. A/B Testing

Serve different ranking models.

---

# 3. Explainable Recommendations

Example:

> Recommended because you liked Sci-Fi movies.

---

# 4. Trending Engine

Compute trending items:

genui{"math_block_widget_always_prefetch_v2": {"content": "TrendingScore = Views + 2(Likes) + 5(Purchases)"}}

---

# 5. Cold Start Handling

For new users:

- Popular items
- Category preferences
- Demographic heuristics

---

# Deployment Options

## Option 1: Render

Easy beginner deployment.

## Option 2: Railway

Good for MVP hosting.

## Option 3: AWS

Use:

- EC2
- ECS
- RDS
- ElastiCache

## Option 4: Kubernetes

Best production option.

---

# Recommended Development Phases

# Phase 1

Build:

- FastAPI CRUD
- PostgreSQL models
- JWT auth
- Recommendation endpoint

---

# Phase 2

Add:

- Redis cache
- Embeddings
- Similarity search
- Docker

---

# Phase 3

Add:

- Hybrid ranking
- Async jobs
- Monitoring
- Recommendation explanations

---

# Phase 4

Add:

- Kubernetes
- CI/CD
- A/B testing
- Real-time streaming

---

# Strong GitHub README Sections

Include:

- Architecture diagram
- API screenshots
- Swagger docs
- Performance metrics
- Load testing results
- Docker setup
- Deployment guide

---

# Sample Metrics to Mention

Example:

- 100K+ recommendations served
- 120ms average latency
- 95% cache hit rate
- 10K concurrent users supported

---

# Interview Questions You Can Answer Using This Project

- How recommendation systems work
- Difference between collaborative vs content filtering
- How caching improves latency
- How vector search works
- Why async APIs matter
- How to scale ML inference
- How Redis improves performance
- How embeddings are generated
- Cold start problem solutions
- Hybrid ranking strategies

---

# Final Resume-Ready Project Description

> Built a production-ready recommendation engine using FastAPI, PostgreSQL, Redis, and vector similarity search supporting personalized ranking, JWT authentication, caching, and hybrid recommendation pipelines with scalable microservice architecture.

