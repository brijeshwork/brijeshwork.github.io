

> **Version:** 1.0  
> **Architecture Type:** Microservices with Event-Driven Components  
> **Scale Target:** 10M+ keywords, 1M+ domains, 100K+ concurrent users

---

## 📋 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Flow & Processing](#2-data-flow--processing)
3. [Database Design](#3-database-design)
4. [API Layer Design](#4-api-layer-design)
5. [Crawler & Data Sources](#5-crawler--data-sources)
6. [Ranking & Analytics Engine](#6-ranking--analytics-engine)
7. [User System](#7-user-system)
8. [Dashboard & UI Modules](#8-dashboard--ui-modules)
9. [Scalability, Performance & Security](#9-scalability-performance--security)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Architecture Overview

### 1.1 System Architecture Pattern

**Hybrid Microservices Architecture** with the following characteristics:
- Core services as independent microservices
- Shared data access layer for performance
- Event-driven communication for async operations
- API Gateway for unified access point

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  [Web Dashboard] [Mobile App] [Browser Extension] [API Clients] │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CDN LAYER (CloudFlare)                     │
│              [Static Assets] [API Response Cache]               │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Kong/AWS ALB)                   │
│    [Rate Limiting] [Auth] [Routing] [Request Validation]        │
└─────┬───────────┬──────────┬──────────┬────────────┬────────────┘
      │           │          │          │            │
┌─────▼─────┐ ┌──▼────┐ ┌───▼─────┐ ┌─▼────┐ ┌────▼──────┐
│  Auth     │ │Keyword│ │ Domain  │ │SERP  │ │ Tracking  │
│  Service  │ │Service│ │ Service │ │Svc   │ │  Service  │
└─────┬─────┘ └──┬────┘ └───┬─────┘ └─┬────┘ └────┬──────┘
      │          │          │          │            │
┌─────▼──────────▼──────────▼──────────▼────────────▼───────────┐
│                   MESSAGE QUEUE (RabbitMQ/Kafka)              │
│  [Crawl Jobs] [Data Processing] [Analytics] [Notifications]   │
└──────┬────────────────┬────────────────┬─────────────┬────────┘
       │                │                │             │
┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐ ┌───▼─────┐
│   Crawler   │  │  Analytics  │  │   Email    │ │ Report  │
│   Workers   │  │   Engine    │  │  Service   │ │ Builder │
└──────┬──────┘  └──────┬──────┘  └─────┬──────┘ └───┬─────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                      DATA STORAGE LAYER                       │
│ [PostgreSQL] [MongoDB] [Redis] [Elasticsearch] [S3/Object]    │
└───────────────────────────────────────────────────────────────┘
    │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                   EXTERNAL INTEGRATIONS                       │
│ [Google APIs] [Bing APIs] [Third-party SEO] [Proxy Services]  │
└───────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components Breakdown

#### **1.3.1 Frontend Layer**
- **Web Dashboard**: React/Next.js with SSR for SEO
- **Mobile Apps**: React Native for iOS/Android
- **Browser Extension**: Chrome/Firefox for on-page analysis
- **Component Library**: Shared UI components (charts, tables, forms)

#### **1.3.2 API Gateway**
- **Technology**: Kong API Gateway or AWS Application Load Balancer
- **Responsibilities**:
  - Request routing to microservices
  - Authentication token validation
  - Rate limiting and throttling
  - Request/response transformation
  - API versioning (v1, v2)
  - Logging and monitoring

#### **1.3.3 Microservices**

**Auth Service**
- User authentication and authorization
- JWT token management
- OAuth integration (Google, Facebook)
- API key generation and validation
- Session management

**Keyword Service**
- Keyword search and suggestions
- Keyword metrics (volume, CPC, competition)
- Related keywords and questions
- Keyword difficulty calculation
- Multi-language support

**Domain Service**
- Domain overview and metrics
- Backlink analysis
- Top pages analysis
- Organic keyword tracking
- Domain authority calculation

**SERP Service**
- SERP position tracking
- Featured snippets detection
- Local pack results
- Ads analysis
- SERP feature identification

**Tracking Service**
- Keyword rank tracking
- Position monitoring
- Ranking history
- Competitor tracking
- Alert system for rank changes

**Analytics Engine**
- Trend analysis
- Opportunity scoring
- Content gap analysis
- Competitive intelligence
- Predictive analytics

**Crawler Service**
- Distributed web crawler
- SERP scraping
- Backlink discovery
- Site auditing
- Content extraction

**Report Builder**
- PDF report generation
- Scheduled reports
- White-label reports
- Data export (CSV, Excel)

#### **1.3.4 Data Storage Components**

**PostgreSQL** (Primary Relational Database)
- User accounts and subscriptions
- Projects and settings
- Normalized keyword and domain data
- Transactional data

**MongoDB** (Document Store)
- Raw crawl data
- SERP snapshots
- Historical data
- Flexible schema data

**Redis** (Caching Layer)
- Session cache
- API response cache
- Real-time ranking cache
- Queue management
- Rate limiting counters

**Elasticsearch**
- Full-text keyword search
- Log aggregation and search
- Analytics queries
- Real-time suggestions

**S3/Object Storage**
- Backlink data archives
- Historical SERP screenshots
- Report files
- User uploads

### 1.4 Technology Stack Recommendation

#### **Backend Stack**
```
Language: Python 3.11+ (Primary), Node.js (Real-time services)
Frameworks: 
    - FastAPI (API services) - High performance, async
    - Django (Admin panel, complex business logic)
    - Express.js (Real-time notifications)
  
Task Queue: Celery with RabbitMQ or AWS SQS
Background Workers: Celery workers (CPU-intensive), Node workers (I/O)
Caching: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+
Message Broker: RabbitMQ or Apache Kafka (for high throughput)
```

#### **Frontend Stack**
```
Framework: Next.js 14+ (React with SSR/SSG)
State Management: Zustand or Redux Toolkit
UI Library: TailwindCSS + shadcn/ui components
Charts: Recharts or Apache ECharts
Data Tables: TanStack Table
Forms: React Hook Form + Zod validation
API Client: Axios with React Query for caching
```

#### **Database Stack**
```
Primary: PostgreSQL 15+ with Citus extension (for sharding)
Document: MongoDB 6+ with replica sets
Cache: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+ with ILM policies
Time-series: TimescaleDB (extension on PostgreSQL) for tracking data
```

#### **Infrastructure**
```
Container: Docker + Docker Compose (dev), Kubernetes (production)
Orchestration: Kubernetes (EKS/GKE) or AWS ECS
CI/CD: GitHub Actions or GitLab CI
Monitoring: Prometheus + Grafana, ELK Stack
APM: New Relic or Datadog
Error Tracking: Sentry
```

#### **External Services**
```
CDN: CloudFlare Enterprise
Email: SendGrid or AWS SES
Payment: Stripe
Analytics: Mixpanel, Google Analytics 4
Search APIs: Google Custom Search API, Bing Web Search API
Proxy Services: ScraperAPI, Bright Data, Oxylabs
```

### 1.5 Scalability Strategy

#### **Horizontal Scaling**
- All services stateless for easy replication
- Auto-scaling based on CPU/memory/queue depth
- Load balancers distribute traffic across instances
- Database read replicas for query distribution

#### **Caching Strategy**

**L1 Cache (Application Level)**
- In-memory caching in each service instance
- LRU cache with 5-minute TTL for hot data
- Size limit: 512MB per instance

**L2 Cache (Redis)**
```
Keyword Metrics: TTL 24 hours
Domain Overview: TTL 12 hours  
SERP Results: TTL 6 hours
User Sessions: TTL 30 minutes
API Responses: TTL based on data freshness
Rate Limiting: Real-time, no TTL
```

**L3 Cache (CDN)**
- Static assets: 1 year cache
- API responses: 5 minutes cache with stale-while-revalidate
- Images and fonts: 6 months cache

#### **Database Sharding Strategy**

**PostgreSQL Sharding** (using Citus)
```
Shard Key: domain_hash (for domain data)
Shard Key: keyword_hash (for keyword data)
Shard Key: user_id (for user data)

Distribution:
- 32 shards for keyword data (hash distribution)
- 16 shards for domain data
- 8 shards for user/project data
```

**MongoDB Sharding**
```
Shard Key: {country: 1, language: 1, keyword_hash: 1}
Zones: US, EU, ASIA for geographic distribution
Chunk Size: 64MB
```

### 1.6 Queue and Worker Setup

#### **Task Queue Architecture**

```
┌─────────────────────────────────────────────────────┐
│                  TASK PRODUCERS                      │
│  [API Services] [Scheduled Jobs] [User Actions]     │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│              MESSAGE BROKER (RabbitMQ)              │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ crawl_queue  │  │ analytics_q  │  │ email_q  │ │
│  │ Priority: 1  │  │ Priority: 2  │  │Priority:3│ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└──┬──────────┬──────────────┬────────────┬─────────┘
   │          │              │            │
┌──▼────┐ ┌──▼────┐  ┌──────▼─────┐  ┌──▼──────┐
│Crawler│ │SERP   │  │ Analytics  │  │  Email  │
│Worker │ │Worker │  │  Worker    │  │ Worker  │
│x20    │ │x10    │  │  x5        │  │  x3     │
└───────┘ └───────┘  └────────────┘  └─────────┘
```

#### **Worker Types and Configuration**

**1. Crawler Workers** (CPU + Network intensive)
```
Count: 20-50 workers (auto-scale)
Resources: 2 CPU, 4GB RAM per worker
Tasks:
  - SERP crawling (priority: high)
  - Backlink discovery (priority: medium)
  - Site auditing (priority: low)
  - Content extraction
Max Concurrency: 5 tasks per worker
Retry Strategy: Exponential backoff (max 3 retries)
Timeout: 60 seconds per task
```

**2. Analytics Workers** (CPU intensive)
```
Count: 5-10 workers
Resources: 4 CPU, 8GB RAM per worker
Tasks:
  - Keyword difficulty calculation
  - Domain authority scoring
  - Trend analysis
  - Content gap analysis
  - Opportunity scoring
Max Concurrency: 3 tasks per worker
Timeout: 120 seconds per task
```

**3. Data Processing Workers** (Memory intensive)
```
Count: 10-20 workers
Resources: 2 CPU, 8GB RAM per worker
Tasks:
  - Bulk data import
  - Data enrichment
  - Metric aggregation
  - Historical data processing
Max Concurrency: 2 tasks per worker
Batch Size: 1000 records per batch
```

**4. Notification Workers** (I/O intensive)
```
Count: 3-5 workers
Resources: 1 CPU, 2GB RAM per worker
Tasks:
  - Email notifications
  - Webhook delivery
  - Report generation
  - Alert processing
Max Concurrency: 10 tasks per worker
Timeout: 30 seconds per task
```

#### **Queue Priority System**
```
Priority 1 (Highest): Real-time user requests
Priority 2 (High): Scheduled tracking updates
Priority 3 (Medium): Background data refresh
Priority 4 (Low): Bulk data processing
Priority 5 (Lowest): Analytics and reports
```

---

## 2. Data Flow & Processing

### 2.1 Primary Workflows

#### **2.1.1 Keyword Research Workflow**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: User Input                                           │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ User enters: "best running shoes"                       │  │
│ │ Filters: Country=US, Language=EN, Device=Desktop        │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 2: Request Processing (API Gateway)                     │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ • Validate JWT token                                    │  │
│ │ • Check rate limits (100 req/min for Pro plan)          │  │
│ │ • Normalize keyword (lowercase, trim)                   │  │
│ │ • Generate cache key: "kw:en:us:desktop:best_running..."│  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 3: Cache Lookup (Redis L2 Cache)                        │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ GET cache_key                                           │  │
│ │ TTL: 24 hours                                           │  │
│ │                                                         │  │
│ │ IF FOUND → Return cached response (80% of requests)     │  │
│ │ IF NOT FOUND → Continue to Step 4                       │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Cache Miss)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 4: Database Query (PostgreSQL + Elasticsearch)          │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ Query keywords table:                                   │  │
│ │   SELECT * FROM keywords                                │  │
│ │   WHERE keyword_normalized = 'best running shoes'       │  │
│ │   AND country = 'US' AND language = 'EN'                │  │
│ │                                                         │  │
│ │ IF FOUND and data_age < 30 days:                        │  │
│ │   → Return from database                                │  │
│ │   → Update cache                                        │  │
│ │ IF NOT FOUND or data_age > 30 days:                     │  │
│ │   → Continue to Step 5 (Fresh Data Fetch)               │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Database Miss or Stale)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 5: External Data Fetch (Async Job)                      │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ Publish job to RabbitMQ: "crawl_queue"                  │  │
│ │ {                                                       │  │
│ │   "job_id": "uuid",                                     │  │
│ │   "keyword": "best running shoes",                      │  │
│ │   "country": "US",                                      │  │
│ │   "sources": ["google_api", "serp_scraper"],            │  │
│ │   "priority": "high"                                    │  │
│ │ }                                                       │  │
│ │                                                         │  │
│ │ Return immediate response to user:                      │  │
│ │ {                                                       │  │
│ │   "status": "processing",                               │  │
│ │   "job_id": "uuid",                                     │  │
│ │   "estimated_time": "10-30 seconds",                    │  │
│ │   "partial_data": { ... } ← if available                │  │
│ │ }                                                       │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 6: Crawler Worker Processing                            │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ Worker picks up job from queue                          │  │
│ │                                                         │  │
│ │ Parallel data fetching (asyncio):                       │  │
│ │ ┌─────────────┐  ┌─────────────┐  ┌──────────────┐      │  │
│ │ │ Google Ads  │  │ Google      │  │ Third-party  │      │  │
│ │ │ Keyword API │  │ Trends API  │  │ SEO API      │      │  │
│ │ │ (volume,CPC)│  │ (12mo trend)│  │ (difficulty) │      │  │
│ │ └─────────────┘  └─────────────┘  └──────────────┘      │  │
│ │                                                         │  │
│ │ Data aggregation and enrichment:                        │  │
│ │ • Calculate average from multiple sources               │  │
│ │ • Compute keyword difficulty score                      │  │
│ │ • Generate related keywords                             │  │
│ │ • Extract questions and suggestions                     │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 7: Data Storage                                         │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ PostgreSQL:                                             │  │
│ │   INSERT INTO keywords (keyword, country, language, ...)│  │
│ │   INSERT INTO keyword_metrics (keyword_id, volume, ...) │  │
│ │   INSERT INTO keyword_trends (keyword_id, month, ...)   │  │
│ │                                                         │  │
│ │ Elasticsearch:                                          │  │
│ │   Index document for fast search and suggestions        │  │
│ │                                                         │  │
│ │ Redis Cache:                                            │  │
│ │   SET cache_key = {data} EX 86400 (24 hours)            │  │
│ │                                                         │  │
│ │ MongoDB (Raw Data Archive):                             │  │
│ │   Store original API responses for audit trail          │  │
│ └─────────────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 8: WebSocket Notification                               │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ Push update to user's active session:                   │  │
│ │ {                                                       │  │
│ │   "event": "keyword_data_ready",                        │  │
│ │   "job_id": "uuid",                                     │  │
│ │   "data": { full keyword metrics }                      │  │
│ │ }                                                       │  │
│ │                                                         │  │
│ │ Frontend updates UI with full data                      │  │
│ └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

#### **2.1.2 Domain Analysis Workflow**

```
User Input: "example.com"
    ↓
1. Domain Validation & Normalization
   • Check DNS resolution
   • Normalize to canonical form
   • Extract domain metadata
    ↓
2. Cache Check (Redis)
   • Key: "domain:example.com:overview"
   • TTL: 12 hours
   IF FOUND → Return cached data
    ↓
3. Database Lookup (PostgreSQL)
   • Check domains table
   • Check domain_metrics table
   • If data < 7 days old → Return
    ↓
4. Trigger Async Jobs (if needed)
   Job 1: Backlink Crawler
     → Crawl backlink sources
     → Discover new backlinks
     → Update backlink database
   
   Job 2: Organic Keyword Scraper
     → Fetch ranking keywords
     → Update keyword positions
     → Calculate traffic estimates
   
   Job 3: Top Pages Analyzer
     → Crawl sitemap
     → Analyze top-performing pages
     → Calculate page metrics
   
   Job 4: Domain Authority Calculator
     → Aggregate backlink data
     → Apply authority algorithm
     → Update domain score
    ↓
5. Data Aggregation
   • Combine all metrics
   • Calculate derived values
   • Generate summary stats
    ↓
6. Storage & Cache Update
   • Update PostgreSQL
   • Refresh Redis cache
   • Index in Elasticsearch
    ↓
7. Return Response
   • Domain overview
   • Top metrics
   • Recent changes
   • Recommendations
```

#### **2.1.3 SERP Analysis Workflow**

```
User Input: Keyword + Location
    ↓
1. SERP Fetch Request
   • Generate SERP cache key
   • Check Redis (TTL: 6 hours)
    ↓
2. Cache Miss → Trigger Crawler
   Job: SERP Scraper
     → Use rotating proxies
     → Fetch Google SERP page
     → Extract organic results
     → Extract paid ads
     → Extract SERP features
     → Handle CAPTCHA if needed
    ↓
3. SERP Data Processing
   • Parse HTML/JSON
   • Extract result URLs
   • Identify result types
   • Calculate positions
   • Detect SERP features
    ↓
4. Domain Enrichment
   For each result URL:
     → Lookup domain metrics
     → Calculate domain strength
     → Fetch page metrics
     → Analyze content
    ↓
5. Competitive Analysis
   • Compare domain authorities
   • Analyze content gaps
   • Calculate difficulty score
   • Generate insights
    ↓
6. Storage
   • PostgreSQL: serp_results table
   • MongoDB: Raw SERP snapshots
   • Redis: Cached response
    ↓
7. Return Enriched SERP Data
```

### 2.2 Data Pipeline Architecture

#### **2.2.1 Data Import Pipeline**

```
┌────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                            │
│  [Google APIs] [Bing APIs] [Third-party] [User Uploads]    │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              INGESTION LAYER                               │
│  • API adapters with retry logic                           │
│  • Rate limiting per source                                │
│  • Request queuing and scheduling                          │
│  • Error handling and logging                              │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│            VALIDATION & CLEANING                           │
│  • Schema validation                                       │
│  • Data type conversion                                    │
│  • Null handling                                           │
│  • Duplicate detection                                     │
│  • Outlier detection                                       │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              TRANSFORMATION                                │
│  • Normalization (keywords, URLs)                          │
│  • Enrichment (add metadata)                               │
│  • Aggregation (combine sources)                           │
│  • Calculation (derived metrics)                           │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                LOADING LAYER                               │
│  • Batch insertion to PostgreSQL                           │
│  • Bulk indexing to Elasticsearch                          │
│  • Document insertion to MongoDB                           │
│  • Cache warming (Redis)                                   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│             POST-PROCESSING                                │
│  • Trigger analytics jobs                                  │
│  • Update aggregated tables                                │
│  • Invalidate stale cache                                  │
│  • Send notifications                                      │
└────────────────────────────────────────────────────────────┘
```

#### **2.2.2 Data Processing Stages**

**Stage 1: Raw Data Collection**
```python
# Pseudo-code
async def collect_keyword_data(keyword, country, language):
    sources = [
        fetch_google_ads_data(keyword, country),
        fetch_google_trends(keyword),
        fetch_third_party_api(keyword, country),
        scrape_serp_if_needed(keyword, country)
    ]
    
    results = await asyncio.gather(*sources, return_exceptions=True)
    
    return {
        'raw_data': results,
        'timestamp': utc_now(),
        'sources_succeeded': count_successes(results)
    }
```

**Stage 2: Data Cleaning**
```python
def clean_keyword_data(raw_data):
    cleaned = {
        'keyword': normalize_keyword(raw_data['keyword']),
        'volume': validate_volume(raw_data['volume']),
        'cpc': validate_currency(raw_data['cpc']),
        'competition': normalize_0_to_1(raw_data['competition']),
        'trend_data': interpolate_missing_months(raw_data['trend'])
    }
    
    # Remove outliers
    if is_outlier(cleaned['volume']):
        cleaned['volume_confidence'] = 'low'
    
    return cleaned
```

**Stage 3: Data Enrichment**
```python
def enrich_keyword_data(cleaned_data):
    enriched = cleaned_data.copy()
    
    # Calculate derived metrics
    enriched['difficulty_score'] = calculate_difficulty(
        cleaned_data['competition'],
        cleaned_data['volume'],
        cleaned_data['serp_features']
    )
    
    # Add related data
    enriched['related_keywords'] = find_related_keywords(
        cleaned_data['keyword']
    )
    
    # Add semantic data
    enriched['intent'] = classify_search_intent(
        cleaned_data['keyword']
    )
    
    return enriched
```

**Stage 4: Data Storage**
```python
async def store_keyword_data(enriched_data):
    # Parallel storage operations
    await asyncio.gather(
        store_in_postgres(enriched_data),
        index_in_elasticsearch(enriched_data),
        cache_in_redis(enriched_data),
        archive_in_mongodb(enriched_data['raw_data'])
    )
```

### 2.3 API Rate Limiting & Proxy Rotation

#### **2.3.1 Rate Limiting Strategy**

```
┌─────────────────────────────────────────────────────────────┐
│                  RATE LIMITING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: API Gateway Level (Per User)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Free Plan:     10 requests/minute                     │  │
│  │ Pro Plan:      100 requests/minute                    │  │
│  │ Agency Plan:   500 requests/minute                    │  │
│  │ Enterprise:    Custom limits                          │  │
│  │                                                       │  │
│  │ Implementation: Token bucket algorithm in Redis       │  │
│  │ Key: "ratelimit:user:{user_id}:{endpoint}"            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 2: Service Level (Per External API)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Google Ads API:    15,000/day (shared across users)   │  │
│  │ Google Trends:     1,500/hour                         │  │
│  │ Bing API:          5,000/month                        │  │
│  │ Third-party APIs:  Varies by provider                 │  │
│  │                                                       │  │
│  │ Implementation: Distributed counter in Redis          │  │
│  │ Key: "api_quota:{provider}:{date}"                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 3: Crawler Level (Per Proxy/IP)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Max 60 requests/hour per IP                           │  │
│  │ Randomized delays: 2-5 seconds                        │  │
│  │ Rotating user agents                                  │  │
│  │ Cookie management                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### **2.3.2 Proxy Rotation System**

```
┌─────────────────────────────────────────────────────────────┐
│                  PROXY POOL MANAGEMENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Proxy Sources:                                             │
│  • Residential Proxies (Bright Data, Oxylabs)               │
│  • Datacenter Proxies (backup)                              │
│  • Mobile Proxies (for mobile SERP)                         │
│                                                             │
│  Pool Size: 1,000-10,000 rotating proxies                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    ROTATION STRATEGY                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Round-Robin Selection                                   │
│     • Distribute requests evenly                            │
│     • Track usage per proxy                                 │
│                                                             │
│  2. Health Checking                                         │
│     • Periodic connectivity tests                           │
│     • Response time monitoring                              │
│     • Success rate tracking                                 │
│     • Automatic removal of dead proxies                     │
│                                                             │
│  3. Geographic Targeting                                    │
│     • Match proxy location to search location               │
│     • US proxy for US searches                              │
│     • Local proxies for local SERP                          │
│                                                             │
│  4. Cooldown Management                                     │
│     • 5-minute cooldown after 50 requests                   │
│     • Exponential backoff on errors                         │
│     • Automatic proxy cycling                               │
│                                                             │
│  5. CAPTCHA Handling                                        │
│     • Detect CAPTCHA challenges                             │
│     • Mark proxy as temporary blocked                       │
│     • Integrate CAPTCHA solving service (2Captcha)          │
│     • Fallback to manual verification if needed             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Proxy Selection Algorithm:

```python
def select_proxy(country, previous_failures=[]):
    # Get healthy proxies for country
    candidate_proxies = redis.smembers(f'proxies:healthy:{country}')
    
    # Remove recently failed proxies
    candidate_proxies -= set(previous_failures)
    
    # Sort by recent usage (prefer least recently used)
    proxies_with_scores = []
    for proxy in candidate_proxies:
        last_used = redis.get(f'proxy:last_used:{proxy}')
        success_rate = redis.get(f'proxy:success_rate:{proxy}')
        
        score = calculate_proxy_score(last_used, success_rate)
        proxies_with_scores.append((proxy, score))
    
    # Select best proxy
    selected_proxy = max(proxies_with_scores, key=lambda x: x[1])[0]
    
    # Mark as in-use
    redis.set(f'proxy:last_used:{selected_proxy}', time.now())
    
    return selected_proxy
```

---

## 3. Database Design

### 3.1 Database Schema Overview

The system uses **four database technologies** for different purposes:

1. **PostgreSQL** - Primary relational data (users, projects, core metrics)
2. **MongoDB** - Document storage (raw crawl data, flexible schemas)
3. **Redis** - Caching and real-time data
4. **Elasticsearch** - Full-text search and analytics

### 3.2 PostgreSQL Schema

#### **3.2.1 Users & Authentication**

```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'free', -- free, pro, agency, enterprise
    plan_status VARCHAR(50) DEFAULT 'active', -- active, trial, expired, cancelled
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_plan_type ON users(plan_type);

-- User sessions
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- User subscriptions
CREATE TABLE subscriptions (
    subscription_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL, -- active, cancelled, expired, past_due
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);

-- User quotas and usage
CREATE TABLE user_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    quota_type VARCHAR(50) NOT NULL, -- keyword_searches, domain_analyses, rank_checks
    quota_limit INT NOT NULL,
    quota_used INT DEFAULT 0,
    reset_period VARCHAR(50) NOT NULL, -- daily, monthly
    last_reset_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quotas_user_id ON user_quotas(user_id);
CREATE UNIQUE INDEX idx_quotas_user_type ON user_quotas(user_id, quota_type);
```

#### **3.2.2 Projects & Organization**

```sql
-- Projects (workspace for organizing keywords and domains)
CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    target_country VARCHAR(2) DEFAULT 'US',
    target_language VARCHAR(5) DEFAULT 'en',
    target_location VARCHAR(255), -- city name for local SEO
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_archived BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_country ON projects(target_country);

-- Project members (for team collaboration)
CREATE TABLE project_members (
    member_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- owner, admin, editor, viewer
    invited_by BIGINT REFERENCES users(user_id),
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

CREATE INDEX idx_members_project_id ON project_members(project_id);
CREATE INDEX idx_members_user_id ON project_members(user_id);
```

#### **3.2.3 Keywords Core Tables**

```sql
-- Keywords master table
CREATE TABLE keywords (
    keyword_id BIGSERIAL PRIMARY KEY,
    keyword_text TEXT NOT NULL,
    keyword_normalized TEXT NOT NULL, -- lowercase, trimmed
    keyword_hash VARCHAR(64) NOT NULL, -- for sharding
    country VARCHAR(2) NOT NULL,
    language VARCHAR(5) NOT NULL,
    device_type VARCHAR(20) DEFAULT 'desktop', -- desktop, mobile, tablet
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_fetched_at TIMESTAMP,
    data_source VARCHAR(50), -- google_ads, bing, semrush_api
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(keyword_normalized, country, language, device_type)
);

CREATE INDEX idx_keywords_normalized ON keywords(keyword_normalized);
CREATE INDEX idx_keywords_hash ON keywords(keyword_hash);
CREATE INDEX idx_keywords_country ON keywords(country);
CREATE INDEX idx_keywords_updated_at ON keywords(updated_at);

-- Partitioning strategy (if using native partitioning)
-- CREATE TABLE keywords_us PARTITION OF keywords FOR VALUES IN ('US');
-- CREATE TABLE keywords_uk PARTITION OF keywords FOR VALUES IN ('UK');
-- CREATE TABLE keywords_in PARTITION OF keywords FOR VALUES IN ('IN');

-- Keyword metrics (search volume, CPC, competition)
CREATE TABLE keyword_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    search_volume BIGINT,
    search_volume_trend VARCHAR(20), -- up, down, stable
    cpc_min DECIMAL(10,2),
    cpc_max DECIMAL(10,2),
    cpc_avg DECIMAL(10,2),
    competition_score DECIMAL(3,2), -- 0.00 to 1.00
    competition_level VARCHAR(20), -- low, medium, high
    difficulty_score INT, -- 0-100
    opportunity_score INT, -- 0-100 (custom metric)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, metric_date)
);

CREATE INDEX idx_metrics_keyword_id ON keyword_metrics(keyword_id);
CREATE INDEX idx_metrics_date ON keyword_metrics(metric_date);
CREATE INDEX idx_metrics_volume ON keyword_metrics(search_volume);
CREATE INDEX idx_metrics_difficulty ON keyword_metrics(difficulty_score);

-- Keyword trends (12-month historical data)
CREATE TABLE keyword_trends (
    trend_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    trend_month DATE NOT NULL, -- first day of month
    trend_value INT NOT NULL, -- 0-100 (relative interest)
    search_volume_estimate BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, trend_month)
);

CREATE INDEX idx_trends_keyword_id ON keyword_trends(keyword_id);
CREATE INDEX idx_trends_month ON keyword_trends(trend_month);

-- Related keywords
CREATE TABLE related_keywords (
    relation_id BIGSERIAL PRIMARY KEY,
    source_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    related_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL, -- similar, broader, narrower, question
    relevance_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_keyword_id, related_keyword_id, relation_type)
);

CREATE INDEX idx_related_source ON related_keywords(source_keyword_id);
CREATE INDEX idx_related_target ON related_keywords(related_keyword_id);
CREATE INDEX idx_related_type ON related_keywords(relation_type);

-- Keyword questions (People Also Ask)
CREATE TABLE keyword_questions (
    question_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50), -- who, what, when, where, why, how
    frequency_score INT, -- how often it appears
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_keyword_id ON keyword_questions(keyword_id);
CREATE INDEX idx_questions_type ON keyword_questions(question_type);

-- User keyword lists (saved keywords)
CREATE TABLE user_keyword_lists (
    list_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    tags VARCHAR(255)[],
    priority INT, -- 1-5
    UNIQUE(project_id, keyword_id)
);

CREATE INDEX idx_user_lists_project ON user_keyword_lists(project_id);
CREATE INDEX idx_user_lists_keyword ON user_keyword_lists(keyword_id);
```

#### **3.2.4 Domains & Backlinks**

```sql
-- Domains master table
CREATE TABLE domains (
    domain_id BIGSERIAL PRIMARY KEY,
    domain_name VARCHAR(255) UNIQUE NOT NULL,
    domain_normalized VARCHAR(255) NOT NULL, -- lowercase
    domain_hash VARCHAR(64) NOT NULL,
    tld VARCHAR(50),
    is_subdomain BOOLEAN DEFAULT FALSE,
    root_domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_crawled_at TIMESTAMP,
    crawl_status VARCHAR(50), -- pending, in_progress, completed, failed
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_domains_normalized ON domains(domain_normalized);
CREATE INDEX idx_domains_hash ON domains(domain_hash);
CREATE INDEX idx_domains_tld ON domains(tld);
CREATE INDEX idx_domains_root ON domains(root_domain);

-- Domain metrics
CREATE TABLE domain_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    domain_authority INT, -- 0-100 (our custom score)
    page_authority_avg DECIMAL(5,2),
    total_backlinks BIGINT,
    unique_domains BIGINT,
    dofollow_backlinks BIGINT,
    nofollow_backlinks BIGINT,
    total_referring_ips BIGINT,
    organic_traffic_estimate BIGINT,
    organic_keywords_count BIGINT,
    organic_traffic_value DECIMAL(12,2), -- estimated value in USD
    paid_traffic_estimate BIGINT,
    social_signals JSONB, -- {facebook: 1000, twitter: 500, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, metric_date)
);

CREATE INDEX idx_domain_metrics_domain ON domain_metrics(domain_id);
CREATE INDEX idx_domain_metrics_date ON domain_metrics(metric_date);
CREATE INDEX idx_domain_metrics_authority ON domain_metrics(domain_authority);

-- Backlinks (huge table - consider sharding)
CREATE TABLE backlinks (
    backlink_id BIGSERIAL PRIMARY KEY,
    target_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    source_domain_id BIGINT REFERENCES domains(domain_id),
    source_url TEXT NOT NULL,
    source_page_title TEXT,
    anchor_text TEXT,
    link_type VARCHAR(20), -- dofollow, nofollow, redirect
    first_seen_at TIMESTAMP NOT NULL,
    last_seen_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    http_status INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_backlinks_target_domain ON backlinks(target_domain_id);
CREATE INDEX idx_backlinks_source_domain ON backlinks(source_domain_id);
CREATE INDEX idx_backlinks_first_seen ON backlinks(first_seen_at);
CREATE INDEX idx_backlinks_active ON backlinks(is_active);

-- For sharding large backlinks table:
-- Shard by target_domain_hash using Citus or manual sharding

-- Domain top pages
CREATE TABLE domain_top_pages (
    page_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    page_url TEXT NOT NULL,
    page_title TEXT,
    page_type VARCHAR(50), -- article, product, category, homepage
    organic_traffic_estimate BIGINT,
    organic_keywords_count INT,
    backlinks_count INT,
    social_shares INT,
    content_length INT,
    last_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, page_url)
);

CREATE INDEX idx_top_pages_domain ON domain_top_pages(domain_id);
CREATE INDEX idx_top_pages_traffic ON domain_top_pages(organic_traffic_estimate DESC);

-- Domain organic keywords
CREATE TABLE domain_organic_keywords (
    ranking_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    ranking_url TEXT NOT NULL,
    position INT NOT NULL,
    position_date DATE NOT NULL,
    previous_position INT,
    traffic_estimate INT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, keyword_id, position_date)
);

CREATE INDEX idx_organic_domain ON domain_organic_keywords(domain_id);
CREATE INDEX idx_organic_keyword ON domain_organic_keywords(keyword_id);
CREATE INDEX idx_organic_position ON domain_organic_keywords(position);
CREATE INDEX idx_organic_date ON domain_organic_keywords(position_date);
```

#### **3.2.5 SERP Data**

```sql
-- SERP results snapshots
CREATE TABLE serp_results (
    serp_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    search_date DATE NOT NULL,
    search_location VARCHAR(255), -- city/region for local searches
    device_type VARCHAR(20) DEFAULT 'desktop',
    total_results BIGINT,
    serp_features JSONB, -- {featured_snippet: true, local_pack: true, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, search_date, search_location, device_type)
);

CREATE INDEX idx_serp_keyword ON serp_results(keyword_id);
CREATE INDEX idx_serp_date ON serp_results(search_date);
CREATE INDEX idx_serp_location ON serp_results(search_location);

-- Individual SERP positions
CREATE TABLE serp_positions (
    position_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    position INT NOT NULL,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    title TEXT,
    description TEXT,
    result_type VARCHAR(50), -- organic, paid, featured_snippet, local, image, video
    serp_features JSONB, -- rich snippet data
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_positions_serp ON serp_positions(serp_id);
CREATE INDEX idx_positions_domain ON serp_positions(domain_id);
CREATE INDEX idx_positions_position ON serp_positions(position);

-- SERP features (detailed)
CREATE TABLE serp_features (
    feature_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    feature_type VARCHAR(50) NOT NULL, -- featured_snippet, local_pack, people_also_ask, etc.
    feature_data JSONB NOT NULL, -- flexible structure for different features
    feature_position INT,
    domain_id BIGINT REFERENCES domains(domain_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_features_serp ON serp_features(serp_id);
CREATE INDEX idx_features_type ON serp_features(feature_type);
CREATE INDEX idx_features_domain ON serp_features(domain_id);
```

#### **3.2.6 Keyword Tracking**

```sql
-- Keyword tracking projects
CREATE TABLE tracking_projects (
    tracking_project_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    target_domain VARCHAR(255) NOT NULL,
    check_frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    next_check_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tracking_project ON tracking_projects(project_id);
CREATE INDEX idx_tracking_next_check ON tracking_projects(next_check_at);

-- Tracked keywords
CREATE TABLE tracked_keywords (
    tracked_keyword_id BIGSERIAL PRIMARY KEY,
    tracking_project_id BIGINT REFERENCES tracking_projects(tracking_project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    target_url TEXT, -- specific URL to track
    tags VARCHAR(255)[],
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracking_project_id, keyword_id)
);

CREATE INDEX idx_tracked_project ON tracked_keywords(tracking_project_id);
CREATE INDEX idx_tracked_keyword ON tracked_keywords(keyword_id);

-- Ranking history (time-series data - consider TimescaleDB)
CREATE TABLE ranking_history (
    history_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    check_date DATE NOT NULL,
    check_time TIMESTAMP NOT NULL,
    position INT, -- NULL if not ranking
    ranking_url TEXT,
    serp_features VARCHAR(50)[], -- features present at time of check
    pixel_rank INT, -- position in pixels from top
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracked_keyword_id, check_date, check_time)
);

CREATE INDEX idx_history_tracked ON ranking_history(tracked_keyword_id);
CREATE INDEX idx_history_date ON ranking_history(check_date);
CREATE INDEX idx_history_position ON ranking_history(position);

-- Convert to TimescaleDB hypertable for better time-series performance
-- SELECT create_hypertable('ranking_history', 'check_time');

-- Ranking alerts
CREATE TABLE ranking_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- position_change, entered_top10, dropped_out, etc.
    alert_threshold INT, -- e.g., alert if change > 5 positions
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_tracked ON ranking_alerts(tracked_keyword_id);

-- Alert history
CREATE TABLE alert_notifications (
    notification_id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT REFERENCES ranking_alerts(alert_id) ON DELETE CASCADE,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    trigger_date DATE NOT NULL,
    old_position INT,
    new_position INT,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_alert ON alert_notifications(alert_id);
CREATE INDEX idx_notifications_date ON alert_notifications(trigger_date);
```

#### **3.2.7 Content Analysis & Gap Analysis**

```sql
-- Content analysis
CREATE TABLE content_analysis (
    analysis_id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    keyword_id BIGINT, -- target keyword for analysis
    content_length INT,
    word_count INT,
    readability_score DECIMAL(5,2),
    keyword_density DECIMAL(5,2),
    h1_count INT,
    h2_count INT,
    image_count INT,
    internal_links_count INT,
    external_links_count INT,
    schema_markup JSONB,
    meta_title TEXT,
    meta_description TEXT,
    analyzed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_content_domain ON content_analysis(domain_id);
CREATE INDEX idx_content_keyword ON content_analysis(keyword_id);

-- Content gap analysis (comparing domains)
CREATE TABLE content_gaps (
    gap_id BIGSERIAL PRIMARY KEY,
    source_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    competitor_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    competitor_position INT,
    source_position INT, -- NULL if not ranking
    gap_score INT, -- 0-100
    opportunity_score INT, -- 0-100
    analysis_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_domain_id, competitor_domain_id, keyword_id, analysis_date)
);

CREATE INDEX idx_gaps_source ON content_gaps(source_domain_id);
CREATE INDEX idx_gaps_competitor ON content_gaps(competitor_domain_id);
CREATE INDEX idx_gaps_keyword ON content_gaps(keyword_id);
CREATE INDEX idx_gaps_score ON content_gaps(gap_score DESC);
```

#### **3.2.8 API Cache & Search History**

```sql
-- API response cache metadata
CREATE TABLE api_cache_metadata (
    cache_id BIGSERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    entity_id BIGINT, -- keyword_id, domain_id, etc.
    cache_ttl INT NOT NULL, -- seconds
    cached_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    hit_count INT DEFAULT 0,
    last_hit_at TIMESTAMP
);

CREATE INDEX idx_cache_key ON api_cache_metadata(cache_key);
CREATE INDEX idx_cache_expires ON api_cache_metadata(expires_at);
CREATE INDEX idx_cache_type ON api_cache_metadata(cache_type);

-- Search history (for analytics and suggestions)
CREATE TABLE search_history (
    search_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    search_query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    search_filters JSONB, -- country, language, device, etc.
    result_count INT,
    searched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_query ON search_history(search_query);
CREATE INDEX idx_search_date ON search_history(searched_at);
```

#### **3.2.9 External API Integration Tracking**

```sql
-- API integration logs
CREATE TABLE api_integration_logs (
    log_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL, -- google_ads, google_trends, semrush, etc.
    endpoint VARCHAR(255) NOT NULL,
    request_method VARCHAR(10),
    request_params JSONB,
    response_status INT,
    response_time_ms INT,
    error_message TEXT,
    requested_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_logs_provider ON api_integration_logs(provider);
CREATE INDEX idx_api_logs_date ON api_integration_logs(requested_at);
CREATE INDEX idx_api_logs_status ON api_integration_logs(response_status);

-- API quota tracking
CREATE TABLE api_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    quota_type VARCHAR(50) NOT NULL, -- daily, monthly
    quota_limit BIGINT NOT NULL,
    quota_used BIGINT DEFAULT 0,
    quota_period DATE NOT NULL,
    reset_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, quota_type, quota_period)
);

CREATE INDEX idx_api_quotas_provider ON api_quotas(provider);
CREATE INDEX idx_api_quotas_period ON api_quotas(quota_period);
```

#### **3.2.10 Indexing & Partitioning Strategy**

```sql
-- Composite indexes for common query patterns

-- Keyword searches by country and language
CREATE INDEX idx_keywords_country_lang_norm 
ON keywords(country, language, keyword_normalized);

-- Keyword metrics for trending keywords
CREATE INDEX idx_metrics_volume_date 
ON keyword_metrics(search_volume DESC, metric_date DESC);

-- Domain backlinks by date and status
CREATE INDEX idx_backlinks_target_active_date 
ON backlinks(target_domain_id, is_active, last_seen_at DESC);

-- SERP tracking queries
CREATE INDEX idx_ranking_history_tracked_date 
ON ranking_history(tracked_keyword_id, check_date DESC);

-- Content gaps by score
CREATE INDEX idx_content_gaps_source_score 
ON content_gaps(source_domain_id, gap_score DESC, analysis_date DESC);

-- Partitioning strategy for large tables
-- Example: Partition ranking_history by month
CREATE TABLE ranking_history_y2025m01 PARTITION OF ranking_history
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE ranking_history_y2025m02 PARTITION OF ranking_history
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automated partition creation via pg_cron or external script
```

### 3.3 MongoDB Collections

MongoDB stores **flexible, document-based data** and **raw crawl results**.

#### **3.3.1 Raw SERP Snapshots**

```javascript
// Collection: serp_snapshots
{
    _id: ObjectId(),
    keyword: "best running shoes",
    country: "US",
    language: "en",
    device: "desktop",
    search_date: ISODate("2025-01-15T10:30:00Z"),
    raw_html: "<html>...</html>", // Full SERP HTML
    raw_json: { /* Google API response */ },
    screenshot_url: "s3://bucket/serp-snapshots/uuid.png",
    results: [
        {
            position: 1,
            url: "https://example.com/running-shoes",
            title: "Best Running Shoes 2025",
            description: "...",
            type: "organic",
            rich_snippet: {
                rating: 4.5,
                reviews: 1200,
                price: "$129.99"
            }
        }
        // ... more results
    ],
    serp_features: [
        {
            type: "featured_snippet",
            content: "...",
            source_url: "https://example.com"
        },
        {
            type: "people_also_ask",
            questions: [...]
        }
    ],
    ads: [
        {
            position: "top1",
            url: "...",
            title: "...",
            description: "..."
        }
    ],
    metadata: {
        total_results: 2340000000,
        search_time_ms: 234,
        proxy_used: "proxy123",
        crawler_version: "2.0"
    },
    created_at: ISODate("2025-01-15T10:30:05Z")
}

// Indexes
db.serp_snapshots.createIndex({ keyword: 1, country: 1, search_date: -1 });
db.serp_snapshots.createIndex({ search_date: -1 });
db.serp_snapshots.createIndex({ "results.url": 1 });
```

#### **3.3.2 Crawl Queue**

```javascript
// Collection: crawl_queue
{
    _id: ObjectId(),
    job_id: "uuid",
    job_type: "serp_crawl", // serp_crawl, backlink_discovery, content_extraction
    priority: 1, // 1-5
    status: "pending", // pending, in_progress, completed, failed
    keyword: "running shoes",
    country: "US",
    language: "en",
    parameters: {
        device: "desktop",
        location: "New York, NY",
        num_results: 100
    },
    retry_count: 0,
    max_retries: 3,
    assigned_worker: null,
    started_at: null,
    completed_at: null,
    error_message: null,
    result_reference: null, // Reference to result in other collection
    created_at: ISODate("2025-01-15T10:00:00Z"),
    updated_at: ISODate("2025-01-15T10:00:00Z"),
    scheduled_for: ISODate("2025-01-15T10:05:00Z")
}

// Indexes
db.crawl_queue.createIndex({ status: 1, priority: 1, scheduled_for: 1 });
db.crawl_queue.createIndex({ job_id: 1 });
db.crawl_queue.createIndex({ created_at: -1 });
```

#### **3.3.3 Backlink Discovery Data**

```javascript
// Collection: backlink_raw_data
{
    _id: ObjectId(),
    target_domain: "example.com",
    target_url: "https://example.com/page",
    discovered_backlinks: [
        {
            source_url: "https://source.com/article",
            source_domain: "source.com",
            anchor_text: "click here",
            link_type: "dofollow",
            context: "... surrounding text ...",
            discovered_at: ISODate("2025-01-15T10:00:00Z"),
            http_status: 200,
            source_page_title: "Article Title",
            source_page_metrics: {
                domain_authority: 45,
                page_authority: 38,
                spam_score: 2
            }
        }
        // ... thousands more
    ],
    crawl_method: "ahrefs_api", // ahrefs_api, moz_api, manual_crawl
    crawl_date: ISODate("2025-01-15T10:00:00Z"),
    total_backlinks_found: 15234,
    metadata: {
        api_version: "v3",
        cost_credits: 50
    },
    created_at: ISODate("2025-01-15T10:30:00Z")
}

// Indexes
db.backlink_raw_data.createIndex({ target_domain: 1, crawl_date: -1 });
db.backlink_raw_data.createIndex({ "discovered_backlinks.source_domain": 1 });
```

#### **3.3.4 Historical Metrics Archive**

```javascript
// Collection: keyword_metrics_archive
// Old keyword metrics (>90 days) moved from PostgreSQL to MongoDB
{
    _id: ObjectId(),
    keyword_id: 12345,
    keyword: "running shoes",
    country: "US",
    metrics_by_month: {
        "2024-01": {
            search_volume: 110000,
            cpc_avg: 1.25,
            competition: 0.78,
            difficulty_score: 65
        },
        "2024-02": {
            search_volume: 135000,
            cpc_avg: 1.32,
            competition: 0.81,
            difficulty_score: 68
        }
        // ... 12+ months of data
    },
    archived_at: ISODate("2025-01-15T00:00:00Z")
}

// Indexes
db.keyword_metrics_archive.createIndex({ keyword_id: 1 });
db.keyword_metrics_archive.createIndex({ archived_at: -1 });
```

### 3.4 Redis Data Structures

Redis handles **caching, real-time data, and queue management**.

#### **3.4.1 Cache Keys Structure**

```redis
# Keyword data cache
Key: "cache:keyword:en:us:desktop:running_shoes"
Type: String (JSON)
TTL: 86400 seconds (24 hours)
Value: {
    "keyword": "running shoes",
    "volume": 110000,
    "cpc": 1.25,
    "difficulty": 65,
    "trend": [100, 95, 98, ...]
}

# Domain overview cache
Key: "cache:domain:example.com:overview"
Type: String (JSON)
TTL: 43200 seconds (12 hours)
Value: {
    "domain": "example.com",
    "authority": 75,
    "backlinks": 125000,
    "keywords": 45000,
    "traffic": 850000
}

# SERP results cache
Key: "cache:serp:en:us:running_shoes"
Type: String (JSON)
TTL: 21600 seconds (6 hours)
Value: {
    "keyword": "running shoes",
    "results": [...],
    "features": [...]
}

# User session
Key: "session:{user_id}:{session_token}"
Type: String (JSON)
TTL: 1800 seconds (30 minutes, sliding)
Value: {
    "user_id": 123,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": [...]
}
```

#### **3.4.2 Rate Limiting**

```redis
# User rate limit (token bucket)
Key: "ratelimit:user:{user_id}:keyword_search"
Type: String (integer)
TTL: 60 seconds
Value: 95  # requests remaining this minute
Algorithm: Token bucket with sliding window

# API provider rate limit
Key: "ratelimit:api:google_ads:daily"
Type: String (integer)
TTL: Until midnight UTC
Value: 14523  # requests used today

# IP-based rate limit (for crawlers)
Key: "ratelimit:ip:{proxy_ip}"
Type: Sorted Set
TTL: 3600 seconds
Members: {timestamp: request_id}
Algorithm: Sliding window log
```

#### **3.4.3 Real-time Ranking Data**

```redis
# Current rankings (hot data)
Key: "ranking:live:{tracked_keyword_id}"
Type: Hash
TTL: 3600 seconds
Fields:
    position: 5
    url: "https://example.com/page"
    last_check: 1705320000
    previous_position: 7

# Ranking change notifications
Key: "ranking:changes:{user_id}"
Type: List
TTL: 604800 seconds (7 days)
Values: [
    {"keyword": "...", "old": 7, "new": 5, "date": "..."},
    ...
]
```

#### **3.4.4 Queue Management**

```redis
# Priority queue for crawl jobs
Key: "queue:crawl:priority:{1-5}"
Type: List (FIFO)
Values: [job_id1, job_id2, ...]

# Job status tracking
Key: "job:{job_id}:status"
Type: Hash
Fields:
    status: "in_progress"
    worker_id: "worker-1"
    started_at: 1705320000
    progress: 45  # percentage

# Worker heartbeat
Key: "worker:{worker_id}:heartbeat"
Type: String
TTL: 60 seconds
Value: timestamp
```

### 3.5 Elasticsearch Indices

Elasticsearch provides **full-text search** and **fast analytics**.

#### **3.5.1 Keywords Index**

```json
// Index: keywords
{
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "snowball"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "keyword_id": {"type": "long"},
            "keyword_text": {
                "type": "text",
                "analyzer": "keyword_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "country": {"type": "keyword"},
            "language": {"type": "keyword"},
            "search_volume": {"type": "long"},
            "cpc_avg": {"type": "float"},
            "difficulty_score": {"type": "integer"},
            "opportunity_score": {"type": "integer"},
            "trend_direction": {"type": "keyword"},
            "related_keywords": {
                "type": "text",
                "analyzer": "keyword_analyzer"
            },
            "last_updated": {"type": "date"}
        }
    }
}
```

#### **3.5.2 Domains Index**

```json
// Index: domains
{
    "mappings": {
        "properties": {
            "domain_id": {"type": "long"},
            "domain_name": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "domain_authority": {"type": "integer"},
            "total_backlinks": {"type": "long"},
            "organic_keywords": {"type": "long"},
            "organic_traffic": {"type": "long"},
            "tld": {"type": "keyword"},
            "category": {"type": "keyword"},
            "last_crawled": {"type": "date"}
        }
    }
}
```

#### **3.5.3 Search Suggestions Index**

```json
// Index: search_suggestions
{
    "mappings": {
        "properties": {
            "suggestion": {
                "type": "completion",
                "analyzer": "simple",
                "search_analyzer": "simple"
            },
            "type": {"type": "keyword"}, // keyword, domain
            "popularity": {"type": "integer"},
            "country": {"type": "keyword"}
        }
    }
}
```

### 3.6 Sharding & Partitioning Plan

#### **3.6.1 PostgreSQL Sharding (using Citus)**

```sql
-- Distribute keywords table across shards
SELECT create_distributed_table('keywords', 'keyword_hash');
SELECT create_distributed_table('keyword_metrics', 'keyword_id');

-- Co-locate related tables for join performance
SELECT create_distributed_table('related_keywords', 'source_keyword_id', 
    colocate_with => 'keywords');

-- Distribute backlinks by target domain
SELECT create_distributed_table('backlinks', 'target_domain_id');

-- Reference tables (replicated to all shards)
SELECT create_reference_table('users');
SELECT create_reference_table('projects');
```

#### **3.6.2 MongoDB Sharding**

```javascript
// Enable sharding on database
sh.enableSharding("seo_platform");

// Shard serp_snapshots by compound key
sh.shardCollection("seo_platform.serp_snapshots", {
    country: 1,
    language: 1,
    search_date: 1
});

// Shard backlink_raw_data by target domain
sh.shardCollection("seo_platform.backlink_raw_data", {
    target_domain: "hashed"
});

// Shard crawl_queue by job_id
sh.shardCollection("seo_platform.crawl_queue", {
    job_id: "hashed"
});
```

#### **3.6.3 Data Retention & Archival**

```
Hot Data (PostgreSQL):
  - Last 90 days: Full metrics in main tables
  - Query performance: <100ms

Warm Data (PostgreSQL + compression):
  - 90 days - 1 year: Aggregated daily metrics
  - Query performance: <500ms

Cold Data (MongoDB):
  - 1+ years: Monthly aggregates only
  - Raw data archived to S3
  - Query performance: <2s

Archival Policy:
  - Ranking history: Keep daily for 90 days, weekly for 1 year, monthly forever
  - SERP snapshots: Keep full HTML for 30 days, metadata only after
  - Backlinks: Keep active backlinks in PostgreSQL, historical in MongoDB
  - API logs: Keep 30 days in PostgreSQL, archive to S3 after
```

---

## 4. API Layer Design

### 4.1 API Architecture

**Protocol:** REST API with optional GraphQL endpoint  
**Format:** JSON  
**Authentication:** JWT tokens + API keys  
**Versioning:** URL-based (`/api/v1/`, `/api/v2/`)

### 4.2 API Endpoints

#### **4.2.1 Keyword Research API**

```
POST /api/v1/keywords/search
Description: Search for keyword data
Authentication: Required (JWT or API key)
Rate Limit: 100/min (Pro), 500/min (Agency)

Request:
{
    "keyword": "running shoes",
    "country": "US",  // ISO 3166-1 alpha-2
    "language": "en",
    "device": "desktop",  // desktop, mobile, tablet
    "include_related": true,
    "include_questions": true,
    "include_trends": true
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "normalized": "running shoes",
        "metrics": {
            "search_volume": 110000,
            "search_volume_trend": "up",  // up, down, stable
            "cpc": {
                "min": 0.85,
                "max": 2.50,
                "avg": 1.25,
                "currency": "USD"
            },
            "competition": {
                "score": 0.78,
                "level": "high"  // low, medium, high
            },
            "difficulty_score": 65,  // 0-100
            "opportunity_score": 42  // 0-100 (custom metric)
        },
        "trends": {
            "last_12_months": [
                {"month": "2024-02", "value": 95},
                {"month": "2024-03", "value": 100},
                ...
            ],
            "year_over_year": 8.5  // % change
        },
        "related_keywords": [
            {
                "keyword": "best running shoes",
                "volume": 90500,
                "relevance": 0.95,
                "type": "similar"
            },
            ...
        ],
        "questions": [
            {
                "question": "what are the best running shoes for beginners",
                "type": "what",
                "frequency": 85
            },
            ...
        ],
        "serp_features": [
            "featured_snippet",
            "people_also_ask",
            "local_pack"
        ],
        "last_updated": "2025-01-15T10:30:00Z"
    },
    "metadata": {
        "cached": true,
        "cache_age_seconds": 3600,
        "sources": ["google_ads", "google_trends"],
        "credits_used": 1
    }
}

Error Responses:
400 Bad Request:
{
    "status": "error",
    "error": {
        "code": "INVALID_COUNTRY",
        "message": "Country code must be ISO 3166-1 alpha-2",
        "field": "country"
    }
}

429 Too Many Requests:
{
    "status": "error",
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Try again in 45 seconds",
        "retry_after": 45
    }
}

402 Payment Required:
{
    "status": "error",
    "error": {
        "code": "QUOTA_EXCEEDED",
        "message": "Monthly quota exceeded. Upgrade plan to continue",
        "quota_limit": 1000,
        "quota_used": 1000,
        "reset_date": "2025-02-01T00:00:00Z"
    }
}
```

```
GET /api/v1/keywords/{keyword_id}/suggestions
Description: Get related keywords and suggestions
Authentication: Required

Query Parameters:
- type: related|questions|broader|narrower (default: all)
- limit: 1-100 (default: 50)
- min_volume: minimum search volume filter
- max_difficulty: maximum difficulty score filter

Response (200 OK):
{
    "status": "success",
    "data": {
        "suggestions": [
            {
                "keyword": "best running shoes for flat feet",
                "search_volume": 22000,
                "difficulty_score": 58,
                "relevance_score": 0.88,
                "type": "narrower"
            },
            ...
        ],
        "total": 247,
        "returned": 50
    }
}
```

```
POST /api/v1/keywords/bulk
Description: Bulk keyword lookup (up to 100 keywords)
Authentication: Required
Rate Limit: 10/min (Pro), 50/min (Agency)

Request:
{
    "keywords": ["running shoes", "hiking boots", ...],
    "country": "US",
    "language": "en",
    "metrics": ["volume", "cpc", "difficulty"]  // optional filter
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "results": [
            {
                "keyword": "running shoes",
                "status": "success",
                "metrics": {...}
            },
            {
                "keyword": "xyz123invalid",
                "status": "not_found",
                "error": "No data available"
            }
        ],
        "summary": {
            "total": 100,
            "successful": 98,
            "failed": 2
        }
    },
    "metadata": {
        "credits_used": 10,
        "processing_time_ms": 1250
    }
}
```

#### **4.2.2 Domain Analysis API**

```
GET /api/v1/domains/{domain}/overview
Description: Get comprehensive domain metrics
Authentication: Required
Rate Limit: 50/min (Pro), 200/min (Agency)

Path Parameters:
- domain: example.com or www.example.com

Query Parameters:
- include_backlinks: true|false (default: false)
- include_top_pages: true|false (default: false)
- include_keywords: true|false (default: false)

Response (200 OK):
{
    "status": "success",
    "data": {
        "domain": "example.com",
        "metrics": {
            "domain_authority": 75,
            "page_authority_avg": 48.5,
            "spam_score": 2,
            "backlinks": {
                "total": 125847,
                "unique_domains": 8542,
                "dofollow": 98234,
                "nofollow": 27613,
                "referring_ips": 7234,
                "new_last_month": 1234,
                "lost_last_month": 456
            },
            "organic": {
                "keywords_count": 45231,
                "traffic_estimate": 850000,
                "traffic_value": 425000.00,
                "traffic_trend": "up",
                "top_keywords_count": 150,
                "keywords_top_3": 1234,
                "keywords_top_10": 4567,
                "keywords_top_100": 18923
            },
            "paid": {
                "keywords_count": 234,
                "traffic_estimate": 12000,
                "traffic_cost": 15000.00
            },
            "content": {
                "pages_indexed": 1547,
                "pages_crawled": 1892,
                "avg_page_speed": 2.3,
                "mobile_friendly_score": 95
            }
        },
        "competitors": [
            {
                "domain": "competitor1.com",
                "authority": 72,
                "keyword_overlap": 1234,
                "similarity_score": 0.78
            },
            ...
        ],
        "last_updated": "2025-01-15T08:00:00Z"
    }
}
```

```
GET /api/v1/domains/{domain}/backlinks
Description: Get backlink data for domain
Authentication: Required

Query Parameters:
- page: 1-1000 (default: 1)
- limit: 10-100 (default: 50)
- type: all|dofollow|nofollow (default: all)
- sort: authority|date_found|anchor_text (default: authority)
- order: desc|asc (default: desc)
- min_authority: 0-100 (filter)
- only_active: true|false (default: true)

Response (200 OK):
{
    "status": "success",
    "data": {
        "backlinks": [
            {
                "source_url": "https://source.com/article",
                "source_domain": "source.com",
                "source_authority": 68,
                "target_url": "https://example.com/page",
                "anchor_text": "click here",
                "link_type": "dofollow",
                "first_seen": "2024-06-15T00:00:00Z",
                "last_seen": "2025-01-15T00:00:00Z",
                "http_status": 200,
                "is_active": true
            },
            ...
        ],
        "pagination": {
            "page": 1,
            "limit": 50,
            "total": 125847,
            "pages": 2517
        }
    }
}
```

```
GET /api/v1/domains/{domain}/top-pages
Description: Get top-performing pages
Authentication: Required

Query Parameters:
- page: 1-100 (default: 1)
- limit: 10-100 (default: 20)
- sort: traffic|keywords|backlinks (default: traffic)
- metric: organic|paid|all (default: organic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "pages": [
            {
                "url": "https://example.com/best-products",
                "title": "Best Products 2025",
                "page_authority": 52,
                "organic_traffic": 85000,
                "organic_keywords": 1234,
                "backlinks": 456,
                "social_shares": 1200,
                "traffic_value": 42500.00,
                "top_keywords": [
                    {
                        "keyword": "best products",
                        "position": 2,
                        "volume": 22000,
                        "traffic_estimate": 8800
                    },
                    ...
                ]
            },
            ...
        ],
        "pagination": {...}
    }
}
```

```
GET /api/v1/domains/{domain}/organic-keywords
Description: Get ranking keywords for domain
Authentication: Required

Query Parameters:
- page: 1-1000
- limit: 10-100
- position: 1-100 (filter)
- min_volume: minimum search volume
- sort: position|volume|traffic (default: traffic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "keywords": [
            {
                "keyword": "running shoes",
                "position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "search_volume": 110000,
                "traffic_estimate": 8800,
                "traffic_value": 11000.00,
                "serp_features": ["featured_snippet"]
            },
            ...
        ],
        "summary": {
            "total_keywords": 45231,
            "top_3": 1234,
            "top_10": 4567,
            "top_100": 18923
        },
        "pagination": {...}
    }
}
```

#### **4.2.3 SERP Analysis API**

```
POST /api/v1/serp/analyze
Description: Get SERP analysis for keyword
Authentication: Required
Rate Limit: 50/min

Request:
{
    "keyword": "running shoes",
    "country": "US",
    "language": "en",
    "device": "desktop",
    "location": "New York, NY",  // optional for local searches
    "num_results": 100  // 10-100, default: 10
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "total_results": 234000000,
        "serp_features": [
            {
                "type": "featured_snippet",
                "position": 0,
                "domain": "example.com",
                "url": "https://example.com/guide",
                "content_preview": "Running shoes are..."
            },
            {
                "type": "people_also_ask",
                "questions": [
                    "What are the best running shoes?",
                    "How to choose running shoes?",
                    ...
                ]
            },
            {
                "type": "local_pack",
                "businesses": [...]
            }
        ],
        "organic_results": [
            {
                "position": 1,
                "title": "Best Running Shoes 2025",
                "url": "https://example.com/running-shoes",
                "domain": "example.com",
                "domain_authority": 75,
                "description": "Discover the best...",
                "rich_snippet": {
                    "type": "product",
                    "rating": 4.5,
                    "reviews": 1200,
                    "price": "$129.99"
                },
                "backlinks": 1234,
                "referring_domains": 456,
                "estimated_traffic": 35000
            },
            ...
        ],
        "paid_results": [
            {
                "position": "top1",
                "title": "Running Shoes Sale",
                "url": "https://shop.com/running",
                "domain": "shop.com",
                "description": "50% off all running shoes"
            },
            ...
        ],
        "analysis": {
            "difficulty_score": 68,
            "opportunity_score": 45,
            "avg_domain_authority": 72.5,
            "avg_backlinks": 8542,
            "content_length_avg": 2850,
            "content_recommendations": [
                "Include product comparisons",
                "Add video content",
                "Target featured snippet opportunity"
            ]
        },
        "last_updated": "2025-01-15T10:30:00Z"
    }
}
```

```
GET /api/v1/serp/features
Description: Get SERP features statistics
Authentication: Required

Query Parameters:
- keyword: specific keyword or keyword_id
- country: US, UK, etc.
- date_range: last_7_days|last_30_days|last_90_days

Response (200 OK):
{
    "status": "success",
    "data": {
        "features_present": [
            {
                "feature": "featured_snippet",
                "frequency": 85,  // % of time present
                "domains_winning": [
                    {"domain": "example.com", "count": 45},
                    ...
                ]
            },
            {
                "feature": "people_also_ask",
                "frequency": 92
            },
            {
                "feature": "local_pack",
                "frequency": 12
            }
        ],
        "feature_history": [
            {
                "date": "2025-01-15",
                "features": ["featured_snippet", "people_also_ask", "images"]
            },
            ...
        ]
    }
}
```

#### **4.2.4 Rank Tracking API**

```
POST /api/v1/tracking/projects
Description: Create new tracking project
Authentication: Required

Request:
{
    "project_id": 123,  // existing project
    "name": "My Website Tracking",
    "target_domain": "example.com",
    "check_frequency": "daily",  // daily, weekly, monthly
    "keywords": [
        {
            "keyword": "running shoes",
            "target_url": "https://example.com/running-shoes",
            "tags": ["product", "priority-high"]
        },
        ...
    ]
}

Response (201 Created):
{
    "status": "success",
    "data": {
        "tracking_project_id": 456,
        "keywords_added": 50,
        "next_check_at": "2025-01-16T00:00:00Z",
        "estimated_credits_per_check": 50
    }
}
```

```
GET /api/v1/tracking/projects/{project_id}/rankings
Description: Get ranking data for tracked keywords
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD (default: 30 days ago)
- date_to: YYYY-MM-DD (default: today)
- tags: filter by tags (comma-separated)
- position_change: improved|declined|unchanged|new|lost
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "rankings": [
            {
                "keyword": "running shoes",
                "current_position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "best_position": 3,
                "worst_position": 15,
                "average_position": 6.8,
                "history": [
                    {"date": "2025-01-15", "position": 5},
                    {"date": "2025-01-14", "position": 6},
                    ...
                ],
                "serp_features": ["featured_snippet"],
                "visibility_score": 85  // 0-100
            },
            ...
        ],
        "summary": {
            "total_keywords": 50,
            "improved": 12,
            "declined": 8,
            "unchanged": 28,
            "new": 2,
            "lost": 0,
            "avg_position": 15.4,
            "visibility_score": 72
        }
    }
}
```

```
GET /api/v1/tracking/rankings/{keyword_id}/history
Description: Get detailed ranking history
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- granularity: daily|weekly|monthly

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "domain": "example.com",
        "history": [
            {
                "date": "2025-01-15",
                "position": 5,
                "ranking_url": "https://example.com/running-shoes",
                "serp_features": ["featured_snippet"],
                "competitors_above": [
                    {"domain": "competitor.com", "position": 1},
                    ...
                ]
            },
            ...
        ],
        "statistics": {
            "best_position": 3,
            "worst_position": 15,
            "average_position": 6.8,
            "position_changes": 23,
            "days_tracked": 90,
            "trend": "improving"  // improving, declining, stable
        }
    }
}
```

#### **4.2.5 Trends & Analytics API**

```
GET /api/v1/trends/keywords
Description: Get trending keywords
Authentication: Required

Query Parameters:
- country: US, UK, etc.
- category: all|shopping|sports|technology|...
- timeframe: today|week|month
- min_volume: minimum search volume
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "trending_keywords": [
            {
                "keyword": "ai chatbot",
                "search_volume": 246000,
                "volume_change_percent": 350,
                "trend_score": 95,
                "related_topics": ["artificial intelligence", "chatgpt"],
                "category": "technology"
            },
            ...
        ],
        "generated_at": "2025-01-15T10:00:00Z"
    }
}
```

```
POST /api/v1/analysis/content-gap
Description: Compare content gaps between domains
Authentication: Required
Rate Limit: 20/min

Request:
{
    "source_domain": "example.com",
    "competitor_domains": ["competitor1.com", "competitor2.com"],
    "country": "US",
    "min_volume": 1000,
    "max_difficulty": 70,
    "limit": 100
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "opportunities": [
            {
                "keyword": "best running shoes for beginners",
                "search_volume": 22000,
                "difficulty_score": 58,
                "gap_score": 85,  // 0-100 (higher = better opportunity)
                "source_position": null,  // not ranking
                "competitors": [
                    {
                        "domain": "competitor1.com",
                        "position": 3,
                        "url": "...",
                        "page_authority": 45
                    },
                    {
                        "domain": "competitor2.com",
                        "position": 7,
                        "url": "...",
                        "page_authority": 38
                    }
                ],
                "opportunity_reasons": [
                    "Competitors ranking with lower authority",
                    "High search volume with medium difficulty",
                    "Related to existing content on your site"
                ]
            },
            ...
        ],
        "summary": {
            "total_opportunities": 247,
            "high_priority": 45,
            "medium_priority": 128,
            "low_priority": 74,
            "estimated_traffic_potential": 125000
        }
    }
}
```

### 4.3 Pagination Strategy

All list endpoints use **cursor-based pagination** for performance:

```
GET /api/v1/keywords/search?page=1&limit=50

Response:
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 50,
        "total": 1247,
        "pages": 25,
        "has_next": true,
        "has_prev": false,
        "next_page": 2,
        "prev_page": null
    },
    "links": {
        "first": "/api/v1/keywords/search?page=1&limit=50",
        "last": "/api/v1/keywords/search?page=25&limit=50",
        "next": "/api/v1/keywords/search?page=2&limit=50",
        "prev": null
    }
}
```

For very large datasets (backlinks, SERP history), use **cursor pagination**:

```
GET /api/v1/domains/{domain}/backlinks?cursor=abc123&limit=100

Response:
{
    "data": [...],
    "pagination": {
        "cursor": "def456",
        "has_more": true,
        "limit": 100
    },
    "links": {
        "next": "/api/v1/domains/{domain}/backlinks?cursor=def456&limit=100"
    }
}
```

### 4.4 Filtering & Sorting

**Standard filters across endpoints:**
- `min_volume`: Minimum search volume
- `max_volume`: Maximum search volume
- `min_difficulty`: Minimum difficulty score
- `max_difficulty`: Maximum difficulty score
- `country`: Country code(s) - comma-separated
- `language`: Language code(s)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Standard sorting:**
- `sort`: Field to sort by
- `order`: asc|desc

Example:
```
GET /api/v1/keywords/search?
    keyword=shoes&
    min_volume=10000&
    max_difficulty=60&
    country=US,CA&
    sort=volume&
    order=desc&
    page=1&
    limit=50
```

### 4.5 Caching Strategy

```
Cache-Control Headers:
- Keyword data: max-age=86400 (24 hours)
- Domain overview: max-age=43200 (12 hours)
- SERP data: max-age=21600 (6 hours)
- Ranking data: max-age=3600 (1 hour)
- Trending data: max-age=600 (10 minutes)

ETag Support:
- Include ETag header in responses
- Support If-None-Match requests
- Return 304 Not Modified when appropriate

Example Response Headers:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=86400, public
ETag: "abc123def456"
X-Cache: HIT
X-Cache-Age: 3600
```

---

## 5. Crawler & Data Sources

### 5.1 Data Source Integration

#### **5.1.1 Google APIs**

**Google Ads Keyword Planner API**
```python
Purpose: Search volume, CPC, competition data
Rate Limit: 15,000 requests/day
Cost: Free with Google Ads account
Data Freshness: Updated monthly

Integration:
- OAuth 2.0 authentication
- REST API calls
- Batch requests (up to 100 keywords)
- Response caching (30 days)

Data Retrieved:
- Monthly search volume
- Competition level (low/medium/high)
- Suggested bid (CPC)
- Historical data (12 months)
- Related keywords
```

**Google Search Console API**
```python
Purpose: Verified site ranking data, clicks, impressions
Rate Limit: 1,200 requests/day
Cost: Free
Data Freshness: 2-3 days delay

Integration:
- OAuth 2.0 with Search Console verification
- Query for ranking data, impressions, clicks
- Filter by country, device, search appearance

Data Retrieved:
- Keyword rankings for verified sites
- Click-through rates
- Impressions
- Average position
```

**Google Trends API (Unofficial)**
```python
Purpose: 12-month trend data, related queries
Rate Limit: 1,500 requests/hour
Cost: Free (via pytrends library)
Data Freshness: Real-time

Integration:
- Python pytrends library
- Rotating proxies to avoid blocks
- Delayed requests (2-5 seconds)

Data Retrieved:
- Interest over time (0-100 scale)
- Related topics and queries
- Regional interest
- Rising keywords
```

#### **5.1.2 Bing Webmaster Tools API**

```python
Purpose: Alternative search data, Bing-specific metrics
Rate Limit: 5,000 requests/month
Cost: Free
Data Freshness: Daily updates

Integration:
- API key authentication
- REST API

Data Retrieved:
- Keyword rankings
- Traffic data
- Backlink data (limited)
- Page-level metrics
```

#### **5.1.3 Third-Party SEO APIs**

**DataForSEO API**
```python
Purpose: Comprehensive SERP data, backlinks, metrics
Rate Limit: Based on subscription
Cost: Pay-per-request ($0.001 - $0.02 per request)
Data Freshness: Real-time for SERP, daily for backlinks

Data Retrieved:
- SERP results with rich data
- Backlink profiles
- Keyword difficulty scores
- Domain metrics
- Historical data
```

**SEMrush API** (Alternative)
```python
Purpose: Keyword data, competition analysis
Cost: $199-$499/month + API credits
Data Retrieved:
- Keyword metrics
- Domain analytics
- Competitor analysis
- Backlink data
```

### 5.2 Headless Browser Crawling

For SERP scraping when APIs are insufficient:

```python
Technology Stack:
- Selenium with Chrome/Firefox headless
- Playwright (modern alternative, faster)
- Puppeteer (Node.js option)

Proxy Integration:
- Bright Data (Luminati) residential proxies
- Oxylabs datacenter & residential proxies
- ScraperAPI (handles proxies + CAPTCHA)

CAPTCHA Handling:
- 2Captcha API integration
- Anti-Captcha service
- Automatic retry with new proxy
- Fallback to human verification queue

User Agent Rotation:
- Random desktop user agents
- Mobile user agents for mobile SERP
- Update monthly from real browser stats
```

#### **5.2.1 SERP Crawler Implementation**

```python
# Pseudo-code for SERP crawler

class SERPCrawler:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        
    async def crawl_serp(self, keyword, country, device):
        # Select appropriate proxy
        proxy = self.proxy_manager.get_proxy(country)
        
        # Configure browser
        browser = await self.launch_browser(
            proxy=proxy,
            user_agent=self.get_user_agent(device),
            headless=True
        )
        
        try:
            # Navigate to Google search
            page = await browser.new_page()
            search_url = self.build_search_url(keyword, country)
            await page.goto(search_url, wait_until='networkidle')
            
            # Check for CAPTCHA
            if await self.detect_captcha(page):
                solved = await self.captcha_solver.solve(page)
                if not solved:
                    raise CaptchaError("Failed to solve CAPTCHA")
            
            # Extract SERP data
            serp_data = await self.extract_serp_data(page)
            
            # Take screenshot for archive
            screenshot = await page.screenshot(full_page=True)
            
            return {
                'results': serp_data,
                'screenshot': screenshot,
                'timestamp': datetime.utcnow(),
                'proxy_used': proxy.id
            }
            
        except Exception as e:
            # Mark proxy as failed
            self.proxy_manager.mark_failed(proxy)
            raise
            
        finally:
            await browser.close()
    
    async def extract_serp_data(self, page):
        # Extract organic results
        organic = await page.eval("""
            () => Array.from(document.querySelectorAll('.g')).map(el => ({
                position: Array.from(el.parentNode.children).indexOf(el) + 1,
                title: el.querySelector('h3')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.VwiC3b')?.textContent,
                rich_snippet: extractRichSnippet(el)
            }))
        """)
        
        # Extract SERP features
        featured_snippet = await page.querySelector('.ifM9O')
        people_also_ask = await page.querySelectorAll('.related-question-pair')
        local_pack = await page.querySelector('.rllt__details')
        
        # Extract paid ads
        ads = await page.eval("""
            () => Array.from(document.querySelectorAll('.uEierd')).map(el => ({
                position: 'top' + (Array.from(el.parentNode.children).indexOf(el) + 1),
                title: el.querySelector('.CCgQ5')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.MUxGbd')?.textContent
            }))
        """)
        
        return {
            'organic': organic,
            'ads': ads,
            'features': {
                'featured_snippet': featured_snippet,
                'people_also_ask': people_also_ask,
                'local_pack': local_pack
            }
        }
```

### 5.3 Crawler Scheduler

```python
# Celery beat schedule for periodic crawls

CELERYBEAT_SCHEDULE = {
    'crawl-high-priority-keywords': {
        'task': 'crawlers.tasks.crawl_keywords',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ({'priority': 'high'},)
    },
    'crawl-tracked-keywords-daily': {
        'task': 'crawlers.tasks.crawl_tracked_keywords',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'args': ({'frequency': 'daily'},)
    },
    'refresh-domain-backlinks': {
        'task': 'crawlers.tasks.refresh_backlinks',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'args': ()
    },
    'update-keyword-trends': {
        'task': 'crawlers.tasks.update_trends',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),  # Monthly
        'args': ()
    }
}
```

### 5.4 Proxy Management System

```python
class ProxyManager:
    def __init__(self):
        self.redis = Redis()
        self.proxy_pool = []
        
    def load_proxies(self):
        # Load from providers: Bright Data, Oxylabs, etc.
        proxies = [
            {'ip': '1.2.3.4:8080', 'country': 'US', 'type': 'residential'},
            {'ip': '5.6.7.8:8080', 'country': 'UK', 'type': 'datacenter'},
            ...
        ]
        self.proxy_pool = proxies
    
    def get_proxy(self, country='US', exclude_failed=True):
        # Get least recently used proxy for country
        candidates = [p for p in self.proxy_pool if p['country'] == country]
        
        if exclude_failed:
            # Filter out proxies that failed recently
            candidates = [p for p in candidates 
                         if not self.is_in_cooldown(p['ip'])]
        
        # Sort by last used time
        candidates.sort(key=lambda p: self.get_last_used(p['ip']))
        
        if not candidates:
            raise NoProxyAvailable(f"No proxies available for {country}")
        
        selected = candidates[0]
        self.mark_used(selected['ip'])
        return selected
    
    def mark_used(self, proxy_ip):
        self.redis.set(f'proxy:last_used:{proxy_ip}', time.time())
        self.redis.incr(f'proxy:usage_count:{proxy_ip}')
    
    def mark_failed(self, proxy, reason='unknown'):
        # Put proxy in cooldown for 5 minutes
        self.redis.setex(
            f'proxy:cooldown:{proxy["ip"]}',
            300,  # 5 minutes
            reason
        )
        self.redis.incr(f'proxy:failure_count:{proxy["ip"]}')
        
        # If too many failures, remove from pool
        failures = int(self.redis.get(f'proxy:failure_count:{proxy["ip"]}') or 0)
        if failures > 10:
            self.remove_proxy(proxy['ip'])
    
    def is_in_cooldown(self, proxy_ip):
        return self.redis.exists(f'proxy:cooldown:{proxy_ip}')
    
    def get_last_used(self, proxy_ip):
        return float(self.redis.get(f'proxy:last_used:{proxy_ip}') or 0)
    
    def health_check(self, proxy):
        # Test proxy connectivity
        try:
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies={'https': f'http://{proxy["ip"]}'},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    async def periodic_health_check(self):
        # Run every 5 minutes to check all proxies
        for proxy in self.proxy_pool:
            if not self.health_check(proxy):
                self.mark_failed(proxy, 'health_check_failed')
```

### 5.5 CAPTCHA Handling Strategy

```python
class CaptchaSolver:
    def __init__(self):
        self.twocaptcha_api_key = settings.TWOCAPTCHA_API_KEY
        
    async def solve(self, page, captcha_type='recaptcha_v2'):
        if captcha_type == 'recaptcha_v2':
            return await self.solve_recaptcha_v2(page)
        elif captcha_type == 'recaptcha_v3':
            return await self.solve_recaptcha_v3(page)
        elif captcha_type == 'image':
            return await self.solve_image_captcha(page)
    
    async def solve_recaptcha_v2(self, page):
        # Extract site key
        site_key = await page.evaluate("""
            () => document.querySelector('[data-sitekey]')?.getAttribute('data-sitekey')
        """)
        
        if not site_key:
            return False
        
        # Send to 2Captcha service
        task_id = self.create_captcha_task(
            site_key=site_key,
            page_url=page.url
        )
        
        # Wait for solution (can take 30-60 seconds)
        solution = self.wait_for_solution(task_id, timeout=120)
        
        if solution:
            # Inject solution into page
            await page.evaluate(f"""
                {% raw %}
                {% raw %}document.getElementById('g-recaptcha-response').innerHTML = '{solution}';{% endraw %}
                    document.getElementById('g-recaptcha-response').innerHTML = '{solution}';
                    document.querySelector('form').submit();
                }}{% endraw %}
                "
            """)
            return True
        
        return False
    
    def create_captcha_task(self, site_key, page_url):
        response = requests.post(
            'https://2captcha.com/in.php',
            data={
                'key': self.twocaptcha_api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
        )
        return response.json()['request']
    
    def wait_for_solution(self, task_id, timeout=120):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(
                'https://2captcha.com/res.php',
                params={
                    'key': self.twocaptcha_api_key,
                    'action': 'get',
                    'id': task_id,
                    'json': 1
                }
            )
            result = response.json()
            
            if result['status'] == 1:
                return result['request']
            
            time.sleep(5)
        
        return None
```

---

## 6. Ranking & Analytics Engine

### 6.1 Keyword Difficulty Algorithm

```python
def calculate_keyword_difficulty(keyword_data, serp_data):
    """
    Calculate keyword difficulty score (0-100)
    Higher = more difficult to rank
    
    Factors:
    1. Competition level from Google Ads (weight: 20%)
    2. Domain authority of top 10 results (weight: 40%)
    3. Backlink profile of top 10 (weight: 30%)
    4. SERP features present (weight: 10%)
    """
    
    # Factor 1: Competition level
    competition_score = keyword_data['competition'] * 100  # 0-100
    
    # Factor 2: Domain authority
    top_10_domains = serp_data['organic_results'][:10]
    avg_domain_authority = sum(d['domain_authority'] for d in top_10_domains) / 10
    
    # Factor 3: Backlinks
    avg_backlinks = sum(d['backlinks_count'] for d in top_10_domains) / 10
    backlink_score = min(100, (avg_backlinks / 1000) * 100)  # Normalize
    
    # Factor 4: SERP features
    serp_features_count = len(serp_data['serp_features'])
    serp_feature_score = min(100, serp_features_count * 15)
    
    # Weighted calculation
    difficulty = (
        competition_score * 0.20 +
        avg_domain_authority * 0.40 +
        backlink_score * 0.30 +
        serp_feature_score * 0.10
    )
    
    return round(difficulty, 2)
```

### 6.2 Opportunity Score Algorithm

```python
def calculate_opportunity_score(keyword_data, serp_data, user_domain_data):
    """
    Calculate opportunity score (0-100)
    Higher = better opportunity for ranking
    
    Factors:
    1. Search volume (high volume = more opportunity)
    2. Low difficulty (easier to rank)
    3. Low competition from strong domains
    4. User's domain strength relative to competitors
    5. Traffic value (CPC * volume)
    6. Trend direction (rising = more opportunity)
    """
    
    # Factor 1: Search volume score
    volume = keyword_data['search_volume']
    volume_score = min(100, (volume / 100000) * 100)  # Normalize to 100k
    
    # Factor 2: Difficulty score (inverse)
    difficulty = keyword_data['difficulty_score']
    difficulty_score = 100 - difficulty
    
    # Factor 3: Competition gap
    user_authority = user_domain_data['domain_authority']
    avg_competitor_authority = sum(
        d['domain_authority'] for d in serp_data['organic_results'][:10]
    ) / 10
    
    authority_gap = avg_competitor_authority - user_authority
    competition_score = max(0, 100 - authority_gap)
    
    # Factor 4: Traffic value
    traffic_value = keyword_data['cpc_avg'] * volume
    value_score = min(100, (traffic_value / 10000) * 100)
    
    # Factor 5: Trend score
    trend = keyword_data.get('trend_direction', 'stable')
    trend_score = {
        'rising': 100,
        'stable': 50,
        'declining': 20
    }.get(trend, 50)
    
    # Weighted calculation
    opportunity = (
        volume_score * 0.25 +
        difficulty_score * 0.30 +
        competition_score * 0.25 +
        value_score * 0.10 +
        trend_score * 0.10
    )
    
    return round(opportunity, 2)
```

### 6.3 Domain Authority Algorithm

```python
def calculate_domain_authority(domain_data):
    """
    Calculate domain authority (0-100)
    Similar to Moz's DA or Ahrefs DR
    
    Factors:
    1. Total backlinks (log scale)
    2. Unique referring domains (log scale)
    3. Quality of referring domains
    4. Link velocity (new vs lost)
    5. Organic traffic estimate
    6. Number of ranking keywords
    """
    
    # Factor 1: Total backlinks (log scale for diminishing returns)
    backlinks = domain_data['total_backlinks']
    backlink_score = min(100, math.log10(backlinks + 1) * 20)
    
    # Factor 2: Unique referring domains
    referring_domains = domain_data['unique_referring_domains']
    referring_score = min(100, math.log10(referring_domains + 1) * 25)
    
    # Factor 3: Quality of backlinks (avg authority of referring domains)
    avg_referring_authority = domain_data['avg_referring_domain_authority']
    quality_score = avg_referring_authority
    
    # Factor 4: Link velocity
    new_links_month = domain_data['new_backlinks_last_month']
    lost_links_month = domain_data['lost_backlinks_last_month']
    velocity = (new_links_month - lost_links_month) / max(1, backlinks) * 100
    velocity_score = min(100, max(0, 50 + velocity * 10))
    
    # Factor 5: Organic traffic
    organic_traffic = domain_data['organic_traffic_estimate']
    traffic_score = min(100, math.log10(organic_traffic + 1) * 15)
    
    # Factor 6: Ranking keywords
    ranking_keywords = domain_data['organic_keywords_count']
    keyword_score = min(100, math.log10(ranking_keywords + 1) * 20)
    
    # Weighted calculation
    authority = (
        backlink_score * 0.25 +
        referring_score * 0.30 +
        quality_score * 0.20 +
        velocity_score * 0.05 +
        traffic_score * 0.10 +
        keyword_score * 0.10
    )
    
    return round(authority, 2)
```

### 6.4 Trend Analysis Engine

```python
class TrendAnalyzer:
    def analyze_keyword_trend(self, historical_data):
        """
        Analyze 12-month trend data
        Returns: trend_direction, trend_strength, seasonality
        """
        
        # Extract monthly values
        months = sorted(historical_data.keys())
        values = [historical_data[m] for m in months]
        
        # Calculate linear regression
        slope, intercept = self.linear_regression(range(len(values)), values)
        
        # Determine trend direction
        if slope > 5:
            direction = 'rising'
        elif slope < -5:
            direction = 'declining'
        else:
            direction = 'stable'
        
        # Calculate trend strength (0-100)
        strength = min(100, abs(slope) * 2)
        
        # Detect seasonality
        seasonality = self.detect_seasonality(values)
        
        # Calculate volatility
        volatility = np.std(values) / np.mean(values) * 100
        
        return {
            'direction': direction,
            'strength': strength,
            'seasonality': seasonality,
            'volatility': volatility,
            'forecast_next_month': intercept + slope * len(values)
        }
    
    def detect_seasonality(self, values):
        """
        Detect seasonal patterns (monthly, quarterly, annual)
        """
        if len(values) < 12:
            return None
        
        # Check for quarterly pattern
        q1_avg = np.mean(values[0:3] + values[3:6] + values[6:9] + values[9:12])
        # ... more complex seasonality detection
        
        return {
            'has_seasonality': True,
            'pattern': 'quarterly',
            'peak_months': [6, 7, 8]  # Summer peak
        }
    
    def linear_regression(self, x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
```

### 6.5 Content Gap Analysis Algorithm

```python
def analyze_content_gap(source_domain, competitor_domains, filters):
    """
    Find keyword opportunities where competitors rank but source doesn't
    """
    
    # Get all keywords competitors rank for
    competitor_keywords = set()
    for competitor in competitor_domains:
        keywords = fetch_competitor_keywords(competitor, filters)
        competitor_keywords.update(keywords)
    
    # Get keywords source domain ranks for
    source_keywords = set(fetch_domain_keywords(source_domain))
    
    # Find gaps (keywords only competitors have)
    gap_keywords = competitor_keywords - source_keywords
    
    # Score each gap keyword
    opportunities = []
    for keyword in gap_keywords:
        # Get keyword data
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        # Calculate scores
        difficulty = calculate_keyword_difficulty(keyword_data, serp_data)
        opportunity = calculate_opportunity_score(
            keyword_data, 
            serp_data,
            fetch_domain_data(source_domain)
        )
        
        # Calculate gap score
        # Higher when multiple competitors rank highly
        competitor_positions = [
            pos for comp in competitor_domains 
            for pos in get_keyword_position(comp, keyword)
            if pos
        ]
        
        if competitor_positions:
            avg_competitor_position = sum(competitor_positions) / len(competitor_positions)
            gap_score = (
                opportunity * 0.5 +
                (100 - difficulty) * 0.3 +
                (100 - avg_competitor_position * 10) * 0.2
            )
        else:
            gap_score = 0
        
        opportunities.append({
            'keyword': keyword,
            'difficulty': difficulty,
            'opportunity': opportunity,
            'gap_score': gap_score,
            'competitor_positions': competitor_positions,
            'volume': keyword_data['search_volume'],
            'cpc': keyword_data['cpc_avg']
        })
    
    # Sort by gap score
    opportunities.sort(key=lambda x: x['gap_score'], reverse=True)
    
    return opportunities
```

### 6.6 Machine Learning for Keyword Clustering

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class KeywordClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def cluster_keywords(self, keywords, n_clusters=10):
        """
        Group similar keywords into topic clusters
        """
        
        # Vectorize keywords using TF-IDF
        keyword_texts = [kw['keyword'] for kw in keywords]
        tfidf_matrix = self.vectorizer.fit_transform(keyword_texts)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Reduce dimensionality for visualization
        pca = PCA(n_components=2)
        coords = pca.fit_transform(tfidf_matrix.toarray())
        
        # Group keywords by cluster
        clusters = {}
        for i, keyword in enumerate(keywords):
            cluster_id = cluster_labels[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'keywords': [],
                    'total_volume': 0,
                    'avg_difficulty': 0,
                    'center': coords[i].tolist()
                }
            
            clusters[cluster_id]['keywords'].append(keyword)
            clusters[cluster_id]['total_volume'] += keyword['search_volume']
        
        # Calculate cluster statistics and labels
        for cluster_id, cluster_data in clusters.items():
            keywords_in_cluster = cluster_data['keywords']
            
            # Calculate average difficulty
            cluster_data['avg_difficulty'] = sum(
                kw['difficulty_score'] for kw in keywords_in_cluster
            ) / len(keywords_in_cluster)
            
            # Generate cluster label (most common terms)
            cluster_label = self.generate_cluster_label(
                [kw['keyword'] for kw in keywords_in_cluster]
            )
            cluster_data['label'] = cluster_label
        
        return clusters
    
    def generate_cluster_label(self, keywords):
        # Extract most common words
        word_freq = {}
        for keyword in keywords:
            for word in keyword.split():
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 2-3 words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        return ' '.join(word for word, _ in top_words)
```

### 6.7 Predictive Analytics

```python
class RankingPredictor:
    def predict_ranking_potential(self, target_url, keyword, current_ranking):
        """
        Predict likelihood of ranking improvement
        Uses historical data and ML model
        """
        
        # Extract features
        features = self.extract_features(target_url, keyword, current_ranking)
        
        # Load trained model (e.g., Random Forest or XGBoost)
        model = self.load_model()
        
        # Predict probability of improvement
        prediction = model.predict_proba([features])[0]
        
        # Estimate time to rank in top 10
        estimated_days = self.estimate_time_to_rank(features, prediction)
        
        return {
            'probability_top_10': prediction[1],
            'probability_top_3': prediction[2] if len(prediction) > 2 else 0,
            'estimated_days_to_top_10': estimated_days,
            'confidence': self.calculate_confidence(features),
            'recommended_actions': self.generate_recommendations(features)
        }
    
    def extract_features(self, target_url, keyword, current_ranking):
        page_data = fetch_page_data(target_url)
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        return {
            'current_position': current_ranking or 100,
            'page_authority': page_data['page_authority'],
            'domain_authority': page_data['domain_authority'],
            'backlinks_count': page_data['backlinks_count'],
            'content_length': page_data['content_length'],
            'keyword_density': page_data['keyword_density'],
            'keyword_difficulty': keyword_data['difficulty_score'],
            'search_volume': keyword_data['search_volume'],
            'avg_competitor_authority': serp_data['avg_domain_authority'],
            'serp_features_count': len(serp_data['serp_features']),
            'has_featured_snippet': 'featured_snippet' in serp_data['serp_features']
        }
    
    def generate_recommendations(self, features):
        recommendations = []
        
        if features['content_length'] < 1500:
            recommendations.append({
                'priority': 'high',
                'action': 'Increase content length',
                'details': f'Current: {features["content_length"]} words. Target: 2000+ words',
                'impact': 'medium'
            })
        
        if features['backlinks_count'] < 50:
            recommendations.append({
                'priority': 'high',
                'action': 'Build more backlinks',
                'details': f'Current: {features["backlinks_count"]}. Target: 100+ backlinks',
                'impact': 'high'
            })
        
        if features['keyword_density'] < 0.5:
            recommendations.append({
                'priority': 'medium',
                'action': 'Optimize keyword usage',
                'details': 'Include target keyword more naturally in content',
                'impact': 'low'
            })
        
        return recommendations
```

---

## 7. User System

### 7.1 Authentication & Authorization

```python
# JWT token structure
{
    "user_id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": ["keyword_search", "domain_analysis", "rank_tracking"],
    "iat": 1705320000,
    "exp": 1705406400  # 24 hour expiry
}

# API Key structure
{
    "key_id": "ak_live_abc123xyz789",
    "user_id": 12345,
    "name": "Production API Key",
    "permissions": ["keyword_search", "serp_analysis"],
    "rate_limit": 500,  # requests per minute
    "created_at": "2025-01-01T00:00:00Z",
    "last_used_at": "2025-01-15T10:30:00Z"
}
```

### 7.2 Subscription Plans

```yaml
Plans:
  Free:
    price: $0/month
    features:
      keyword_searches: 10/day
      domain_analyses: 3/day
      serp_checks: 10/day
      tracked_keywords: 0
      historical_data: 7 days
      api_access: false
      export: false
      team_members: 1
      
  Pro:
    price: $99/month
    features:
      keyword_searches: 100/day (3000/month)
      domain_analyses: 50/day
      serp_checks: 100/day
      tracked_keywords: 500
      rank_checks_frequency: daily
      historical_data: 90 days
      api_access: true
      api_calls: 10,000/month
      export: true (CSV, Excel)
      team_members: 3
      reports: 10/month
      
  Agency:
    price: $299/month
    features:
      keyword_searches: unlimited
      domain_analyses: unlimited
      serp_checks: unlimited
      tracked_keywords: 5000
      rank_checks_frequency: daily
      historical_data: 2 years
      api_access: true
      api_calls: 100,000/month
      export: true (CSV, Excel, API)
      team_members: 10
      reports: unlimited
      white_label: true
      priority_support: true
      
  Enterprise:
    price: Custom
    features:
      everything_unlimited: true
      dedicated_account_manager: true
      custom_integrations: true
      on_premise_option: true
      sla_guarantee: 99.9%
```

### 7.3 Quota Management

```python
class QuotaManager:
    def check_quota(self, user_id, action_type):
        """
        Check if user has quota remaining for action
        Returns: (allowed: bool, remaining: int, reset_at: datetime)
        """
        
        # Get user plan
        user = fetch_user(user_id)
        plan = PLANS[user.plan_type]
        
        # Get quota limits
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        quota_used = redis.get(quota_key) or 0
        quota_limit = plan['features'][f'{action_type}']
        
        # Check if unlimited
        if quota_limit == 'unlimited':
            return (True, -1, None)
        
        # Check limit
        allowed = int(quota_used) < int(quota_limit)
        remaining = max(0, int(quota_limit) - int(quota_used))
        reset_at = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        
        return (allowed, remaining, reset_at)
    
    def consume_quota(self, user_id, action_type, amount=1):
        """
        Consume quota for action
        """
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        
        # Increment usage
        new_usage = redis.incr(quota_key, amount)
        
        # Set expiry to end of day if first use
        if new_usage == amount:
            redis.expireat(quota_key, datetime.combine(
                date.today() + timedelta(days=1),
                datetime.min.time()
            ))
        
        # Log usage
        log_quota_usage(user_id, action_type, amount)
        
        return new_usage
```

### 7.4 Role-Based Access Control (RBAC)

```python
ROLES = {
    'owner': {
        'permissions': [
            'manage_project',
            'manage_team',
            'view_billing',
            'manage_billing',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'admin': {
        'permissions': [
            'manage_team',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'editor': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data'
        ]
    },
    'viewer': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'view_rankings'
        ]
    }
}

def check_permission(user_id, project_id, permission):
    # Get user's role in project
    membership = fetch_project_membership(user_id, project_id)
    
    if not membership:
        return False
    
    # Check if role has permission
    role_permissions = ROLES[membership.role]['permissions']
    return permission in role_permissions
```

---

## 8. Dashboard & UI Modules

### 8.1 Dashboard Components

#### **8.1.1 Keyword Explorer Module**

```
Components:
├── Search Bar
│   ├── Keyword input with autocomplete
│   ├── Country selector (dropdown with flags)
│   ├── Language selector
│   └── Device type selector (desktop/mobile/tablet)
│
├── Results Table
│   ├── Columns: Keyword, Volume, CPC, Competition, Difficulty, Trend
│   ├── Sortable columns
│   ├── Filterable (volume range, difficulty range)
│   ├── Bulk select for export
│   └── Add to project button
│
├── Keyword Details Panel (expandable row)
│   ├── 12-month trend chart
│   ├── Related keywords list
│   ├── Question keywords
│   ├── SERP features present
│   └── Top 10 ranking URLs
│
└── Sidebar Filters
    ├── Search volume range slider
    ├── Difficulty range slider
    ├── Competition level checkboxes
    ├── SERP features filters
    └── Keyword intent filters (informational, commercial, transactional)

Features:
- Real-time search with debounce (300ms)
- Export to CSV/Excel
- Save search history
- Favorite keywords
- Bulk keyword upload (CSV)
```

#### **8.1.2 Domain Overview Module**

```
Layout:
┌─────────────────────────────────────────────────────────────┐
│ Domain Input & Analysis                                      │
│ [example.com                              ] [Analyze]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Authority: 75│ Backlinks:   │ Org Keywords:│ Est. Traffic:│
│              │ 125,847      │ 45,231       │ 850,000/mo   │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Traffic Trend (Last 12 Months) - Line Chart                 │
│ [Interactive chart showing organic traffic over time]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Top Organic Keywords         │ Top Pages                     │
│ [Sortable table]             │ [Sortable table]              │
│ - Keyword                    │ - URL                         │
│ - Position                   │ - Traffic                     │
│ - Volume                     │ - Keywords                    │
│ - Traffic                    │ - Backlinks                   │
└──────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Backlink Growth              │ Competitors                   │
│ [Area chart]                 │ [List with metrics]           │
│ New vs Lost backlinks        │ - Domain                      │
│                              │ - Authority                   │
│                              │ - Keyword Overlap             │
└──────────────────────────────┴──────────────────────────────┘

Tabs:
- Overview
- Organic Keywords
- Top Pages
- Backlinks
- Competitors
- Historical Data
```

#### **8.1.3 SERP Overview Module**

```
Components:
├── SERP Search
│   ├── Keyword input
│   ├── Location selector (with map)
│   ├── Device type tabs
│   └── Analyze button
│
├── SERP Preview
│   ├── Visual SERP representation
│   ├── Organic results (1-100)
│   ├── Paid ads highlighted
│   ├── SERP features marked
│   └── Each result expandable for details
│
├── SERP Analysis
│   ├── Difficulty score gauge
│   ├── Opportunity score gauge
│   ├── Avg domain authority
│   ├── Avg backlinks
│   ├── Content length avg
│   └── SERP features breakdown
│
├── Competitor Analysis Table
│   )
    language: constr(regex='^[a-z]{2}# 🎯 Keyword Research & SEO Analysis Platform
## Complete System Design Document

> **Version:** 1.0  
> **Architecture Type:** Microservices with Event-Driven Components  
> **Scale Target:** 10M+ keywords, 1M+ domains, 100K+ concurrent users

---

## 📋 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Flow & Processing](#2-data-flow--processing)
3. [Database Design](#3-database-design)
4. [API Layer Design](#4-api-layer-design)
5. [Crawler & Data Sources](#5-crawler--data-sources)
6. [Ranking & Analytics Engine](#6-ranking--analytics-engine)
7. [User System](#7-user-system)
8. [Dashboard & UI Modules](#8-dashboard--ui-modules)
9. [Scalability, Performance & Security](#9-scalability-performance--security)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Architecture Overview

### 1.1 System Architecture Pattern

**Hybrid Microservices Architecture** with the following characteristics:
- Core services as independent microservices
- Shared data access layer for performance
- Event-driven communication for async operations
- API Gateway for unified access point

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  [Web Dashboard] [Mobile App] [Browser Extension] [API Clients] │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CDN LAYER (CloudFlare)                      │
│              [Static Assets] [API Response Cache]                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Kong/AWS ALB)                    │
│    [Rate Limiting] [Auth] [Routing] [Request Validation]        │
└─────┬───────────┬──────────┬──────────┬────────────┬───────────┘
      │           │          │          │            │
┌─────▼─────┐ ┌──▼────┐ ┌───▼─────┐ ┌─▼────┐ ┌────▼──────┐
│  Auth     │ │Keyword│ │ Domain  │ │SERP  │ │ Tracking  │
│  Service  │ │Service│ │ Service │ │Svc   │ │  Service  │
└─────┬─────┘ └──┬────┘ └───┬─────┘ └─┬────┘ └────┬──────┘
      │          │          │          │            │
┌─────▼──────────▼──────────▼──────────▼────────────▼───────────┐
│                   MESSAGE QUEUE (RabbitMQ/Kafka)               │
│  [Crawl Jobs] [Data Processing] [Analytics] [Notifications]   │
└──────┬────────────────┬────────────────┬─────────────┬────────┘
       │                │                │             │
┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐ ┌───▼─────┐
│   Crawler   │  │  Analytics  │  │   Email    │ │ Report  │
│   Workers   │  │   Engine    │  │  Service   │ │ Builder │
└──────┬──────┘  └──────┬──────┘  └─────┬──────┘ └───┬─────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                      DATA STORAGE LAYER                        │
│ [PostgreSQL] [MongoDB] [Redis] [Elasticsearch] [S3/Object]    │
└────────────────────────────────────────────────────────────────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                   EXTERNAL INTEGRATIONS                        │
│ [Google APIs] [Bing APIs] [Third-party SEO] [Proxy Services]  │
└────────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components Breakdown

#### **1.3.1 Frontend Layer**
- **Web Dashboard**: React/Next.js with SSR for SEO
- **Mobile Apps**: React Native for iOS/Android
- **Browser Extension**: Chrome/Firefox for on-page analysis
- **Component Library**: Shared UI components (charts, tables, forms)

#### **1.3.2 API Gateway**
- **Technology**: Kong API Gateway or AWS Application Load Balancer
- **Responsibilities**:
  - Request routing to microservices
  - Authentication token validation
  - Rate limiting and throttling
  - Request/response transformation
  - API versioning (v1, v2)
  - Logging and monitoring

#### **1.3.3 Microservices**

**Auth Service**
- User authentication and authorization
- JWT token management
- OAuth integration (Google, Facebook)
- API key generation and validation
- Session management

**Keyword Service**
- Keyword search and suggestions
- Keyword metrics (volume, CPC, competition)
- Related keywords and questions
- Keyword difficulty calculation
- Multi-language support

**Domain Service**
- Domain overview and metrics
- Backlink analysis
- Top pages analysis
- Organic keyword tracking
- Domain authority calculation

**SERP Service**
- SERP position tracking
- Featured snippets detection
- Local pack results
- Ads analysis
- SERP feature identification

**Tracking Service**
- Keyword rank tracking
- Position monitoring
- Ranking history
- Competitor tracking
- Alert system for rank changes

**Analytics Engine**
- Trend analysis
- Opportunity scoring
- Content gap analysis
- Competitive intelligence
- Predictive analytics

**Crawler Service**
- Distributed web crawler
- SERP scraping
- Backlink discovery
- Site auditing
- Content extraction

**Report Builder**
- PDF report generation
- Scheduled reports
- White-label reports
- Data export (CSV, Excel)

#### **1.3.4 Data Storage Components**

**PostgreSQL** (Primary Relational Database)
- User accounts and subscriptions
- Projects and settings
- Normalized keyword and domain data
- Transactional data

**MongoDB** (Document Store)
- Raw crawl data
- SERP snapshots
- Historical data
- Flexible schema data

**Redis** (Caching Layer)
- Session cache
- API response cache
- Real-time ranking cache
- Queue management
- Rate limiting counters

**Elasticsearch**
- Full-text keyword search
- Log aggregation and search
- Analytics queries
- Real-time suggestions

**S3/Object Storage**
- Backlink data archives
- Historical SERP screenshots
- Report files
- User uploads

### 1.4 Technology Stack Recommendation

#### **Backend Stack**
```
Language: Python 3.11+ (Primary), Node.js (Real-time services)
Frameworks: 
  - FastAPI (API services) - High performance, async
  - Django (Admin panel, complex business logic)
  - Express.js (Real-time notifications)
  
Task Queue: Celery with RabbitMQ or AWS SQS
Background Workers: Celery workers (CPU-intensive), Node workers (I/O)
Caching: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+
Message Broker: RabbitMQ or Apache Kafka (for high throughput)
```

#### **Frontend Stack**
```
Framework: Next.js 14+ (React with SSR/SSG)
State Management: Zustand or Redux Toolkit
UI Library: TailwindCSS + shadcn/ui components
Charts: Recharts or Apache ECharts
Data Tables: TanStack Table
Forms: React Hook Form + Zod validation
API Client: Axios with React Query for caching
```

#### **Database Stack**
```
Primary: PostgreSQL 15+ with Citus extension (for sharding)
Document: MongoDB 6+ with replica sets
Cache: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+ with ILM policies
Time-series: TimescaleDB (extension on PostgreSQL) for tracking data
```

#### **Infrastructure**
```
Container: Docker + Docker Compose (dev), Kubernetes (production)
Orchestration: Kubernetes (EKS/GKE) or AWS ECS
CI/CD: GitHub Actions or GitLab CI
Monitoring: Prometheus + Grafana, ELK Stack
APM: New Relic or Datadog
Error Tracking: Sentry
```

#### **External Services**
```
CDN: CloudFlare Enterprise
Email: SendGrid or AWS SES
Payment: Stripe
Analytics: Mixpanel, Google Analytics 4
Search APIs: Google Custom Search API, Bing Web Search API
Proxy Services: ScraperAPI, Bright Data, Oxylabs
```

### 1.5 Scalability Strategy

#### **Horizontal Scaling**
- All services stateless for easy replication
- Auto-scaling based on CPU/memory/queue depth
- Load balancers distribute traffic across instances
- Database read replicas for query distribution

#### **Caching Strategy**

**L1 Cache (Application Level)**
- In-memory caching in each service instance
- LRU cache with 5-minute TTL for hot data
- Size limit: 512MB per instance

**L2 Cache (Redis)**
```
Keyword Metrics: TTL 24 hours
Domain Overview: TTL 12 hours  
SERP Results: TTL 6 hours
User Sessions: TTL 30 minutes
API Responses: TTL based on data freshness
Rate Limiting: Real-time, no TTL
```

**L3 Cache (CDN)**
- Static assets: 1 year cache
- API responses: 5 minutes cache with stale-while-revalidate
- Images and fonts: 6 months cache

#### **Database Sharding Strategy**

**PostgreSQL Sharding** (using Citus)
```
Shard Key: domain_hash (for domain data)
Shard Key: keyword_hash (for keyword data)
Shard Key: user_id (for user data)

Distribution:
- 32 shards for keyword data (hash distribution)
- 16 shards for domain data
- 8 shards for user/project data
```

**MongoDB Sharding**
```
Shard Key: {country: 1, language: 1, keyword_hash: 1}
Zones: US, EU, ASIA for geographic distribution
Chunk Size: 64MB
```

### 1.6 Queue and Worker Setup

#### **Task Queue Architecture**

```
┌─────────────────────────────────────────────────────┐
│                  TASK PRODUCERS                      │
│  [API Services] [Scheduled Jobs] [User Actions]     │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│              MESSAGE BROKER (RabbitMQ)              │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ crawl_queue  │  │ analytics_q  │  │ email_q  │ │
│  │ Priority: 1  │  │ Priority: 2  │  │Priority:3│ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└──┬──────────┬──────────────┬────────────┬─────────┘
   │          │              │            │
┌──▼────┐ ┌──▼────┐  ┌──────▼─────┐  ┌──▼──────┐
│Crawler│ │SERP   │  │ Analytics  │  │  Email  │
│Worker │ │Worker │  │  Worker    │  │ Worker  │
│x20    │ │x10    │  │  x5        │  │  x3     │
└───────┘ └───────┘  └────────────┘  └─────────┘
```

#### **Worker Types and Configuration**

**1. Crawler Workers** (CPU + Network intensive)
```
Count: 20-50 workers (auto-scale)
Resources: 2 CPU, 4GB RAM per worker
Tasks:
  - SERP crawling (priority: high)
  - Backlink discovery (priority: medium)
  - Site auditing (priority: low)
  - Content extraction
Max Concurrency: 5 tasks per worker
Retry Strategy: Exponential backoff (max 3 retries)
Timeout: 60 seconds per task
```

**2. Analytics Workers** (CPU intensive)
```
Count: 5-10 workers
Resources: 4 CPU, 8GB RAM per worker
Tasks:
  - Keyword difficulty calculation
  - Domain authority scoring
  - Trend analysis
  - Content gap analysis
  - Opportunity scoring
Max Concurrency: 3 tasks per worker
Timeout: 120 seconds per task
```

**3. Data Processing Workers** (Memory intensive)
```
Count: 10-20 workers
Resources: 2 CPU, 8GB RAM per worker
Tasks:
  - Bulk data import
  - Data enrichment
  - Metric aggregation
  - Historical data processing
Max Concurrency: 2 tasks per worker
Batch Size: 1000 records per batch
```

**4. Notification Workers** (I/O intensive)
```
Count: 3-5 workers
Resources: 1 CPU, 2GB RAM per worker
Tasks:
  - Email notifications
  - Webhook delivery
  - Report generation
  - Alert processing
Max Concurrency: 10 tasks per worker
Timeout: 30 seconds per task
```

#### **Queue Priority System**
```
Priority 1 (Highest): Real-time user requests
Priority 2 (High): Scheduled tracking updates
Priority 3 (Medium): Background data refresh
Priority 4 (Low): Bulk data processing
Priority 5 (Lowest): Analytics and reports
```

---

## 2. Data Flow & Processing

### 2.1 Primary Workflows

#### **2.1.1 Keyword Research Workflow**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: User Input                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ User enters: "best running shoes"                       │ │
│ │ Filters: Country=US, Language=EN, Device=Desktop        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 2: Request Processing (API Gateway)                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ • Validate JWT token                                     │ │
│ │ • Check rate limits (100 req/min for Pro plan)          │ │
│ │ • Normalize keyword (lowercase, trim)                   │ │
│ │ • Generate cache key: "kw:en:us:desktop:best_running..."│ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 3: Cache Lookup (Redis L2 Cache)                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GET cache_key                                            │ │
│ │ TTL: 24 hours                                            │ │
│ │                                                          │ │
│ │ IF FOUND → Return cached response (80% of requests)     │ │
│ │ IF NOT FOUND → Continue to Step 4                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Cache Miss)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 4: Database Query (PostgreSQL + Elasticsearch)         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Query keywords table:                                    │ │
│ │   SELECT * FROM keywords                                 │ │
│ │   WHERE keyword_normalized = 'best running shoes'        │ │
│ │   AND country = 'US' AND language = 'EN'                │ │
│ │                                                          │ │
│ │ IF FOUND and data_age < 30 days:                        │ │
│ │   → Return from database                                │ │
│ │   → Update cache                                        │ │
│ │ IF NOT FOUND or data_age > 30 days:                     │ │
│ │   → Continue to Step 5 (Fresh Data Fetch)               │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Database Miss or Stale)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 5: External Data Fetch (Async Job)                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Publish job to RabbitMQ: "crawl_queue"                  │ │
│ │ {                                                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "keyword": "best running shoes",                      │ │
│ │   "country": "US",                                      │ │
│ │   "sources": ["google_api", "serp_scraper"],           │ │
│ │   "priority": "high"                                    │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Return immediate response to user:                      │ │
│ │ {                                                        │ │
│ │   "status": "processing",                               │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "estimated_time": "10-30 seconds",                   │ │
│ │   "partial_data": { ... } ← if available               │ │
│ │ }                                                        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 6: Crawler Worker Processing                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Worker picks up job from queue                          │ │
│ │                                                          │ │
│ │ Parallel data fetching (asyncio):                       │ │
│ │ ┌─────────────┐  ┌─────────────┐  ┌──────────────┐    │ │
│ │ │ Google Ads  │  │ Google      │  │ Third-party  │    │ │
│ │ │ Keyword API │  │ Trends API  │  │ SEO API      │    │ │
│ │ │ (volume,CPC)│  │ (12mo trend)│  │ (difficulty) │    │ │
│ │ └─────────────┘  └─────────────┘  └──────────────┘    │ │
│ │                                                          │ │
│ │ Data aggregation and enrichment:                        │ │
│ │ • Calculate average from multiple sources               │ │
│ │ • Compute keyword difficulty score                      │ │
│ │ • Generate related keywords                             │ │
│ │ • Extract questions and suggestions                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 7: Data Storage                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ PostgreSQL:                                              │ │
│ │   INSERT INTO keywords (keyword, country, language, ...) │ │
│ │   INSERT INTO keyword_metrics (keyword_id, volume, ...)  │ │
│ │   INSERT INTO keyword_trends (keyword_id, month, ...)    │ │
│ │                                                          │ │
│ │ Elasticsearch:                                           │ │
│ │   Index document for fast search and suggestions        │ │
│ │                                                          │ │
│ │ Redis Cache:                                             │ │
│ │   SET cache_key = {data} EX 86400 (24 hours)           │ │
│ │                                                          │ │
│ │ MongoDB (Raw Data Archive):                              │ │
│ │   Store original API responses for audit trail          │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 8: WebSocket Notification                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Push update to user's active session:                   │ │
│ │ {                                                        │ │
│ │   "event": "keyword_data_ready",                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "data": { full keyword metrics }                      │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Frontend updates UI with full data                      │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

#### **2.1.2 Domain Analysis Workflow**

```
User Input: "example.com"
    ↓
1. Domain Validation & Normalization
   • Check DNS resolution
   • Normalize to canonical form
   • Extract domain metadata
    ↓
2. Cache Check (Redis)
   • Key: "domain:example.com:overview"
   • TTL: 12 hours
   IF FOUND → Return cached data
    ↓
3. Database Lookup (PostgreSQL)
   • Check domains table
   • Check domain_metrics table
   • If data < 7 days old → Return
    ↓
4. Trigger Async Jobs (if needed)
   Job 1: Backlink Crawler
     → Crawl backlink sources
     → Discover new backlinks
     → Update backlink database
   
   Job 2: Organic Keyword Scraper
     → Fetch ranking keywords
     → Update keyword positions
     → Calculate traffic estimates
   
   Job 3: Top Pages Analyzer
     → Crawl sitemap
     → Analyze top-performing pages
     → Calculate page metrics
   
   Job 4: Domain Authority Calculator
     → Aggregate backlink data
     → Apply authority algorithm
     → Update domain score
    ↓
5. Data Aggregation
   • Combine all metrics
   • Calculate derived values
   • Generate summary stats
    ↓
6. Storage & Cache Update
   • Update PostgreSQL
   • Refresh Redis cache
   • Index in Elasticsearch
    ↓
7. Return Response
   • Domain overview
   • Top metrics
   • Recent changes
   • Recommendations
```

#### **2.1.3 SERP Analysis Workflow**

```
User Input: Keyword + Location
    ↓
1. SERP Fetch Request
   • Generate SERP cache key
   • Check Redis (TTL: 6 hours)
    ↓
2. Cache Miss → Trigger Crawler
   Job: SERP Scraper
     → Use rotating proxies
     → Fetch Google SERP page
     → Extract organic results
     → Extract paid ads
     → Extract SERP features
     → Handle CAPTCHA if needed
    ↓
3. SERP Data Processing
   • Parse HTML/JSON
   • Extract result URLs
   • Identify result types
   • Calculate positions
   • Detect SERP features
    ↓
4. Domain Enrichment
   For each result URL:
     → Lookup domain metrics
     → Calculate domain strength
     → Fetch page metrics
     → Analyze content
    ↓
5. Competitive Analysis
   • Compare domain authorities
   • Analyze content gaps
   • Calculate difficulty score
   • Generate insights
    ↓
6. Storage
   • PostgreSQL: serp_results table
   • MongoDB: Raw SERP snapshots
   • Redis: Cached response
    ↓
7. Return Enriched SERP Data
```

### 2.2 Data Pipeline Architecture

#### **2.2.1 Data Import Pipeline**

```
┌────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                            │
│  [Google APIs] [Bing APIs] [Third-party] [User Uploads]   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              INGESTION LAYER                               │
│  • API adapters with retry logic                           │
│  • Rate limiting per source                                │
│  • Request queuing and scheduling                          │
│  • Error handling and logging                              │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│            VALIDATION & CLEANING                           │
│  • Schema validation                                       │
│  • Data type conversion                                    │
│  • Null handling                                           │
│  • Duplicate detection                                     │
│  • Outlier detection                                       │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              TRANSFORMATION                                │
│  • Normalization (keywords, URLs)                          │
│  • Enrichment (add metadata)                               │
│  • Aggregation (combine sources)                           │
│  • Calculation (derived metrics)                           │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                LOADING LAYER                               │
│  • Batch insertion to PostgreSQL                           │
│  • Bulk indexing to Elasticsearch                          │
│  • Document insertion to MongoDB                           │
│  • Cache warming (Redis)                                   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│             POST-PROCESSING                                │
│  • Trigger analytics jobs                                  │
│  • Update aggregated tables                                │
│  • Invalidate stale cache                                  │
│  • Send notifications                                      │
└────────────────────────────────────────────────────────────┘
```

#### **2.2.2 Data Processing Stages**

**Stage 1: Raw Data Collection**
```python
# Pseudo-code
async def collect_keyword_data(keyword, country, language):
    sources = [
        fetch_google_ads_data(keyword, country),
        fetch_google_trends(keyword),
        fetch_third_party_api(keyword, country),
        scrape_serp_if_needed(keyword, country)
    ]
    
    results = await asyncio.gather(*sources, return_exceptions=True)
    
    return {
        'raw_data': results,
        'timestamp': utc_now(),
        'sources_succeeded': count_successes(results)
    }
```

**Stage 2: Data Cleaning**
```python
def clean_keyword_data(raw_data):
    cleaned = {
        'keyword': normalize_keyword(raw_data['keyword']),
        'volume': validate_volume(raw_data['volume']),
        'cpc': validate_currency(raw_data['cpc']),
        'competition': normalize_0_to_1(raw_data['competition']),
        'trend_data': interpolate_missing_months(raw_data['trend'])
    }
    
    # Remove outliers
    if is_outlier(cleaned['volume']):
        cleaned['volume_confidence'] = 'low'
    
    return cleaned
```

**Stage 3: Data Enrichment**
```python
def enrich_keyword_data(cleaned_data):
    enriched = cleaned_data.copy()
    
    # Calculate derived metrics
    enriched['difficulty_score'] = calculate_difficulty(
        cleaned_data['competition'],
        cleaned_data['volume'],
        cleaned_data['serp_features']
    )
    
    # Add related data
    enriched['related_keywords'] = find_related_keywords(
        cleaned_data['keyword']
    )
    
    # Add semantic data
    enriched['intent'] = classify_search_intent(
        cleaned_data['keyword']
    )
    
    return enriched
```

**Stage 4: Data Storage**
```python
async def store_keyword_data(enriched_data):
    # Parallel storage operations
    await asyncio.gather(
        store_in_postgres(enriched_data),
        index_in_elasticsearch(enriched_data),
        cache_in_redis(enriched_data),
        archive_in_mongodb(enriched_data['raw_data'])
    )
```

### 2.3 API Rate Limiting & Proxy Rotation

#### **2.3.1 Rate Limiting Strategy**

```
┌─────────────────────────────────────────────────────────────┐
│                  RATE LIMITING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: API Gateway Level (Per User)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Free Plan:     10 requests/minute                     │  │
│  │ Pro Plan:      100 requests/minute                    │  │
│  │ Agency Plan:   500 requests/minute                    │  │
│  │ Enterprise:    Custom limits                          │  │
│  │                                                       │  │
│  │ Implementation: Token bucket algorithm in Redis       │  │
│  │ Key: "ratelimit:user:{user_id}:{endpoint}"            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 2: Service Level (Per External API)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Google Ads API:    15,000/day (shared across users)   │  │
│  │ Google Trends:     1,500/hour                         │  │
│  │ Bing API:          5,000/month                        │  │
│  │ Third-party APIs:  Varies by provider                 │  │
│  │                                                       │  │
│  │ Implementation: Distributed counter in Redis          │  │
│  │ Key: "api_quota:{provider}:{date}"                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Layer 3: Crawler Level (Per Proxy/IP)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Max 60 requests/hour per IP                           │  │
│  │ Randomized delays: 2-5 seconds                        │  │
│  │ Rotating user agents                                  │  │
│  │ Cookie management                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### **2.3.2 Proxy Rotation System**

```
┌─────────────────────────────────────────────────────────────┐
│                  PROXY POOL MANAGEMENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Proxy Sources:                                             │
│  • Residential Proxies (Bright Data, Oxylabs)               │
│  • Datacenter Proxies (backup)                              │
│  • Mobile Proxies (for mobile SERP)                         │
│                                                             │
│  Pool Size: 1,000-10,000 rotating proxies                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    ROTATION STRATEGY                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Round-Robin Selection                                   │
│     • Distribute requests evenly                            │
│     • Track usage per proxy                                 │
│                                                             │
│  2. Health Checking                                         │
│     • Periodic connectivity tests                           │
│     • Response time monitoring                              │
│     • Success rate tracking                                 │
│     • Automatic removal of dead proxies                     │
│                                                             │
│  3. Geographic Targeting                                    │
│     • Match proxy location to search location               │
│     • US proxy for US searches                              │
│     • Local proxies for local SERP                          │
│                                                             │
│  4. Cooldown Management                                     │
│     • 5-minute cooldown after 50 requests                   │
│     • Exponential backoff on errors                         │
│     • Automatic proxy cycling                               │
│                                                             │
│  5. CAPTCHA Handling                                        │
│     • Detect CAPTCHA challenges                             │
│     • Mark proxy as temporary blocked                       │
│     • Integrate CAPTCHA solving service (2Captcha)          │
│     • Fallback to manual verification if needed             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Proxy Selection Algorithm:

```python
def select_proxy(country, previous_failures=[]):
    # Get healthy proxies for country
    candidate_proxies = redis.smembers(f'proxies:healthy:{country}')
    
    # Remove recently failed proxies
    candidate_proxies -= set(previous_failures)
    
    # Sort by recent usage (prefer least recently used)
    proxies_with_scores = []
    for proxy in candidate_proxies:
        last_used = redis.get(f'proxy:last_used:{proxy}')
        success_rate = redis.get(f'proxy:success_rate:{proxy}')
        
        score = calculate_proxy_score(last_used, success_rate)
        proxies_with_scores.append((proxy, score))
    
    # Select best proxy
    selected_proxy = max(proxies_with_scores, key=lambda x: x[1])[0]
    
    # Mark as in-use
    redis.set(f'proxy:last_used:{selected_proxy}', time.now())
    
    return selected_proxy
```

---

## 3. Database Design

### 3.1 Database Schema Overview

The system uses **four database technologies** for different purposes:

1. **PostgreSQL** - Primary relational data (users, projects, core metrics)
2. **MongoDB** - Document storage (raw crawl data, flexible schemas)
3. **Redis** - Caching and real-time data
4. **Elasticsearch** - Full-text search and analytics

### 3.2 PostgreSQL Schema

#### **3.2.1 Users & Authentication**

```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'free', -- free, pro, agency, enterprise
    plan_status VARCHAR(50) DEFAULT 'active', -- active, trial, expired, cancelled
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_plan_type ON users(plan_type);

-- User sessions
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- User subscriptions
CREATE TABLE subscriptions (
    subscription_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL, -- active, cancelled, expired, past_due
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);

-- User quotas and usage
CREATE TABLE user_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    quota_type VARCHAR(50) NOT NULL, -- keyword_searches, domain_analyses, rank_checks
    quota_limit INT NOT NULL,
    quota_used INT DEFAULT 0,
    reset_period VARCHAR(50) NOT NULL, -- daily, monthly
    last_reset_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quotas_user_id ON user_quotas(user_id);
CREATE UNIQUE INDEX idx_quotas_user_type ON user_quotas(user_id, quota_type);
```

#### **3.2.2 Projects & Organization**

```sql
-- Projects (workspace for organizing keywords and domains)
CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    target_country VARCHAR(2) DEFAULT 'US',
    target_language VARCHAR(5) DEFAULT 'en',
    target_location VARCHAR(255), -- city name for local SEO
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_archived BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_country ON projects(target_country);

-- Project members (for team collaboration)
CREATE TABLE project_members (
    member_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- owner, admin, editor, viewer
    invited_by BIGINT REFERENCES users(user_id),
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

CREATE INDEX idx_members_project_id ON project_members(project_id);
CREATE INDEX idx_members_user_id ON project_members(user_id);
```

#### **3.2.3 Keywords Core Tables**

```sql
-- Keywords master table
CREATE TABLE keywords (
    keyword_id BIGSERIAL PRIMARY KEY,
    keyword_text TEXT NOT NULL,
    keyword_normalized TEXT NOT NULL, -- lowercase, trimmed
    keyword_hash VARCHAR(64) NOT NULL, -- for sharding
    country VARCHAR(2) NOT NULL,
    language VARCHAR(5) NOT NULL,
    device_type VARCHAR(20) DEFAULT 'desktop', -- desktop, mobile, tablet
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_fetched_at TIMESTAMP,
    data_source VARCHAR(50), -- google_ads, bing, semrush_api
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(keyword_normalized, country, language, device_type)
);

CREATE INDEX idx_keywords_normalized ON keywords(keyword_normalized);
CREATE INDEX idx_keywords_hash ON keywords(keyword_hash);
CREATE INDEX idx_keywords_country ON keywords(country);
CREATE INDEX idx_keywords_updated_at ON keywords(updated_at);

-- Partitioning strategy (if using native partitioning)
-- CREATE TABLE keywords_us PARTITION OF keywords FOR VALUES IN ('US');
-- CREATE TABLE keywords_uk PARTITION OF keywords FOR VALUES IN ('UK');
-- CREATE TABLE keywords_in PARTITION OF keywords FOR VALUES IN ('IN');

-- Keyword metrics (search volume, CPC, competition)
CREATE TABLE keyword_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    search_volume BIGINT,
    search_volume_trend VARCHAR(20), -- up, down, stable
    cpc_min DECIMAL(10,2),
    cpc_max DECIMAL(10,2),
    cpc_avg DECIMAL(10,2),
    competition_score DECIMAL(3,2), -- 0.00 to 1.00
    competition_level VARCHAR(20), -- low, medium, high
    difficulty_score INT, -- 0-100
    opportunity_score INT, -- 0-100 (custom metric)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, metric_date)
);

CREATE INDEX idx_metrics_keyword_id ON keyword_metrics(keyword_id);
CREATE INDEX idx_metrics_date ON keyword_metrics(metric_date);
CREATE INDEX idx_metrics_volume ON keyword_metrics(search_volume);
CREATE INDEX idx_metrics_difficulty ON keyword_metrics(difficulty_score);

-- Keyword trends (12-month historical data)
CREATE TABLE keyword_trends (
    trend_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    trend_month DATE NOT NULL, -- first day of month
    trend_value INT NOT NULL, -- 0-100 (relative interest)
    search_volume_estimate BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, trend_month)
);

CREATE INDEX idx_trends_keyword_id ON keyword_trends(keyword_id);
CREATE INDEX idx_trends_month ON keyword_trends(trend_month);

-- Related keywords
CREATE TABLE related_keywords (
    relation_id BIGSERIAL PRIMARY KEY,
    source_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    related_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL, -- similar, broader, narrower, question
    relevance_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_keyword_id, related_keyword_id, relation_type)
);

CREATE INDEX idx_related_source ON related_keywords(source_keyword_id);
CREATE INDEX idx_related_target ON related_keywords(related_keyword_id);
CREATE INDEX idx_related_type ON related_keywords(relation_type);

-- Keyword questions (People Also Ask)
CREATE TABLE keyword_questions (
    question_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50), -- who, what, when, where, why, how
    frequency_score INT, -- how often it appears
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_keyword_id ON keyword_questions(keyword_id);
CREATE INDEX idx_questions_type ON keyword_questions(question_type);

-- User keyword lists (saved keywords)
CREATE TABLE user_keyword_lists (
    list_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    tags VARCHAR(255)[],
    priority INT, -- 1-5
    UNIQUE(project_id, keyword_id)
);

CREATE INDEX idx_user_lists_project ON user_keyword_lists(project_id);
CREATE INDEX idx_user_lists_keyword ON user_keyword_lists(keyword_id);
```

#### **3.2.4 Domains & Backlinks**

```sql
-- Domains master table
CREATE TABLE domains (
    domain_id BIGSERIAL PRIMARY KEY,
    domain_name VARCHAR(255) UNIQUE NOT NULL,
    domain_normalized VARCHAR(255) NOT NULL, -- lowercase
    domain_hash VARCHAR(64) NOT NULL,
    tld VARCHAR(50),
    is_subdomain BOOLEAN DEFAULT FALSE,
    root_domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_crawled_at TIMESTAMP,
    crawl_status VARCHAR(50), -- pending, in_progress, completed, failed
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_domains_normalized ON domains(domain_normalized);
CREATE INDEX idx_domains_hash ON domains(domain_hash);
CREATE INDEX idx_domains_tld ON domains(tld);
CREATE INDEX idx_domains_root ON domains(root_domain);

-- Domain metrics
CREATE TABLE domain_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    domain_authority INT, -- 0-100 (our custom score)
    page_authority_avg DECIMAL(5,2),
    total_backlinks BIGINT,
    unique_domains BIGINT,
    dofollow_backlinks BIGINT,
    nofollow_backlinks BIGINT,
    total_referring_ips BIGINT,
    organic_traffic_estimate BIGINT,
    organic_keywords_count BIGINT,
    organic_traffic_value DECIMAL(12,2), -- estimated value in USD
    paid_traffic_estimate BIGINT,
    social_signals JSONB, -- {facebook: 1000, twitter: 500, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, metric_date)
);

CREATE INDEX idx_domain_metrics_domain ON domain_metrics(domain_id);
CREATE INDEX idx_domain_metrics_date ON domain_metrics(metric_date);
CREATE INDEX idx_domain_metrics_authority ON domain_metrics(domain_authority);

-- Backlinks (huge table - consider sharding)
CREATE TABLE backlinks (
    backlink_id BIGSERIAL PRIMARY KEY,
    target_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    source_domain_id BIGINT REFERENCES domains(domain_id),
    source_url TEXT NOT NULL,
    source_page_title TEXT,
    anchor_text TEXT,
    link_type VARCHAR(20), -- dofollow, nofollow, redirect
    first_seen_at TIMESTAMP NOT NULL,
    last_seen_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    http_status INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_backlinks_target_domain ON backlinks(target_domain_id);
CREATE INDEX idx_backlinks_source_domain ON backlinks(source_domain_id);
CREATE INDEX idx_backlinks_first_seen ON backlinks(first_seen_at);
CREATE INDEX idx_backlinks_active ON backlinks(is_active);

-- For sharding large backlinks table:
-- Shard by target_domain_hash using Citus or manual sharding

-- Domain top pages
CREATE TABLE domain_top_pages (
    page_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    page_url TEXT NOT NULL,
    page_title TEXT,
    page_type VARCHAR(50), -- article, product, category, homepage
    organic_traffic_estimate BIGINT,
    organic_keywords_count INT,
    backlinks_count INT,
    social_shares INT,
    content_length INT,
    last_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, page_url)
);

CREATE INDEX idx_top_pages_domain ON domain_top_pages(domain_id);
CREATE INDEX idx_top_pages_traffic ON domain_top_pages(organic_traffic_estimate DESC);

-- Domain organic keywords
CREATE TABLE domain_organic_keywords (
    ranking_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    ranking_url TEXT NOT NULL,
    position INT NOT NULL,
    position_date DATE NOT NULL,
    previous_position INT,
    traffic_estimate INT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, keyword_id, position_date)
);

CREATE INDEX idx_organic_domain ON domain_organic_keywords(domain_id);
CREATE INDEX idx_organic_keyword ON domain_organic_keywords(keyword_id);
CREATE INDEX idx_organic_position ON domain_organic_keywords(position);
CREATE INDEX idx_organic_date ON domain_organic_keywords(position_date);
```

#### **3.2.5 SERP Data**

```sql
-- SERP results snapshots
CREATE TABLE serp_results (
    serp_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    search_date DATE NOT NULL,
    search_location VARCHAR(255), -- city/region for local searches
    device_type VARCHAR(20) DEFAULT 'desktop',
    total_results BIGINT,
    serp_features JSONB, -- {featured_snippet: true, local_pack: true, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, search_date, search_location, device_type)
);

CREATE INDEX idx_serp_keyword ON serp_results(keyword_id);
CREATE INDEX idx_serp_date ON serp_results(search_date);
CREATE INDEX idx_serp_location ON serp_results(search_location);

-- Individual SERP positions
CREATE TABLE serp_positions (
    position_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    position INT NOT NULL,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    title TEXT,
    description TEXT,
    result_type VARCHAR(50), -- organic, paid, featured_snippet, local, image, video
    serp_features JSONB, -- rich snippet data
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_positions_serp ON serp_positions(serp_id);
CREATE INDEX idx_positions_domain ON serp_positions(domain_id);
CREATE INDEX idx_positions_position ON serp_positions(position);

-- SERP features (detailed)
CREATE TABLE serp_features (
    feature_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    feature_type VARCHAR(50) NOT NULL, -- featured_snippet, local_pack, people_also_ask, etc.
    feature_data JSONB NOT NULL, -- flexible structure for different features
    feature_position INT,
    domain_id BIGINT REFERENCES domains(domain_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_features_serp ON serp_features(serp_id);
CREATE INDEX idx_features_type ON serp_features(feature_type);
CREATE INDEX idx_features_domain ON serp_features(domain_id);
```

#### **3.2.6 Keyword Tracking**

```sql
-- Keyword tracking projects
CREATE TABLE tracking_projects (
    tracking_project_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    target_domain VARCHAR(255) NOT NULL,
    check_frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    next_check_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tracking_project ON tracking_projects(project_id);
CREATE INDEX idx_tracking_next_check ON tracking_projects(next_check_at);

-- Tracked keywords
CREATE TABLE tracked_keywords (
    tracked_keyword_id BIGSERIAL PRIMARY KEY,
    tracking_project_id BIGINT REFERENCES tracking_projects(tracking_project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    target_url TEXT, -- specific URL to track
    tags VARCHAR(255)[],
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracking_project_id, keyword_id)
);

CREATE INDEX idx_tracked_project ON tracked_keywords(tracking_project_id);
CREATE INDEX idx_tracked_keyword ON tracked_keywords(keyword_id);

-- Ranking history (time-series data - consider TimescaleDB)
CREATE TABLE ranking_history (
    history_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    check_date DATE NOT NULL,
    check_time TIMESTAMP NOT NULL,
    position INT, -- NULL if not ranking
    ranking_url TEXT,
    serp_features VARCHAR(50)[], -- features present at time of check
    pixel_rank INT, -- position in pixels from top
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracked_keyword_id, check_date, check_time)
);

CREATE INDEX idx_history_tracked ON ranking_history(tracked_keyword_id);
CREATE INDEX idx_history_date ON ranking_history(check_date);
CREATE INDEX idx_history_position ON ranking_history(position);

-- Convert to TimescaleDB hypertable for better time-series performance
-- SELECT create_hypertable('ranking_history', 'check_time');

-- Ranking alerts
CREATE TABLE ranking_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- position_change, entered_top10, dropped_out, etc.
    alert_threshold INT, -- e.g., alert if change > 5 positions
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_tracked ON ranking_alerts(tracked_keyword_id);

-- Alert history
CREATE TABLE alert_notifications (
    notification_id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT REFERENCES ranking_alerts(alert_id) ON DELETE CASCADE,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    trigger_date DATE NOT NULL,
    old_position INT,
    new_position INT,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_alert ON alert_notifications(alert_id);
CREATE INDEX idx_notifications_date ON alert_notifications(trigger_date);
```

#### **3.2.7 Content Analysis & Gap Analysis**

```sql
-- Content analysis
CREATE TABLE content_analysis (
    analysis_id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    keyword_id BIGINT, -- target keyword for analysis
    content_length INT,
    word_count INT,
    readability_score DECIMAL(5,2),
    keyword_density DECIMAL(5,2),
    h1_count INT,
    h2_count INT,
    image_count INT,
    internal_links_count INT,
    external_links_count INT,
    schema_markup JSONB,
    meta_title TEXT,
    meta_description TEXT,
    analyzed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_content_domain ON content_analysis(domain_id);
CREATE INDEX idx_content_keyword ON content_analysis(keyword_id);

-- Content gap analysis (comparing domains)
CREATE TABLE content_gaps (
    gap_id BIGSERIAL PRIMARY KEY,
    source_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    competitor_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    competitor_position INT,
    source_position INT, -- NULL if not ranking
    gap_score INT, -- 0-100
    opportunity_score INT, -- 0-100
    analysis_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_domain_id, competitor_domain_id, keyword_id, analysis_date)
);

CREATE INDEX idx_gaps_source ON content_gaps(source_domain_id);
CREATE INDEX idx_gaps_competitor ON content_gaps(competitor_domain_id);
CREATE INDEX idx_gaps_keyword ON content_gaps(keyword_id);
CREATE INDEX idx_gaps_score ON content_gaps(gap_score DESC);
```

#### **3.2.8 API Cache & Search History**

```sql
-- API response cache metadata
CREATE TABLE api_cache_metadata (
    cache_id BIGSERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    entity_id BIGINT, -- keyword_id, domain_id, etc.
    cache_ttl INT NOT NULL, -- seconds
    cached_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    hit_count INT DEFAULT 0,
    last_hit_at TIMESTAMP
);

CREATE INDEX idx_cache_key ON api_cache_metadata(cache_key);
CREATE INDEX idx_cache_expires ON api_cache_metadata(expires_at);
CREATE INDEX idx_cache_type ON api_cache_metadata(cache_type);

-- Search history (for analytics and suggestions)
CREATE TABLE search_history (
    search_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    search_query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    search_filters JSONB, -- country, language, device, etc.
    result_count INT,
    searched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_query ON search_history(search_query);
CREATE INDEX idx_search_date ON search_history(searched_at);
```

#### **3.2.9 External API Integration Tracking**

```sql
-- API integration logs
CREATE TABLE api_integration_logs (
    log_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL, -- google_ads, google_trends, semrush, etc.
    endpoint VARCHAR(255) NOT NULL,
    request_method VARCHAR(10),
    request_params JSONB,
    response_status INT,
    response_time_ms INT,
    error_message TEXT,
    requested_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_logs_provider ON api_integration_logs(provider);
CREATE INDEX idx_api_logs_date ON api_integration_logs(requested_at);
CREATE INDEX idx_api_logs_status ON api_integration_logs(response_status);

-- API quota tracking
CREATE TABLE api_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    quota_type VARCHAR(50) NOT NULL, -- daily, monthly
    quota_limit BIGINT NOT NULL,
    quota_used BIGINT DEFAULT 0,
    quota_period DATE NOT NULL,
    reset_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, quota_type, quota_period)
);

CREATE INDEX idx_api_quotas_provider ON api_quotas(provider);
CREATE INDEX idx_api_quotas_period ON api_quotas(quota_period);
```

#### **3.2.10 Indexing & Partitioning Strategy**

```sql
-- Composite indexes for common query patterns

-- Keyword searches by country and language
CREATE INDEX idx_keywords_country_lang_norm 
ON keywords(country, language, keyword_normalized);

-- Keyword metrics for trending keywords
CREATE INDEX idx_metrics_volume_date 
ON keyword_metrics(search_volume DESC, metric_date DESC);

-- Domain backlinks by date and status
CREATE INDEX idx_backlinks_target_active_date 
ON backlinks(target_domain_id, is_active, last_seen_at DESC);

-- SERP tracking queries
CREATE INDEX idx_ranking_history_tracked_date 
ON ranking_history(tracked_keyword_id, check_date DESC);

-- Content gaps by score
CREATE INDEX idx_content_gaps_source_score 
ON content_gaps(source_domain_id, gap_score DESC, analysis_date DESC);

-- Partitioning strategy for large tables
-- Example: Partition ranking_history by month
CREATE TABLE ranking_history_y2025m01 PARTITION OF ranking_history
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE ranking_history_y2025m02 PARTITION OF ranking_history
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automated partition creation via pg_cron or external script
```

### 3.3 MongoDB Collections

MongoDB stores **flexible, document-based data** and **raw crawl results**.

#### **3.3.1 Raw SERP Snapshots**

```javascript
// Collection: serp_snapshots
{
    _id: ObjectId(),
    keyword: "best running shoes",
    country: "US",
    language: "en",
    device: "desktop",
    search_date: ISODate("2025-01-15T10:30:00Z"),
    raw_html: "<html>...</html>", // Full SERP HTML
    raw_json: { /* Google API response */ },
    screenshot_url: "s3://bucket/serp-snapshots/uuid.png",
    results: [
        {
            position: 1,
            url: "https://example.com/running-shoes",
            title: "Best Running Shoes 2025",
            description: "...",
            type: "organic",
            rich_snippet: {
                rating: 4.5,
                reviews: 1200,
                price: "$129.99"
            }
        }
        // ... more results
    ],
    serp_features: [
        {
            type: "featured_snippet",
            content: "...",
            source_url: "https://example.com"
        },
        {
            type: "people_also_ask",
            questions: [...]
        }
    ],
    ads: [
        {
            position: "top1",
            url: "...",
            title: "...",
            description: "..."
        }
    ],
    metadata: {
        total_results: 2340000000,
        search_time_ms: 234,
        proxy_used: "proxy123",
        crawler_version: "2.0"
    },
    created_at: ISODate("2025-01-15T10:30:05Z")
}

// Indexes
db.serp_snapshots.createIndex({ keyword: 1, country: 1, search_date: -1 });
db.serp_snapshots.createIndex({ search_date: -1 });
db.serp_snapshots.createIndex({ "results.url": 1 });
```

#### **3.3.2 Crawl Queue**

```javascript
// Collection: crawl_queue
{
    _id: ObjectId(),
    job_id: "uuid",
    job_type: "serp_crawl", // serp_crawl, backlink_discovery, content_extraction
    priority: 1, // 1-5
    status: "pending", // pending, in_progress, completed, failed
    keyword: "running shoes",
    country: "US",
    language: "en",
    parameters: {
        device: "desktop",
        location: "New York, NY",
        num_results: 100
    },
    retry_count: 0,
    max_retries: 3,
    assigned_worker: null,
    started_at: null,
    completed_at: null,
    error_message: null,
    result_reference: null, // Reference to result in other collection
    created_at: ISODate("2025-01-15T10:00:00Z"),
    updated_at: ISODate("2025-01-15T10:00:00Z"),
    scheduled_for: ISODate("2025-01-15T10:05:00Z")
}

// Indexes
db.crawl_queue.createIndex({ status: 1, priority: 1, scheduled_for: 1 });
db.crawl_queue.createIndex({ job_id: 1 });
db.crawl_queue.createIndex({ created_at: -1 });
```

#### **3.3.3 Backlink Discovery Data**

```javascript
// Collection: backlink_raw_data
{
    _id: ObjectId(),
    target_domain: "example.com",
    target_url: "https://example.com/page",
    discovered_backlinks: [
        {
            source_url: "https://source.com/article",
            source_domain: "source.com",
            anchor_text: "click here",
            link_type: "dofollow",
            context: "... surrounding text ...",
            discovered_at: ISODate("2025-01-15T10:00:00Z"),
            http_status: 200,
            source_page_title: "Article Title",
            source_page_metrics: {
                domain_authority: 45,
                page_authority: 38,
                spam_score: 2
            }
        }
        // ... thousands more
    ],
    crawl_method: "ahrefs_api", // ahrefs_api, moz_api, manual_crawl
    crawl_date: ISODate("2025-01-15T10:00:00Z"),
    total_backlinks_found: 15234,
    metadata: {
        api_version: "v3",
        cost_credits: 50
    },
    created_at: ISODate("2025-01-15T10:30:00Z")
}

// Indexes
db.backlink_raw_data.createIndex({ target_domain: 1, crawl_date: -1 });
db.backlink_raw_data.createIndex({ "discovered_backlinks.source_domain": 1 });
```

#### **3.3.4 Historical Metrics Archive**

```javascript
// Collection: keyword_metrics_archive
// Old keyword metrics (>90 days) moved from PostgreSQL to MongoDB
{
    _id: ObjectId(),
    keyword_id: 12345,
    keyword: "running shoes",
    country: "US",
    metrics_by_month: {
        "2024-01": {
            search_volume: 110000,
            cpc_avg: 1.25,
            competition: 0.78,
            difficulty_score: 65
        },
        "2024-02": {
            search_volume: 135000,
            cpc_avg: 1.32,
            competition: 0.81,
            difficulty_score: 68
        }
        // ... 12+ months of data
    },
    archived_at: ISODate("2025-01-15T00:00:00Z")
}

// Indexes
db.keyword_metrics_archive.createIndex({ keyword_id: 1 });
db.keyword_metrics_archive.createIndex({ archived_at: -1 });
```

### 3.4 Redis Data Structures

Redis handles **caching, real-time data, and queue management**.

#### **3.4.1 Cache Keys Structure**

```redis
# Keyword data cache
Key: "cache:keyword:en:us:desktop:running_shoes"
Type: String (JSON)
TTL: 86400 seconds (24 hours)
Value: {
    "keyword": "running shoes",
    "volume": 110000,
    "cpc": 1.25,
    "difficulty": 65,
    "trend": [100, 95, 98, ...]
}

# Domain overview cache
Key: "cache:domain:example.com:overview"
Type: String (JSON)
TTL: 43200 seconds (12 hours)
Value: {
    "domain": "example.com",
    "authority": 75,
    "backlinks": 125000,
    "keywords": 45000,
    "traffic": 850000
}

# SERP results cache
Key: "cache:serp:en:us:running_shoes"
Type: String (JSON)
TTL: 21600 seconds (6 hours)
Value: {
    "keyword": "running shoes",
    "results": [...],
    "features": [...]
}

# User session
Key: "session:{user_id}:{session_token}"
Type: String (JSON)
TTL: 1800 seconds (30 minutes, sliding)
Value: {
    "user_id": 123,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": [...]
}
```

#### **3.4.2 Rate Limiting**

```redis
# User rate limit (token bucket)
Key: "ratelimit:user:{user_id}:keyword_search"
Type: String (integer)
TTL: 60 seconds
Value: 95  # requests remaining this minute
Algorithm: Token bucket with sliding window

# API provider rate limit
Key: "ratelimit:api:google_ads:daily"
Type: String (integer)
TTL: Until midnight UTC
Value: 14523  # requests used today

# IP-based rate limit (for crawlers)
Key: "ratelimit:ip:{proxy_ip}"
Type: Sorted Set
TTL: 3600 seconds
Members: {timestamp: request_id}
Algorithm: Sliding window log
```

#### **3.4.3 Real-time Ranking Data**

```redis
# Current rankings (hot data)
Key: "ranking:live:{tracked_keyword_id}"
Type: Hash
TTL: 3600 seconds
Fields:
    position: 5
    url: "https://example.com/page"
    last_check: 1705320000
    previous_position: 7

# Ranking change notifications
Key: "ranking:changes:{user_id}"
Type: List
TTL: 604800 seconds (7 days)
Values: [
    {"keyword": "...", "old": 7, "new": 5, "date": "..."},
    ...
]
```

#### **3.4.4 Queue Management**

```redis
# Priority queue for crawl jobs
Key: "queue:crawl:priority:{1-5}"
Type: List (FIFO)
Values: [job_id1, job_id2, ...]

# Job status tracking
Key: "job:{job_id}:status"
Type: Hash
Fields:
    status: "in_progress"
    worker_id: "worker-1"
    started_at: 1705320000
    progress: 45  # percentage

# Worker heartbeat
Key: "worker:{worker_id}:heartbeat"
Type: String
TTL: 60 seconds
Value: timestamp
```

### 3.5 Elasticsearch Indices

Elasticsearch provides **full-text search** and **fast analytics**.

#### **3.5.1 Keywords Index**

```json
// Index: keywords
{
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "snowball"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "keyword_id": {"type": "long"},
            "keyword_text": {
                "type": "text",
                "analyzer": "keyword_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "country": {"type": "keyword"},
            "language": {"type": "keyword"},
            "search_volume": {"type": "long"},
            "cpc_avg": {"type": "float"},
            "difficulty_score": {"type": "integer"},
            "opportunity_score": {"type": "integer"},
            "trend_direction": {"type": "keyword"},
            "related_keywords": {
                "type": "text",
                "analyzer": "keyword_analyzer"
            },
            "last_updated": {"type": "date"}
        }
    }
}
```

#### **3.5.2 Domains Index**

```json
// Index: domains
{
    "mappings": {
        "properties": {
            "domain_id": {"type": "long"},
            "domain_name": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "domain_authority": {"type": "integer"},
            "total_backlinks": {"type": "long"},
            "organic_keywords": {"type": "long"},
            "organic_traffic": {"type": "long"},
            "tld": {"type": "keyword"},
            "category": {"type": "keyword"},
            "last_crawled": {"type": "date"}
        }
    }
}
```

#### **3.5.3 Search Suggestions Index**

```json
// Index: search_suggestions
{
    "mappings": {
        "properties": {
            "suggestion": {
                "type": "completion",
                "analyzer": "simple",
                "search_analyzer": "simple"
            },
            "type": {"type": "keyword"}, // keyword, domain
            "popularity": {"type": "integer"},
            "country": {"type": "keyword"}
        }
    }
}
```

### 3.6 Sharding & Partitioning Plan

#### **3.6.1 PostgreSQL Sharding (using Citus)**

```sql
-- Distribute keywords table across shards
SELECT create_distributed_table('keywords', 'keyword_hash');
SELECT create_distributed_table('keyword_metrics', 'keyword_id');

-- Co-locate related tables for join performance
SELECT create_distributed_table('related_keywords', 'source_keyword_id', 
    colocate_with => 'keywords');

-- Distribute backlinks by target domain
SELECT create_distributed_table('backlinks', 'target_domain_id');

-- Reference tables (replicated to all shards)
SELECT create_reference_table('users');
SELECT create_reference_table('projects');
```

#### **3.6.2 MongoDB Sharding**

```javascript
// Enable sharding on database
sh.enableSharding("seo_platform");

// Shard serp_snapshots by compound key
sh.shardCollection("seo_platform.serp_snapshots", {
    country: 1,
    language: 1,
    search_date: 1
});

// Shard backlink_raw_data by target domain
sh.shardCollection("seo_platform.backlink_raw_data", {
    target_domain: "hashed"
});

// Shard crawl_queue by job_id
sh.shardCollection("seo_platform.crawl_queue", {
    job_id: "hashed"
});
```

#### **3.6.3 Data Retention & Archival**

```
Hot Data (PostgreSQL):
  - Last 90 days: Full metrics in main tables
  - Query performance: <100ms

Warm Data (PostgreSQL + compression):
  - 90 days - 1 year: Aggregated daily metrics
  - Query performance: <500ms

Cold Data (MongoDB):
  - 1+ years: Monthly aggregates only
  - Raw data archived to S3
  - Query performance: <2s

Archival Policy:
  - Ranking history: Keep daily for 90 days, weekly for 1 year, monthly forever
  - SERP snapshots: Keep full HTML for 30 days, metadata only after
  - Backlinks: Keep active backlinks in PostgreSQL, historical in MongoDB
  - API logs: Keep 30 days in PostgreSQL, archive to S3 after
```

---

## 4. API Layer Design

### 4.1 API Architecture

**Protocol:** REST API with optional GraphQL endpoint  
**Format:** JSON  
**Authentication:** JWT tokens + API keys  
**Versioning:** URL-based (`/api/v1/`, `/api/v2/`)

### 4.2 API Endpoints

#### **4.2.1 Keyword Research API**

```
POST /api/v1/keywords/search
Description: Search for keyword data
Authentication: Required (JWT or API key)
Rate Limit: 100/min (Pro), 500/min (Agency)

Request:
{
    "keyword": "running shoes",
    "country": "US",  // ISO 3166-1 alpha-2
    "language": "en",
    "device": "desktop",  // desktop, mobile, tablet
    "include_related": true,
    "include_questions": true,
    "include_trends": true
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "normalized": "running shoes",
        "metrics": {
            "search_volume": 110000,
            "search_volume_trend": "up",  // up, down, stable
            "cpc": {
                "min": 0.85,
                "max": 2.50,
                "avg": 1.25,
                "currency": "USD"
            },
            "competition": {
                "score": 0.78,
                "level": "high"  // low, medium, high
            },
            "difficulty_score": 65,  // 0-100
            "opportunity_score": 42  // 0-100 (custom metric)
        },
        "trends": {
            "last_12_months": [
                {"month": "2024-02", "value": 95},
                {"month": "2024-03", "value": 100},
                ...
            ],
            "year_over_year": 8.5  // % change
        },
        "related_keywords": [
            {
                "keyword": "best running shoes",
                "volume": 90500,
                "relevance": 0.95,
                "type": "similar"
            },
            ...
        ],
        "questions": [
            {
                "question": "what are the best running shoes for beginners",
                "type": "what",
                "frequency": 85
            },
            ...
        ],
        "serp_features": [
            "featured_snippet",
            "people_also_ask",
            "local_pack"
        ],
        "last_updated": "2025-01-15T10:30:00Z"
    },
    "metadata": {
        "cached": true,
        "cache_age_seconds": 3600,
        "sources": ["google_ads", "google_trends"],
        "credits_used": 1
    }
}

Error Responses:
400 Bad Request:
{
    "status": "error",
    "error": {
        "code": "INVALID_COUNTRY",
        "message": "Country code must be ISO 3166-1 alpha-2",
        "field": "country"
    }
}

429 Too Many Requests:
{
    "status": "error",
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Try again in 45 seconds",
        "retry_after": 45
    }
}

402 Payment Required:
{
    "status": "error",
    "error": {
        "code": "QUOTA_EXCEEDED",
        "message": "Monthly quota exceeded. Upgrade plan to continue",
        "quota_limit": 1000,
        "quota_used": 1000,
        "reset_date": "2025-02-01T00:00:00Z"
    }
}
```

```
GET /api/v1/keywords/{keyword_id}/suggestions
Description: Get related keywords and suggestions
Authentication: Required

Query Parameters:
- type: related|questions|broader|narrower (default: all)
- limit: 1-100 (default: 50)
- min_volume: minimum search volume filter
- max_difficulty: maximum difficulty score filter

Response (200 OK):
{
    "status": "success",
    "data": {
        "suggestions": [
            {
                "keyword": "best running shoes for flat feet",
                "search_volume": 22000,
                "difficulty_score": 58,
                "relevance_score": 0.88,
                "type": "narrower"
            },
            ...
        ],
        "total": 247,
        "returned": 50
    }
}
```

```
POST /api/v1/keywords/bulk
Description: Bulk keyword lookup (up to 100 keywords)
Authentication: Required
Rate Limit: 10/min (Pro), 50/min (Agency)

Request:
{
    "keywords": ["running shoes", "hiking boots", ...],
    "country": "US",
    "language": "en",
    "metrics": ["volume", "cpc", "difficulty"]  // optional filter
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "results": [
            {
                "keyword": "running shoes",
                "status": "success",
                "metrics": {...}
            },
            {
                "keyword": "xyz123invalid",
                "status": "not_found",
                "error": "No data available"
            }
        ],
        "summary": {
            "total": 100,
            "successful": 98,
            "failed": 2
        }
    },
    "metadata": {
        "credits_used": 10,
        "processing_time_ms": 1250
    }
}
```

#### **4.2.2 Domain Analysis API**

```
GET /api/v1/domains/{domain}/overview
Description: Get comprehensive domain metrics
Authentication: Required
Rate Limit: 50/min (Pro), 200/min (Agency)

Path Parameters:
- domain: example.com or www.example.com

Query Parameters:
- include_backlinks: true|false (default: false)
- include_top_pages: true|false (default: false)
- include_keywords: true|false (default: false)

Response (200 OK):
{
    "status": "success",
    "data": {
        "domain": "example.com",
        "metrics": {
            "domain_authority": 75,
            "page_authority_avg": 48.5,
            "spam_score": 2,
            "backlinks": {
                "total": 125847,
                "unique_domains": 8542,
                "dofollow": 98234,
                "nofollow": 27613,
                "referring_ips": 7234,
                "new_last_month": 1234,
                "lost_last_month": 456
            },
            "organic": {
                "keywords_count": 45231,
                "traffic_estimate": 850000,
                "traffic_value": 425000.00,
                "traffic_trend": "up",
                "top_keywords_count": 150,
                "keywords_top_3": 1234,
                "keywords_top_10": 4567,
                "keywords_top_100": 18923
            },
            "paid": {
                "keywords_count": 234,
                "traffic_estimate": 12000,
                "traffic_cost": 15000.00
            },
            "content": {
                "pages_indexed": 1547,
                "pages_crawled": 1892,
                "avg_page_speed": 2.3,
                "mobile_friendly_score": 95
            }
        },
        "competitors": [
            {
                "domain": "competitor1.com",
                "authority": 72,
                "keyword_overlap": 1234,
                "similarity_score": 0.78
            },
            ...
        ],
        "last_updated": "2025-01-15T08:00:00Z"
    }
}
```

```
GET /api/v1/domains/{domain}/backlinks
Description: Get backlink data for domain
Authentication: Required

Query Parameters:
- page: 1-1000 (default: 1)
- limit: 10-100 (default: 50)
- type: all|dofollow|nofollow (default: all)
- sort: authority|date_found|anchor_text (default: authority)
- order: desc|asc (default: desc)
- min_authority: 0-100 (filter)
- only_active: true|false (default: true)

Response (200 OK):
{
    "status": "success",
    "data": {
        "backlinks": [
            {
                "source_url": "https://source.com/article",
                "source_domain": "source.com",
                "source_authority": 68,
                "target_url": "https://example.com/page",
                "anchor_text": "click here",
                "link_type": "dofollow",
                "first_seen": "2024-06-15T00:00:00Z",
                "last_seen": "2025-01-15T00:00:00Z",
                "http_status": 200,
                "is_active": true
            },
            ...
        ],
        "pagination": {
            "page": 1,
            "limit": 50,
            "total": 125847,
            "pages": 2517
        }
    }
}
```

```
GET /api/v1/domains/{domain}/top-pages
Description: Get top-performing pages
Authentication: Required

Query Parameters:
- page: 1-100 (default: 1)
- limit: 10-100 (default: 20)
- sort: traffic|keywords|backlinks (default: traffic)
- metric: organic|paid|all (default: organic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "pages": [
            {
                "url": "https://example.com/best-products",
                "title": "Best Products 2025",
                "page_authority": 52,
                "organic_traffic": 85000,
                "organic_keywords": 1234,
                "backlinks": 456,
                "social_shares": 1200,
                "traffic_value": 42500.00,
                "top_keywords": [
                    {
                        "keyword": "best products",
                        "position": 2,
                        "volume": 22000,
                        "traffic_estimate": 8800
                    },
                    ...
                ]
            },
            ...
        ],
        "pagination": {...}
    }
}
```

```
GET /api/v1/domains/{domain}/organic-keywords
Description: Get ranking keywords for domain
Authentication: Required

Query Parameters:
- page: 1-1000
- limit: 10-100
- position: 1-100 (filter)
- min_volume: minimum search volume
- sort: position|volume|traffic (default: traffic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "keywords": [
            {
                "keyword": "running shoes",
                "position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "search_volume": 110000,
                "traffic_estimate": 8800,
                "traffic_value": 11000.00,
                "serp_features": ["featured_snippet"]
            },
            ...
        ],
        "summary": {
            "total_keywords": 45231,
            "top_3": 1234,
            "top_10": 4567,
            "top_100": 18923
        },
        "pagination": {...}
    }
}
```

#### **4.2.3 SERP Analysis API**

```
POST /api/v1/serp/analyze
Description: Get SERP analysis for keyword
Authentication: Required
Rate Limit: 50/min

Request:
{
    "keyword": "running shoes",
    "country": "US",
    "language": "en",
    "device": "desktop",
    "location": "New York, NY",  // optional for local searches
    "num_results": 100  // 10-100, default: 10
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "total_results": 234000000,
        "serp_features": [
            {
                "type": "featured_snippet",
                "position": 0,
                "domain": "example.com",
                "url": "https://example.com/guide",
                "content_preview": "Running shoes are..."
            },
            {
                "type": "people_also_ask",
                "questions": [
                    "What are the best running shoes?",
                    "How to choose running shoes?",
                    ...
                ]
            },
            {
                "type": "local_pack",
                "businesses": [...]
            }
        ],
        "organic_results": [
            {
                "position": 1,
                "title": "Best Running Shoes 2025",
                "url": "https://example.com/running-shoes",
                "domain": "example.com",
                "domain_authority": 75,
                "description": "Discover the best...",
                "rich_snippet": {
                    "type": "product",
                    "rating": 4.5,
                    "reviews": 1200,
                    "price": "$129.99"
                },
                "backlinks": 1234,
                "referring_domains": 456,
                "estimated_traffic": 35000
            },
            ...
        ],
        "paid_results": [
            {
                "position": "top1",
                "title": "Running Shoes Sale",
                "url": "https://shop.com/running",
                "domain": "shop.com",
                "description": "50% off all running shoes"
            },
            ...
        ],
        "analysis": {
            "difficulty_score": 68,
            "opportunity_score": 45,
            "avg_domain_authority": 72.5,
            "avg_backlinks": 8542,
            "content_length_avg": 2850,
            "content_recommendations": [
                "Include product comparisons",
                "Add video content",
                "Target featured snippet opportunity"
            ]
        },
        "last_updated": "2025-01-15T10:30:00Z"
    }
}
```

```
GET /api/v1/serp/features
Description: Get SERP features statistics
Authentication: Required

Query Parameters:
- keyword: specific keyword or keyword_id
- country: US, UK, etc.
- date_range: last_7_days|last_30_days|last_90_days

Response (200 OK):
{
    "status": "success",
    "data": {
        "features_present": [
            {
                "feature": "featured_snippet",
                "frequency": 85,  // % of time present
                "domains_winning": [
                    {"domain": "example.com", "count": 45},
                    ...
                ]
            },
            {
                "feature": "people_also_ask",
                "frequency": 92
            },
            {
                "feature": "local_pack",
                "frequency": 12
            }
        ],
        "feature_history": [
            {
                "date": "2025-01-15",
                "features": ["featured_snippet", "people_also_ask", "images"]
            },
            ...
        ]
    }
}
```

#### **4.2.4 Rank Tracking API**

```
POST /api/v1/tracking/projects
Description: Create new tracking project
Authentication: Required

Request:
{
    "project_id": 123,  // existing project
    "name": "My Website Tracking",
    "target_domain": "example.com",
    "check_frequency": "daily",  // daily, weekly, monthly
    "keywords": [
        {
            "keyword": "running shoes",
            "target_url": "https://example.com/running-shoes",
            "tags": ["product", "priority-high"]
        },
        ...
    ]
}

Response (201 Created):
{
    "status": "success",
    "data": {
        "tracking_project_id": 456,
        "keywords_added": 50,
        "next_check_at": "2025-01-16T00:00:00Z",
        "estimated_credits_per_check": 50
    }
}
```

```
GET /api/v1/tracking/projects/{project_id}/rankings
Description: Get ranking data for tracked keywords
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD (default: 30 days ago)
- date_to: YYYY-MM-DD (default: today)
- tags: filter by tags (comma-separated)
- position_change: improved|declined|unchanged|new|lost
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "rankings": [
            {
                "keyword": "running shoes",
                "current_position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "best_position": 3,
                "worst_position": 15,
                "average_position": 6.8,
                "history": [
                    {"date": "2025-01-15", "position": 5},
                    {"date": "2025-01-14", "position": 6},
                    ...
                ],
                "serp_features": ["featured_snippet"],
                "visibility_score": 85  // 0-100
            },
            ...
        ],
        "summary": {
            "total_keywords": 50,
            "improved": 12,
            "declined": 8,
            "unchanged": 28,
            "new": 2,
            "lost": 0,
            "avg_position": 15.4,
            "visibility_score": 72
        }
    }
}
```

```
GET /api/v1/tracking/rankings/{keyword_id}/history
Description: Get detailed ranking history
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- granularity: daily|weekly|monthly

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "domain": "example.com",
        "history": [
            {
                "date": "2025-01-15",
                "position": 5,
                "ranking_url": "https://example.com/running-shoes",
                "serp_features": ["featured_snippet"],
                "competitors_above": [
                    {"domain": "competitor.com", "position": 1},
                    ...
                ]
            },
            ...
        ],
        "statistics": {
            "best_position": 3,
            "worst_position": 15,
            "average_position": 6.8,
            "position_changes": 23,
            "days_tracked": 90,
            "trend": "improving"  // improving, declining, stable
        }
    }
}
```

#### **4.2.5 Trends & Analytics API**

```
GET /api/v1/trends/keywords
Description: Get trending keywords
Authentication: Required

Query Parameters:
- country: US, UK, etc.
- category: all|shopping|sports|technology|...
- timeframe: today|week|month
- min_volume: minimum search volume
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "trending_keywords": [
            {
                "keyword": "ai chatbot",
                "search_volume": 246000,
                "volume_change_percent": 350,
                "trend_score": 95,
                "related_topics": ["artificial intelligence", "chatgpt"],
                "category": "technology"
            },
            ...
        ],
        "generated_at": "2025-01-15T10:00:00Z"
    }
}
```

```
POST /api/v1/analysis/content-gap
Description: Compare content gaps between domains
Authentication: Required
Rate Limit: 20/min

Request:
{
    "source_domain": "example.com",
    "competitor_domains": ["competitor1.com", "competitor2.com"],
    "country": "US",
    "min_volume": 1000,
    "max_difficulty": 70,
    "limit": 100
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "opportunities": [
            {
                "keyword": "best running shoes for beginners",
                "search_volume": 22000,
                "difficulty_score": 58,
                "gap_score": 85,  // 0-100 (higher = better opportunity)
                "source_position": null,  // not ranking
                "competitors": [
                    {
                        "domain": "competitor1.com",
                        "position": 3,
                        "url": "...",
                        "page_authority": 45
                    },
                    {
                        "domain": "competitor2.com",
                        "position": 7,
                        "url": "...",
                        "page_authority": 38
                    }
                ],
                "opportunity_reasons": [
                    "Competitors ranking with lower authority",
                    "High search volume with medium difficulty",
                    "Related to existing content on your site"
                ]
            },
            ...
        ],
        "summary": {
            "total_opportunities": 247,
            "high_priority": 45,
            "medium_priority": 128,
            "low_priority": 74,
            "estimated_traffic_potential": 125000
        }
    }
}
```

### 4.3 Pagination Strategy

All list endpoints use **cursor-based pagination** for performance:

```
GET /api/v1/keywords/search?page=1&limit=50

Response:
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 50,
        "total": 1247,
        "pages": 25,
        "has_next": true,
        "has_prev": false,
        "next_page": 2,
        "prev_page": null
    },
    "links": {
        "first": "/api/v1/keywords/search?page=1&limit=50",
        "last": "/api/v1/keywords/search?page=25&limit=50",
        "next": "/api/v1/keywords/search?page=2&limit=50",
        "prev": null
    }
}
```

For very large datasets (backlinks, SERP history), use **cursor pagination**:

```
GET /api/v1/domains/{domain}/backlinks?cursor=abc123&limit=100

Response:
{
    "data": [...],
    "pagination": {
        "cursor": "def456",
        "has_more": true,
        "limit": 100
    },
    "links": {
        "next": "/api/v1/domains/{domain}/backlinks?cursor=def456&limit=100"
    }
}
```

### 4.4 Filtering & Sorting

**Standard filters across endpoints:**
- `min_volume`: Minimum search volume
- `max_volume`: Maximum search volume
- `min_difficulty`: Minimum difficulty score
- `max_difficulty`: Maximum difficulty score
- `country`: Country code(s) - comma-separated
- `language`: Language code(s)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Standard sorting:**
- `sort`: Field to sort by
- `order`: asc|desc

Example:
```
GET /api/v1/keywords/search?
    keyword=shoes&
    min_volume=10000&
    max_difficulty=60&
    country=US,CA&
    sort=volume&
    order=desc&
    page=1&
    limit=50
```

### 4.5 Caching Strategy

```
Cache-Control Headers:
- Keyword data: max-age=86400 (24 hours)
- Domain overview: max-age=43200 (12 hours)
- SERP data: max-age=21600 (6 hours)
- Ranking data: max-age=3600 (1 hour)
- Trending data: max-age=600 (10 minutes)

ETag Support:
- Include ETag header in responses
- Support If-None-Match requests
- Return 304 Not Modified when appropriate

Example Response Headers:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=86400, public
ETag: "abc123def456"
X-Cache: HIT
X-Cache-Age: 3600
```

---

## 5. Crawler & Data Sources

### 5.1 Data Source Integration

#### **5.1.1 Google APIs**

**Google Ads Keyword Planner API**
```python
Purpose: Search volume, CPC, competition data
Rate Limit: 15,000 requests/day
Cost: Free with Google Ads account
Data Freshness: Updated monthly

Integration:
- OAuth 2.0 authentication
- REST API calls
- Batch requests (up to 100 keywords)
- Response caching (30 days)

Data Retrieved:
- Monthly search volume
- Competition level (low/medium/high)
- Suggested bid (CPC)
- Historical data (12 months)
- Related keywords
```

**Google Search Console API**
```python
Purpose: Verified site ranking data, clicks, impressions
Rate Limit: 1,200 requests/day
Cost: Free
Data Freshness: 2-3 days delay

Integration:
- OAuth 2.0 with Search Console verification
- Query for ranking data, impressions, clicks
- Filter by country, device, search appearance

Data Retrieved:
- Keyword rankings for verified sites
- Click-through rates
- Impressions
- Average position
```

**Google Trends API (Unofficial)**
```python
Purpose: 12-month trend data, related queries
Rate Limit: 1,500 requests/hour
Cost: Free (via pytrends library)
Data Freshness: Real-time

Integration:
- Python pytrends library
- Rotating proxies to avoid blocks
- Delayed requests (2-5 seconds)

Data Retrieved:
- Interest over time (0-100 scale)
- Related topics and queries
- Regional interest
- Rising keywords
```

#### **5.1.2 Bing Webmaster Tools API**

```python
Purpose: Alternative search data, Bing-specific metrics
Rate Limit: 5,000 requests/month
Cost: Free
Data Freshness: Daily updates

Integration:
- API key authentication
- REST API

Data Retrieved:
- Keyword rankings
- Traffic data
- Backlink data (limited)
- Page-level metrics
```

#### **5.1.3 Third-Party SEO APIs**

**DataForSEO API**
```python
Purpose: Comprehensive SERP data, backlinks, metrics
Rate Limit: Based on subscription
Cost: Pay-per-request ($0.001 - $0.02 per request)
Data Freshness: Real-time for SERP, daily for backlinks

Data Retrieved:
- SERP results with rich data
- Backlink profiles
- Keyword difficulty scores
- Domain metrics
- Historical data
```

**SEMrush API** (Alternative)
```python
Purpose: Keyword data, competition analysis
Cost: $199-$499/month + API credits
Data Retrieved:
- Keyword metrics
- Domain analytics
- Competitor analysis
- Backlink data
```

### 5.2 Headless Browser Crawling

For SERP scraping when APIs are insufficient:

```python
Technology Stack:
- Selenium with Chrome/Firefox headless
- Playwright (modern alternative, faster)
- Puppeteer (Node.js option)

Proxy Integration:
- Bright Data (Luminati) residential proxies
- Oxylabs datacenter & residential proxies
- ScraperAPI (handles proxies + CAPTCHA)

CAPTCHA Handling:
- 2Captcha API integration
- Anti-Captcha service
- Automatic retry with new proxy
- Fallback to human verification queue

User Agent Rotation:
- Random desktop user agents
- Mobile user agents for mobile SERP
- Update monthly from real browser stats
```

#### **5.2.1 SERP Crawler Implementation**

```python
# Pseudo-code for SERP crawler

class SERPCrawler:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        
    async def crawl_serp(self, keyword, country, device):
        # Select appropriate proxy
        proxy = self.proxy_manager.get_proxy(country)
        
        # Configure browser
        browser = await self.launch_browser(
            proxy=proxy,
            user_agent=self.get_user_agent(device),
            headless=True
        )
        
        try:
            # Navigate to Google search
            page = await browser.new_page()
            search_url = self.build_search_url(keyword, country)
            await page.goto(search_url, wait_until='networkidle')
            
            # Check for CAPTCHA
            if await self.detect_captcha(page):
                solved = await self.captcha_solver.solve(page)
                if not solved:
                    raise CaptchaError("Failed to solve CAPTCHA")
            
            # Extract SERP data
            serp_data = await self.extract_serp_data(page)
            
            # Take screenshot for archive
            screenshot = await page.screenshot(full_page=True)
            
            return {
                'results': serp_data,
                'screenshot': screenshot,
                'timestamp': datetime.utcnow(),
                'proxy_used': proxy.id
            }
            
        except Exception as e:
            # Mark proxy as failed
            self.proxy_manager.mark_failed(proxy)
            raise
            
        finally:
            await browser.close()
    
    async def extract_serp_data(self, page):
        # Extract organic results
        organic = await page.eval("""
            () => Array.from(document.querySelectorAll('.g')).map(el => ({
                position: Array.from(el.parentNode.children).indexOf(el) + 1,
                title: el.querySelector('h3')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.VwiC3b')?.textContent,
                rich_snippet: extractRichSnippet(el)
            }))
        """)
        
        # Extract SERP features
        featured_snippet = await page.querySelector('.ifM9O')
        people_also_ask = await page.querySelectorAll('.related-question-pair')
        local_pack = await page.querySelector('.rllt__details')
        
        # Extract paid ads
        ads = await page.eval("""
            () => Array.from(document.querySelectorAll('.uEierd')).map(el => ({
                position: 'top' + (Array.from(el.parentNode.children).indexOf(el) + 1),
                title: el.querySelector('.CCgQ5')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.MUxGbd')?.textContent
            }))
        """)
        
        return {
            'organic': organic,
            'ads': ads,
            'features': {
                'featured_snippet': featured_snippet,
                'people_also_ask': people_also_ask,
                'local_pack': local_pack
            }
        }
```

### 5.3 Crawler Scheduler

```python
# Celery beat schedule for periodic crawls

CELERYBEAT_SCHEDULE = {
    'crawl-high-priority-keywords': {
        'task': 'crawlers.tasks.crawl_keywords',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ({'priority': 'high'},)
    },
    'crawl-tracked-keywords-daily': {
        'task': 'crawlers.tasks.crawl_tracked_keywords',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'args': ({'frequency': 'daily'},)
    },
    'refresh-domain-backlinks': {
        'task': 'crawlers.tasks.refresh_backlinks',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'args': ()
    },
    'update-keyword-trends': {
        'task': 'crawlers.tasks.update_trends',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),  # Monthly
        'args': ()
    }
}
```

### 5.4 Proxy Management System

```python
class ProxyManager:
    def __init__(self):
        self.redis = Redis()
        self.proxy_pool = []
        
    def load_proxies(self):
        # Load from providers: Bright Data, Oxylabs, etc.
        proxies = [
            {'ip': '1.2.3.4:8080', 'country': 'US', 'type': 'residential'},
            {'ip': '5.6.7.8:8080', 'country': 'UK', 'type': 'datacenter'},
            ...
        ]
        self.proxy_pool = proxies
    
    def get_proxy(self, country='US', exclude_failed=True):
        # Get least recently used proxy for country
        candidates = [p for p in self.proxy_pool if p['country'] == country]
        
        if exclude_failed:
            # Filter out proxies that failed recently
            candidates = [p for p in candidates 
                         if not self.is_in_cooldown(p['ip'])]
        
        # Sort by last used time
        candidates.sort(key=lambda p: self.get_last_used(p['ip']))
        
        if not candidates:
            raise NoProxyAvailable(f"No proxies available for {country}")
        
        selected = candidates[0]
        self.mark_used(selected['ip'])
        return selected
    
    def mark_used(self, proxy_ip):
        self.redis.set(f'proxy:last_used:{proxy_ip}', time.time())
        self.redis.incr(f'proxy:usage_count:{proxy_ip}')
    
    def mark_failed(self, proxy, reason='unknown'):
        # Put proxy in cooldown for 5 minutes
        self.redis.setex(
            f'proxy:cooldown:{proxy["ip"]}',
            300,  # 5 minutes
            reason
        )
        self.redis.incr(f'proxy:failure_count:{proxy["ip"]}')
        
        # If too many failures, remove from pool
        failures = int(self.redis.get(f'proxy:failure_count:{proxy["ip"]}') or 0)
        if failures > 10:
            self.remove_proxy(proxy['ip'])
    
    def is_in_cooldown(self, proxy_ip):
        return self.redis.exists(f'proxy:cooldown:{proxy_ip}')
    
    def get_last_used(self, proxy_ip):
        return float(self.redis.get(f'proxy:last_used:{proxy_ip}') or 0)
    
    def health_check(self, proxy):
        # Test proxy connectivity
        try:
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies={'https': f'http://{proxy["ip"]}'},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    async def periodic_health_check(self):
        # Run every 5 minutes to check all proxies
        for proxy in self.proxy_pool:
            if not self.health_check(proxy):
                self.mark_failed(proxy, 'health_check_failed')
```

### 5.5 CAPTCHA Handling Strategy

```python
class CaptchaSolver:
    def __init__(self):
        self.twocaptcha_api_key = settings.TWOCAPTCHA_API_KEY
        
    async def solve(self, page, captcha_type='recaptcha_v2'):
        if captcha_type == 'recaptcha_v2':
            return await self.solve_recaptcha_v2(page)
        elif captcha_type == 'recaptcha_v3':
            return await self.solve_recaptcha_v3(page)
        elif captcha_type == 'image':
            return await self.solve_image_captcha(page)
    
    async def solve_recaptcha_v2(self, page):
        # Extract site key
        site_key = await page.evaluate("""
            () => document.querySelector('[data-sitekey]')?.getAttribute('data-sitekey')
        """)
        
        if not site_key:
            return False
        
        # Send to 2Captcha service
        task_id = self.create_captcha_task(
            site_key=site_key,
            page_url=page.url
        )
        
        # Wait for solution (can take 30-60 seconds)
        solution = self.wait_for_solution(task_id, timeout=120)
        
        if solution:
            # Inject solution into page
            await page.evaluate(f"""
                {% raw %}
                () => {{
                    document.getElementById('g-recaptcha-response').innerHTML = '{solution}';
                    document.querySelector('form').submit();
                }}{% endraw %}
                "
            """)
            return True
        
        return False
    
    def create_captcha_task(self, site_key, page_url):
        response = requests.post(
            'https://2captcha.com/in.php',
            data={
                'key': self.twocaptcha_api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
        )
        return response.json()['request']
    
    def wait_for_solution(self, task_id, timeout=120):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(
                'https://2captcha.com/res.php',
                params={
                    'key': self.twocaptcha_api_key,
                    'action': 'get',
                    'id': task_id,
                    'json': 1
                }
            )
            result = response.json()
            
            if result['status'] == 1:
                return result['request']
            
            time.sleep(5)
        
        return None
```

---

## 6. Ranking & Analytics Engine

### 6.1 Keyword Difficulty Algorithm

```python
def calculate_keyword_difficulty(keyword_data, serp_data):
    """
    Calculate keyword difficulty score (0-100)
    Higher = more difficult to rank
    
    Factors:
    1. Competition level from Google Ads (weight: 20%)
    2. Domain authority of top 10 results (weight: 40%)
    3. Backlink profile of top 10 (weight: 30%)
    4. SERP features present (weight: 10%)
    """
    
    # Factor 1: Competition level
    competition_score = keyword_data['competition'] * 100  # 0-100
    
    # Factor 2: Domain authority
    top_10_domains = serp_data['organic_results'][:10]
    avg_domain_authority = sum(d['domain_authority'] for d in top_10_domains) / 10
    
    # Factor 3: Backlinks
    avg_backlinks = sum(d['backlinks_count'] for d in top_10_domains) / 10
    backlink_score = min(100, (avg_backlinks / 1000) * 100)  # Normalize
    
    # Factor 4: SERP features
    serp_features_count = len(serp_data['serp_features'])
    serp_feature_score = min(100, serp_features_count * 15)
    
    # Weighted calculation
    difficulty = (
        competition_score * 0.20 +
        avg_domain_authority * 0.40 +
        backlink_score * 0.30 +
        serp_feature_score * 0.10
    )
    
    return round(difficulty, 2)
```

### 6.2 Opportunity Score Algorithm

```python
def calculate_opportunity_score(keyword_data, serp_data, user_domain_data):
    """
    Calculate opportunity score (0-100)
    Higher = better opportunity for ranking
    
    Factors:
    1. Search volume (high volume = more opportunity)
    2. Low difficulty (easier to rank)
    3. Low competition from strong domains
    4. User's domain strength relative to competitors
    5. Traffic value (CPC * volume)
    6. Trend direction (rising = more opportunity)
    """
    
    # Factor 1: Search volume score
    volume = keyword_data['search_volume']
    volume_score = min(100, (volume / 100000) * 100)  # Normalize to 100k
    
    # Factor 2: Difficulty score (inverse)
    difficulty = keyword_data['difficulty_score']
    difficulty_score = 100 - difficulty
    
    # Factor 3: Competition gap
    user_authority = user_domain_data['domain_authority']
    avg_competitor_authority = sum(
        d['domain_authority'] for d in serp_data['organic_results'][:10]
    ) / 10
    
    authority_gap = avg_competitor_authority - user_authority
    competition_score = max(0, 100 - authority_gap)
    
    # Factor 4: Traffic value
    traffic_value = keyword_data['cpc_avg'] * volume
    value_score = min(100, (traffic_value / 10000) * 100)
    
    # Factor 5: Trend score
    trend = keyword_data.get('trend_direction', 'stable')
    trend_score = {
        'rising': 100,
        'stable': 50,
        'declining': 20
    }.get(trend, 50)
    
    # Weighted calculation
    opportunity = (
        volume_score * 0.25 +
        difficulty_score * 0.30 +
        competition_score * 0.25 +
        value_score * 0.10 +
        trend_score * 0.10
    )
    
    return round(opportunity, 2)
```

### 6.3 Domain Authority Algorithm

```python
def calculate_domain_authority(domain_data):
    """
    Calculate domain authority (0-100)
    Similar to Moz's DA or Ahrefs DR
    
    Factors:
    1. Total backlinks (log scale)
    2. Unique referring domains (log scale)
    3. Quality of referring domains
    4. Link velocity (new vs lost)
    5. Organic traffic estimate
    6. Number of ranking keywords
    """
    
    # Factor 1: Total backlinks (log scale for diminishing returns)
    backlinks = domain_data['total_backlinks']
    backlink_score = min(100, math.log10(backlinks + 1) * 20)
    
    # Factor 2: Unique referring domains
    referring_domains = domain_data['unique_referring_domains']
    referring_score = min(100, math.log10(referring_domains + 1) * 25)
    
    # Factor 3: Quality of backlinks (avg authority of referring domains)
    avg_referring_authority = domain_data['avg_referring_domain_authority']
    quality_score = avg_referring_authority
    
    # Factor 4: Link velocity
    new_links_month = domain_data['new_backlinks_last_month']
    lost_links_month = domain_data['lost_backlinks_last_month']
    velocity = (new_links_month - lost_links_month) / max(1, backlinks) * 100
    velocity_score = min(100, max(0, 50 + velocity * 10))
    
    # Factor 5: Organic traffic
    organic_traffic = domain_data['organic_traffic_estimate']
    traffic_score = min(100, math.log10(organic_traffic + 1) * 15)
    
    # Factor 6: Ranking keywords
    ranking_keywords = domain_data['organic_keywords_count']
    keyword_score = min(100, math.log10(ranking_keywords + 1) * 20)
    
    # Weighted calculation
    authority = (
        backlink_score * 0.25 +
        referring_score * 0.30 +
        quality_score * 0.20 +
        velocity_score * 0.05 +
        traffic_score * 0.10 +
        keyword_score * 0.10
    )
    
    return round(authority, 2)
```

### 6.4 Trend Analysis Engine

```python
class TrendAnalyzer:
    def analyze_keyword_trend(self, historical_data):
        """
        Analyze 12-month trend data
        Returns: trend_direction, trend_strength, seasonality
        """
        
        # Extract monthly values
        months = sorted(historical_data.keys())
        values = [historical_data[m] for m in months]
        
        # Calculate linear regression
        slope, intercept = self.linear_regression(range(len(values)), values)
        
        # Determine trend direction
        if slope > 5:
            direction = 'rising'
        elif slope < -5:
            direction = 'declining'
        else:
            direction = 'stable'
        
        # Calculate trend strength (0-100)
        strength = min(100, abs(slope) * 2)
        
        # Detect seasonality
        seasonality = self.detect_seasonality(values)
        
        # Calculate volatility
        volatility = np.std(values) / np.mean(values) * 100
        
        return {
            'direction': direction,
            'strength': strength,
            'seasonality': seasonality,
            'volatility': volatility,
            'forecast_next_month': intercept + slope * len(values)
        }
    
    def detect_seasonality(self, values):
        """
        Detect seasonal patterns (monthly, quarterly, annual)
        """
        if len(values) < 12:
            return None
        
        # Check for quarterly pattern
        q1_avg = np.mean(values[0:3] + values[3:6] + values[6:9] + values[9:12])
        # ... more complex seasonality detection
        
        return {
            'has_seasonality': True,
            'pattern': 'quarterly',
            'peak_months': [6, 7, 8]  # Summer peak
        }
    
    def linear_regression(self, x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
```

### 6.5 Content Gap Analysis Algorithm

```python
def analyze_content_gap(source_domain, competitor_domains, filters):
    """
    Find keyword opportunities where competitors rank but source doesn't
    """
    
    # Get all keywords competitors rank for
    competitor_keywords = set()
    for competitor in competitor_domains:
        keywords = fetch_competitor_keywords(competitor, filters)
        competitor_keywords.update(keywords)
    
    # Get keywords source domain ranks for
    source_keywords = set(fetch_domain_keywords(source_domain))
    
    # Find gaps (keywords only competitors have)
    gap_keywords = competitor_keywords - source_keywords
    
    # Score each gap keyword
    opportunities = []
    for keyword in gap_keywords:
        # Get keyword data
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        # Calculate scores
        difficulty = calculate_keyword_difficulty(keyword_data, serp_data)
        opportunity = calculate_opportunity_score(
            keyword_data, 
            serp_data,
            fetch_domain_data(source_domain)
        )
        
        # Calculate gap score
        # Higher when multiple competitors rank highly
        competitor_positions = [
            pos for comp in competitor_domains 
            for pos in get_keyword_position(comp, keyword)
            if pos
        ]
        
        if competitor_positions:
            avg_competitor_position = sum(competitor_positions) / len(competitor_positions)
            gap_score = (
                opportunity * 0.5 +
                (100 - difficulty) * 0.3 +
                (100 - avg_competitor_position * 10) * 0.2
            )
        else:
            gap_score = 0
        
        opportunities.append({
            'keyword': keyword,
            'difficulty': difficulty,
            'opportunity': opportunity,
            'gap_score': gap_score,
            'competitor_positions': competitor_positions,
            'volume': keyword_data['search_volume'],
            'cpc': keyword_data['cpc_avg']
        })
    
    # Sort by gap score
    opportunities.sort(key=lambda x: x['gap_score'], reverse=True)
    
    return opportunities
```

### 6.6 Machine Learning for Keyword Clustering

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class KeywordClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def cluster_keywords(self, keywords, n_clusters=10):
        """
        Group similar keywords into topic clusters
        """
        
        # Vectorize keywords using TF-IDF
        keyword_texts = [kw['keyword'] for kw in keywords]
        tfidf_matrix = self.vectorizer.fit_transform(keyword_texts)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Reduce dimensionality for visualization
        pca = PCA(n_components=2)
        coords = pca.fit_transform(tfidf_matrix.toarray())
        
        # Group keywords by cluster
        clusters = {}
        for i, keyword in enumerate(keywords):
            cluster_id = cluster_labels[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'keywords': [],
                    'total_volume': 0,
                    'avg_difficulty': 0,
                    'center': coords[i].tolist()
                }
            
            clusters[cluster_id]['keywords'].append(keyword)
            clusters[cluster_id]['total_volume'] += keyword['search_volume']
        
        # Calculate cluster statistics and labels
        for cluster_id, cluster_data in clusters.items():
            keywords_in_cluster = cluster_data['keywords']
            
            # Calculate average difficulty
            cluster_data['avg_difficulty'] = sum(
                kw['difficulty_score'] for kw in keywords_in_cluster
            ) / len(keywords_in_cluster)
            
            # Generate cluster label (most common terms)
            cluster_label = self.generate_cluster_label(
                [kw['keyword'] for kw in keywords_in_cluster]
            )
            cluster_data['label'] = cluster_label
        
        return clusters
    
    def generate_cluster_label(self, keywords):
        # Extract most common words
        word_freq = {}
        for keyword in keywords:
            for word in keyword.split():
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 2-3 words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        return ' '.join(word for word, _ in top_words)
```

### 6.7 Predictive Analytics

```python
class RankingPredictor:
    def predict_ranking_potential(self, target_url, keyword, current_ranking):
        """
        Predict likelihood of ranking improvement
        Uses historical data and ML model
        """
        
        # Extract features
        features = self.extract_features(target_url, keyword, current_ranking)
        
        # Load trained model (e.g., Random Forest or XGBoost)
        model = self.load_model()
        
        # Predict probability of improvement
        prediction = model.predict_proba([features])[0]
        
        # Estimate time to rank in top 10
        estimated_days = self.estimate_time_to_rank(features, prediction)
        
        return {
            'probability_top_10': prediction[1],
            'probability_top_3': prediction[2] if len(prediction) > 2 else 0,
            'estimated_days_to_top_10': estimated_days,
            'confidence': self.calculate_confidence(features),
            'recommended_actions': self.generate_recommendations(features)
        }
    
    def extract_features(self, target_url, keyword, current_ranking):
        page_data = fetch_page_data(target_url)
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        return {
            'current_position': current_ranking or 100,
            'page_authority': page_data['page_authority'],
            'domain_authority': page_data['domain_authority'],
            'backlinks_count': page_data['backlinks_count'],
            'content_length': page_data['content_length'],
            'keyword_density': page_data['keyword_density'],
            'keyword_difficulty': keyword_data['difficulty_score'],
            'search_volume': keyword_data['search_volume'],
            'avg_competitor_authority': serp_data['avg_domain_authority'],
            'serp_features_count': len(serp_data['serp_features']),
            'has_featured_snippet': 'featured_snippet' in serp_data['serp_features']
        }
    
    def generate_recommendations(self, features):
        recommendations = []
        
        if features['content_length'] < 1500:
            recommendations.append({
                'priority': 'high',
                'action': 'Increase content length',
                'details': f'Current: {features["content_length"]} words. Target: 2000+ words',
                'impact': 'medium'
            })
        
        if features['backlinks_count'] < 50:
            recommendations.append({
                'priority': 'high',
                'action': 'Build more backlinks',
                'details': f'Current: {features["backlinks_count"]}. Target: 100+ backlinks',
                'impact': 'high'
            })
        
        if features['keyword_density'] < 0.5:
            recommendations.append({
                'priority': 'medium',
                'action': 'Optimize keyword usage',
                'details': 'Include target keyword more naturally in content',
                'impact': 'low'
            })
        
        return recommendations
```

---

## 7. User System

### 7.1 Authentication & Authorization

```python
# JWT token structure
{
    "user_id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": ["keyword_search", "domain_analysis", "rank_tracking"],
    "iat": 1705320000,
    "exp": 1705406400  # 24 hour expiry
}

# API Key structure
{
    "key_id": "ak_live_abc123xyz789",
    "user_id": 12345,
    "name": "Production API Key",
    "permissions": ["keyword_search", "serp_analysis"],
    "rate_limit": 500,  # requests per minute
    "created_at": "2025-01-01T00:00:00Z",
    "last_used_at": "2025-01-15T10:30:00Z"
}
```

### 7.2 Subscription Plans

```yaml
Plans:
  Free:
    price: $0/month
    features:
      keyword_searches: 10/day
      domain_analyses: 3/day
      serp_checks: 10/day
      tracked_keywords: 0
      historical_data: 7 days
      api_access: false
      export: false
      team_members: 1
      
  Pro:
    price: $99/month
    features:
      keyword_searches: 100/day (3000/month)
      domain_analyses: 50/day
      serp_checks: 100/day
      tracked_keywords: 500
      rank_checks_frequency: daily
      historical_data: 90 days
      api_access: true
      api_calls: 10,000/month
      export: true (CSV, Excel)
      team_members: 3
      reports: 10/month
      
  Agency:
    price: $299/month
    features:
      keyword_searches: unlimited
      domain_analyses: unlimited
      serp_checks: unlimited
      tracked_keywords: 5000
      rank_checks_frequency: daily
      historical_data: 2 years
      api_access: true
      api_calls: 100,000/month
      export: true (CSV, Excel, API)
      team_members: 10
      reports: unlimited
      white_label: true
      priority_support: true
      
  Enterprise:
    price: Custom
    features:
      everything_unlimited: true
      dedicated_account_manager: true
      custom_integrations: true
      on_premise_option: true
      sla_guarantee: 99.9%
```

### 7.3 Quota Management

```python
class QuotaManager:
    def check_quota(self, user_id, action_type):
        """
        Check if user has quota remaining for action
        Returns: (allowed: bool, remaining: int, reset_at: datetime)
        """
        
        # Get user plan
        user = fetch_user(user_id)
        plan = PLANS[user.plan_type]
        
        # Get quota limits
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        quota_used = redis.get(quota_key) or 0
        quota_limit = plan['features'][f'{action_type}']
        
        # Check if unlimited
        if quota_limit == 'unlimited':
            return (True, -1, None)
        
        # Check limit
        allowed = int(quota_used) < int(quota_limit)
        remaining = max(0, int(quota_limit) - int(quota_used))
        reset_at = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        
        return (allowed, remaining, reset_at)
    
    def consume_quota(self, user_id, action_type, amount=1):
        """
        Consume quota for action
        """
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        
        # Increment usage
        new_usage = redis.incr(quota_key, amount)
        
        # Set expiry to end of day if first use
        if new_usage == amount:
            redis.expireat(quota_key, datetime.combine(
                date.today() + timedelta(days=1),
                datetime.min.time()
            ))
        
        # Log usage
        log_quota_usage(user_id, action_type, amount)
        
        return new_usage
```

### 7.4 Role-Based Access Control (RBAC)

```python
ROLES = {
    'owner': {
        'permissions': [
            'manage_project',
            'manage_team',
            'view_billing',
            'manage_billing',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'admin': {
        'permissions': [
            'manage_team',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'editor': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data'
        ]
    },
    'viewer': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'view_rankings'
        ]
    }
}

def check_permission(user_id, project_id, permission):
    # Get user's role in project
    membership = fetch_project_membership(user_id, project_id)
    
    if not membership:
        return False
    
    # Check if role has permission
    role_permissions = ROLES[membership.role]['permissions']
    return permission in role_permissions
```

---

## 8. Dashboard & UI Modules

### 8.1 Dashboard Components

#### **8.1.1 Keyword Explorer Module**

```
Components:
├── Search Bar
│   ├── Keyword input with autocomplete
│   ├── Country selector (dropdown with flags)
│   ├── Language selector
│   └── Device type selector (desktop/mobile/tablet)
│
├── Results Table
│   ├── Columns: Keyword, Volume, CPC, Competition, Difficulty, Trend
│   ├── Sortable columns
│   ├── Filterable (volume range, difficulty range)
│   ├── Bulk select for export
│   └── Add to project button
│
├── Keyword Details Panel (expandable row)
│   ├── 12-month trend chart
│   ├── Related keywords list
│   ├── Question keywords
│   ├── SERP features present
│   └── Top 10 ranking URLs
│
└── Sidebar Filters
    ├── Search volume range slider
    ├── Difficulty range slider
    ├── Competition level checkboxes
    ├── SERP features filters
    └── Keyword intent filters (informational, commercial, transactional)

Features:
- Real-time search with debounce (300ms)
- Export to CSV/Excel
- Save search history
- Favorite keywords
- Bulk keyword upload (CSV)
```

#### **8.1.2 Domain Overview Module**

```
Layout:
┌─────────────────────────────────────────────────────────────┐
│ Domain Input & Analysis                                      │
│ [example.com                              ] [Analyze]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Authority: 75│ Backlinks:   │ Org Keywords:│ Est. Traffic:│
│              │ 125,847      │ 45,231       │ 850,000/mo   │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Traffic Trend (Last 12 Months) - Line Chart                 │
│ [Interactive chart showing organic traffic over time]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Top Organic Keywords         │ Top Pages                     │
│ [Sortable table]             │ [Sortable table]              │
│ - Keyword                    │ - URL                         │
│ - Position                   │ - Traffic                     │
│ - Volume                     │ - Keywords                    │
│ - Traffic                    │ - Backlinks                   │
└──────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Backlink Growth              │ Competitors                   │
│ [Area chart]                 │ [List with metrics]           │
│ New vs Lost backlinks        │ - Domain                      │
│                              │ - Authority                   │
│                              │ - Keyword Overlap             │
└──────────────────────────────┴──────────────────────────────┘

Tabs:
- Overview
- Organic Keywords
- Top Pages
- Backlinks
- Competitors
- Historical Data
```

#### **8.1.3 SERP Overview Module**

```
Components:
├── SERP Search
│   ├── Keyword input
│   ├── Location selector (with map)
│   ├── Device type tabs
│   └── Analyze button
│
├── SERP Preview
│   ├── Visual SERP representation
│   ├── Organic results (1-100)
│   ├── Paid ads highlighted
│   ├── SERP features marked
│   └── Each result expandable for details
│
├── SERP Analysis
│   ├── Difficulty score gauge
│   ├── Opportunity score gauge
│   ├── Avg domain authority
│   ├── Avg backlinks
│   ├── Content length avg
│   └── SERP features breakdown
│
├── Competitor Analysis Table
│   )
    device: constr(regex='^(desktop|mobile|tablet)# 🎯 Keyword Research & SEO Analysis Platform
## Complete System Design Document

> **Version:** 1.0  
> **Architecture Type:** Microservices with Event-Driven Components  
> **Scale Target:** 10M+ keywords, 1M+ domains, 100K+ concurrent users

---

## 📋 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Flow & Processing](#2-data-flow--processing)
3. [Database Design](#3-database-design)
4. [API Layer Design](#4-api-layer-design)
5. [Crawler & Data Sources](#5-crawler--data-sources)
6. [Ranking & Analytics Engine](#6-ranking--analytics-engine)
7. [User System](#7-user-system)
8. [Dashboard & UI Modules](#8-dashboard--ui-modules)
9. [Scalability, Performance & Security](#9-scalability-performance--security)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Architecture Overview

### 1.1 System Architecture Pattern

**Hybrid Microservices Architecture** with the following characteristics:
- Core services as independent microservices
- Shared data access layer for performance
- Event-driven communication for async operations
- API Gateway for unified access point

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  [Web Dashboard] [Mobile App] [Browser Extension] [API Clients] │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CDN LAYER (CloudFlare)                      │
│              [Static Assets] [API Response Cache]                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Kong/AWS ALB)                    │
│    [Rate Limiting] [Auth] [Routing] [Request Validation]        │
└─────┬───────────┬──────────┬──────────┬────────────┬───────────┘
      │           │          │          │            │
┌─────▼─────┐ ┌──▼────┐ ┌───▼─────┐ ┌─▼────┐ ┌────▼──────┐
│  Auth     │ │Keyword│ │ Domain  │ │SERP  │ │ Tracking  │
│  Service  │ │Service│ │ Service │ │Svc   │ │  Service  │
└─────┬─────┘ └──┬────┘ └───┬─────┘ └─┬────┘ └────┬──────┘
      │          │          │          │            │
┌─────▼──────────▼──────────▼──────────▼────────────▼───────────┐
│                   MESSAGE QUEUE (RabbitMQ/Kafka)               │
│  [Crawl Jobs] [Data Processing] [Analytics] [Notifications]   │
└──────┬────────────────┬────────────────┬─────────────┬────────┘
       │                │                │             │
┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐ ┌───▼─────┐
│   Crawler   │  │  Analytics  │  │   Email    │ │ Report  │
│   Workers   │  │   Engine    │  │  Service   │ │ Builder │
└──────┬──────┘  └──────┬──────┘  └─────┬──────┘ └───┬─────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                      DATA STORAGE LAYER                        │
│ [PostgreSQL] [MongoDB] [Redis] [Elasticsearch] [S3/Object]    │
└────────────────────────────────────────────────────────────────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                   EXTERNAL INTEGRATIONS                        │
│ [Google APIs] [Bing APIs] [Third-party SEO] [Proxy Services]  │
└────────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components Breakdown

#### **1.3.1 Frontend Layer**
- **Web Dashboard**: React/Next.js with SSR for SEO
- **Mobile Apps**: React Native for iOS/Android
- **Browser Extension**: Chrome/Firefox for on-page analysis
- **Component Library**: Shared UI components (charts, tables, forms)

#### **1.3.2 API Gateway**
- **Technology**: Kong API Gateway or AWS Application Load Balancer
- **Responsibilities**:
  - Request routing to microservices
  - Authentication token validation
  - Rate limiting and throttling
  - Request/response transformation
  - API versioning (v1, v2)
  - Logging and monitoring

#### **1.3.3 Microservices**

**Auth Service**
- User authentication and authorization
- JWT token management
- OAuth integration (Google, Facebook)
- API key generation and validation
- Session management

**Keyword Service**
- Keyword search and suggestions
- Keyword metrics (volume, CPC, competition)
- Related keywords and questions
- Keyword difficulty calculation
- Multi-language support

**Domain Service**
- Domain overview and metrics
- Backlink analysis
- Top pages analysis
- Organic keyword tracking
- Domain authority calculation

**SERP Service**
- SERP position tracking
- Featured snippets detection
- Local pack results
- Ads analysis
- SERP feature identification

**Tracking Service**
- Keyword rank tracking
- Position monitoring
- Ranking history
- Competitor tracking
- Alert system for rank changes

**Analytics Engine**
- Trend analysis
- Opportunity scoring
- Content gap analysis
- Competitive intelligence
- Predictive analytics

**Crawler Service**
- Distributed web crawler
- SERP scraping
- Backlink discovery
- Site auditing
- Content extraction

**Report Builder**
- PDF report generation
- Scheduled reports
- White-label reports
- Data export (CSV, Excel)

#### **1.3.4 Data Storage Components**

**PostgreSQL** (Primary Relational Database)
- User accounts and subscriptions
- Projects and settings
- Normalized keyword and domain data
- Transactional data

**MongoDB** (Document Store)
- Raw crawl data
- SERP snapshots
- Historical data
- Flexible schema data

**Redis** (Caching Layer)
- Session cache
- API response cache
- Real-time ranking cache
- Queue management
- Rate limiting counters

**Elasticsearch**
- Full-text keyword search
- Log aggregation and search
- Analytics queries
- Real-time suggestions

**S3/Object Storage**
- Backlink data archives
- Historical SERP screenshots
- Report files
- User uploads

### 1.4 Technology Stack Recommendation

#### **Backend Stack**
```
Language: Python 3.11+ (Primary), Node.js (Real-time services)
Frameworks: 
  - FastAPI (API services) - High performance, async
  - Django (Admin panel, complex business logic)
  - Express.js (Real-time notifications)
  
Task Queue: Celery with RabbitMQ or AWS SQS
Background Workers: Celery workers (CPU-intensive), Node workers (I/O)
Caching: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+
Message Broker: RabbitMQ or Apache Kafka (for high throughput)
```

#### **Frontend Stack**
```
Framework: Next.js 14+ (React with SSR/SSG)
State Management: Zustand or Redux Toolkit
UI Library: TailwindCSS + shadcn/ui components
Charts: Recharts or Apache ECharts
Data Tables: TanStack Table
Forms: React Hook Form + Zod validation
API Client: Axios with React Query for caching
```

#### **Database Stack**
```
Primary: PostgreSQL 15+ with Citus extension (for sharding)
Document: MongoDB 6+ with replica sets
Cache: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+ with ILM policies
Time-series: TimescaleDB (extension on PostgreSQL) for tracking data
```

#### **Infrastructure**
```
Container: Docker + Docker Compose (dev), Kubernetes (production)
Orchestration: Kubernetes (EKS/GKE) or AWS ECS
CI/CD: GitHub Actions or GitLab CI
Monitoring: Prometheus + Grafana, ELK Stack
APM: New Relic or Datadog
Error Tracking: Sentry
```

#### **External Services**
```
CDN: CloudFlare Enterprise
Email: SendGrid or AWS SES
Payment: Stripe
Analytics: Mixpanel, Google Analytics 4
Search APIs: Google Custom Search API, Bing Web Search API
Proxy Services: ScraperAPI, Bright Data, Oxylabs
```

### 1.5 Scalability Strategy

#### **Horizontal Scaling**
- All services stateless for easy replication
- Auto-scaling based on CPU/memory/queue depth
- Load balancers distribute traffic across instances
- Database read replicas for query distribution

#### **Caching Strategy**

**L1 Cache (Application Level)**
- In-memory caching in each service instance
- LRU cache with 5-minute TTL for hot data
- Size limit: 512MB per instance

**L2 Cache (Redis)**
```
Keyword Metrics: TTL 24 hours
Domain Overview: TTL 12 hours  
SERP Results: TTL 6 hours
User Sessions: TTL 30 minutes
API Responses: TTL based on data freshness
Rate Limiting: Real-time, no TTL
```

**L3 Cache (CDN)**
- Static assets: 1 year cache
- API responses: 5 minutes cache with stale-while-revalidate
- Images and fonts: 6 months cache

#### **Database Sharding Strategy**

**PostgreSQL Sharding** (using Citus)
```
Shard Key: domain_hash (for domain data)
Shard Key: keyword_hash (for keyword data)
Shard Key: user_id (for user data)

Distribution:
- 32 shards for keyword data (hash distribution)
- 16 shards for domain data
- 8 shards for user/project data
```

**MongoDB Sharding**
```
Shard Key: {country: 1, language: 1, keyword_hash: 1}
Zones: US, EU, ASIA for geographic distribution
Chunk Size: 64MB
```

### 1.6 Queue and Worker Setup

#### **Task Queue Architecture**

```
┌─────────────────────────────────────────────────────┐
│                  TASK PRODUCERS                      │
│  [API Services] [Scheduled Jobs] [User Actions]     │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│              MESSAGE BROKER (RabbitMQ)              │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ crawl_queue  │  │ analytics_q  │  │ email_q  │ │
│  │ Priority: 1  │  │ Priority: 2  │  │Priority:3│ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└──┬──────────┬──────────────┬────────────┬─────────┘
   │          │              │            │
┌──▼────┐ ┌──▼────┐  ┌──────▼─────┐  ┌──▼──────┐
│Crawler│ │SERP   │  │ Analytics  │  │  Email  │
│Worker │ │Worker │  │  Worker    │  │ Worker  │
│x20    │ │x10    │  │  x5        │  │  x3     │
└───────┘ └───────┘  └────────────┘  └─────────┘
```

#### **Worker Types and Configuration**

**1. Crawler Workers** (CPU + Network intensive)
```
Count: 20-50 workers (auto-scale)
Resources: 2 CPU, 4GB RAM per worker
Tasks:
  - SERP crawling (priority: high)
  - Backlink discovery (priority: medium)
  - Site auditing (priority: low)
  - Content extraction
Max Concurrency: 5 tasks per worker
Retry Strategy: Exponential backoff (max 3 retries)
Timeout: 60 seconds per task
```

**2. Analytics Workers** (CPU intensive)
```
Count: 5-10 workers
Resources: 4 CPU, 8GB RAM per worker
Tasks:
  - Keyword difficulty calculation
  - Domain authority scoring
  - Trend analysis
  - Content gap analysis
  - Opportunity scoring
Max Concurrency: 3 tasks per worker
Timeout: 120 seconds per task
```

**3. Data Processing Workers** (Memory intensive)
```
Count: 10-20 workers
Resources: 2 CPU, 8GB RAM per worker
Tasks:
  - Bulk data import
  - Data enrichment
  - Metric aggregation
  - Historical data processing
Max Concurrency: 2 tasks per worker
Batch Size: 1000 records per batch
```

**4. Notification Workers** (I/O intensive)
```
Count: 3-5 workers
Resources: 1 CPU, 2GB RAM per worker
Tasks:
  - Email notifications
  - Webhook delivery
  - Report generation
  - Alert processing
Max Concurrency: 10 tasks per worker
Timeout: 30 seconds per task
```

#### **Queue Priority System**
```
Priority 1 (Highest): Real-time user requests
Priority 2 (High): Scheduled tracking updates
Priority 3 (Medium): Background data refresh
Priority 4 (Low): Bulk data processing
Priority 5 (Lowest): Analytics and reports
```

---

## 2. Data Flow & Processing

### 2.1 Primary Workflows

#### **2.1.1 Keyword Research Workflow**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: User Input                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ User enters: "best running shoes"                       │ │
│ │ Filters: Country=US, Language=EN, Device=Desktop        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 2: Request Processing (API Gateway)                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ • Validate JWT token                                     │ │
│ │ • Check rate limits (100 req/min for Pro plan)          │ │
│ │ • Normalize keyword (lowercase, trim)                   │ │
│ │ • Generate cache key: "kw:en:us:desktop:best_running..."│ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 3: Cache Lookup (Redis L2 Cache)                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GET cache_key                                            │ │
│ │ TTL: 24 hours                                            │ │
│ │                                                          │ │
│ │ IF FOUND → Return cached response (80% of requests)     │ │
│ │ IF NOT FOUND → Continue to Step 4                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Cache Miss)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 4: Database Query (PostgreSQL + Elasticsearch)         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Query keywords table:                                    │ │
│ │   SELECT * FROM keywords                                 │ │
│ │   WHERE keyword_normalized = 'best running shoes'        │ │
│ │   AND country = 'US' AND language = 'EN'                │ │
│ │                                                          │ │
│ │ IF FOUND and data_age < 30 days:                        │ │
│ │   → Return from database                                │ │
│ │   → Update cache                                        │ │
│ │ IF NOT FOUND or data_age > 30 days:                     │ │
│ │   → Continue to Step 5 (Fresh Data Fetch)               │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Database Miss or Stale)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 5: External Data Fetch (Async Job)                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Publish job to RabbitMQ: "crawl_queue"                  │ │
│ │ {                                                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "keyword": "best running shoes",                      │ │
│ │   "country": "US",                                      │ │
│ │   "sources": ["google_api", "serp_scraper"],           │ │
│ │   "priority": "high"                                    │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Return immediate response to user:                      │ │
│ │ {                                                        │ │
│ │   "status": "processing",                               │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "estimated_time": "10-30 seconds",                   │ │
│ │   "partial_data": { ... } ← if available               │ │
│ │ }                                                        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 6: Crawler Worker Processing                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Worker picks up job from queue                          │ │
│ │                                                          │ │
│ │ Parallel data fetching (asyncio):                       │ │
│ │ ┌─────────────┐  ┌─────────────┐  ┌──────────────┐    │ │
│ │ │ Google Ads  │  │ Google      │  │ Third-party  │    │ │
│ │ │ Keyword API │  │ Trends API  │  │ SEO API      │    │ │
│ │ │ (volume,CPC)│  │ (12mo trend)│  │ (difficulty) │    │ │
│ │ └─────────────┘  └─────────────┘  └──────────────┘    │ │
│ │                                                          │ │
│ │ Data aggregation and enrichment:                        │ │
│ │ • Calculate average from multiple sources               │ │
│ │ • Compute keyword difficulty score                      │ │
│ │ • Generate related keywords                             │ │
│ │ • Extract questions and suggestions                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 7: Data Storage                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ PostgreSQL:                                              │ │
│ │   INSERT INTO keywords (keyword, country, language, ...) │ │
│ │   INSERT INTO keyword_metrics (keyword_id, volume, ...)  │ │
│ │   INSERT INTO keyword_trends (keyword_id, month, ...)    │ │
│ │                                                          │ │
│ │ Elasticsearch:                                           │ │
│ │   Index document for fast search and suggestions        │ │
│ │                                                          │ │
│ │ Redis Cache:                                             │ │
│ │   SET cache_key = {data} EX 86400 (24 hours)           │ │
│ │                                                          │ │
│ │ MongoDB (Raw Data Archive):                              │ │
│ │   Store original API responses for audit trail          │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 8: WebSocket Notification                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Push update to user's active session:                   │ │
│ │ {                                                        │ │
│ │   "event": "keyword_data_ready",                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "data": { full keyword metrics }                      │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Frontend updates UI with full data                      │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

#### **2.1.2 Domain Analysis Workflow**

```
User Input: "example.com"
    ↓
1. Domain Validation & Normalization
   • Check DNS resolution
   • Normalize to canonical form
   • Extract domain metadata
    ↓
2. Cache Check (Redis)
   • Key: "domain:example.com:overview"
   • TTL: 12 hours
   IF FOUND → Return cached data
    ↓
3. Database Lookup (PostgreSQL)
   • Check domains table
   • Check domain_metrics table
   • If data < 7 days old → Return
    ↓
4. Trigger Async Jobs (if needed)
   Job 1: Backlink Crawler
     → Crawl backlink sources
     → Discover new backlinks
     → Update backlink database
   
   Job 2: Organic Keyword Scraper
     → Fetch ranking keywords
     → Update keyword positions
     → Calculate traffic estimates
   
   Job 3: Top Pages Analyzer
     → Crawl sitemap
     → Analyze top-performing pages
     → Calculate page metrics
   
   Job 4: Domain Authority Calculator
     → Aggregate backlink data
     → Apply authority algorithm
     → Update domain score
    ↓
5. Data Aggregation
   • Combine all metrics
   • Calculate derived values
   • Generate summary stats
    ↓
6. Storage & Cache Update
   • Update PostgreSQL
   • Refresh Redis cache
   • Index in Elasticsearch
    ↓
7. Return Response
   • Domain overview
   • Top metrics
   • Recent changes
   • Recommendations
```

#### **2.1.3 SERP Analysis Workflow**

```
User Input: Keyword + Location
    ↓
1. SERP Fetch Request
   • Generate SERP cache key
   • Check Redis (TTL: 6 hours)
    ↓
2. Cache Miss → Trigger Crawler
   Job: SERP Scraper
     → Use rotating proxies
     → Fetch Google SERP page
     → Extract organic results
     → Extract paid ads
     → Extract SERP features
     → Handle CAPTCHA if needed
    ↓
3. SERP Data Processing
   • Parse HTML/JSON
   • Extract result URLs
   • Identify result types
   • Calculate positions
   • Detect SERP features
    ↓
4. Domain Enrichment
   For each result URL:
     → Lookup domain metrics
     → Calculate domain strength
     → Fetch page metrics
     → Analyze content
    ↓
5. Competitive Analysis
   • Compare domain authorities
   • Analyze content gaps
   • Calculate difficulty score
   • Generate insights
    ↓
6. Storage
   • PostgreSQL: serp_results table
   • MongoDB: Raw SERP snapshots
   • Redis: Cached response
    ↓
7. Return Enriched SERP Data
```

### 2.2 Data Pipeline Architecture

#### **2.2.1 Data Import Pipeline**

```
┌────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                            │
│  [Google APIs] [Bing APIs] [Third-party] [User Uploads]   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              INGESTION LAYER                               │
│  • API adapters with retry logic                           │
│  • Rate limiting per source                                │
│  • Request queuing and scheduling                          │
│  • Error handling and logging                              │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│            VALIDATION & CLEANING                           │
│  • Schema validation                                       │
│  • Data type conversion                                    │
│  • Null handling                                           │
│  • Duplicate detection                                     │
│  • Outlier detection                                       │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              TRANSFORMATION                                │
│  • Normalization (keywords, URLs)                          │
│  • Enrichment (add metadata)                               │
│  • Aggregation (combine sources)                           │
│  • Calculation (derived metrics)                           │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                LOADING LAYER                               │
│  • Batch insertion to PostgreSQL                           │
│  • Bulk indexing to Elasticsearch                          │
│  • Document insertion to MongoDB                           │
│  • Cache warming (Redis)                                   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│             POST-PROCESSING                                │
│  • Trigger analytics jobs                                  │
│  • Update aggregated tables                                │
│  • Invalidate stale cache                                  │
│  • Send notifications                                      │
└────────────────────────────────────────────────────────────┘
```

#### **2.2.2 Data Processing Stages**

**Stage 1: Raw Data Collection**
```python
# Pseudo-code
async def collect_keyword_data(keyword, country, language):
    sources = [
        fetch_google_ads_data(keyword, country),
        fetch_google_trends(keyword),
        fetch_third_party_api(keyword, country),
        scrape_serp_if_needed(keyword, country)
    ]
    
    results = await asyncio.gather(*sources, return_exceptions=True)
    
    return {
        'raw_data': results,
        'timestamp': utc_now(),
        'sources_succeeded': count_successes(results)
    }
```

**Stage 2: Data Cleaning**
```python
def clean_keyword_data(raw_data):
    cleaned = {
        'keyword': normalize_keyword(raw_data['keyword']),
        'volume': validate_volume(raw_data['volume']),
        'cpc': validate_currency(raw_data['cpc']),
        'competition': normalize_0_to_1(raw_data['competition']),
        'trend_data': interpolate_missing_months(raw_data['trend'])
    }
    
    # Remove outliers
    if is_outlier(cleaned['volume']):
        cleaned['volume_confidence'] = 'low'
    
    return cleaned
```

**Stage 3: Data Enrichment**
```python
def enrich_keyword_data(cleaned_data):
    enriched = cleaned_data.copy()
    
    # Calculate derived metrics
    enriched['difficulty_score'] = calculate_difficulty(
        cleaned_data['competition'],
        cleaned_data['volume'],
        cleaned_data['serp_features']
    )
    
    # Add related data
    enriched['related_keywords'] = find_related_keywords(
        cleaned_data['keyword']
    )
    
    # Add semantic data
    enriched['intent'] = classify_search_intent(
        cleaned_data['keyword']
    )
    
    return enriched
```

**Stage 4: Data Storage**
```python
async def store_keyword_data(enriched_data):
    # Parallel storage operations
    await asyncio.gather(
        store_in_postgres(enriched_data),
        index_in_elasticsearch(enriched_data),
        cache_in_redis(enriched_data),
        archive_in_mongodb(enriched_data['raw_data'])
    )
```

### 2.3 API Rate Limiting & Proxy Rotation

#### **2.3.1 Rate Limiting Strategy**

```
┌─────────────────────────────────────────────────────────────┐
│                  RATE LIMITING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: API Gateway Level (Per User)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Free Plan:     10 requests/minute                     │ │
│  │ Pro Plan:      100 requests/minute                    │ │
│  │ Agency Plan:   500 requests/minute                    │ │
│  │ Enterprise:    Custom limits                          │ │
│  │                                                        │ │
│  │ Implementation: Token bucket algorithm in Redis       │ │
│  │ Key: "ratelimit:user:{user_id}:{endpoint}"           │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Layer 2: Service Level (Per External API)                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Google Ads API:    15,000/day (shared across users)  │ │
│  │ Google Trends:     1,500/hour                         │ │
│  │ Bing API:          5,000/month                        │ │
│  │ Third-party APIs:  Varies by provider                 │ │
│  │                                                        │ │
│  │ Implementation: Distributed counter in Redis          │ │
│  │ Key: "api_quota:{provider}:{date}"                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Layer 3: Crawler Level (Per Proxy/IP)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Max 60 requests/hour per IP                          │ │
│  │ Randomized delays: 2-5 seconds                        │ │
│  │ Rotating user agents                                  │ │
│  │ Cookie management                                     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### **2.3.2 Proxy Rotation System**

```
┌─────────────────────────────────────────────────────────────┐
│                  PROXY POOL MANAGEMENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Proxy Sources:                                             │
│  • Residential Proxies (Bright Data, Oxylabs)              │
│  • Datacenter Proxies (backup)                             │
│  • Mobile Proxies (for mobile SERP)                        │
│                                                             │
│  Pool Size: 1,000-10,000 rotating proxies                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    ROTATION STRATEGY                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Round-Robin Selection                                   │
│     • Distribute requests evenly                            │
│     • Track usage per proxy                                 │
│                                                             │
│  2. Health Checking                                         │
│     • Periodic connectivity tests                           │
│     • Response time monitoring                              │
│     • Success rate tracking                                 │
│     • Automatic removal of dead proxies                     │
│                                                             │
│  3. Geographic Targeting                                    │
│     • Match proxy location to search location               │
│     • US proxy for US searches                              │
│     • Local proxies for local SERP                          │
│                                                             │
│  4. Cooldown Management                                     │
│     • 5-minute cooldown after 50 requests                   │
│     • Exponential backoff on errors                         │
│     • Automatic proxy cycling                               │
│                                                             │
│  5. CAPTCHA Handling                                        │
│     • Detect CAPTCHA challenges                             │
│     • Mark proxy as temporary blocked                       │
│     • Integrate CAPTCHA solving service (2Captcha)          │
│     • Fallback to manual verification if needed             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Proxy Selection Algorithm:

```python
def select_proxy(country, previous_failures=[]):
    # Get healthy proxies for country
    candidate_proxies = redis.smembers(f'proxies:healthy:{country}')
    
    # Remove recently failed proxies
    candidate_proxies -= set(previous_failures)
    
    # Sort by recent usage (prefer least recently used)
    proxies_with_scores = []
    for proxy in candidate_proxies:
        last_used = redis.get(f'proxy:last_used:{proxy}')
        success_rate = redis.get(f'proxy:success_rate:{proxy}')
        
        score = calculate_proxy_score(last_used, success_rate)
        proxies_with_scores.append((proxy, score))
    
    # Select best proxy
    selected_proxy = max(proxies_with_scores, key=lambda x: x[1])[0]
    
    # Mark as in-use
    redis.set(f'proxy:last_used:{selected_proxy}', time.now())
    
    return selected_proxy
```

---

## 3. Database Design

### 3.1 Database Schema Overview

The system uses **four database technologies** for different purposes:

1. **PostgreSQL** - Primary relational data (users, projects, core metrics)
2. **MongoDB** - Document storage (raw crawl data, flexible schemas)
3. **Redis** - Caching and real-time data
4. **Elasticsearch** - Full-text search and analytics

### 3.2 PostgreSQL Schema

#### **3.2.1 Users & Authentication**

```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'free', -- free, pro, agency, enterprise
    plan_status VARCHAR(50) DEFAULT 'active', -- active, trial, expired, cancelled
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_plan_type ON users(plan_type);

-- User sessions
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- User subscriptions
CREATE TABLE subscriptions (
    subscription_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL, -- active, cancelled, expired, past_due
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);

-- User quotas and usage
CREATE TABLE user_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    quota_type VARCHAR(50) NOT NULL, -- keyword_searches, domain_analyses, rank_checks
    quota_limit INT NOT NULL,
    quota_used INT DEFAULT 0,
    reset_period VARCHAR(50) NOT NULL, -- daily, monthly
    last_reset_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quotas_user_id ON user_quotas(user_id);
CREATE UNIQUE INDEX idx_quotas_user_type ON user_quotas(user_id, quota_type);
```

#### **3.2.2 Projects & Organization**

```sql
-- Projects (workspace for organizing keywords and domains)
CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    target_country VARCHAR(2) DEFAULT 'US',
    target_language VARCHAR(5) DEFAULT 'en',
    target_location VARCHAR(255), -- city name for local SEO
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_archived BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_country ON projects(target_country);

-- Project members (for team collaboration)
CREATE TABLE project_members (
    member_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- owner, admin, editor, viewer
    invited_by BIGINT REFERENCES users(user_id),
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

CREATE INDEX idx_members_project_id ON project_members(project_id);
CREATE INDEX idx_members_user_id ON project_members(user_id);
```

#### **3.2.3 Keywords Core Tables**

```sql
-- Keywords master table
CREATE TABLE keywords (
    keyword_id BIGSERIAL PRIMARY KEY,
    keyword_text TEXT NOT NULL,
    keyword_normalized TEXT NOT NULL, -- lowercase, trimmed
    keyword_hash VARCHAR(64) NOT NULL, -- for sharding
    country VARCHAR(2) NOT NULL,
    language VARCHAR(5) NOT NULL,
    device_type VARCHAR(20) DEFAULT 'desktop', -- desktop, mobile, tablet
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_fetched_at TIMESTAMP,
    data_source VARCHAR(50), -- google_ads, bing, semrush_api
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(keyword_normalized, country, language, device_type)
);

CREATE INDEX idx_keywords_normalized ON keywords(keyword_normalized);
CREATE INDEX idx_keywords_hash ON keywords(keyword_hash);
CREATE INDEX idx_keywords_country ON keywords(country);
CREATE INDEX idx_keywords_updated_at ON keywords(updated_at);

-- Partitioning strategy (if using native partitioning)
-- CREATE TABLE keywords_us PARTITION OF keywords FOR VALUES IN ('US');
-- CREATE TABLE keywords_uk PARTITION OF keywords FOR VALUES IN ('UK');
-- CREATE TABLE keywords_in PARTITION OF keywords FOR VALUES IN ('IN');

-- Keyword metrics (search volume, CPC, competition)
CREATE TABLE keyword_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    search_volume BIGINT,
    search_volume_trend VARCHAR(20), -- up, down, stable
    cpc_min DECIMAL(10,2),
    cpc_max DECIMAL(10,2),
    cpc_avg DECIMAL(10,2),
    competition_score DECIMAL(3,2), -- 0.00 to 1.00
    competition_level VARCHAR(20), -- low, medium, high
    difficulty_score INT, -- 0-100
    opportunity_score INT, -- 0-100 (custom metric)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, metric_date)
);

CREATE INDEX idx_metrics_keyword_id ON keyword_metrics(keyword_id);
CREATE INDEX idx_metrics_date ON keyword_metrics(metric_date);
CREATE INDEX idx_metrics_volume ON keyword_metrics(search_volume);
CREATE INDEX idx_metrics_difficulty ON keyword_metrics(difficulty_score);

-- Keyword trends (12-month historical data)
CREATE TABLE keyword_trends (
    trend_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    trend_month DATE NOT NULL, -- first day of month
    trend_value INT NOT NULL, -- 0-100 (relative interest)
    search_volume_estimate BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, trend_month)
);

CREATE INDEX idx_trends_keyword_id ON keyword_trends(keyword_id);
CREATE INDEX idx_trends_month ON keyword_trends(trend_month);

-- Related keywords
CREATE TABLE related_keywords (
    relation_id BIGSERIAL PRIMARY KEY,
    source_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    related_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL, -- similar, broader, narrower, question
    relevance_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_keyword_id, related_keyword_id, relation_type)
);

CREATE INDEX idx_related_source ON related_keywords(source_keyword_id);
CREATE INDEX idx_related_target ON related_keywords(related_keyword_id);
CREATE INDEX idx_related_type ON related_keywords(relation_type);

-- Keyword questions (People Also Ask)
CREATE TABLE keyword_questions (
    question_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50), -- who, what, when, where, why, how
    frequency_score INT, -- how often it appears
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_keyword_id ON keyword_questions(keyword_id);
CREATE INDEX idx_questions_type ON keyword_questions(question_type);

-- User keyword lists (saved keywords)
CREATE TABLE user_keyword_lists (
    list_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    tags VARCHAR(255)[],
    priority INT, -- 1-5
    UNIQUE(project_id, keyword_id)
);

CREATE INDEX idx_user_lists_project ON user_keyword_lists(project_id);
CREATE INDEX idx_user_lists_keyword ON user_keyword_lists(keyword_id);
```

#### **3.2.4 Domains & Backlinks**

```sql
-- Domains master table
CREATE TABLE domains (
    domain_id BIGSERIAL PRIMARY KEY,
    domain_name VARCHAR(255) UNIQUE NOT NULL,
    domain_normalized VARCHAR(255) NOT NULL, -- lowercase
    domain_hash VARCHAR(64) NOT NULL,
    tld VARCHAR(50),
    is_subdomain BOOLEAN DEFAULT FALSE,
    root_domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_crawled_at TIMESTAMP,
    crawl_status VARCHAR(50), -- pending, in_progress, completed, failed
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_domains_normalized ON domains(domain_normalized);
CREATE INDEX idx_domains_hash ON domains(domain_hash);
CREATE INDEX idx_domains_tld ON domains(tld);
CREATE INDEX idx_domains_root ON domains(root_domain);

-- Domain metrics
CREATE TABLE domain_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    domain_authority INT, -- 0-100 (our custom score)
    page_authority_avg DECIMAL(5,2),
    total_backlinks BIGINT,
    unique_domains BIGINT,
    dofollow_backlinks BIGINT,
    nofollow_backlinks BIGINT,
    total_referring_ips BIGINT,
    organic_traffic_estimate BIGINT,
    organic_keywords_count BIGINT,
    organic_traffic_value DECIMAL(12,2), -- estimated value in USD
    paid_traffic_estimate BIGINT,
    social_signals JSONB, -- {facebook: 1000, twitter: 500, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, metric_date)
);

CREATE INDEX idx_domain_metrics_domain ON domain_metrics(domain_id);
CREATE INDEX idx_domain_metrics_date ON domain_metrics(metric_date);
CREATE INDEX idx_domain_metrics_authority ON domain_metrics(domain_authority);

-- Backlinks (huge table - consider sharding)
CREATE TABLE backlinks (
    backlink_id BIGSERIAL PRIMARY KEY,
    target_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    source_domain_id BIGINT REFERENCES domains(domain_id),
    source_url TEXT NOT NULL,
    source_page_title TEXT,
    anchor_text TEXT,
    link_type VARCHAR(20), -- dofollow, nofollow, redirect
    first_seen_at TIMESTAMP NOT NULL,
    last_seen_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    http_status INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_backlinks_target_domain ON backlinks(target_domain_id);
CREATE INDEX idx_backlinks_source_domain ON backlinks(source_domain_id);
CREATE INDEX idx_backlinks_first_seen ON backlinks(first_seen_at);
CREATE INDEX idx_backlinks_active ON backlinks(is_active);

-- For sharding large backlinks table:
-- Shard by target_domain_hash using Citus or manual sharding

-- Domain top pages
CREATE TABLE domain_top_pages (
    page_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    page_url TEXT NOT NULL,
    page_title TEXT,
    page_type VARCHAR(50), -- article, product, category, homepage
    organic_traffic_estimate BIGINT,
    organic_keywords_count INT,
    backlinks_count INT,
    social_shares INT,
    content_length INT,
    last_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, page_url)
);

CREATE INDEX idx_top_pages_domain ON domain_top_pages(domain_id);
CREATE INDEX idx_top_pages_traffic ON domain_top_pages(organic_traffic_estimate DESC);

-- Domain organic keywords
CREATE TABLE domain_organic_keywords (
    ranking_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    ranking_url TEXT NOT NULL,
    position INT NOT NULL,
    position_date DATE NOT NULL,
    previous_position INT,
    traffic_estimate INT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, keyword_id, position_date)
);

CREATE INDEX idx_organic_domain ON domain_organic_keywords(domain_id);
CREATE INDEX idx_organic_keyword ON domain_organic_keywords(keyword_id);
CREATE INDEX idx_organic_position ON domain_organic_keywords(position);
CREATE INDEX idx_organic_date ON domain_organic_keywords(position_date);
```

#### **3.2.5 SERP Data**

```sql
-- SERP results snapshots
CREATE TABLE serp_results (
    serp_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    search_date DATE NOT NULL,
    search_location VARCHAR(255), -- city/region for local searches
    device_type VARCHAR(20) DEFAULT 'desktop',
    total_results BIGINT,
    serp_features JSONB, -- {featured_snippet: true, local_pack: true, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, search_date, search_location, device_type)
);

CREATE INDEX idx_serp_keyword ON serp_results(keyword_id);
CREATE INDEX idx_serp_date ON serp_results(search_date);
CREATE INDEX idx_serp_location ON serp_results(search_location);

-- Individual SERP positions
CREATE TABLE serp_positions (
    position_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    position INT NOT NULL,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    title TEXT,
    description TEXT,
    result_type VARCHAR(50), -- organic, paid, featured_snippet, local, image, video
    serp_features JSONB, -- rich snippet data
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_positions_serp ON serp_positions(serp_id);
CREATE INDEX idx_positions_domain ON serp_positions(domain_id);
CREATE INDEX idx_positions_position ON serp_positions(position);

-- SERP features (detailed)
CREATE TABLE serp_features (
    feature_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    feature_type VARCHAR(50) NOT NULL, -- featured_snippet, local_pack, people_also_ask, etc.
    feature_data JSONB NOT NULL, -- flexible structure for different features
    feature_position INT,
    domain_id BIGINT REFERENCES domains(domain_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_features_serp ON serp_features(serp_id);
CREATE INDEX idx_features_type ON serp_features(feature_type);
CREATE INDEX idx_features_domain ON serp_features(domain_id);
```

#### **3.2.6 Keyword Tracking**

```sql
-- Keyword tracking projects
CREATE TABLE tracking_projects (
    tracking_project_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    target_domain VARCHAR(255) NOT NULL,
    check_frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    next_check_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tracking_project ON tracking_projects(project_id);
CREATE INDEX idx_tracking_next_check ON tracking_projects(next_check_at);

-- Tracked keywords
CREATE TABLE tracked_keywords (
    tracked_keyword_id BIGSERIAL PRIMARY KEY,
    tracking_project_id BIGINT REFERENCES tracking_projects(tracking_project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    target_url TEXT, -- specific URL to track
    tags VARCHAR(255)[],
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracking_project_id, keyword_id)
);

CREATE INDEX idx_tracked_project ON tracked_keywords(tracking_project_id);
CREATE INDEX idx_tracked_keyword ON tracked_keywords(keyword_id);

-- Ranking history (time-series data - consider TimescaleDB)
CREATE TABLE ranking_history (
    history_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    check_date DATE NOT NULL,
    check_time TIMESTAMP NOT NULL,
    position INT, -- NULL if not ranking
    ranking_url TEXT,
    serp_features VARCHAR(50)[], -- features present at time of check
    pixel_rank INT, -- position in pixels from top
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracked_keyword_id, check_date, check_time)
);

CREATE INDEX idx_history_tracked ON ranking_history(tracked_keyword_id);
CREATE INDEX idx_history_date ON ranking_history(check_date);
CREATE INDEX idx_history_position ON ranking_history(position);

-- Convert to TimescaleDB hypertable for better time-series performance
-- SELECT create_hypertable('ranking_history', 'check_time');

-- Ranking alerts
CREATE TABLE ranking_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- position_change, entered_top10, dropped_out, etc.
    alert_threshold INT, -- e.g., alert if change > 5 positions
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_tracked ON ranking_alerts(tracked_keyword_id);

-- Alert history
CREATE TABLE alert_notifications (
    notification_id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT REFERENCES ranking_alerts(alert_id) ON DELETE CASCADE,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    trigger_date DATE NOT NULL,
    old_position INT,
    new_position INT,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_alert ON alert_notifications(alert_id);
CREATE INDEX idx_notifications_date ON alert_notifications(trigger_date);
```

#### **3.2.7 Content Analysis & Gap Analysis**

```sql
-- Content analysis
CREATE TABLE content_analysis (
    analysis_id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    keyword_id BIGINT, -- target keyword for analysis
    content_length INT,
    word_count INT,
    readability_score DECIMAL(5,2),
    keyword_density DECIMAL(5,2),
    h1_count INT,
    h2_count INT,
    image_count INT,
    internal_links_count INT,
    external_links_count INT,
    schema_markup JSONB,
    meta_title TEXT,
    meta_description TEXT,
    analyzed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_content_domain ON content_analysis(domain_id);
CREATE INDEX idx_content_keyword ON content_analysis(keyword_id);

-- Content gap analysis (comparing domains)
CREATE TABLE content_gaps (
    gap_id BIGSERIAL PRIMARY KEY,
    source_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    competitor_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    competitor_position INT,
    source_position INT, -- NULL if not ranking
    gap_score INT, -- 0-100
    opportunity_score INT, -- 0-100
    analysis_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_domain_id, competitor_domain_id, keyword_id, analysis_date)
);

CREATE INDEX idx_gaps_source ON content_gaps(source_domain_id);
CREATE INDEX idx_gaps_competitor ON content_gaps(competitor_domain_id);
CREATE INDEX idx_gaps_keyword ON content_gaps(keyword_id);
CREATE INDEX idx_gaps_score ON content_gaps(gap_score DESC);
```

#### **3.2.8 API Cache & Search History**

```sql
-- API response cache metadata
CREATE TABLE api_cache_metadata (
    cache_id BIGSERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    entity_id BIGINT, -- keyword_id, domain_id, etc.
    cache_ttl INT NOT NULL, -- seconds
    cached_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    hit_count INT DEFAULT 0,
    last_hit_at TIMESTAMP
);

CREATE INDEX idx_cache_key ON api_cache_metadata(cache_key);
CREATE INDEX idx_cache_expires ON api_cache_metadata(expires_at);
CREATE INDEX idx_cache_type ON api_cache_metadata(cache_type);

-- Search history (for analytics and suggestions)
CREATE TABLE search_history (
    search_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    search_query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    search_filters JSONB, -- country, language, device, etc.
    result_count INT,
    searched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_query ON search_history(search_query);
CREATE INDEX idx_search_date ON search_history(searched_at);
```

#### **3.2.9 External API Integration Tracking**

```sql
-- API integration logs
CREATE TABLE api_integration_logs (
    log_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL, -- google_ads, google_trends, semrush, etc.
    endpoint VARCHAR(255) NOT NULL,
    request_method VARCHAR(10),
    request_params JSONB,
    response_status INT,
    response_time_ms INT,
    error_message TEXT,
    requested_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_logs_provider ON api_integration_logs(provider);
CREATE INDEX idx_api_logs_date ON api_integration_logs(requested_at);
CREATE INDEX idx_api_logs_status ON api_integration_logs(response_status);

-- API quota tracking
CREATE TABLE api_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    quota_type VARCHAR(50) NOT NULL, -- daily, monthly
    quota_limit BIGINT NOT NULL,
    quota_used BIGINT DEFAULT 0,
    quota_period DATE NOT NULL,
    reset_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, quota_type, quota_period)
);

CREATE INDEX idx_api_quotas_provider ON api_quotas(provider);
CREATE INDEX idx_api_quotas_period ON api_quotas(quota_period);
```

#### **3.2.10 Indexing & Partitioning Strategy**

```sql
-- Composite indexes for common query patterns

-- Keyword searches by country and language
CREATE INDEX idx_keywords_country_lang_norm 
ON keywords(country, language, keyword_normalized);

-- Keyword metrics for trending keywords
CREATE INDEX idx_metrics_volume_date 
ON keyword_metrics(search_volume DESC, metric_date DESC);

-- Domain backlinks by date and status
CREATE INDEX idx_backlinks_target_active_date 
ON backlinks(target_domain_id, is_active, last_seen_at DESC);

-- SERP tracking queries
CREATE INDEX idx_ranking_history_tracked_date 
ON ranking_history(tracked_keyword_id, check_date DESC);

-- Content gaps by score
CREATE INDEX idx_content_gaps_source_score 
ON content_gaps(source_domain_id, gap_score DESC, analysis_date DESC);

-- Partitioning strategy for large tables
-- Example: Partition ranking_history by month
CREATE TABLE ranking_history_y2025m01 PARTITION OF ranking_history
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE ranking_history_y2025m02 PARTITION OF ranking_history
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automated partition creation via pg_cron or external script
```

### 3.3 MongoDB Collections

MongoDB stores **flexible, document-based data** and **raw crawl results**.

#### **3.3.1 Raw SERP Snapshots**

```javascript
// Collection: serp_snapshots
{
    _id: ObjectId(),
    keyword: "best running shoes",
    country: "US",
    language: "en",
    device: "desktop",
    search_date: ISODate("2025-01-15T10:30:00Z"),
    raw_html: "<html>...</html>", // Full SERP HTML
    raw_json: { /* Google API response */ },
    screenshot_url: "s3://bucket/serp-snapshots/uuid.png",
    results: [
        {
            position: 1,
            url: "https://example.com/running-shoes",
            title: "Best Running Shoes 2025",
            description: "...",
            type: "organic",
            rich_snippet: {
                rating: 4.5,
                reviews: 1200,
                price: "$129.99"
            }
        }
        // ... more results
    ],
    serp_features: [
        {
            type: "featured_snippet",
            content: "...",
            source_url: "https://example.com"
        },
        {
            type: "people_also_ask",
            questions: [...]
        }
    ],
    ads: [
        {
            position: "top1",
            url: "...",
            title: "...",
            description: "..."
        }
    ],
    metadata: {
        total_results: 2340000000,
        search_time_ms: 234,
        proxy_used: "proxy123",
        crawler_version: "2.0"
    },
    created_at: ISODate("2025-01-15T10:30:05Z")
}

// Indexes
db.serp_snapshots.createIndex({ keyword: 1, country: 1, search_date: -1 });
db.serp_snapshots.createIndex({ search_date: -1 });
db.serp_snapshots.createIndex({ "results.url": 1 });
```

#### **3.3.2 Crawl Queue**

```javascript
// Collection: crawl_queue
{
    _id: ObjectId(),
    job_id: "uuid",
    job_type: "serp_crawl", // serp_crawl, backlink_discovery, content_extraction
    priority: 1, // 1-5
    status: "pending", // pending, in_progress, completed, failed
    keyword: "running shoes",
    country: "US",
    language: "en",
    parameters: {
        device: "desktop",
        location: "New York, NY",
        num_results: 100
    },
    retry_count: 0,
    max_retries: 3,
    assigned_worker: null,
    started_at: null,
    completed_at: null,
    error_message: null,
    result_reference: null, // Reference to result in other collection
    created_at: ISODate("2025-01-15T10:00:00Z"),
    updated_at: ISODate("2025-01-15T10:00:00Z"),
    scheduled_for: ISODate("2025-01-15T10:05:00Z")
}

// Indexes
db.crawl_queue.createIndex({ status: 1, priority: 1, scheduled_for: 1 });
db.crawl_queue.createIndex({ job_id: 1 });
db.crawl_queue.createIndex({ created_at: -1 });
```

#### **3.3.3 Backlink Discovery Data**

```javascript
// Collection: backlink_raw_data
{
    _id: ObjectId(),
    target_domain: "example.com",
    target_url: "https://example.com/page",
    discovered_backlinks: [
        {
            source_url: "https://source.com/article",
            source_domain: "source.com",
            anchor_text: "click here",
            link_type: "dofollow",
            context: "... surrounding text ...",
            discovered_at: ISODate("2025-01-15T10:00:00Z"),
            http_status: 200,
            source_page_title: "Article Title",
            source_page_metrics: {
                domain_authority: 45,
                page_authority: 38,
                spam_score: 2
            }
        }
        // ... thousands more
    ],
    crawl_method: "ahrefs_api", // ahrefs_api, moz_api, manual_crawl
    crawl_date: ISODate("2025-01-15T10:00:00Z"),
    total_backlinks_found: 15234,
    metadata: {
        api_version: "v3",
        cost_credits: 50
    },
    created_at: ISODate("2025-01-15T10:30:00Z")
}

// Indexes
db.backlink_raw_data.createIndex({ target_domain: 1, crawl_date: -1 });
db.backlink_raw_data.createIndex({ "discovered_backlinks.source_domain": 1 });
```

#### **3.3.4 Historical Metrics Archive**

```javascript
// Collection: keyword_metrics_archive
// Old keyword metrics (>90 days) moved from PostgreSQL to MongoDB
{
    _id: ObjectId(),
    keyword_id: 12345,
    keyword: "running shoes",
    country: "US",
    metrics_by_month: {
        "2024-01": {
            search_volume: 110000,
            cpc_avg: 1.25,
            competition: 0.78,
            difficulty_score: 65
        },
        "2024-02": {
            search_volume: 135000,
            cpc_avg: 1.32,
            competition: 0.81,
            difficulty_score: 68
        }
        // ... 12+ months of data
    },
    archived_at: ISODate("2025-01-15T00:00:00Z")
}

// Indexes
db.keyword_metrics_archive.createIndex({ keyword_id: 1 });
db.keyword_metrics_archive.createIndex({ archived_at: -1 });
```

### 3.4 Redis Data Structures

Redis handles **caching, real-time data, and queue management**.

#### **3.4.1 Cache Keys Structure**

```redis
# Keyword data cache
Key: "cache:keyword:en:us:desktop:running_shoes"
Type: String (JSON)
TTL: 86400 seconds (24 hours)
Value: {
    "keyword": "running shoes",
    "volume": 110000,
    "cpc": 1.25,
    "difficulty": 65,
    "trend": [100, 95, 98, ...]
}

# Domain overview cache
Key: "cache:domain:example.com:overview"
Type: String (JSON)
TTL: 43200 seconds (12 hours)
Value: {
    "domain": "example.com",
    "authority": 75,
    "backlinks": 125000,
    "keywords": 45000,
    "traffic": 850000
}

# SERP results cache
Key: "cache:serp:en:us:running_shoes"
Type: String (JSON)
TTL: 21600 seconds (6 hours)
Value: {
    "keyword": "running shoes",
    "results": [...],
    "features": [...]
}

# User session
Key: "session:{user_id}:{session_token}"
Type: String (JSON)
TTL: 1800 seconds (30 minutes, sliding)
Value: {
    "user_id": 123,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": [...]
}
```

#### **3.4.2 Rate Limiting**

```redis
# User rate limit (token bucket)
Key: "ratelimit:user:{user_id}:keyword_search"
Type: String (integer)
TTL: 60 seconds
Value: 95  # requests remaining this minute
Algorithm: Token bucket with sliding window

# API provider rate limit
Key: "ratelimit:api:google_ads:daily"
Type: String (integer)
TTL: Until midnight UTC
Value: 14523  # requests used today

# IP-based rate limit (for crawlers)
Key: "ratelimit:ip:{proxy_ip}"
Type: Sorted Set
TTL: 3600 seconds
Members: {timestamp: request_id}
Algorithm: Sliding window log
```

#### **3.4.3 Real-time Ranking Data**

```redis
# Current rankings (hot data)
Key: "ranking:live:{tracked_keyword_id}"
Type: Hash
TTL: 3600 seconds
Fields:
    position: 5
    url: "https://example.com/page"
    last_check: 1705320000
    previous_position: 7

# Ranking change notifications
Key: "ranking:changes:{user_id}"
Type: List
TTL: 604800 seconds (7 days)
Values: [
    {"keyword": "...", "old": 7, "new": 5, "date": "..."},
    ...
]
```

#### **3.4.4 Queue Management**

```redis
# Priority queue for crawl jobs
Key: "queue:crawl:priority:{1-5}"
Type: List (FIFO)
Values: [job_id1, job_id2, ...]

# Job status tracking
Key: "job:{job_id}:status"
Type: Hash
Fields:
    status: "in_progress"
    worker_id: "worker-1"
    started_at: 1705320000
    progress: 45  # percentage

# Worker heartbeat
Key: "worker:{worker_id}:heartbeat"
Type: String
TTL: 60 seconds
Value: timestamp
```

### 3.5 Elasticsearch Indices

Elasticsearch provides **full-text search** and **fast analytics**.

#### **3.5.1 Keywords Index**

```json
// Index: keywords
{
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "snowball"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "keyword_id": {"type": "long"},
            "keyword_text": {
                "type": "text",
                "analyzer": "keyword_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "country": {"type": "keyword"},
            "language": {"type": "keyword"},
            "search_volume": {"type": "long"},
            "cpc_avg": {"type": "float"},
            "difficulty_score": {"type": "integer"},
            "opportunity_score": {"type": "integer"},
            "trend_direction": {"type": "keyword"},
            "related_keywords": {
                "type": "text",
                "analyzer": "keyword_analyzer"
            },
            "last_updated": {"type": "date"}
        }
    }
}
```

#### **3.5.2 Domains Index**

```json
// Index: domains
{
    "mappings": {
        "properties": {
            "domain_id": {"type": "long"},
            "domain_name": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "domain_authority": {"type": "integer"},
            "total_backlinks": {"type": "long"},
            "organic_keywords": {"type": "long"},
            "organic_traffic": {"type": "long"},
            "tld": {"type": "keyword"},
            "category": {"type": "keyword"},
            "last_crawled": {"type": "date"}
        }
    }
}
```

#### **3.5.3 Search Suggestions Index**

```json
// Index: search_suggestions
{
    "mappings": {
        "properties": {
            "suggestion": {
                "type": "completion",
                "analyzer": "simple",
                "search_analyzer": "simple"
            },
            "type": {"type": "keyword"}, // keyword, domain
            "popularity": {"type": "integer"},
            "country": {"type": "keyword"}
        }
    }
}
```

### 3.6 Sharding & Partitioning Plan

#### **3.6.1 PostgreSQL Sharding (using Citus)**

```sql
-- Distribute keywords table across shards
SELECT create_distributed_table('keywords', 'keyword_hash');
SELECT create_distributed_table('keyword_metrics', 'keyword_id');

-- Co-locate related tables for join performance
SELECT create_distributed_table('related_keywords', 'source_keyword_id', 
    colocate_with => 'keywords');

-- Distribute backlinks by target domain
SELECT create_distributed_table('backlinks', 'target_domain_id');

-- Reference tables (replicated to all shards)
SELECT create_reference_table('users');
SELECT create_reference_table('projects');
```

#### **3.6.2 MongoDB Sharding**

```javascript
// Enable sharding on database
sh.enableSharding("seo_platform");

// Shard serp_snapshots by compound key
sh.shardCollection("seo_platform.serp_snapshots", {
    country: 1,
    language: 1,
    search_date: 1
});

// Shard backlink_raw_data by target domain
sh.shardCollection("seo_platform.backlink_raw_data", {
    target_domain: "hashed"
});

// Shard crawl_queue by job_id
sh.shardCollection("seo_platform.crawl_queue", {
    job_id: "hashed"
});
```

#### **3.6.3 Data Retention & Archival**

```
Hot Data (PostgreSQL):
  - Last 90 days: Full metrics in main tables
  - Query performance: <100ms

Warm Data (PostgreSQL + compression):
  - 90 days - 1 year: Aggregated daily metrics
  - Query performance: <500ms

Cold Data (MongoDB):
  - 1+ years: Monthly aggregates only
  - Raw data archived to S3
  - Query performance: <2s

Archival Policy:
  - Ranking history: Keep daily for 90 days, weekly for 1 year, monthly forever
  - SERP snapshots: Keep full HTML for 30 days, metadata only after
  - Backlinks: Keep active backlinks in PostgreSQL, historical in MongoDB
  - API logs: Keep 30 days in PostgreSQL, archive to S3 after
```

---

## 4. API Layer Design

### 4.1 API Architecture

**Protocol:** REST API with optional GraphQL endpoint  
**Format:** JSON  
**Authentication:** JWT tokens + API keys  
**Versioning:** URL-based (`/api/v1/`, `/api/v2/`)

### 4.2 API Endpoints

#### **4.2.1 Keyword Research API**

```
POST /api/v1/keywords/search
Description: Search for keyword data
Authentication: Required (JWT or API key)
Rate Limit: 100/min (Pro), 500/min (Agency)

Request:
{
    "keyword": "running shoes",
    "country": "US",  // ISO 3166-1 alpha-2
    "language": "en",
    "device": "desktop",  // desktop, mobile, tablet
    "include_related": true,
    "include_questions": true,
    "include_trends": true
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "normalized": "running shoes",
        "metrics": {
            "search_volume": 110000,
            "search_volume_trend": "up",  // up, down, stable
            "cpc": {
                "min": 0.85,
                "max": 2.50,
                "avg": 1.25,
                "currency": "USD"
            },
            "competition": {
                "score": 0.78,
                "level": "high"  // low, medium, high
            },
            "difficulty_score": 65,  // 0-100
            "opportunity_score": 42  // 0-100 (custom metric)
        },
        "trends": {
            "last_12_months": [
                {"month": "2024-02", "value": 95},
                {"month": "2024-03", "value": 100},
                ...
            ],
            "year_over_year": 8.5  // % change
        },
        "related_keywords": [
            {
                "keyword": "best running shoes",
                "volume": 90500,
                "relevance": 0.95,
                "type": "similar"
            },
            ...
        ],
        "questions": [
            {
                "question": "what are the best running shoes for beginners",
                "type": "what",
                "frequency": 85
            },
            ...
        ],
        "serp_features": [
            "featured_snippet",
            "people_also_ask",
            "local_pack"
        ],
        "last_updated": "2025-01-15T10:30:00Z"
    },
    "metadata": {
        "cached": true,
        "cache_age_seconds": 3600,
        "sources": ["google_ads", "google_trends"],
        "credits_used": 1
    }
}

Error Responses:
400 Bad Request:
{
    "status": "error",
    "error": {
        "code": "INVALID_COUNTRY",
        "message": "Country code must be ISO 3166-1 alpha-2",
        "field": "country"
    }
}

429 Too Many Requests:
{
    "status": "error",
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Try again in 45 seconds",
        "retry_after": 45
    }
}

402 Payment Required:
{
    "status": "error",
    "error": {
        "code": "QUOTA_EXCEEDED",
        "message": "Monthly quota exceeded. Upgrade plan to continue",
        "quota_limit": 1000,
        "quota_used": 1000,
        "reset_date": "2025-02-01T00:00:00Z"
    }
}
```

```
GET /api/v1/keywords/{keyword_id}/suggestions
Description: Get related keywords and suggestions
Authentication: Required

Query Parameters:
- type: related|questions|broader|narrower (default: all)
- limit: 1-100 (default: 50)
- min_volume: minimum search volume filter
- max_difficulty: maximum difficulty score filter

Response (200 OK):
{
    "status": "success",
    "data": {
        "suggestions": [
            {
                "keyword": "best running shoes for flat feet",
                "search_volume": 22000,
                "difficulty_score": 58,
                "relevance_score": 0.88,
                "type": "narrower"
            },
            ...
        ],
        "total": 247,
        "returned": 50
    }
}
```

```
POST /api/v1/keywords/bulk
Description: Bulk keyword lookup (up to 100 keywords)
Authentication: Required
Rate Limit: 10/min (Pro), 50/min (Agency)

Request:
{
    "keywords": ["running shoes", "hiking boots", ...],
    "country": "US",
    "language": "en",
    "metrics": ["volume", "cpc", "difficulty"]  // optional filter
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "results": [
            {
                "keyword": "running shoes",
                "status": "success",
                "metrics": {...}
            },
            {
                "keyword": "xyz123invalid",
                "status": "not_found",
                "error": "No data available"
            }
        ],
        "summary": {
            "total": 100,
            "successful": 98,
            "failed": 2
        }
    },
    "metadata": {
        "credits_used": 10,
        "processing_time_ms": 1250
    }
}
```

#### **4.2.2 Domain Analysis API**

```
GET /api/v1/domains/{domain}/overview
Description: Get comprehensive domain metrics
Authentication: Required
Rate Limit: 50/min (Pro), 200/min (Agency)

Path Parameters:
- domain: example.com or www.example.com

Query Parameters:
- include_backlinks: true|false (default: false)
- include_top_pages: true|false (default: false)
- include_keywords: true|false (default: false)

Response (200 OK):
{
    "status": "success",
    "data": {
        "domain": "example.com",
        "metrics": {
            "domain_authority": 75,
            "page_authority_avg": 48.5,
            "spam_score": 2,
            "backlinks": {
                "total": 125847,
                "unique_domains": 8542,
                "dofollow": 98234,
                "nofollow": 27613,
                "referring_ips": 7234,
                "new_last_month": 1234,
                "lost_last_month": 456
            },
            "organic": {
                "keywords_count": 45231,
                "traffic_estimate": 850000,
                "traffic_value": 425000.00,
                "traffic_trend": "up",
                "top_keywords_count": 150,
                "keywords_top_3": 1234,
                "keywords_top_10": 4567,
                "keywords_top_100": 18923
            },
            "paid": {
                "keywords_count": 234,
                "traffic_estimate": 12000,
                "traffic_cost": 15000.00
            },
            "content": {
                "pages_indexed": 1547,
                "pages_crawled": 1892,
                "avg_page_speed": 2.3,
                "mobile_friendly_score": 95
            }
        },
        "competitors": [
            {
                "domain": "competitor1.com",
                "authority": 72,
                "keyword_overlap": 1234,
                "similarity_score": 0.78
            },
            ...
        ],
        "last_updated": "2025-01-15T08:00:00Z"
    }
}
```

```
GET /api/v1/domains/{domain}/backlinks
Description: Get backlink data for domain
Authentication: Required

Query Parameters:
- page: 1-1000 (default: 1)
- limit: 10-100 (default: 50)
- type: all|dofollow|nofollow (default: all)
- sort: authority|date_found|anchor_text (default: authority)
- order: desc|asc (default: desc)
- min_authority: 0-100 (filter)
- only_active: true|false (default: true)

Response (200 OK):
{
    "status": "success",
    "data": {
        "backlinks": [
            {
                "source_url": "https://source.com/article",
                "source_domain": "source.com",
                "source_authority": 68,
                "target_url": "https://example.com/page",
                "anchor_text": "click here",
                "link_type": "dofollow",
                "first_seen": "2024-06-15T00:00:00Z",
                "last_seen": "2025-01-15T00:00:00Z",
                "http_status": 200,
                "is_active": true
            },
            ...
        ],
        "pagination": {
            "page": 1,
            "limit": 50,
            "total": 125847,
            "pages": 2517
        }
    }
}
```

```
GET /api/v1/domains/{domain}/top-pages
Description: Get top-performing pages
Authentication: Required

Query Parameters:
- page: 1-100 (default: 1)
- limit: 10-100 (default: 20)
- sort: traffic|keywords|backlinks (default: traffic)
- metric: organic|paid|all (default: organic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "pages": [
            {
                "url": "https://example.com/best-products",
                "title": "Best Products 2025",
                "page_authority": 52,
                "organic_traffic": 85000,
                "organic_keywords": 1234,
                "backlinks": 456,
                "social_shares": 1200,
                "traffic_value": 42500.00,
                "top_keywords": [
                    {
                        "keyword": "best products",
                        "position": 2,
                        "volume": 22000,
                        "traffic_estimate": 8800
                    },
                    ...
                ]
            },
            ...
        ],
        "pagination": {...}
    }
}
```

```
GET /api/v1/domains/{domain}/organic-keywords
Description: Get ranking keywords for domain
Authentication: Required

Query Parameters:
- page: 1-1000
- limit: 10-100
- position: 1-100 (filter)
- min_volume: minimum search volume
- sort: position|volume|traffic (default: traffic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "keywords": [
            {
                "keyword": "running shoes",
                "position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "search_volume": 110000,
                "traffic_estimate": 8800,
                "traffic_value": 11000.00,
                "serp_features": ["featured_snippet"]
            },
            ...
        ],
        "summary": {
            "total_keywords": 45231,
            "top_3": 1234,
            "top_10": 4567,
            "top_100": 18923
        },
        "pagination": {...}
    }
}
```

#### **4.2.3 SERP Analysis API**

```
POST /api/v1/serp/analyze
Description: Get SERP analysis for keyword
Authentication: Required
Rate Limit: 50/min

Request:
{
    "keyword": "running shoes",
    "country": "US",
    "language": "en",
    "device": "desktop",
    "location": "New York, NY",  // optional for local searches
    "num_results": 100  // 10-100, default: 10
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "total_results": 234000000,
        "serp_features": [
            {
                "type": "featured_snippet",
                "position": 0,
                "domain": "example.com",
                "url": "https://example.com/guide",
                "content_preview": "Running shoes are..."
            },
            {
                "type": "people_also_ask",
                "questions": [
                    "What are the best running shoes?",
                    "How to choose running shoes?",
                    ...
                ]
            },
            {
                "type": "local_pack",
                "businesses": [...]
            }
        ],
        "organic_results": [
            {
                "position": 1,
                "title": "Best Running Shoes 2025",
                "url": "https://example.com/running-shoes",
                "domain": "example.com",
                "domain_authority": 75,
                "description": "Discover the best...",
                "rich_snippet": {
                    "type": "product",
                    "rating": 4.5,
                    "reviews": 1200,
                    "price": "$129.99"
                },
                "backlinks": 1234,
                "referring_domains": 456,
                "estimated_traffic": 35000
            },
            ...
        ],
        "paid_results": [
            {
                "position": "top1",
                "title": "Running Shoes Sale",
                "url": "https://shop.com/running",
                "domain": "shop.com",
                "description": "50% off all running shoes"
            },
            ...
        ],
        "analysis": {
            "difficulty_score": 68,
            "opportunity_score": 45,
            "avg_domain_authority": 72.5,
            "avg_backlinks": 8542,
            "content_length_avg": 2850,
            "content_recommendations": [
                "Include product comparisons",
                "Add video content",
                "Target featured snippet opportunity"
            ]
        },
        "last_updated": "2025-01-15T10:30:00Z"
    }
}
```

```
GET /api/v1/serp/features
Description: Get SERP features statistics
Authentication: Required

Query Parameters:
- keyword: specific keyword or keyword_id
- country: US, UK, etc.
- date_range: last_7_days|last_30_days|last_90_days

Response (200 OK):
{
    "status": "success",
    "data": {
        "features_present": [
            {
                "feature": "featured_snippet",
                "frequency": 85,  // % of time present
                "domains_winning": [
                    {"domain": "example.com", "count": 45},
                    ...
                ]
            },
            {
                "feature": "people_also_ask",
                "frequency": 92
            },
            {
                "feature": "local_pack",
                "frequency": 12
            }
        ],
        "feature_history": [
            {
                "date": "2025-01-15",
                "features": ["featured_snippet", "people_also_ask", "images"]
            },
            ...
        ]
    }
}
```

#### **4.2.4 Rank Tracking API**

```
POST /api/v1/tracking/projects
Description: Create new tracking project
Authentication: Required

Request:
{
    "project_id": 123,  // existing project
    "name": "My Website Tracking",
    "target_domain": "example.com",
    "check_frequency": "daily",  // daily, weekly, monthly
    "keywords": [
        {
            "keyword": "running shoes",
            "target_url": "https://example.com/running-shoes",
            "tags": ["product", "priority-high"]
        },
        ...
    ]
}

Response (201 Created):
{
    "status": "success",
    "data": {
        "tracking_project_id": 456,
        "keywords_added": 50,
        "next_check_at": "2025-01-16T00:00:00Z",
        "estimated_credits_per_check": 50
    }
}
```

```
GET /api/v1/tracking/projects/{project_id}/rankings
Description: Get ranking data for tracked keywords
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD (default: 30 days ago)
- date_to: YYYY-MM-DD (default: today)
- tags: filter by tags (comma-separated)
- position_change: improved|declined|unchanged|new|lost
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "rankings": [
            {
                "keyword": "running shoes",
                "current_position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "best_position": 3,
                "worst_position": 15,
                "average_position": 6.8,
                "history": [
                    {"date": "2025-01-15", "position": 5},
                    {"date": "2025-01-14", "position": 6},
                    ...
                ],
                "serp_features": ["featured_snippet"],
                "visibility_score": 85  // 0-100
            },
            ...
        ],
        "summary": {
            "total_keywords": 50,
            "improved": 12,
            "declined": 8,
            "unchanged": 28,
            "new": 2,
            "lost": 0,
            "avg_position": 15.4,
            "visibility_score": 72
        }
    }
}
```

```
GET /api/v1/tracking/rankings/{keyword_id}/history
Description: Get detailed ranking history
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- granularity: daily|weekly|monthly

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "domain": "example.com",
        "history": [
            {
                "date": "2025-01-15",
                "position": 5,
                "ranking_url": "https://example.com/running-shoes",
                "serp_features": ["featured_snippet"],
                "competitors_above": [
                    {"domain": "competitor.com", "position": 1},
                    ...
                ]
            },
            ...
        ],
        "statistics": {
            "best_position": 3,
            "worst_position": 15,
            "average_position": 6.8,
            "position_changes": 23,
            "days_tracked": 90,
            "trend": "improving"  // improving, declining, stable
        }
    }
}
```

#### **4.2.5 Trends & Analytics API**

```
GET /api/v1/trends/keywords
Description: Get trending keywords
Authentication: Required

Query Parameters:
- country: US, UK, etc.
- category: all|shopping|sports|technology|...
- timeframe: today|week|month
- min_volume: minimum search volume
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "trending_keywords": [
            {
                "keyword": "ai chatbot",
                "search_volume": 246000,
                "volume_change_percent": 350,
                "trend_score": 95,
                "related_topics": ["artificial intelligence", "chatgpt"],
                "category": "technology"
            },
            ...
        ],
        "generated_at": "2025-01-15T10:00:00Z"
    }
}
```

```
POST /api/v1/analysis/content-gap
Description: Compare content gaps between domains
Authentication: Required
Rate Limit: 20/min

Request:
{
    "source_domain": "example.com",
    "competitor_domains": ["competitor1.com", "competitor2.com"],
    "country": "US",
    "min_volume": 1000,
    "max_difficulty": 70,
    "limit": 100
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "opportunities": [
            {
                "keyword": "best running shoes for beginners",
                "search_volume": 22000,
                "difficulty_score": 58,
                "gap_score": 85,  // 0-100 (higher = better opportunity)
                "source_position": null,  // not ranking
                "competitors": [
                    {
                        "domain": "competitor1.com",
                        "position": 3,
                        "url": "...",
                        "page_authority": 45
                    },
                    {
                        "domain": "competitor2.com",
                        "position": 7,
                        "url": "...",
                        "page_authority": 38
                    }
                ],
                "opportunity_reasons": [
                    "Competitors ranking with lower authority",
                    "High search volume with medium difficulty",
                    "Related to existing content on your site"
                ]
            },
            ...
        ],
        "summary": {
            "total_opportunities": 247,
            "high_priority": 45,
            "medium_priority": 128,
            "low_priority": 74,
            "estimated_traffic_potential": 125000
        }
    }
}
```

### 4.3 Pagination Strategy

All list endpoints use **cursor-based pagination** for performance:

```
GET /api/v1/keywords/search?page=1&limit=50

Response:
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 50,
        "total": 1247,
        "pages": 25,
        "has_next": true,
        "has_prev": false,
        "next_page": 2,
        "prev_page": null
    },
    "links": {
        "first": "/api/v1/keywords/search?page=1&limit=50",
        "last": "/api/v1/keywords/search?page=25&limit=50",
        "next": "/api/v1/keywords/search?page=2&limit=50",
        "prev": null
    }
}
```

For very large datasets (backlinks, SERP history), use **cursor pagination**:

```
GET /api/v1/domains/{domain}/backlinks?cursor=abc123&limit=100

Response:
{
    "data": [...],
    "pagination": {
        "cursor": "def456",
        "has_more": true,
        "limit": 100
    },
    "links": {
        "next": "/api/v1/domains/{domain}/backlinks?cursor=def456&limit=100"
    }
}
```

### 4.4 Filtering & Sorting

**Standard filters across endpoints:**
- `min_volume`: Minimum search volume
- `max_volume`: Maximum search volume
- `min_difficulty`: Minimum difficulty score
- `max_difficulty`: Maximum difficulty score
- `country`: Country code(s) - comma-separated
- `language`: Language code(s)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Standard sorting:**
- `sort`: Field to sort by
- `order`: asc|desc

Example:
```
GET /api/v1/keywords/search?
    keyword=shoes&
    min_volume=10000&
    max_difficulty=60&
    country=US,CA&
    sort=volume&
    order=desc&
    page=1&
    limit=50
```

### 4.5 Caching Strategy

```
Cache-Control Headers:
- Keyword data: max-age=86400 (24 hours)
- Domain overview: max-age=43200 (12 hours)
- SERP data: max-age=21600 (6 hours)
- Ranking data: max-age=3600 (1 hour)
- Trending data: max-age=600 (10 minutes)

ETag Support:
- Include ETag header in responses
- Support If-None-Match requests
- Return 304 Not Modified when appropriate

Example Response Headers:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=86400, public
ETag: "abc123def456"
X-Cache: HIT
X-Cache-Age: 3600
```

---

## 5. Crawler & Data Sources

### 5.1 Data Source Integration

#### **5.1.1 Google APIs**

**Google Ads Keyword Planner API**
```python
Purpose: Search volume, CPC, competition data
Rate Limit: 15,000 requests/day
Cost: Free with Google Ads account
Data Freshness: Updated monthly

Integration:
- OAuth 2.0 authentication
- REST API calls
- Batch requests (up to 100 keywords)
- Response caching (30 days)

Data Retrieved:
- Monthly search volume
- Competition level (low/medium/high)
- Suggested bid (CPC)
- Historical data (12 months)
- Related keywords
```

**Google Search Console API**
```python
Purpose: Verified site ranking data, clicks, impressions
Rate Limit: 1,200 requests/day
Cost: Free
Data Freshness: 2-3 days delay

Integration:
- OAuth 2.0 with Search Console verification
- Query for ranking data, impressions, clicks
- Filter by country, device, search appearance

Data Retrieved:
- Keyword rankings for verified sites
- Click-through rates
- Impressions
- Average position
```

**Google Trends API (Unofficial)**
```python
Purpose: 12-month trend data, related queries
Rate Limit: 1,500 requests/hour
Cost: Free (via pytrends library)
Data Freshness: Real-time

Integration:
- Python pytrends library
- Rotating proxies to avoid blocks
- Delayed requests (2-5 seconds)

Data Retrieved:
- Interest over time (0-100 scale)
- Related topics and queries
- Regional interest
- Rising keywords
```

#### **5.1.2 Bing Webmaster Tools API**

```python
Purpose: Alternative search data, Bing-specific metrics
Rate Limit: 5,000 requests/month
Cost: Free
Data Freshness: Daily updates

Integration:
- API key authentication
- REST API

Data Retrieved:
- Keyword rankings
- Traffic data
- Backlink data (limited)
- Page-level metrics
```

#### **5.1.3 Third-Party SEO APIs**

**DataForSEO API**
```python
Purpose: Comprehensive SERP data, backlinks, metrics
Rate Limit: Based on subscription
Cost: Pay-per-request ($0.001 - $0.02 per request)
Data Freshness: Real-time for SERP, daily for backlinks

Data Retrieved:
- SERP results with rich data
- Backlink profiles
- Keyword difficulty scores
- Domain metrics
- Historical data
```

**SEMrush API** (Alternative)
```python
Purpose: Keyword data, competition analysis
Cost: $199-$499/month + API credits
Data Retrieved:
- Keyword metrics
- Domain analytics
- Competitor analysis
- Backlink data
```

### 5.2 Headless Browser Crawling

For SERP scraping when APIs are insufficient:

```python
Technology Stack:
- Selenium with Chrome/Firefox headless
- Playwright (modern alternative, faster)
- Puppeteer (Node.js option)

Proxy Integration:
- Bright Data (Luminati) residential proxies
- Oxylabs datacenter & residential proxies
- ScraperAPI (handles proxies + CAPTCHA)

CAPTCHA Handling:
- 2Captcha API integration
- Anti-Captcha service
- Automatic retry with new proxy
- Fallback to human verification queue

User Agent Rotation:
- Random desktop user agents
- Mobile user agents for mobile SERP
- Update monthly from real browser stats
```

#### **5.2.1 SERP Crawler Implementation**

```python
# Pseudo-code for SERP crawler

class SERPCrawler:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        
    async def crawl_serp(self, keyword, country, device):
        # Select appropriate proxy
        proxy = self.proxy_manager.get_proxy(country)
        
        # Configure browser
        browser = await self.launch_browser(
            proxy=proxy,
            user_agent=self.get_user_agent(device),
            headless=True
        )
        
        try:
            # Navigate to Google search
            page = await browser.new_page()
            search_url = self.build_search_url(keyword, country)
            await page.goto(search_url, wait_until='networkidle')
            
            # Check for CAPTCHA
            if await self.detect_captcha(page):
                solved = await self.captcha_solver.solve(page)
                if not solved:
                    raise CaptchaError("Failed to solve CAPTCHA")
            
            # Extract SERP data
            serp_data = await self.extract_serp_data(page)
            
            # Take screenshot for archive
            screenshot = await page.screenshot(full_page=True)
            
            return {
                'results': serp_data,
                'screenshot': screenshot,
                'timestamp': datetime.utcnow(),
                'proxy_used': proxy.id
            }
            
        except Exception as e:
            # Mark proxy as failed
            self.proxy_manager.mark_failed(proxy)
            raise
            
        finally:
            await browser.close()
    
    async def extract_serp_data(self, page):
        # Extract organic results
        organic = await page.eval("""
            () => Array.from(document.querySelectorAll('.g')).map(el => ({
                position: Array.from(el.parentNode.children).indexOf(el) + 1,
                title: el.querySelector('h3')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.VwiC3b')?.textContent,
                rich_snippet: extractRichSnippet(el)
            }))
        """)
        
        # Extract SERP features
        featured_snippet = await page.querySelector('.ifM9O')
        people_also_ask = await page.querySelectorAll('.related-question-pair')
        local_pack = await page.querySelector('.rllt__details')
        
        # Extract paid ads
        ads = await page.eval("""
            () => Array.from(document.querySelectorAll('.uEierd')).map(el => ({
                position: 'top' + (Array.from(el.parentNode.children).indexOf(el) + 1),
                title: el.querySelector('.CCgQ5')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.MUxGbd')?.textContent
            }))
        """)
        
        return {
            'organic': organic,
            'ads': ads,
            'features': {
                'featured_snippet': featured_snippet,
                'people_also_ask': people_also_ask,
                'local_pack': local_pack
            }
        }
```

### 5.3 Crawler Scheduler

```python
# Celery beat schedule for periodic crawls

CELERYBEAT_SCHEDULE = {
    'crawl-high-priority-keywords': {
        'task': 'crawlers.tasks.crawl_keywords',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ({'priority': 'high'},)
    },
    'crawl-tracked-keywords-daily': {
        'task': 'crawlers.tasks.crawl_tracked_keywords',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'args': ({'frequency': 'daily'},)
    },
    'refresh-domain-backlinks': {
        'task': 'crawlers.tasks.refresh_backlinks',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'args': ()
    },
    'update-keyword-trends': {
        'task': 'crawlers.tasks.update_trends',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),  # Monthly
        'args': ()
    }
}
```

### 5.4 Proxy Management System

```python
class ProxyManager:
    def __init__(self):
        self.redis = Redis()
        self.proxy_pool = []
        
    def load_proxies(self):
        # Load from providers: Bright Data, Oxylabs, etc.
        proxies = [
            {'ip': '1.2.3.4:8080', 'country': 'US', 'type': 'residential'},
            {'ip': '5.6.7.8:8080', 'country': 'UK', 'type': 'datacenter'},
            ...
        ]
        self.proxy_pool = proxies
    
    def get_proxy(self, country='US', exclude_failed=True):
        # Get least recently used proxy for country
        candidates = [p for p in self.proxy_pool if p['country'] == country]
        
        if exclude_failed:
            # Filter out proxies that failed recently
            candidates = [p for p in candidates 
                         if not self.is_in_cooldown(p['ip'])]
        
        # Sort by last used time
        candidates.sort(key=lambda p: self.get_last_used(p['ip']))
        
        if not candidates:
            raise NoProxyAvailable(f"No proxies available for {country}")
        
        selected = candidates[0]
        self.mark_used(selected['ip'])
        return selected
    
    def mark_used(self, proxy_ip):
        self.redis.set(f'proxy:last_used:{proxy_ip}', time.time())
        self.redis.incr(f'proxy:usage_count:{proxy_ip}')
    
    def mark_failed(self, proxy, reason='unknown'):
        # Put proxy in cooldown for 5 minutes
        self.redis.setex(
            f'proxy:cooldown:{proxy["ip"]}',
            300,  # 5 minutes
            reason
        )
        self.redis.incr(f'proxy:failure_count:{proxy["ip"]}')
        
        # If too many failures, remove from pool
        failures = int(self.redis.get(f'proxy:failure_count:{proxy["ip"]}') or 0)
        if failures > 10:
            self.remove_proxy(proxy['ip'])
    
    def is_in_cooldown(self, proxy_ip):
        return self.redis.exists(f'proxy:cooldown:{proxy_ip}')
    
    def get_last_used(self, proxy_ip):
        return float(self.redis.get(f'proxy:last_used:{proxy_ip}') or 0)
    
    def health_check(self, proxy):
        # Test proxy connectivity
        try:
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies={'https': f'http://{proxy["ip"]}'},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    async def periodic_health_check(self):
        # Run every 5 minutes to check all proxies
        for proxy in self.proxy_pool:
            if not self.health_check(proxy):
                self.mark_failed(proxy, 'health_check_failed')
```

### 5.5 CAPTCHA Handling Strategy

```python
class CaptchaSolver:
    def __init__(self):
        self.twocaptcha_api_key = settings.TWOCAPTCHA_API_KEY
        
    async def solve(self, page, captcha_type='recaptcha_v2'):
        if captcha_type == 'recaptcha_v2':
            return await self.solve_recaptcha_v2(page)
        elif captcha_type == 'recaptcha_v3':
            return await self.solve_recaptcha_v3(page)
        elif captcha_type == 'image':
            return await self.solve_image_captcha(page)
    
    async def solve_recaptcha_v2(self, page):
        # Extract site key
        site_key = await page.evaluate("""
            () => document.querySelector('[data-sitekey]')?.getAttribute('data-sitekey')
        """)
        
        if not site_key:
            return False
        
        # Send to 2Captcha service
        task_id = self.create_captcha_task(
            site_key=site_key,
            page_url=page.url
        )
        
        # Wait for solution (can take 30-60 seconds)
        solution = self.wait_for_solution(task_id, timeout=120)
        
        if solution:
            # Inject solution into page
            await page.evaluate(f"""
                {% raw %}
                () => {{
                    document.getElementById('g-recaptcha-response').innerHTML = '{solution}';
                    document.querySelector('form').submit();
                }}{% endraw %}
                "
            """)
            return True
        
        return False
    
    def create_captcha_task(self, site_key, page_url):
        response = requests.post(
            'https://2captcha.com/in.php',
            data={
                'key': self.twocaptcha_api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
        )
        return response.json()['request']
    
    def wait_for_solution(self, task_id, timeout=120):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(
                'https://2captcha.com/res.php',
                params={
                    'key': self.twocaptcha_api_key,
                    'action': 'get',
                    'id': task_id,
                    'json': 1
                }
            )
            result = response.json()
            
            if result['status'] == 1:
                return result['request']
            
            time.sleep(5)
        
        return None
```

---

## 6. Ranking & Analytics Engine

### 6.1 Keyword Difficulty Algorithm

```python
def calculate_keyword_difficulty(keyword_data, serp_data):
    """
    Calculate keyword difficulty score (0-100)
    Higher = more difficult to rank
    
    Factors:
    1. Competition level from Google Ads (weight: 20%)
    2. Domain authority of top 10 results (weight: 40%)
    3. Backlink profile of top 10 (weight: 30%)
    4. SERP features present (weight: 10%)
    """
    
    # Factor 1: Competition level
    competition_score = keyword_data['competition'] * 100  # 0-100
    
    # Factor 2: Domain authority
    top_10_domains = serp_data['organic_results'][:10]
    avg_domain_authority = sum(d['domain_authority'] for d in top_10_domains) / 10
    
    # Factor 3: Backlinks
    avg_backlinks = sum(d['backlinks_count'] for d in top_10_domains) / 10
    backlink_score = min(100, (avg_backlinks / 1000) * 100)  # Normalize
    
    # Factor 4: SERP features
    serp_features_count = len(serp_data['serp_features'])
    serp_feature_score = min(100, serp_features_count * 15)
    
    # Weighted calculation
    difficulty = (
        competition_score * 0.20 +
        avg_domain_authority * 0.40 +
        backlink_score * 0.30 +
        serp_feature_score * 0.10
    )
    
    return round(difficulty, 2)
```

### 6.2 Opportunity Score Algorithm

```python
def calculate_opportunity_score(keyword_data, serp_data, user_domain_data):
    """
    Calculate opportunity score (0-100)
    Higher = better opportunity for ranking
    
    Factors:
    1. Search volume (high volume = more opportunity)
    2. Low difficulty (easier to rank)
    3. Low competition from strong domains
    4. User's domain strength relative to competitors
    5. Traffic value (CPC * volume)
    6. Trend direction (rising = more opportunity)
    """
    
    # Factor 1: Search volume score
    volume = keyword_data['search_volume']
    volume_score = min(100, (volume / 100000) * 100)  # Normalize to 100k
    
    # Factor 2: Difficulty score (inverse)
    difficulty = keyword_data['difficulty_score']
    difficulty_score = 100 - difficulty
    
    # Factor 3: Competition gap
    user_authority = user_domain_data['domain_authority']
    avg_competitor_authority = sum(
        d['domain_authority'] for d in serp_data['organic_results'][:10]
    ) / 10
    
    authority_gap = avg_competitor_authority - user_authority
    competition_score = max(0, 100 - authority_gap)
    
    # Factor 4: Traffic value
    traffic_value = keyword_data['cpc_avg'] * volume
    value_score = min(100, (traffic_value / 10000) * 100)
    
    # Factor 5: Trend score
    trend = keyword_data.get('trend_direction', 'stable')
    trend_score = {
        'rising': 100,
        'stable': 50,
        'declining': 20
    }.get(trend, 50)
    
    # Weighted calculation
    opportunity = (
        volume_score * 0.25 +
        difficulty_score * 0.30 +
        competition_score * 0.25 +
        value_score * 0.10 +
        trend_score * 0.10
    )
    
    return round(opportunity, 2)
```

### 6.3 Domain Authority Algorithm

```python
def calculate_domain_authority(domain_data):
    """
    Calculate domain authority (0-100)
    Similar to Moz's DA or Ahrefs DR
    
    Factors:
    1. Total backlinks (log scale)
    2. Unique referring domains (log scale)
    3. Quality of referring domains
    4. Link velocity (new vs lost)
    5. Organic traffic estimate
    6. Number of ranking keywords
    """
    
    # Factor 1: Total backlinks (log scale for diminishing returns)
    backlinks = domain_data['total_backlinks']
    backlink_score = min(100, math.log10(backlinks + 1) * 20)
    
    # Factor 2: Unique referring domains
    referring_domains = domain_data['unique_referring_domains']
    referring_score = min(100, math.log10(referring_domains + 1) * 25)
    
    # Factor 3: Quality of backlinks (avg authority of referring domains)
    avg_referring_authority = domain_data['avg_referring_domain_authority']
    quality_score = avg_referring_authority
    
    # Factor 4: Link velocity
    new_links_month = domain_data['new_backlinks_last_month']
    lost_links_month = domain_data['lost_backlinks_last_month']
    velocity = (new_links_month - lost_links_month) / max(1, backlinks) * 100
    velocity_score = min(100, max(0, 50 + velocity * 10))
    
    # Factor 5: Organic traffic
    organic_traffic = domain_data['organic_traffic_estimate']
    traffic_score = min(100, math.log10(organic_traffic + 1) * 15)
    
    # Factor 6: Ranking keywords
    ranking_keywords = domain_data['organic_keywords_count']
    keyword_score = min(100, math.log10(ranking_keywords + 1) * 20)
    
    # Weighted calculation
    authority = (
        backlink_score * 0.25 +
        referring_score * 0.30 +
        quality_score * 0.20 +
        velocity_score * 0.05 +
        traffic_score * 0.10 +
        keyword_score * 0.10
    )
    
    return round(authority, 2)
```

### 6.4 Trend Analysis Engine

```python
class TrendAnalyzer:
    def analyze_keyword_trend(self, historical_data):
        """
        Analyze 12-month trend data
        Returns: trend_direction, trend_strength, seasonality
        """
        
        # Extract monthly values
        months = sorted(historical_data.keys())
        values = [historical_data[m] for m in months]
        
        # Calculate linear regression
        slope, intercept = self.linear_regression(range(len(values)), values)
        
        # Determine trend direction
        if slope > 5:
            direction = 'rising'
        elif slope < -5:
            direction = 'declining'
        else:
            direction = 'stable'
        
        # Calculate trend strength (0-100)
        strength = min(100, abs(slope) * 2)
        
        # Detect seasonality
        seasonality = self.detect_seasonality(values)
        
        # Calculate volatility
        volatility = np.std(values) / np.mean(values) * 100
        
        return {
            'direction': direction,
            'strength': strength,
            'seasonality': seasonality,
            'volatility': volatility,
            'forecast_next_month': intercept + slope * len(values)
        }
    
    def detect_seasonality(self, values):
        """
        Detect seasonal patterns (monthly, quarterly, annual)
        """
        if len(values) < 12:
            return None
        
        # Check for quarterly pattern
        q1_avg = np.mean(values[0:3] + values[3:6] + values[6:9] + values[9:12])
        # ... more complex seasonality detection
        
        return {
            'has_seasonality': True,
            'pattern': 'quarterly',
            'peak_months': [6, 7, 8]  # Summer peak
        }
    
    def linear_regression(self, x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
```

### 6.5 Content Gap Analysis Algorithm

```python
def analyze_content_gap(source_domain, competitor_domains, filters):
    """
    Find keyword opportunities where competitors rank but source doesn't
    """
    
    # Get all keywords competitors rank for
    competitor_keywords = set()
    for competitor in competitor_domains:
        keywords = fetch_competitor_keywords(competitor, filters)
        competitor_keywords.update(keywords)
    
    # Get keywords source domain ranks for
    source_keywords = set(fetch_domain_keywords(source_domain))
    
    # Find gaps (keywords only competitors have)
    gap_keywords = competitor_keywords - source_keywords
    
    # Score each gap keyword
    opportunities = []
    for keyword in gap_keywords:
        # Get keyword data
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        # Calculate scores
        difficulty = calculate_keyword_difficulty(keyword_data, serp_data)
        opportunity = calculate_opportunity_score(
            keyword_data, 
            serp_data,
            fetch_domain_data(source_domain)
        )
        
        # Calculate gap score
        # Higher when multiple competitors rank highly
        competitor_positions = [
            pos for comp in competitor_domains 
            for pos in get_keyword_position(comp, keyword)
            if pos
        ]
        
        if competitor_positions:
            avg_competitor_position = sum(competitor_positions) / len(competitor_positions)
            gap_score = (
                opportunity * 0.5 +
                (100 - difficulty) * 0.3 +
                (100 - avg_competitor_position * 10) * 0.2
            )
        else:
            gap_score = 0
        
        opportunities.append({
            'keyword': keyword,
            'difficulty': difficulty,
            'opportunity': opportunity,
            'gap_score': gap_score,
            'competitor_positions': competitor_positions,
            'volume': keyword_data['search_volume'],
            'cpc': keyword_data['cpc_avg']
        })
    
    # Sort by gap score
    opportunities.sort(key=lambda x: x['gap_score'], reverse=True)
    
    return opportunities
```

### 6.6 Machine Learning for Keyword Clustering

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class KeywordClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def cluster_keywords(self, keywords, n_clusters=10):
        """
        Group similar keywords into topic clusters
        """
        
        # Vectorize keywords using TF-IDF
        keyword_texts = [kw['keyword'] for kw in keywords]
        tfidf_matrix = self.vectorizer.fit_transform(keyword_texts)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Reduce dimensionality for visualization
        pca = PCA(n_components=2)
        coords = pca.fit_transform(tfidf_matrix.toarray())
        
        # Group keywords by cluster
        clusters = {}
        for i, keyword in enumerate(keywords):
            cluster_id = cluster_labels[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'keywords': [],
                    'total_volume': 0,
                    'avg_difficulty': 0,
                    'center': coords[i].tolist()
                }
            
            clusters[cluster_id]['keywords'].append(keyword)
            clusters[cluster_id]['total_volume'] += keyword['search_volume']
        
        # Calculate cluster statistics and labels
        for cluster_id, cluster_data in clusters.items():
            keywords_in_cluster = cluster_data['keywords']
            
            # Calculate average difficulty
            cluster_data['avg_difficulty'] = sum(
                kw['difficulty_score'] for kw in keywords_in_cluster
            ) / len(keywords_in_cluster)
            
            # Generate cluster label (most common terms)
            cluster_label = self.generate_cluster_label(
                [kw['keyword'] for kw in keywords_in_cluster]
            )
            cluster_data['label'] = cluster_label
        
        return clusters
    
    def generate_cluster_label(self, keywords):
        # Extract most common words
        word_freq = {}
        for keyword in keywords:
            for word in keyword.split():
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 2-3 words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        return ' '.join(word for word, _ in top_words)
```

### 6.7 Predictive Analytics

```python
class RankingPredictor:
    def predict_ranking_potential(self, target_url, keyword, current_ranking):
        """
        Predict likelihood of ranking improvement
        Uses historical data and ML model
        """
        
        # Extract features
        features = self.extract_features(target_url, keyword, current_ranking)
        
        # Load trained model (e.g., Random Forest or XGBoost)
        model = self.load_model()
        
        # Predict probability of improvement
        prediction = model.predict_proba([features])[0]
        
        # Estimate time to rank in top 10
        estimated_days = self.estimate_time_to_rank(features, prediction)
        
        return {
            'probability_top_10': prediction[1],
            'probability_top_3': prediction[2] if len(prediction) > 2 else 0,
            'estimated_days_to_top_10': estimated_days,
            'confidence': self.calculate_confidence(features),
            'recommended_actions': self.generate_recommendations(features)
        }
    
    def extract_features(self, target_url, keyword, current_ranking):
        page_data = fetch_page_data(target_url)
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        return {
            'current_position': current_ranking or 100,
            'page_authority': page_data['page_authority'],
            'domain_authority': page_data['domain_authority'],
            'backlinks_count': page_data['backlinks_count'],
            'content_length': page_data['content_length'],
            'keyword_density': page_data['keyword_density'],
            'keyword_difficulty': keyword_data['difficulty_score'],
            'search_volume': keyword_data['search_volume'],
            'avg_competitor_authority': serp_data['avg_domain_authority'],
            'serp_features_count': len(serp_data['serp_features']),
            'has_featured_snippet': 'featured_snippet' in serp_data['serp_features']
        }
    
    def generate_recommendations(self, features):
        recommendations = []
        
        if features['content_length'] < 1500:
            recommendations.append({
                'priority': 'high',
                'action': 'Increase content length',
                'details': f'Current: {features["content_length"]} words. Target: 2000+ words',
                'impact': 'medium'
            })
        
        if features['backlinks_count'] < 50:
            recommendations.append({
                'priority': 'high',
                'action': 'Build more backlinks',
                'details': f'Current: {features["backlinks_count"]}. Target: 100+ backlinks',
                'impact': 'high'
            })
        
        if features['keyword_density'] < 0.5:
            recommendations.append({
                'priority': 'medium',
                'action': 'Optimize keyword usage',
                'details': 'Include target keyword more naturally in content',
                'impact': 'low'
            })
        
        return recommendations
```

---

## 7. User System

### 7.1 Authentication & Authorization

```python
# JWT token structure
{
    "user_id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": ["keyword_search", "domain_analysis", "rank_tracking"],
    "iat": 1705320000,
    "exp": 1705406400  # 24 hour expiry
}

# API Key structure
{
    "key_id": "ak_live_abc123xyz789",
    "user_id": 12345,
    "name": "Production API Key",
    "permissions": ["keyword_search", "serp_analysis"],
    "rate_limit": 500,  # requests per minute
    "created_at": "2025-01-01T00:00:00Z",
    "last_used_at": "2025-01-15T10:30:00Z"
}
```

### 7.2 Subscription Plans

```yaml
Plans:
  Free:
    price: $0/month
    features:
      keyword_searches: 10/day
      domain_analyses: 3/day
      serp_checks: 10/day
      tracked_keywords: 0
      historical_data: 7 days
      api_access: false
      export: false
      team_members: 1
      
  Pro:
    price: $99/month
    features:
      keyword_searches: 100/day (3000/month)
      domain_analyses: 50/day
      serp_checks: 100/day
      tracked_keywords: 500
      rank_checks_frequency: daily
      historical_data: 90 days
      api_access: true
      api_calls: 10,000/month
      export: true (CSV, Excel)
      team_members: 3
      reports: 10/month
      
  Agency:
    price: $299/month
    features:
      keyword_searches: unlimited
      domain_analyses: unlimited
      serp_checks: unlimited
      tracked_keywords: 5000
      rank_checks_frequency: daily
      historical_data: 2 years
      api_access: true
      api_calls: 100,000/month
      export: true (CSV, Excel, API)
      team_members: 10
      reports: unlimited
      white_label: true
      priority_support: true
      
  Enterprise:
    price: Custom
    features:
      everything_unlimited: true
      dedicated_account_manager: true
      custom_integrations: true
      on_premise_option: true
      sla_guarantee: 99.9%
```

### 7.3 Quota Management

```python
class QuotaManager:
    def check_quota(self, user_id, action_type):
        """
        Check if user has quota remaining for action
        Returns: (allowed: bool, remaining: int, reset_at: datetime)
        """
        
        # Get user plan
        user = fetch_user(user_id)
        plan = PLANS[user.plan_type]
        
        # Get quota limits
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        quota_used = redis.get(quota_key) or 0
        quota_limit = plan['features'][f'{action_type}']
        
        # Check if unlimited
        if quota_limit == 'unlimited':
            return (True, -1, None)
        
        # Check limit
        allowed = int(quota_used) < int(quota_limit)
        remaining = max(0, int(quota_limit) - int(quota_used))
        reset_at = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        
        return (allowed, remaining, reset_at)
    
    def consume_quota(self, user_id, action_type, amount=1):
        """
        Consume quota for action
        """
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        
        # Increment usage
        new_usage = redis.incr(quota_key, amount)
        
        # Set expiry to end of day if first use
        if new_usage == amount:
            redis.expireat(quota_key, datetime.combine(
                date.today() + timedelta(days=1),
                datetime.min.time()
            ))
        
        # Log usage
        log_quota_usage(user_id, action_type, amount)
        
        return new_usage
```

### 7.4 Role-Based Access Control (RBAC)

```python
ROLES = {
    'owner': {
        'permissions': [
            'manage_project',
            'manage_team',
            'view_billing',
            'manage_billing',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'admin': {
        'permissions': [
            'manage_team',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'editor': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data'
        ]
    },
    'viewer': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'view_rankings'
        ]
    }
}

def check_permission(user_id, project_id, permission):
    # Get user's role in project
    membership = fetch_project_membership(user_id, project_id)
    
    if not membership:
        return False
    
    # Check if role has permission
    role_permissions = ROLES[membership.role]['permissions']
    return permission in role_permissions
```

---

## 8. Dashboard & UI Modules

### 8.1 Dashboard Components

#### **8.1.1 Keyword Explorer Module**

```
Components:
├── Search Bar
│   ├── Keyword input with autocomplete
│   ├── Country selector (dropdown with flags)
│   ├── Language selector
│   └── Device type selector (desktop/mobile/tablet)
│
├── Results Table
│   ├── Columns: Keyword, Volume, CPC, Competition, Difficulty, Trend
│   ├── Sortable columns
│   ├── Filterable (volume range, difficulty range)
│   ├── Bulk select for export
│   └── Add to project button
│
├── Keyword Details Panel (expandable row)
│   ├── 12-month trend chart
│   ├── Related keywords list
│   ├── Question keywords
│   ├── SERP features present
│   └── Top 10 ranking URLs
│
└── Sidebar Filters
    ├── Search volume range slider
    ├── Difficulty range slider
    ├── Competition level checkboxes
    ├── SERP features filters
    └── Keyword intent filters (informational, commercial, transactional)

Features:
- Real-time search with debounce (300ms)
- Export to CSV/Excel
- Save search history
- Favorite keywords
- Bulk keyword upload (CSV)
```

#### **8.1.2 Domain Overview Module**

```
Layout:
┌─────────────────────────────────────────────────────────────┐
│ Domain Input & Analysis                                      │
│ [example.com                              ] [Analyze]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Authority: 75│ Backlinks:   │ Org Keywords:│ Est. Traffic:│
│              │ 125,847      │ 45,231       │ 850,000/mo   │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Traffic Trend (Last 12 Months) - Line Chart                 │
│ [Interactive chart showing organic traffic over time]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Top Organic Keywords         │ Top Pages                     │
│ [Sortable table]             │ [Sortable table]              │
│ - Keyword                    │ - URL                         │
│ - Position                   │ - Traffic                     │
│ - Volume                     │ - Keywords                    │
│ - Traffic                    │ - Backlinks                   │
└──────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Backlink Growth              │ Competitors                   │
│ [Area chart]                 │ [List with metrics]           │
│ New vs Lost backlinks        │ - Domain                      │
│                              │ - Authority                   │
│                              │ - Keyword Overlap             │
└──────────────────────────────┴──────────────────────────────┘

Tabs:
- Overview
- Organic Keywords
- Top Pages
- Backlinks
- Competitors
- Historical Data
```

#### **8.1.3 SERP Overview Module**

```
Components:
├── SERP Search
│   ├── Keyword input
│   ├── Location selector (with map)
│   ├── Device type tabs
│   └── Analyze button
│
├── SERP Preview
│   ├── Visual SERP representation
│   ├── Organic results (1-100)
│   ├── Paid ads highlighted
│   ├── SERP features marked
│   └── Each result expandable for details
│
├── SERP Analysis
│   ├── Difficulty score gauge
│   ├── Opportunity score gauge
│   ├── Avg domain authority
│   ├── Avg backlinks
│   ├── Content length avg
│   └── SERP features breakdown
│
├── Competitor Analysis Table
│   ) = 'desktop'
    
    @validator('keyword')
    def sanitize_keyword(cls, v):
        # Remove potentially dangerous characters
        return v.strip().lower()

# SQL injection prevention (using ORM)
def search_keywords(keyword_text):
    # Safe - using parameterized query
    keywords = session.query(Keyword)\
        .filter(Keyword.keyword_normalized.ilike(f'%{keyword_text}%'))\
        .all()
    
    # NEVER do this:
    # query = f"SELECT * FROM keywords WHERE keyword LIKE '%{keyword_text}%'"
    # results = session.execute(query)  # VULNERABLE TO SQL INJECTION
    
    return keywords

# XSS prevention
from markupsafe import escape

def sanitize_user_input(text):
    return escape(text)

# CSRF protection
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/api/v1/keywords', methods=['POST'])
@csrf.exempt  # Only for API routes with token auth
def create_keyword():
    # CSRF protection not needed for token-authenticated APIs
    pass
```

#### **9.3.3 Data Encryption**

```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self):
        self.key = settings.ENCRYPTION_KEY.encode()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()
    
    def decrypt(self, encrypted_data):
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data).decode()

# Encrypt API keys in database
def store_api_key(user_id, api_key):
    encrypted_key = encryptor.encrypt(api_key)
    session.add(APIKey(
        user_id=user_id,
        encrypted_key=encrypted_key
    ))
    session.commit()

# Use HTTPS everywhere
# Force HTTPS redirect
@app.before_request
def force_https():
    if not request.is_secure and not app.debug:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

#### **9.3.4 Security Headers**

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response
```

### 9.4 Monitoring & Observability

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

cache_hit_rate = Gauge(
    'cache_hit_rate',
    'Cache hit rate percentage',
    ['cache_layer']
)

# Logging
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

logger.info('API request', extra={
    'user_id': user_id,
    'endpoint': request.path,
    'method': request.method,
    'response_time': response_time,
    'status_code': status_code
})

# APM with Datadog
from ddtrace import tracer

@tracer.wrap('keyword.search')
def search_keyword(keyword):
    with tracer.trace('database.query'):
        result = db.query(keyword)
    
    with tracer.trace('cache.set'):
        cache.set(keyword, result)
    
    return result
```

---

## 10. Future Enhancements

### 10.1 AI-Powered Features

```
1. Semantic Keyword Expansion
   - Use NLP models (BERT, GPT) to find semantically related keywords
   - Understand search intent beyond exact match
   - Generate keyword variations based on meaning

2. Content Optimization AI
   - Analyze top-ranking content
   - Generate content briefs with AI
   - Suggest content improvements
   - Predict ranking potential before publishing

3. Automated Competitor Analysis
   - ML-based competitor identification
   - Automatic strategy recommendations
   - Predict competitor moves

4. Smart Alerts
   - Anomaly detection for ranking drops
   - Predictive alerts (warning before drop)
   - Opportunity alerts (emerging trends)
```

### 10.2 Advanced Analytics

```
1. Attribution Modeling
   - Track which keywords drive conversions
   - Multi-touch attribution
   - ROI calculation per keyword

2. Predictive Analytics
   - Forecast traffic growth
   - Predict ranking timeline
   - Estimate budget needed for rankings

3. Custom Dashboards
   - Drag-and-drop dashboard builder
   - Custom metrics and KPIs
   - Real-time data visualization
```

### 10.3 Integrations

```
1. Google Analytics Integration
   - Import actual traffic data
   - Compare estimates vs actuals
   - Track conversions

2. Google Search Console Deep Integration
   - Automatic project setup
   - Real-time ranking updates
   - Click/impression data

3. CMS Integrations
   - WordPress plugin
   - Shopify app
   - Content suggestions in editor

4. Browser Extension
   - On-page SEO analysis
   - Competitor analysis while browsing
   - Quick SERP checks from search results
```

### 10.4 Enterprise Features

```
1. White-Label Platform
   - Custom branding
   - Custom domain
   - Reseller program

2. API Marketplace
   - Allow third-party integrations
   - Developer platform
   - Webhooks for events

3. Advanced Collaboration
   - Approval workflows
   - Task management
   - Team performance tracking

4. SLA & Support
   - Dedicated account managers
   - 24/7 priority support
   - Custom SLA agreements
```

---

## 11. Cloud Architecture Recommendation

### AWS Architecture (Recommended)

```
Region: Multi-region (us-east-1 primary, eu-west-1 secondary)

Compute:
├── ECS Fargate for microservices
├── Lambda for serverless functions
├── EC2 for crawler workers (Spot Instances)
└── Auto Scaling Groups

Storage:
├── RDS PostgreSQL Multi-AZ
│   ├── db.r6g.2xlarge (primary)
│   ├── Read replicas (3x)
│   └── Automated backups + snapshots
├── DocumentDB (MongoDB-compatible)
│   └── 3-node cluster
├── ElastiCache Redis Cluster
│   └── 6 nodes (3 shards, 2 replicas each)
├── S3 buckets
│   ├── SERP screenshots
│   ├── Report PDFs
│   ├── Backlink archives
│   └── Static assets
└── EFS for shared file storage

Networking:
├── VPC with public/private subnets
├── Application Load Balancer
├── NAT Gateway for private subnets
├── VPC Peering for multi-region
└── CloudFront CDN

Queues & Messaging:
├── SQS for job queues
├── SNS for notifications
└── EventBridge for scheduled tasks

Monitoring:
├── CloudWatch for metrics/logs
├── X-Ray for distributed tracing
├── CloudWatch Alarms
└── AWS Systems Manager

Security:
├── IAM roles and policies
├── Secrets Manager for credentials
├── KMS for encryption
├── WAF for API protection
├── Shield Standard (DDoS)
└── Certificate Manager for SSL

Estimated Monthly Cost:
├── Compute (ECS): $800-1,500
├── Databases: $2,000-4,000
├── Cache (Redis): $500-800
├── Storage (S3): $300-600
├── Data Transfer: $400-800
├── CloudFront: $200-400
├── Monitoring: $100-200
├── Other services: $200-400
└── Total: $4,500-8,700/month
   (Can be optimized with Reserved Instances: -40%)
```

### GCP Architecture (Alternative)

```
Region: Multi-region (us-central1, europe-west1)

Compute:
├── Cloud Run for microservices (serverless)
├── GKE for Kubernetes orchestration
├── Compute Engine Spot VMs for crawlers
└── Cloud Functions for event-driven tasks

Storage:
├── Cloud SQL PostgreSQL (HA)
├── MongoDB Atlas (GCP marketplace)
├── Memorystore Redis (HA)
├── Cloud Storage buckets
└── Filestore for NFS

Networking:
├── Cloud Load Balancing (Global)
├── Cloud CDN
├── Cloud Armor (DDoS + WAF)
└── VPC with private Google access

Data Processing:
├── Pub/Sub for messaging
├── Cloud Tasks for job queues
├── Cloud Scheduler for cron jobs
└── Dataflow for ETL pipelines

Monitoring:
├── Cloud Monitoring (Stackdriver)
├── Cloud Logging
├── Cloud Trace
└── Error Reporting

Security:
├── Cloud IAM
├── Secret Manager
├── Cloud KMS
├── Binary Authorization
└── VPC Service Controls

Estimated Monthly Cost:
├── Similar to AWS: $4,000-8,000/month
└── Benefits: Better global networking, simpler pricing
```

### 11.1 Disaster Recovery Plan

```yaml
Backup Strategy:
  Databases:
    - Automated daily backups (retained 30 days)
    - Weekly backups (retained 90 days)
    - Monthly backups (retained 1 year)
    - Point-in-time recovery (7 days)
    - Cross-region backup replication
  
  Redis:
    - Snapshot every 6 hours
    - AOF (Append Only File) enabled
    - Automatic failover to replica
  
  Files (S3):
    - Versioning enabled
    - Cross-region replication
    - Lifecycle policies (archive to Glacier after 90 days)

Recovery Time Objectives (RTO):
  - Critical services (Auth, API Gateway): 5 minutes
  - Core services (Keyword, Domain): 15 minutes
  - Background workers: 30 minutes
  - Full system: 1 hour

Recovery Point Objectives (RPO):
  - Transactional data: 5 minutes
  - Cached data: Acceptable loss
  - User data: Zero data loss
  - Analytics data: 1 hour acceptable loss

Disaster Recovery Procedures:
  1. Database Failure:
     - Promote read replica to primary
     - Update DNS to point to new primary
     - Restore application connections
  
  2. Region Failure:
     - Activate secondary region
     - Route traffic via CloudFlare
     - Sync data from backups
  
  3. Data Corruption:
     - Restore from point-in-time backup
     - Replay transaction logs
     - Validate data integrity
  
  4. Ransomware/Security Breach:
     - Isolate affected systems
     - Restore from clean backups
     - Audit and patch vulnerabilities
```

---

## 12. Implementation Roadmap

### Phase 1: MVP (3-4 months)

```
Month 1: Foundation
Week 1-2: Infrastructure Setup
  - Set up AWS/GCP accounts
  - Configure VPC, subnets, security groups
  - Deploy PostgreSQL and Redis
  - Set up CI/CD pipeline

Week 3-4: Core Backend
  - User authentication system
  - API Gateway setup
  - Database schema creation
  - Basic API endpoints

Month 2: Core Features
Week 1-2: Keyword Research
  - Google Ads API integration
  - Keyword search endpoint
  - Basic keyword metrics
  - Results caching

Week 3-4: Domain Analysis
  - Domain metrics calculation
  - Backlink data structure
  - Third-party API integrations
  - Domain overview endpoint

Month 3: Frontend & Polish
Week 1-2: Dashboard Development
  - React/Next.js setup
  - Keyword Explorer UI
  - Domain Overview UI
  - Authentication flow

Week 3-4: Testing & Launch Prep
  - End-to-end testing
  - Performance optimization
  - Security audit
  - Documentation

Month 4: Beta Launch
Week 1-2: Beta Testing
  - Invite beta users
  - Gather feedback
  - Bug fixes
  - Performance tuning

Week 3-4: Public Launch
  - Marketing site
  - Payment integration (Stripe)
  - Email notifications
  - Launch! 🚀

MVP Features:
✅ User registration and authentication
✅ Keyword research (volume, CPC, difficulty)
✅ Domain analysis (authority, backlinks, keywords)
✅ SERP analysis
✅ Basic reporting
✅ 3 subscription plans
✅ API access (Pro and above)
```

### Phase 2: Growth (Months 5-8)

```
Month 5-6: Rank Tracking
  - Keyword tracking setup
  - Daily rank checks
  - Historical data storage
  - Email alerts
  - Competitor tracking

Month 7-8: Advanced Features
  - Content gap analysis
  - Trend analysis
  - Backlink discovery
  - Advanced filtering
  - Bulk operations
  - Team collaboration

New Features:
✅ Rank tracking (500+ keywords)
✅ Content gap analysis
✅ Competitor comparison
✅ Advanced reports (PDF export)
✅ Team workspaces
✅ API rate limit increase
```

### Phase 3: Scale (Months 9-12)

```
Month 9-10: Enterprise Features
  - White-label platform
  - Custom branding
  - Advanced team management
  - SSO integration
  - SLA guarantees

Month 11-12: AI & Automation
  - ML-powered keyword suggestions
  - Content optimization AI
  - Predictive analytics
  - Automated recommendations
  - Smart alerts

Enterprise Features:
✅ White-label solution
✅ Unlimited tracking
✅ AI-powered insights
✅ Predictive analytics
✅ Custom integrations
✅ Dedicated support
```

---

## 13. Success Metrics & KPIs

### 13.1 Business Metrics

```yaml
User Acquisition:
  - Monthly Active Users (MAU)
  - Sign-up conversion rate
  - Free to Paid conversion: Target 10-15%
  - Churn rate: Target <5% monthly

Revenue:
  - Monthly Recurring Revenue (MRR)
  - Annual Recurring Revenue (ARR)
  - Average Revenue Per User (ARPU)
  - Customer Lifetime Value (LTV)
  - Customer Acquisition Cost (CAC)
  - LTV:CAC ratio: Target >3:1

Product Usage:
  - Daily Active Users (DAU)
  - Features used per session
  - Average session duration
  - Keywords searched per user/month
  - Domains analyzed per user/month
  - API calls per user/month

Customer Satisfaction:
  - Net Promoter Score (NPS): Target >50
  - Customer Satisfaction (CSAT): Target >4.5/5
  - Support ticket response time: <2 hours
  - Support resolution time: <24 hours
```

### 13.2 Technical Metrics

```yaml
Performance:
  - API response time: p50 <200ms, p99 <1s
  - Page load time: <2 seconds
  - Time to interactive: <3 seconds
  - Database query time: p99 <100ms
  - Cache hit rate: >80%
  - CDN hit rate: >90%

Reliability:
  - Uptime: 99.9% (8.76 hours downtime/year)
  - Error rate: <0.1%
  - Failed jobs rate: <1%
  - Data accuracy: >98%

Scalability:
  - Concurrent users supported: 100,000+
  - API requests per second: 10,000+
  - Database connections: 1,000+
  - Queue throughput: 100,000 jobs/hour

Security:
  - Mean time to detect (MTTD): <1 hour
  - Mean time to respond (MTTR): <4 hours
  - Vulnerability patch time: <24 hours
  - Security audit: Quarterly
```

---

## 14. Cost Analysis

### 14.1 Infrastructure Costs (Monthly)

```yaml
AWS Infrastructure (Mid-scale):
  Compute:
    - ECS Fargate (10 services, 2GB each): $800
    - EC2 crawler workers (10 t3.large spot): $300
    - Lambda functions: $100
    - Total: $1,200
  
  Databases:
    - RDS PostgreSQL (db.r6g.2xlarge): $1,200
    - Read replicas (3x db.r6g.large): $900
    - DocumentDB (3 nodes): $600
    - Total: $2,700
  
  Cache & Storage:
    - ElastiCache Redis (6 nodes): $600
    - S3 storage (10TB): $240
    - Data transfer: $400
    - Total: $1,240
  
  Networking:
    - Load balancers: $150
    - CloudFront CDN: $300
    - Data transfer: $200
    - Total: $650
  
  Other Services:
    - CloudWatch: $100
    - Backup storage: $80
    - Secrets Manager: $20
    - Total: $200
  
  Grand Total: $5,990/month
  
  With Reserved Instances (1-year): -30% = $4,193/month
  With 3-year Reserved: -60% = $2,396/month

External Services:
  - Proxy services (Bright Data): $500-2,000/month
  - CAPTCHA solving (2Captcha): $100-300/month
  - Third-party APIs (DataForSEO): $500-2,000/month
  - Email service (SendGrid): $50-200/month
  - Error tracking (Sentry): $50/month
  - APM (Datadog): $300/month
  - Total external: $1,500-5,000/month

Total Monthly Infrastructure: $6,000-10,000
```

### 14.2 Team & Operational Costs

```yaml
Development Team (Minimum Viable):
  - Tech Lead / Architect: $150k-200k/year
  - Backend Engineers (2): $120k-150k/year each
  - Frontend Engineer (1): $110k-140k/year
  - DevOps Engineer (1): $130k-160k/year
  - QA Engineer (1): $90k-120k/year
  - Total: $720k-920k/year ($60k-77k/month)

Product & Business:
  - Product Manager: $120k-150k/year
  - UI/UX Designer: $90k-120k/year
  - Marketing Manager: $80k-110k/year
  - Customer Success (2): $60k-80k/year each
  - Total: $410k-540k/year ($34k-45k/month)

Total Team Cost: $1.13M-1.46M/year ($94k-122k/month)

Other Costs:
  - Office/Co-working: $2k-5k/month
  - Software licenses: $1k-2k/month
  - Legal/Accounting: $2k-5k/month
  - Marketing/Ads: $5k-20k/month
  - Total: $10k-32k/month

Grand Total Operating Cost: $110k-165k/month
```

### 14.3 Revenue Model

```yaml
Revenue Projections (Conservative):

Year 1:
  Month 1-3 (Beta): 100 users, 10 paying ($99 avg)
    - MRR: $990
  Month 4-6 (Launch): 500 users, 75 paying
    - MRR: $7,425
  Month 7-9 (Growth): 2,000 users, 350 paying
    - MRR: $34,650
  Month 10-12 (Scale): 5,000 users, 900 paying
    - MRR: $89,100
  Year 1 ARR: ~$400k

Year 2:
  - 20,000 users, 4,000 paying (20% conversion)
  - MRR: $396,000
  - ARR: $4.75M

Year 3:
  - 50,000 users, 12,000 paying (24% conversion)
  - MRR: $1.19M
  - ARR: $14.3M

Break-even Analysis:
  - Monthly costs: $120k
  - Break-even MRR: $120k
  - Required paying users: 1,200 at $99/month
  - Timeline: Month 10-11 of Year 1
```

---

## 15. Competitive Analysis

### 15.1 Major Competitors

```yaml
Ahrefs:
  Strengths:
    - Industry-leading backlink database
    - Excellent crawler (AhrefsBot)
    - Site audit features
    - Content Explorer
  Weaknesses:
    - Expensive ($99-999/month)
    - Steep learning curve
    - Limited free tier
  Market Position: Premium, professional

SEMrush:
  Strengths:
    - All-in-one SEO platform
    - PPC and social media tools
    - Large keyword database
    - Content marketing tools
  Weaknesses:
    - Expensive ($119-449/month)
    - Overwhelming interface
    - Data accuracy issues
  Market Position: Comprehensive, enterprise

Moz:
  Strengths:
    - User-friendly interface
    - Good educational content
    - Domain Authority metric (widely used)
    - Free tools available
  Weaknesses:
    - Smaller database than competitors
    - Slower updates
    - Limited international data
  Market Position: User-friendly, SMB

Ubersuggest:
  Strengths:
    - Affordable ($29-99/month)
    - Simple, clean interface
    - Good for beginners
    - Lifetime deal available
  Weaknesses:
    - Limited data depth
    - Basic features
    - Less accurate metrics
  Market Position: Budget-friendly, beginners

Our Differentiation:
  1. Pricing: More affordable than Ahrefs/SEMrush
  2. UX: Simpler than SEMrush, more powerful than Ubersuggest
  3. API: Developer-friendly with generous limits
  4. Real-time: Faster data updates
  5. AI: ML-powered insights and recommendations
  6. Transparency: Clear pricing, no hidden limits
```

### 15.2 Competitive Pricing

```
Competitor Pricing Comparison:

Ahrefs:
  - Lite: $99/month (500 keywords tracked)
  - Standard: $199/month (1,500 keywords)
  - Advanced: $399/month (5,000 keywords)
  - Enterprise: $999/month (10,000 keywords)

SEMrush:
  - Pro: $119/month (500 keywords)
  - Guru: $229/month (1,500 keywords)
  - Business: $449/month (5,000 keywords)

Moz:
  - Standard: $99/month (300 keywords)
  - Medium: $179/month (1,500 keywords)
  - Large: $299/month (3,000 keywords)
  - Premium: $599/month (7,500 keywords)

Ubersuggest:
  - Individual: $29/month (25 keywords)
  - Business: $49/month (75 keywords)
  - Enterprise: $99/month (150 keywords)

Our Pricing (Competitive):
  - Free: $0 (10 keywords/day)
  - Pro: $99/month (500 keywords tracked)
  - Agency: $299/month (5,000 keywords)
  - Enterprise: Custom (unlimited)

Value Proposition:
  - 30% cheaper than Ahrefs/SEMrush
  - More features than Ubersuggest
  - Better UX than all competitors
  - Generous API access
```

---

## 16. Go-to-Market Strategy

### 16.1 Launch Strategy

```yaml
Pre-Launch (Month -2 to 0):
  1. Build landing page
     - Value proposition
     - Features overview
     - Pricing table
     - Email signup (waitlist)
  
  2. Content marketing
     - SEO blog posts (10-15 articles)
     - YouTube tutorials
     - Free tools (keyword generator, SERP checker)
  
  3. Beta program
     - Invite 100 beta users
     - Gather feedback
     - Build case studies
     - Generate testimonials
  
  4. Partnership outreach
     - SEO agencies
     - Marketing consultants
     - Web design firms
     - Affiliate program setup

Launch (Month 1-3):
  1. Product Hunt launch
  2. Social media campaign
  3. SEO community outreach (Reddit, forums)
  4. Influencer partnerships
  5. Paid ads (Google, Facebook)
  6. Content calendar (2-3 posts/week)
  7. Email drip campaigns
  8. Webinars and demos

Growth (Month 4-12):
  1. SEO content strategy
  2. Affiliate program expansion
  3. Partner ecosystem
  4. Case studies and ROI calculators
  5. Integration marketplace
  6. Referral program
  7. Community building (Slack, Discord)
  8. Conference sponsorships
```

### 16.2 Customer Acquisition Channels

```yaml
Organic Channels (60% of traffic):
  1. SEO Blog Content
     - "How to" guides
     - Keyword research tutorials
     - SEO best practices
     - Competitor comparison pages
     - Target: 50,000 organic visits/month by Month 6
  
  2. Free Tools
     - Free keyword research tool
     - Domain authority checker
     - SERP preview tool
     - Backlink checker (limited)
     - Conversion rate: 5-10% to signup
  
  3. YouTube Channel
     - Tutorial videos
     - Tool walkthroughs
     - SEO tips
     - Target: 10,000 subscribers by Month 12

Paid Channels (25% of traffic):
  1. Google Ads
     - Target keywords: "keyword research tool", "SEO software"
     - Budget: $3,000-5,000/month
     - CPA target: $30-50
  
  2. Facebook/LinkedIn Ads
     - Target: Marketing professionals, agencies
     - Retargeting campaigns
     - Budget: $2,000-3,000/month
  
  3. Comparison Site Ads
     - Capterra, G2, Software Advice
     - Budget: $500-1,000/month

Partnerships (15% of traffic):
  1. Affiliate Program
     - 20-30% recurring commission
     - Target: 50 active affiliates
  
  2. Agency Partners
     - White-label offering
     - Revenue share
  
  3. Integration Partners
     - WordPress, Shopify, etc.
     - Co-marketing opportunities
```

---

## 17. Conclusion

### Summary

This comprehensive system design provides a **production-ready blueprint** for building an enterprise-grade SEO analysis platform comparable to Ahrefs, SEMrush, and Ubersuggest. The architecture is designed for:

✅ **Scalability**: Handles millions of keywords and domains  
✅ **Performance**: Sub-second API responses with intelligent caching  
✅ **Reliability**: 99.9% uptime with disaster recovery  
✅ **Security**: Enterprise-grade authentication and data protection  
✅ **Cost-Efficiency**: Optimized infrastructure with ~$6k-10k monthly costs  
✅ **Extensibility**: Modular design for easy feature additions  

### Key Technical Decisions

1. **Hybrid Architecture**: Microservices for flexibility, shared database for performance
2. **Multi-Database Strategy**: PostgreSQL (relational), MongoDB (documents), Redis (cache), Elasticsearch (search)
3. **Async Processing**: Queue-based workers for scalability
4. **Intelligent Caching**: 3-layer cache (L1: memory, L2: Redis, L3: CDN)
5. **Data Sharding**: Horizontal partitioning for massive datasets
6. **API-First Design**: RESTful APIs with optional GraphQL

### Implementation Priorities

**Phase 1 (Months 1-4)**: MVP with core features  
**Phase 2 (Months 5-8)**: Rank tracking and advanced features  
**Phase 3 (Months 9-12)**: Enterprise and AI-powered features  

### Success Factors

- **Data Accuracy**: Primary competitive advantage
- **User Experience**: Simpler than competitors
- **Pricing**: 30% cheaper than premium tools
- **API Access**: Developer-friendly with generous limits
- **Performance**: Faster than existing solutions

### Risk Mitigation

- **API Rate Limits**: Diversified data sources + proprietary crawler
- **Data Freshness**: Intelligent caching with background updates
- **Scalability**: Auto-scaling from day one
- **Competition**: Differentiation through UX, pricing, and API

---

## Appendix: Quick Reference

### Essential API Endpoints

```
POST /api/v1/keywords/search
GET  /api/v1/keywords/{id}
POST /api/v1/keywords/bulk
GET  /api/v1/domains/{domain}/overview
GET  /api/v1/domains/{domain}/backlinks
GET  /api/v1/domains/{domain}/organic-keywords
POST /api/v1/serp/analyze
GET  /api/v1/tracking/projects/{id}/rankings
POST /api/v1/analysis/content-gap
GET  /api/v1/trends/keywords
```

### Database Tables Summary

```
Core Tables:
- users, subscriptions, user_quotas
- projects, project_members
- keywords, keyword_metrics, keyword_trends
- domains, domain_metrics, backlinks
- serp_results, serp_positions
- tracking_projects, tracked_keywords, ranking_history

Total Tables: 30+
Indexes: 100+
Partitions: Time-series tables (monthly)
Sharding: Keywords, domains, backlinks
```

### Tech Stack at a Glance

```
Backend: Python (FastAPI), Node.js
Frontend: Next.js (React), TailwindCSS
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
Queue: RabbitMQ or AWS SQS
Cache: Redis Cluster, CloudFlare CDN
Search: Elasticsearch
Monitoring: Prometheus, Grafana, Datadog
Cloud: AWS (recommended) or GCP
```

### Cost Summary

```
Infrastructure: $6k-10k/month
Team: $94k-122k/month
Total Operating: $100k-132k/month

Break-even: 1,200 paying users ($99/month)
Timeline: Month 10-11 of Year 1
```

---

**End of System Design Document**

*This document provides a complete technical blueprint for building a world-class SEO analysis platform. All architectural decisions are based on proven patterns used by successful SaaS companies at scale.*# 🎯 Keyword Research & SEO Analysis Platform
## Complete System Design Document

> **Version:** 1.0  
> **Architecture Type:** Microservices with Event-Driven Components  
> **Scale Target:** 10M+ keywords, 1M+ domains, 100K+ concurrent users

---

## 📋 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Data Flow & Processing](#2-data-flow--processing)
3. [Database Design](#3-database-design)
4. [API Layer Design](#4-api-layer-design)
5. [Crawler & Data Sources](#5-crawler--data-sources)
6. [Ranking & Analytics Engine](#6-ranking--analytics-engine)
7. [User System](#7-user-system)
8. [Dashboard & UI Modules](#8-dashboard--ui-modules)
9. [Scalability, Performance & Security](#9-scalability-performance--security)
10. [Future Enhancements](#10-future-enhancements)

---

## 1. Architecture Overview

### 1.1 System Architecture Pattern

**Hybrid Microservices Architecture** with the following characteristics:
- Core services as independent microservices
- Shared data access layer for performance
- Event-driven communication for async operations
- API Gateway for unified access point

### 1.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  [Web Dashboard] [Mobile App] [Browser Extension] [API Clients] │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CDN LAYER (CloudFlare)                      │
│              [Static Assets] [API Response Cache]                │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY (Kong/AWS ALB)                    │
│    [Rate Limiting] [Auth] [Routing] [Request Validation]        │
└─────┬───────────┬──────────┬──────────┬────────────┬───────────┘
      │           │          │          │            │
┌─────▼─────┐ ┌──▼────┐ ┌───▼─────┐ ┌─▼────┐ ┌────▼──────┐
│  Auth     │ │Keyword│ │ Domain  │ │SERP  │ │ Tracking  │
│  Service  │ │Service│ │ Service │ │Svc   │ │  Service  │
└─────┬─────┘ └──┬────┘ └───┬─────┘ └─┬────┘ └────┬──────┘
      │          │          │          │            │
┌─────▼──────────▼──────────▼──────────▼────────────▼───────────┐
│                   MESSAGE QUEUE (RabbitMQ/Kafka)               │
│  [Crawl Jobs] [Data Processing] [Analytics] [Notifications]   │
└──────┬────────────────┬────────────────┬─────────────┬────────┘
       │                │                │             │
┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐ ┌───▼─────┐
│   Crawler   │  │  Analytics  │  │   Email    │ │ Report  │
│   Workers   │  │   Engine    │  │  Service   │ │ Builder │
└──────┬──────┘  └──────┬──────┘  └─────┬──────┘ └───┬─────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                      DATA STORAGE LAYER                        │
│ [PostgreSQL] [MongoDB] [Redis] [Elasticsearch] [S3/Object]    │
└────────────────────────────────────────────────────────────────┘
       │                │                │             │
┌──────▼────────────────▼────────────────▼─────────────▼────────┐
│                   EXTERNAL INTEGRATIONS                        │
│ [Google APIs] [Bing APIs] [Third-party SEO] [Proxy Services]  │
└────────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components Breakdown

#### **1.3.1 Frontend Layer**
- **Web Dashboard**: React/Next.js with SSR for SEO
- **Mobile Apps**: React Native for iOS/Android
- **Browser Extension**: Chrome/Firefox for on-page analysis
- **Component Library**: Shared UI components (charts, tables, forms)

#### **1.3.2 API Gateway**
- **Technology**: Kong API Gateway or AWS Application Load Balancer
- **Responsibilities**:
  - Request routing to microservices
  - Authentication token validation
  - Rate limiting and throttling
  - Request/response transformation
  - API versioning (v1, v2)
  - Logging and monitoring

#### **1.3.3 Microservices**

**Auth Service**
- User authentication and authorization
- JWT token management
- OAuth integration (Google, Facebook)
- API key generation and validation
- Session management

**Keyword Service**
- Keyword search and suggestions
- Keyword metrics (volume, CPC, competition)
- Related keywords and questions
- Keyword difficulty calculation
- Multi-language support

**Domain Service**
- Domain overview and metrics
- Backlink analysis
- Top pages analysis
- Organic keyword tracking
- Domain authority calculation

**SERP Service**
- SERP position tracking
- Featured snippets detection
- Local pack results
- Ads analysis
- SERP feature identification

**Tracking Service**
- Keyword rank tracking
- Position monitoring
- Ranking history
- Competitor tracking
- Alert system for rank changes

**Analytics Engine**
- Trend analysis
- Opportunity scoring
- Content gap analysis
- Competitive intelligence
- Predictive analytics

**Crawler Service**
- Distributed web crawler
- SERP scraping
- Backlink discovery
- Site auditing
- Content extraction

**Report Builder**
- PDF report generation
- Scheduled reports
- White-label reports
- Data export (CSV, Excel)

#### **1.3.4 Data Storage Components**

**PostgreSQL** (Primary Relational Database)
- User accounts and subscriptions
- Projects and settings
- Normalized keyword and domain data
- Transactional data

**MongoDB** (Document Store)
- Raw crawl data
- SERP snapshots
- Historical data
- Flexible schema data

**Redis** (Caching Layer)
- Session cache
- API response cache
- Real-time ranking cache
- Queue management
- Rate limiting counters

**Elasticsearch**
- Full-text keyword search
- Log aggregation and search
- Analytics queries
- Real-time suggestions

**S3/Object Storage**
- Backlink data archives
- Historical SERP screenshots
- Report files
- User uploads

### 1.4 Technology Stack Recommendation

#### **Backend Stack**
```
Language: Python 3.11+ (Primary), Node.js (Real-time services)
Frameworks: 
  - FastAPI (API services) - High performance, async
  - Django (Admin panel, complex business logic)
  - Express.js (Real-time notifications)
  
Task Queue: Celery with RabbitMQ or AWS SQS
Background Workers: Celery workers (CPU-intensive), Node workers (I/O)
Caching: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+
Message Broker: RabbitMQ or Apache Kafka (for high throughput)
```

#### **Frontend Stack**
```
Framework: Next.js 14+ (React with SSR/SSG)
State Management: Zustand or Redux Toolkit
UI Library: TailwindCSS + shadcn/ui components
Charts: Recharts or Apache ECharts
Data Tables: TanStack Table
Forms: React Hook Form + Zod validation
API Client: Axios with React Query for caching
```

#### **Database Stack**
```
Primary: PostgreSQL 15+ with Citus extension (for sharding)
Document: MongoDB 6+ with replica sets
Cache: Redis 7+ with Redis Cluster
Search: Elasticsearch 8+ with ILM policies
Time-series: TimescaleDB (extension on PostgreSQL) for tracking data
```

#### **Infrastructure**
```
Container: Docker + Docker Compose (dev), Kubernetes (production)
Orchestration: Kubernetes (EKS/GKE) or AWS ECS
CI/CD: GitHub Actions or GitLab CI
Monitoring: Prometheus + Grafana, ELK Stack
APM: New Relic or Datadog
Error Tracking: Sentry
```

#### **External Services**
```
CDN: CloudFlare Enterprise
Email: SendGrid or AWS SES
Payment: Stripe
Analytics: Mixpanel, Google Analytics 4
Search APIs: Google Custom Search API, Bing Web Search API
Proxy Services: ScraperAPI, Bright Data, Oxylabs
```

### 1.5 Scalability Strategy

#### **Horizontal Scaling**
- All services stateless for easy replication
- Auto-scaling based on CPU/memory/queue depth
- Load balancers distribute traffic across instances
- Database read replicas for query distribution

#### **Caching Strategy**

**L1 Cache (Application Level)**
- In-memory caching in each service instance
- LRU cache with 5-minute TTL for hot data
- Size limit: 512MB per instance

**L2 Cache (Redis)**
```
Keyword Metrics: TTL 24 hours
Domain Overview: TTL 12 hours  
SERP Results: TTL 6 hours
User Sessions: TTL 30 minutes
API Responses: TTL based on data freshness
Rate Limiting: Real-time, no TTL
```

**L3 Cache (CDN)**
- Static assets: 1 year cache
- API responses: 5 minutes cache with stale-while-revalidate
- Images and fonts: 6 months cache

#### **Database Sharding Strategy**

**PostgreSQL Sharding** (using Citus)
```
Shard Key: domain_hash (for domain data)
Shard Key: keyword_hash (for keyword data)
Shard Key: user_id (for user data)

Distribution:
- 32 shards for keyword data (hash distribution)
- 16 shards for domain data
- 8 shards for user/project data
```

**MongoDB Sharding**
```
Shard Key: {country: 1, language: 1, keyword_hash: 1}
Zones: US, EU, ASIA for geographic distribution
Chunk Size: 64MB
```

### 1.6 Queue and Worker Setup

#### **Task Queue Architecture**

```
┌─────────────────────────────────────────────────────┐
│                  TASK PRODUCERS                      │
│  [API Services] [Scheduled Jobs] [User Actions]     │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│              MESSAGE BROKER (RabbitMQ)              │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ crawl_queue  │  │ analytics_q  │  │ email_q  │ │
│  │ Priority: 1  │  │ Priority: 2  │  │Priority:3│ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└──┬──────────┬──────────────┬────────────┬─────────┘
   │          │              │            │
┌──▼────┐ ┌──▼────┐  ┌──────▼─────┐  ┌──▼──────┐
│Crawler│ │SERP   │  │ Analytics  │  │  Email  │
│Worker │ │Worker │  │  Worker    │  │ Worker  │
│x20    │ │x10    │  │  x5        │  │  x3     │
└───────┘ └───────┘  └────────────┘  └─────────┘
```

#### **Worker Types and Configuration**

**1. Crawler Workers** (CPU + Network intensive)
```
Count: 20-50 workers (auto-scale)
Resources: 2 CPU, 4GB RAM per worker
Tasks:
  - SERP crawling (priority: high)
  - Backlink discovery (priority: medium)
  - Site auditing (priority: low)
  - Content extraction
Max Concurrency: 5 tasks per worker
Retry Strategy: Exponential backoff (max 3 retries)
Timeout: 60 seconds per task
```

**2. Analytics Workers** (CPU intensive)
```
Count: 5-10 workers
Resources: 4 CPU, 8GB RAM per worker
Tasks:
  - Keyword difficulty calculation
  - Domain authority scoring
  - Trend analysis
  - Content gap analysis
  - Opportunity scoring
Max Concurrency: 3 tasks per worker
Timeout: 120 seconds per task
```

**3. Data Processing Workers** (Memory intensive)
```
Count: 10-20 workers
Resources: 2 CPU, 8GB RAM per worker
Tasks:
  - Bulk data import
  - Data enrichment
  - Metric aggregation
  - Historical data processing
Max Concurrency: 2 tasks per worker
Batch Size: 1000 records per batch
```

**4. Notification Workers** (I/O intensive)
```
Count: 3-5 workers
Resources: 1 CPU, 2GB RAM per worker
Tasks:
  - Email notifications
  - Webhook delivery
  - Report generation
  - Alert processing
Max Concurrency: 10 tasks per worker
Timeout: 30 seconds per task
```

#### **Queue Priority System**
```
Priority 1 (Highest): Real-time user requests
Priority 2 (High): Scheduled tracking updates
Priority 3 (Medium): Background data refresh
Priority 4 (Low): Bulk data processing
Priority 5 (Lowest): Analytics and reports
```

---

## 2. Data Flow & Processing

### 2.1 Primary Workflows

#### **2.1.1 Keyword Research Workflow**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: User Input                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ User enters: "best running shoes"                       │ │
│ │ Filters: Country=US, Language=EN, Device=Desktop        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 2: Request Processing (API Gateway)                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ • Validate JWT token                                     │ │
│ │ • Check rate limits (100 req/min for Pro plan)          │ │
│ │ • Normalize keyword (lowercase, trim)                   │ │
│ │ • Generate cache key: "kw:en:us:desktop:best_running..."│ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 3: Cache Lookup (Redis L2 Cache)                       │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ GET cache_key                                            │ │
│ │ TTL: 24 hours                                            │ │
│ │                                                          │ │
│ │ IF FOUND → Return cached response (80% of requests)     │ │
│ │ IF NOT FOUND → Continue to Step 4                       │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Cache Miss)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 4: Database Query (PostgreSQL + Elasticsearch)         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Query keywords table:                                    │ │
│ │   SELECT * FROM keywords                                 │ │
│ │   WHERE keyword_normalized = 'best running shoes'        │ │
│ │   AND country = 'US' AND language = 'EN'                │ │
│ │                                                          │ │
│ │ IF FOUND and data_age < 30 days:                        │ │
│ │   → Return from database                                │ │
│ │   → Update cache                                        │ │
│ │ IF NOT FOUND or data_age > 30 days:                     │ │
│ │   → Continue to Step 5 (Fresh Data Fetch)               │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ (Database Miss or Stale)
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 5: External Data Fetch (Async Job)                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Publish job to RabbitMQ: "crawl_queue"                  │ │
│ │ {                                                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "keyword": "best running shoes",                      │ │
│ │   "country": "US",                                      │ │
│ │   "sources": ["google_api", "serp_scraper"],           │ │
│ │   "priority": "high"                                    │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Return immediate response to user:                      │ │
│ │ {                                                        │ │
│ │   "status": "processing",                               │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "estimated_time": "10-30 seconds",                   │ │
│ │   "partial_data": { ... } ← if available               │ │
│ │ }                                                        │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 6: Crawler Worker Processing                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Worker picks up job from queue                          │ │
│ │                                                          │ │
│ │ Parallel data fetching (asyncio):                       │ │
│ │ ┌─────────────┐  ┌─────────────┐  ┌──────────────┐    │ │
│ │ │ Google Ads  │  │ Google      │  │ Third-party  │    │ │
│ │ │ Keyword API │  │ Trends API  │  │ SEO API      │    │ │
│ │ │ (volume,CPC)│  │ (12mo trend)│  │ (difficulty) │    │ │
│ │ └─────────────┘  └─────────────┘  └──────────────┘    │ │
│ │                                                          │ │
│ │ Data aggregation and enrichment:                        │ │
│ │ • Calculate average from multiple sources               │ │
│ │ • Compute keyword difficulty score                      │ │
│ │ • Generate related keywords                             │ │
│ │ • Extract questions and suggestions                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 7: Data Storage                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ PostgreSQL:                                              │ │
│ │   INSERT INTO keywords (keyword, country, language, ...) │ │
│ │   INSERT INTO keyword_metrics (keyword_id, volume, ...)  │ │
│ │   INSERT INTO keyword_trends (keyword_id, month, ...)    │ │
│ │                                                          │ │
│ │ Elasticsearch:                                           │ │
│ │   Index document for fast search and suggestions        │ │
│ │                                                          │ │
│ │ Redis Cache:                                             │ │
│ │   SET cache_key = {data} EX 86400 (24 hours)           │ │
│ │                                                          │ │
│ │ MongoDB (Raw Data Archive):                              │ │
│ │   Store original API responses for audit trail          │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│ STEP 8: WebSocket Notification                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Push update to user's active session:                   │ │
│ │ {                                                        │ │
│ │   "event": "keyword_data_ready",                        │ │
│ │   "job_id": "uuid",                                     │ │
│ │   "data": { full keyword metrics }                      │ │
│ │ }                                                        │ │
│ │                                                          │ │
│ │ Frontend updates UI with full data                      │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

#### **2.1.2 Domain Analysis Workflow**

```
User Input: "example.com"
    ↓
1. Domain Validation & Normalization
   • Check DNS resolution
   • Normalize to canonical form
   • Extract domain metadata
    ↓
2. Cache Check (Redis)
   • Key: "domain:example.com:overview"
   • TTL: 12 hours
   IF FOUND → Return cached data
    ↓
3. Database Lookup (PostgreSQL)
   • Check domains table
   • Check domain_metrics table
   • If data < 7 days old → Return
    ↓
4. Trigger Async Jobs (if needed)
   Job 1: Backlink Crawler
     → Crawl backlink sources
     → Discover new backlinks
     → Update backlink database
   
   Job 2: Organic Keyword Scraper
     → Fetch ranking keywords
     → Update keyword positions
     → Calculate traffic estimates
   
   Job 3: Top Pages Analyzer
     → Crawl sitemap
     → Analyze top-performing pages
     → Calculate page metrics
   
   Job 4: Domain Authority Calculator
     → Aggregate backlink data
     → Apply authority algorithm
     → Update domain score
    ↓
5. Data Aggregation
   • Combine all metrics
   • Calculate derived values
   • Generate summary stats
    ↓
6. Storage & Cache Update
   • Update PostgreSQL
   • Refresh Redis cache
   • Index in Elasticsearch
    ↓
7. Return Response
   • Domain overview
   • Top metrics
   • Recent changes
   • Recommendations
```

#### **2.1.3 SERP Analysis Workflow**

```
User Input: Keyword + Location
    ↓
1. SERP Fetch Request
   • Generate SERP cache key
   • Check Redis (TTL: 6 hours)
    ↓
2. Cache Miss → Trigger Crawler
   Job: SERP Scraper
     → Use rotating proxies
     → Fetch Google SERP page
     → Extract organic results
     → Extract paid ads
     → Extract SERP features
     → Handle CAPTCHA if needed
    ↓
3. SERP Data Processing
   • Parse HTML/JSON
   • Extract result URLs
   • Identify result types
   • Calculate positions
   • Detect SERP features
    ↓
4. Domain Enrichment
   For each result URL:
     → Lookup domain metrics
     → Calculate domain strength
     → Fetch page metrics
     → Analyze content
    ↓
5. Competitive Analysis
   • Compare domain authorities
   • Analyze content gaps
   • Calculate difficulty score
   • Generate insights
    ↓
6. Storage
   • PostgreSQL: serp_results table
   • MongoDB: Raw SERP snapshots
   • Redis: Cached response
    ↓
7. Return Enriched SERP Data
```

### 2.2 Data Pipeline Architecture

#### **2.2.1 Data Import Pipeline**

```
┌────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                            │
│  [Google APIs] [Bing APIs] [Third-party] [User Uploads]   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              INGESTION LAYER                               │
│  • API adapters with retry logic                           │
│  • Rate limiting per source                                │
│  • Request queuing and scheduling                          │
│  • Error handling and logging                              │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│            VALIDATION & CLEANING                           │
│  • Schema validation                                       │
│  • Data type conversion                                    │
│  • Null handling                                           │
│  • Duplicate detection                                     │
│  • Outlier detection                                       │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              TRANSFORMATION                                │
│  • Normalization (keywords, URLs)                          │
│  • Enrichment (add metadata)                               │
│  • Aggregation (combine sources)                           │
│  • Calculation (derived metrics)                           │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                LOADING LAYER                               │
│  • Batch insertion to PostgreSQL                           │
│  • Bulk indexing to Elasticsearch                          │
│  • Document insertion to MongoDB                           │
│  • Cache warming (Redis)                                   │
└─────────────────────┬──────────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│             POST-PROCESSING                                │
│  • Trigger analytics jobs                                  │
│  • Update aggregated tables                                │
│  • Invalidate stale cache                                  │
│  • Send notifications                                      │
└────────────────────────────────────────────────────────────┘
```

#### **2.2.2 Data Processing Stages**

**Stage 1: Raw Data Collection**
```python
# Pseudo-code
async def collect_keyword_data(keyword, country, language):
    sources = [
        fetch_google_ads_data(keyword, country),
        fetch_google_trends(keyword),
        fetch_third_party_api(keyword, country),
        scrape_serp_if_needed(keyword, country)
    ]
    
    results = await asyncio.gather(*sources, return_exceptions=True)
    
    return {
        'raw_data': results,
        'timestamp': utc_now(),
        'sources_succeeded': count_successes(results)
    }
```

**Stage 2: Data Cleaning**
```python
def clean_keyword_data(raw_data):
    cleaned = {
        'keyword': normalize_keyword(raw_data['keyword']),
        'volume': validate_volume(raw_data['volume']),
        'cpc': validate_currency(raw_data['cpc']),
        'competition': normalize_0_to_1(raw_data['competition']),
        'trend_data': interpolate_missing_months(raw_data['trend'])
    }
    
    # Remove outliers
    if is_outlier(cleaned['volume']):
        cleaned['volume_confidence'] = 'low'
    
    return cleaned
```

**Stage 3: Data Enrichment**
```python
def enrich_keyword_data(cleaned_data):
    enriched = cleaned_data.copy()
    
    # Calculate derived metrics
    enriched['difficulty_score'] = calculate_difficulty(
        cleaned_data['competition'],
        cleaned_data['volume'],
        cleaned_data['serp_features']
    )
    
    # Add related data
    enriched['related_keywords'] = find_related_keywords(
        cleaned_data['keyword']
    )
    
    # Add semantic data
    enriched['intent'] = classify_search_intent(
        cleaned_data['keyword']
    )
    
    return enriched
```

**Stage 4: Data Storage**
```python
async def store_keyword_data(enriched_data):
    # Parallel storage operations
    await asyncio.gather(
        store_in_postgres(enriched_data),
        index_in_elasticsearch(enriched_data),
        cache_in_redis(enriched_data),
        archive_in_mongodb(enriched_data['raw_data'])
    )
```

### 2.3 API Rate Limiting & Proxy Rotation

#### **2.3.1 Rate Limiting Strategy**

```
┌─────────────────────────────────────────────────────────────┐
│                  RATE LIMITING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: API Gateway Level (Per User)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Free Plan:     10 requests/minute                     │ │
│  │ Pro Plan:      100 requests/minute                    │ │
│  │ Agency Plan:   500 requests/minute                    │ │
│  │ Enterprise:    Custom limits                          │ │
│  │                                                        │ │
│  │ Implementation: Token bucket algorithm in Redis       │ │
│  │ Key: "ratelimit:user:{user_id}:{endpoint}"           │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Layer 2: Service Level (Per External API)                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Google Ads API:    15,000/day (shared across users)  │ │
│  │ Google Trends:     1,500/hour                         │ │
│  │ Bing API:          5,000/month                        │ │
│  │ Third-party APIs:  Varies by provider                 │ │
│  │                                                        │ │
│  │ Implementation: Distributed counter in Redis          │ │
│  │ Key: "api_quota:{provider}:{date}"                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  Layer 3: Crawler Level (Per Proxy/IP)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Max 60 requests/hour per IP                          │ │
│  │ Randomized delays: 2-5 seconds                        │ │
│  │ Rotating user agents                                  │ │
│  │ Cookie management                                     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### **2.3.2 Proxy Rotation System**

```
┌─────────────────────────────────────────────────────────────┐
│                  PROXY POOL MANAGEMENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Proxy Sources:                                             │
│  • Residential Proxies (Bright Data, Oxylabs)              │
│  • Datacenter Proxies (backup)                             │
│  • Mobile Proxies (for mobile SERP)                        │
│                                                             │
│  Pool Size: 1,000-10,000 rotating proxies                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    ROTATION STRATEGY                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Round-Robin Selection                                   │
│     • Distribute requests evenly                            │
│     • Track usage per proxy                                 │
│                                                             │
│  2. Health Checking                                         │
│     • Periodic connectivity tests                           │
│     • Response time monitoring                              │
│     • Success rate tracking                                 │
│     • Automatic removal of dead proxies                     │
│                                                             │
│  3. Geographic Targeting                                    │
│     • Match proxy location to search location               │
│     • US proxy for US searches                              │
│     • Local proxies for local SERP                          │
│                                                             │
│  4. Cooldown Management                                     │
│     • 5-minute cooldown after 50 requests                   │
│     • Exponential backoff on errors                         │
│     • Automatic proxy cycling                               │
│                                                             │
│  5. CAPTCHA Handling                                        │
│     • Detect CAPTCHA challenges                             │
│     • Mark proxy as temporary blocked                       │
│     • Integrate CAPTCHA solving service (2Captcha)          │
│     • Fallback to manual verification if needed             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Proxy Selection Algorithm:

```python
def select_proxy(country, previous_failures=[]):
    # Get healthy proxies for country
    candidate_proxies = redis.smembers(f'proxies:healthy:{country}')
    
    # Remove recently failed proxies
    candidate_proxies -= set(previous_failures)
    
    # Sort by recent usage (prefer least recently used)
    proxies_with_scores = []
    for proxy in candidate_proxies:
        last_used = redis.get(f'proxy:last_used:{proxy}')
        success_rate = redis.get(f'proxy:success_rate:{proxy}')
        
        score = calculate_proxy_score(last_used, success_rate)
        proxies_with_scores.append((proxy, score))
    
    # Select best proxy
    selected_proxy = max(proxies_with_scores, key=lambda x: x[1])[0]
    
    # Mark as in-use
    redis.set(f'proxy:last_used:{selected_proxy}', time.now())
    
    return selected_proxy
```

---

## 3. Database Design

### 3.1 Database Schema Overview

The system uses **four database technologies** for different purposes:

1. **PostgreSQL** - Primary relational data (users, projects, core metrics)
2. **MongoDB** - Document storage (raw crawl data, flexible schemas)
3. **Redis** - Caching and real-time data
4. **Elasticsearch** - Full-text search and analytics

### 3.2 PostgreSQL Schema

#### **3.2.1 Users & Authentication**

```sql
-- Users table
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    plan_type VARCHAR(50) DEFAULT 'free', -- free, pro, agency, enterprise
    plan_status VARCHAR(50) DEFAULT 'active', -- active, trial, expired, cancelled
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_plan_type ON users(plan_type);

-- User sessions
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);

-- User subscriptions
CREATE TABLE subscriptions (
    subscription_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    plan_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL, -- active, cancelled, expired, past_due
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    cancelled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);

-- User quotas and usage
CREATE TABLE user_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    quota_type VARCHAR(50) NOT NULL, -- keyword_searches, domain_analyses, rank_checks
    quota_limit INT NOT NULL,
    quota_used INT DEFAULT 0,
    reset_period VARCHAR(50) NOT NULL, -- daily, monthly
    last_reset_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quotas_user_id ON user_quotas(user_id);
CREATE UNIQUE INDEX idx_quotas_user_type ON user_quotas(user_id, quota_type);
```

#### **3.2.2 Projects & Organization**

```sql
-- Projects (workspace for organizing keywords and domains)
CREATE TABLE projects (
    project_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_description TEXT,
    target_country VARCHAR(2) DEFAULT 'US',
    target_language VARCHAR(5) DEFAULT 'en',
    target_location VARCHAR(255), -- city name for local SEO
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_archived BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_country ON projects(target_country);

-- Project members (for team collaboration)
CREATE TABLE project_members (
    member_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- owner, admin, editor, viewer
    invited_by BIGINT REFERENCES users(user_id),
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

CREATE INDEX idx_members_project_id ON project_members(project_id);
CREATE INDEX idx_members_user_id ON project_members(user_id);
```

#### **3.2.3 Keywords Core Tables**

```sql
-- Keywords master table
CREATE TABLE keywords (
    keyword_id BIGSERIAL PRIMARY KEY,
    keyword_text TEXT NOT NULL,
    keyword_normalized TEXT NOT NULL, -- lowercase, trimmed
    keyword_hash VARCHAR(64) NOT NULL, -- for sharding
    country VARCHAR(2) NOT NULL,
    language VARCHAR(5) NOT NULL,
    device_type VARCHAR(20) DEFAULT 'desktop', -- desktop, mobile, tablet
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_fetched_at TIMESTAMP,
    data_source VARCHAR(50), -- google_ads, bing, semrush_api
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(keyword_normalized, country, language, device_type)
);

CREATE INDEX idx_keywords_normalized ON keywords(keyword_normalized);
CREATE INDEX idx_keywords_hash ON keywords(keyword_hash);
CREATE INDEX idx_keywords_country ON keywords(country);
CREATE INDEX idx_keywords_updated_at ON keywords(updated_at);

-- Partitioning strategy (if using native partitioning)
-- CREATE TABLE keywords_us PARTITION OF keywords FOR VALUES IN ('US');
-- CREATE TABLE keywords_uk PARTITION OF keywords FOR VALUES IN ('UK');
-- CREATE TABLE keywords_in PARTITION OF keywords FOR VALUES IN ('IN');

-- Keyword metrics (search volume, CPC, competition)
CREATE TABLE keyword_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    search_volume BIGINT,
    search_volume_trend VARCHAR(20), -- up, down, stable
    cpc_min DECIMAL(10,2),
    cpc_max DECIMAL(10,2),
    cpc_avg DECIMAL(10,2),
    competition_score DECIMAL(3,2), -- 0.00 to 1.00
    competition_level VARCHAR(20), -- low, medium, high
    difficulty_score INT, -- 0-100
    opportunity_score INT, -- 0-100 (custom metric)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, metric_date)
);

CREATE INDEX idx_metrics_keyword_id ON keyword_metrics(keyword_id);
CREATE INDEX idx_metrics_date ON keyword_metrics(metric_date);
CREATE INDEX idx_metrics_volume ON keyword_metrics(search_volume);
CREATE INDEX idx_metrics_difficulty ON keyword_metrics(difficulty_score);

-- Keyword trends (12-month historical data)
CREATE TABLE keyword_trends (
    trend_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    trend_month DATE NOT NULL, -- first day of month
    trend_value INT NOT NULL, -- 0-100 (relative interest)
    search_volume_estimate BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, trend_month)
);

CREATE INDEX idx_trends_keyword_id ON keyword_trends(keyword_id);
CREATE INDEX idx_trends_month ON keyword_trends(trend_month);

-- Related keywords
CREATE TABLE related_keywords (
    relation_id BIGSERIAL PRIMARY KEY,
    source_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    related_keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL, -- similar, broader, narrower, question
    relevance_score DECIMAL(3,2), -- 0.00 to 1.00
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_keyword_id, related_keyword_id, relation_type)
);

CREATE INDEX idx_related_source ON related_keywords(source_keyword_id);
CREATE INDEX idx_related_target ON related_keywords(related_keyword_id);
CREATE INDEX idx_related_type ON related_keywords(relation_type);

-- Keyword questions (People Also Ask)
CREATE TABLE keyword_questions (
    question_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50), -- who, what, when, where, why, how
    frequency_score INT, -- how often it appears
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_keyword_id ON keyword_questions(keyword_id);
CREATE INDEX idx_questions_type ON keyword_questions(question_type);

-- User keyword lists (saved keywords)
CREATE TABLE user_keyword_lists (
    list_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    tags VARCHAR(255)[],
    priority INT, -- 1-5
    UNIQUE(project_id, keyword_id)
);

CREATE INDEX idx_user_lists_project ON user_keyword_lists(project_id);
CREATE INDEX idx_user_lists_keyword ON user_keyword_lists(keyword_id);
```

#### **3.2.4 Domains & Backlinks**

```sql
-- Domains master table
CREATE TABLE domains (
    domain_id BIGSERIAL PRIMARY KEY,
    domain_name VARCHAR(255) UNIQUE NOT NULL,
    domain_normalized VARCHAR(255) NOT NULL, -- lowercase
    domain_hash VARCHAR(64) NOT NULL,
    tld VARCHAR(50),
    is_subdomain BOOLEAN DEFAULT FALSE,
    root_domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_crawled_at TIMESTAMP,
    crawl_status VARCHAR(50), -- pending, in_progress, completed, failed
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_domains_normalized ON domains(domain_normalized);
CREATE INDEX idx_domains_hash ON domains(domain_hash);
CREATE INDEX idx_domains_tld ON domains(tld);
CREATE INDEX idx_domains_root ON domains(root_domain);

-- Domain metrics
CREATE TABLE domain_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    domain_authority INT, -- 0-100 (our custom score)
    page_authority_avg DECIMAL(5,2),
    total_backlinks BIGINT,
    unique_domains BIGINT,
    dofollow_backlinks BIGINT,
    nofollow_backlinks BIGINT,
    total_referring_ips BIGINT,
    organic_traffic_estimate BIGINT,
    organic_keywords_count BIGINT,
    organic_traffic_value DECIMAL(12,2), -- estimated value in USD
    paid_traffic_estimate BIGINT,
    social_signals JSONB, -- {facebook: 1000, twitter: 500, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, metric_date)
);

CREATE INDEX idx_domain_metrics_domain ON domain_metrics(domain_id);
CREATE INDEX idx_domain_metrics_date ON domain_metrics(metric_date);
CREATE INDEX idx_domain_metrics_authority ON domain_metrics(domain_authority);

-- Backlinks (huge table - consider sharding)
CREATE TABLE backlinks (
    backlink_id BIGSERIAL PRIMARY KEY,
    target_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    target_url TEXT NOT NULL,
    source_domain_id BIGINT REFERENCES domains(domain_id),
    source_url TEXT NOT NULL,
    source_page_title TEXT,
    anchor_text TEXT,
    link_type VARCHAR(20), -- dofollow, nofollow, redirect
    first_seen_at TIMESTAMP NOT NULL,
    last_seen_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    http_status INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_backlinks_target_domain ON backlinks(target_domain_id);
CREATE INDEX idx_backlinks_source_domain ON backlinks(source_domain_id);
CREATE INDEX idx_backlinks_first_seen ON backlinks(first_seen_at);
CREATE INDEX idx_backlinks_active ON backlinks(is_active);

-- For sharding large backlinks table:
-- Shard by target_domain_hash using Citus or manual sharding

-- Domain top pages
CREATE TABLE domain_top_pages (
    page_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    page_url TEXT NOT NULL,
    page_title TEXT,
    page_type VARCHAR(50), -- article, product, category, homepage
    organic_traffic_estimate BIGINT,
    organic_keywords_count INT,
    backlinks_count INT,
    social_shares INT,
    content_length INT,
    last_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, page_url)
);

CREATE INDEX idx_top_pages_domain ON domain_top_pages(domain_id);
CREATE INDEX idx_top_pages_traffic ON domain_top_pages(organic_traffic_estimate DESC);

-- Domain organic keywords
CREATE TABLE domain_organic_keywords (
    ranking_id BIGSERIAL PRIMARY KEY,
    domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    ranking_url TEXT NOT NULL,
    position INT NOT NULL,
    position_date DATE NOT NULL,
    previous_position INT,
    traffic_estimate INT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(domain_id, keyword_id, position_date)
);

CREATE INDEX idx_organic_domain ON domain_organic_keywords(domain_id);
CREATE INDEX idx_organic_keyword ON domain_organic_keywords(keyword_id);
CREATE INDEX idx_organic_position ON domain_organic_keywords(position);
CREATE INDEX idx_organic_date ON domain_organic_keywords(position_date);
```

#### **3.2.5 SERP Data**

```sql
-- SERP results snapshots
CREATE TABLE serp_results (
    serp_id BIGSERIAL PRIMARY KEY,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    search_date DATE NOT NULL,
    search_location VARCHAR(255), -- city/region for local searches
    device_type VARCHAR(20) DEFAULT 'desktop',
    total_results BIGINT,
    serp_features JSONB, -- {featured_snippet: true, local_pack: true, ...}
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(keyword_id, search_date, search_location, device_type)
);

CREATE INDEX idx_serp_keyword ON serp_results(keyword_id);
CREATE INDEX idx_serp_date ON serp_results(search_date);
CREATE INDEX idx_serp_location ON serp_results(search_location);

-- Individual SERP positions
CREATE TABLE serp_positions (
    position_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    position INT NOT NULL,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    title TEXT,
    description TEXT,
    result_type VARCHAR(50), -- organic, paid, featured_snippet, local, image, video
    serp_features JSONB, -- rich snippet data
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_positions_serp ON serp_positions(serp_id);
CREATE INDEX idx_positions_domain ON serp_positions(domain_id);
CREATE INDEX idx_positions_position ON serp_positions(position);

-- SERP features (detailed)
CREATE TABLE serp_features (
    feature_id BIGSERIAL PRIMARY KEY,
    serp_id BIGINT REFERENCES serp_results(serp_id) ON DELETE CASCADE,
    feature_type VARCHAR(50) NOT NULL, -- featured_snippet, local_pack, people_also_ask, etc.
    feature_data JSONB NOT NULL, -- flexible structure for different features
    feature_position INT,
    domain_id BIGINT REFERENCES domains(domain_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_features_serp ON serp_features(serp_id);
CREATE INDEX idx_features_type ON serp_features(feature_type);
CREATE INDEX idx_features_domain ON serp_features(domain_id);
```

#### **3.2.6 Keyword Tracking**

```sql
-- Keyword tracking projects
CREATE TABLE tracking_projects (
    tracking_project_id BIGSERIAL PRIMARY KEY,
    project_id BIGINT REFERENCES projects(project_id) ON DELETE CASCADE,
    target_domain VARCHAR(255) NOT NULL,
    check_frequency VARCHAR(20) DEFAULT 'daily', -- daily, weekly, monthly
    next_check_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tracking_project ON tracking_projects(project_id);
CREATE INDEX idx_tracking_next_check ON tracking_projects(next_check_at);

-- Tracked keywords
CREATE TABLE tracked_keywords (
    tracked_keyword_id BIGSERIAL PRIMARY KEY,
    tracking_project_id BIGINT REFERENCES tracking_projects(tracking_project_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    target_url TEXT, -- specific URL to track
    tags VARCHAR(255)[],
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracking_project_id, keyword_id)
);

CREATE INDEX idx_tracked_project ON tracked_keywords(tracking_project_id);
CREATE INDEX idx_tracked_keyword ON tracked_keywords(keyword_id);

-- Ranking history (time-series data - consider TimescaleDB)
CREATE TABLE ranking_history (
    history_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    check_date DATE NOT NULL,
    check_time TIMESTAMP NOT NULL,
    position INT, -- NULL if not ranking
    ranking_url TEXT,
    serp_features VARCHAR(50)[], -- features present at time of check
    pixel_rank INT, -- position in pixels from top
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tracked_keyword_id, check_date, check_time)
);

CREATE INDEX idx_history_tracked ON ranking_history(tracked_keyword_id);
CREATE INDEX idx_history_date ON ranking_history(check_date);
CREATE INDEX idx_history_position ON ranking_history(position);

-- Convert to TimescaleDB hypertable for better time-series performance
-- SELECT create_hypertable('ranking_history', 'check_time');

-- Ranking alerts
CREATE TABLE ranking_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- position_change, entered_top10, dropped_out, etc.
    alert_threshold INT, -- e.g., alert if change > 5 positions
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_tracked ON ranking_alerts(tracked_keyword_id);

-- Alert history
CREATE TABLE alert_notifications (
    notification_id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT REFERENCES ranking_alerts(alert_id) ON DELETE CASCADE,
    tracked_keyword_id BIGINT REFERENCES tracked_keywords(tracked_keyword_id) ON DELETE CASCADE,
    trigger_date DATE NOT NULL,
    old_position INT,
    new_position INT,
    message TEXT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_alert ON alert_notifications(alert_id);
CREATE INDEX idx_notifications_date ON alert_notifications(trigger_date);
```

#### **3.2.7 Content Analysis & Gap Analysis**

```sql
-- Content analysis
CREATE TABLE content_analysis (
    analysis_id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    domain_id BIGINT REFERENCES domains(domain_id),
    keyword_id BIGINT, -- target keyword for analysis
    content_length INT,
    word_count INT,
    readability_score DECIMAL(5,2),
    keyword_density DECIMAL(5,2),
    h1_count INT,
    h2_count INT,
    image_count INT,
    internal_links_count INT,
    external_links_count INT,
    schema_markup JSONB,
    meta_title TEXT,
    meta_description TEXT,
    analyzed_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_content_domain ON content_analysis(domain_id);
CREATE INDEX idx_content_keyword ON content_analysis(keyword_id);

-- Content gap analysis (comparing domains)
CREATE TABLE content_gaps (
    gap_id BIGSERIAL PRIMARY KEY,
    source_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    competitor_domain_id BIGINT REFERENCES domains(domain_id) ON DELETE CASCADE,
    keyword_id BIGINT REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    competitor_position INT,
    source_position INT, -- NULL if not ranking
    gap_score INT, -- 0-100
    opportunity_score INT, -- 0-100
    analysis_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(source_domain_id, competitor_domain_id, keyword_id, analysis_date)
);

CREATE INDEX idx_gaps_source ON content_gaps(source_domain_id);
CREATE INDEX idx_gaps_competitor ON content_gaps(competitor_domain_id);
CREATE INDEX idx_gaps_keyword ON content_gaps(keyword_id);
CREATE INDEX idx_gaps_score ON content_gaps(gap_score DESC);
```

#### **3.2.8 API Cache & Search History**

```sql
-- API response cache metadata
CREATE TABLE api_cache_metadata (
    cache_id BIGSERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    entity_id BIGINT, -- keyword_id, domain_id, etc.
    cache_ttl INT NOT NULL, -- seconds
    cached_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    hit_count INT DEFAULT 0,
    last_hit_at TIMESTAMP
);

CREATE INDEX idx_cache_key ON api_cache_metadata(cache_key);
CREATE INDEX idx_cache_expires ON api_cache_metadata(expires_at);
CREATE INDEX idx_cache_type ON api_cache_metadata(cache_type);

-- Search history (for analytics and suggestions)
CREATE TABLE search_history (
    search_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    search_query TEXT NOT NULL,
    search_type VARCHAR(50) NOT NULL, -- keyword, domain, serp
    search_filters JSONB, -- country, language, device, etc.
    result_count INT,
    searched_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_query ON search_history(search_query);
CREATE INDEX idx_search_date ON search_history(searched_at);
```

#### **3.2.9 External API Integration Tracking**

```sql
-- API integration logs
CREATE TABLE api_integration_logs (
    log_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL, -- google_ads, google_trends, semrush, etc.
    endpoint VARCHAR(255) NOT NULL,
    request_method VARCHAR(10),
    request_params JSONB,
    response_status INT,
    response_time_ms INT,
    error_message TEXT,
    requested_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_logs_provider ON api_integration_logs(provider);
CREATE INDEX idx_api_logs_date ON api_integration_logs(requested_at);
CREATE INDEX idx_api_logs_status ON api_integration_logs(response_status);

-- API quota tracking
CREATE TABLE api_quotas (
    quota_id BIGSERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    quota_type VARCHAR(50) NOT NULL, -- daily, monthly
    quota_limit BIGINT NOT NULL,
    quota_used BIGINT DEFAULT 0,
    quota_period DATE NOT NULL,
    reset_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, quota_type, quota_period)
);

CREATE INDEX idx_api_quotas_provider ON api_quotas(provider);
CREATE INDEX idx_api_quotas_period ON api_quotas(quota_period);
```

#### **3.2.10 Indexing & Partitioning Strategy**

```sql
-- Composite indexes for common query patterns

-- Keyword searches by country and language
CREATE INDEX idx_keywords_country_lang_norm 
ON keywords(country, language, keyword_normalized);

-- Keyword metrics for trending keywords
CREATE INDEX idx_metrics_volume_date 
ON keyword_metrics(search_volume DESC, metric_date DESC);

-- Domain backlinks by date and status
CREATE INDEX idx_backlinks_target_active_date 
ON backlinks(target_domain_id, is_active, last_seen_at DESC);

-- SERP tracking queries
CREATE INDEX idx_ranking_history_tracked_date 
ON ranking_history(tracked_keyword_id, check_date DESC);

-- Content gaps by score
CREATE INDEX idx_content_gaps_source_score 
ON content_gaps(source_domain_id, gap_score DESC, analysis_date DESC);

-- Partitioning strategy for large tables
-- Example: Partition ranking_history by month
CREATE TABLE ranking_history_y2025m01 PARTITION OF ranking_history
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE ranking_history_y2025m02 PARTITION OF ranking_history
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Automated partition creation via pg_cron or external script
```

### 3.3 MongoDB Collections

MongoDB stores **flexible, document-based data** and **raw crawl results**.

#### **3.3.1 Raw SERP Snapshots**

```javascript
// Collection: serp_snapshots
{
    _id: ObjectId(),
    keyword: "best running shoes",
    country: "US",
    language: "en",
    device: "desktop",
    search_date: ISODate("2025-01-15T10:30:00Z"),
    raw_html: "<html>...</html>", // Full SERP HTML
    raw_json: { /* Google API response */ },
    screenshot_url: "s3://bucket/serp-snapshots/uuid.png",
    results: [
        {
            position: 1,
            url: "https://example.com/running-shoes",
            title: "Best Running Shoes 2025",
            description: "...",
            type: "organic",
            rich_snippet: {
                rating: 4.5,
                reviews: 1200,
                price: "$129.99"
            }
        }
        // ... more results
    ],
    serp_features: [
        {
            type: "featured_snippet",
            content: "...",
            source_url: "https://example.com"
        },
        {
            type: "people_also_ask",
            questions: [...]
        }
    ],
    ads: [
        {
            position: "top1",
            url: "...",
            title: "...",
            description: "..."
        }
    ],
    metadata: {
        total_results: 2340000000,
        search_time_ms: 234,
        proxy_used: "proxy123",
        crawler_version: "2.0"
    },
    created_at: ISODate("2025-01-15T10:30:05Z")
}

// Indexes
db.serp_snapshots.createIndex({ keyword: 1, country: 1, search_date: -1 });
db.serp_snapshots.createIndex({ search_date: -1 });
db.serp_snapshots.createIndex({ "results.url": 1 });
```

#### **3.3.2 Crawl Queue**

```javascript
// Collection: crawl_queue
{
    _id: ObjectId(),
    job_id: "uuid",
    job_type: "serp_crawl", // serp_crawl, backlink_discovery, content_extraction
    priority: 1, // 1-5
    status: "pending", // pending, in_progress, completed, failed
    keyword: "running shoes",
    country: "US",
    language: "en",
    parameters: {
        device: "desktop",
        location: "New York, NY",
        num_results: 100
    },
    retry_count: 0,
    max_retries: 3,
    assigned_worker: null,
    started_at: null,
    completed_at: null,
    error_message: null,
    result_reference: null, // Reference to result in other collection
    created_at: ISODate("2025-01-15T10:00:00Z"),
    updated_at: ISODate("2025-01-15T10:00:00Z"),
    scheduled_for: ISODate("2025-01-15T10:05:00Z")
}

// Indexes
db.crawl_queue.createIndex({ status: 1, priority: 1, scheduled_for: 1 });
db.crawl_queue.createIndex({ job_id: 1 });
db.crawl_queue.createIndex({ created_at: -1 });
```

#### **3.3.3 Backlink Discovery Data**

```javascript
// Collection: backlink_raw_data
{
    _id: ObjectId(),
    target_domain: "example.com",
    target_url: "https://example.com/page",
    discovered_backlinks: [
        {
            source_url: "https://source.com/article",
            source_domain: "source.com",
            anchor_text: "click here",
            link_type: "dofollow",
            context: "... surrounding text ...",
            discovered_at: ISODate("2025-01-15T10:00:00Z"),
            http_status: 200,
            source_page_title: "Article Title",
            source_page_metrics: {
                domain_authority: 45,
                page_authority: 38,
                spam_score: 2
            }
        }
        // ... thousands more
    ],
    crawl_method: "ahrefs_api", // ahrefs_api, moz_api, manual_crawl
    crawl_date: ISODate("2025-01-15T10:00:00Z"),
    total_backlinks_found: 15234,
    metadata: {
        api_version: "v3",
        cost_credits: 50
    },
    created_at: ISODate("2025-01-15T10:30:00Z")
}

// Indexes
db.backlink_raw_data.createIndex({ target_domain: 1, crawl_date: -1 });
db.backlink_raw_data.createIndex({ "discovered_backlinks.source_domain": 1 });
```

#### **3.3.4 Historical Metrics Archive**

```javascript
// Collection: keyword_metrics_archive
// Old keyword metrics (>90 days) moved from PostgreSQL to MongoDB
{
    _id: ObjectId(),
    keyword_id: 12345,
    keyword: "running shoes",
    country: "US",
    metrics_by_month: {
        "2024-01": {
            search_volume: 110000,
            cpc_avg: 1.25,
            competition: 0.78,
            difficulty_score: 65
        },
        "2024-02": {
            search_volume: 135000,
            cpc_avg: 1.32,
            competition: 0.81,
            difficulty_score: 68
        }
        // ... 12+ months of data
    },
    archived_at: ISODate("2025-01-15T00:00:00Z")
}

// Indexes
db.keyword_metrics_archive.createIndex({ keyword_id: 1 });
db.keyword_metrics_archive.createIndex({ archived_at: -1 });
```

### 3.4 Redis Data Structures

Redis handles **caching, real-time data, and queue management**.

#### **3.4.1 Cache Keys Structure**

```redis
# Keyword data cache
Key: "cache:keyword:en:us:desktop:running_shoes"
Type: String (JSON)
TTL: 86400 seconds (24 hours)
Value: {
    "keyword": "running shoes",
    "volume": 110000,
    "cpc": 1.25,
    "difficulty": 65,
    "trend": [100, 95, 98, ...]
}

# Domain overview cache
Key: "cache:domain:example.com:overview"
Type: String (JSON)
TTL: 43200 seconds (12 hours)
Value: {
    "domain": "example.com",
    "authority": 75,
    "backlinks": 125000,
    "keywords": 45000,
    "traffic": 850000
}

# SERP results cache
Key: "cache:serp:en:us:running_shoes"
Type: String (JSON)
TTL: 21600 seconds (6 hours)
Value: {
    "keyword": "running shoes",
    "results": [...],
    "features": [...]
}

# User session
Key: "session:{user_id}:{session_token}"
Type: String (JSON)
TTL: 1800 seconds (30 minutes, sliding)
Value: {
    "user_id": 123,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": [...]
}
```

#### **3.4.2 Rate Limiting**

```redis
# User rate limit (token bucket)
Key: "ratelimit:user:{user_id}:keyword_search"
Type: String (integer)
TTL: 60 seconds
Value: 95  # requests remaining this minute
Algorithm: Token bucket with sliding window

# API provider rate limit
Key: "ratelimit:api:google_ads:daily"
Type: String (integer)
TTL: Until midnight UTC
Value: 14523  # requests used today

# IP-based rate limit (for crawlers)
Key: "ratelimit:ip:{proxy_ip}"
Type: Sorted Set
TTL: 3600 seconds
Members: {timestamp: request_id}
Algorithm: Sliding window log
```

#### **3.4.3 Real-time Ranking Data**

```redis
# Current rankings (hot data)
Key: "ranking:live:{tracked_keyword_id}"
Type: Hash
TTL: 3600 seconds
Fields:
    position: 5
    url: "https://example.com/page"
    last_check: 1705320000
    previous_position: 7

# Ranking change notifications
Key: "ranking:changes:{user_id}"
Type: List
TTL: 604800 seconds (7 days)
Values: [
    {"keyword": "...", "old": 7, "new": 5, "date": "..."},
    ...
]
```

#### **3.4.4 Queue Management**

```redis
# Priority queue for crawl jobs
Key: "queue:crawl:priority:{1-5}"
Type: List (FIFO)
Values: [job_id1, job_id2, ...]

# Job status tracking
Key: "job:{job_id}:status"
Type: Hash
Fields:
    status: "in_progress"
    worker_id: "worker-1"
    started_at: 1705320000
    progress: 45  # percentage

# Worker heartbeat
Key: "worker:{worker_id}:heartbeat"
Type: String
TTL: 60 seconds
Value: timestamp
```

### 3.5 Elasticsearch Indices

Elasticsearch provides **full-text search** and **fast analytics**.

#### **3.5.1 Keywords Index**

```json
// Index: keywords
{
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "snowball"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "keyword_id": {"type": "long"},
            "keyword_text": {
                "type": "text",
                "analyzer": "keyword_analyzer",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "country": {"type": "keyword"},
            "language": {"type": "keyword"},
            "search_volume": {"type": "long"},
            "cpc_avg": {"type": "float"},
            "difficulty_score": {"type": "integer"},
            "opportunity_score": {"type": "integer"},
            "trend_direction": {"type": "keyword"},
            "related_keywords": {
                "type": "text",
                "analyzer": "keyword_analyzer"
            },
            "last_updated": {"type": "date"}
        }
    }
}
```

#### **3.5.2 Domains Index**

```json
// Index: domains
{
    "mappings": {
        "properties": {
            "domain_id": {"type": "long"},
            "domain_name": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "domain_authority": {"type": "integer"},
            "total_backlinks": {"type": "long"},
            "organic_keywords": {"type": "long"},
            "organic_traffic": {"type": "long"},
            "tld": {"type": "keyword"},
            "category": {"type": "keyword"},
            "last_crawled": {"type": "date"}
        }
    }
}
```

#### **3.5.3 Search Suggestions Index**

```json
// Index: search_suggestions
{
    "mappings": {
        "properties": {
            "suggestion": {
                "type": "completion",
                "analyzer": "simple",
                "search_analyzer": "simple"
            },
            "type": {"type": "keyword"}, // keyword, domain
            "popularity": {"type": "integer"},
            "country": {"type": "keyword"}
        }
    }
}
```

### 3.6 Sharding & Partitioning Plan

#### **3.6.1 PostgreSQL Sharding (using Citus)**

```sql
-- Distribute keywords table across shards
SELECT create_distributed_table('keywords', 'keyword_hash');
SELECT create_distributed_table('keyword_metrics', 'keyword_id');

-- Co-locate related tables for join performance
SELECT create_distributed_table('related_keywords', 'source_keyword_id', 
    colocate_with => 'keywords');

-- Distribute backlinks by target domain
SELECT create_distributed_table('backlinks', 'target_domain_id');

-- Reference tables (replicated to all shards)
SELECT create_reference_table('users');
SELECT create_reference_table('projects');
```

#### **3.6.2 MongoDB Sharding**

```javascript
// Enable sharding on database
sh.enableSharding("seo_platform");

// Shard serp_snapshots by compound key
sh.shardCollection("seo_platform.serp_snapshots", {
    country: 1,
    language: 1,
    search_date: 1
});

// Shard backlink_raw_data by target domain
sh.shardCollection("seo_platform.backlink_raw_data", {
    target_domain: "hashed"
});

// Shard crawl_queue by job_id
sh.shardCollection("seo_platform.crawl_queue", {
    job_id: "hashed"
});
```

#### **3.6.3 Data Retention & Archival**

```
Hot Data (PostgreSQL):
  - Last 90 days: Full metrics in main tables
  - Query performance: <100ms

Warm Data (PostgreSQL + compression):
  - 90 days - 1 year: Aggregated daily metrics
  - Query performance: <500ms

Cold Data (MongoDB):
  - 1+ years: Monthly aggregates only
  - Raw data archived to S3
  - Query performance: <2s

Archival Policy:
  - Ranking history: Keep daily for 90 days, weekly for 1 year, monthly forever
  - SERP snapshots: Keep full HTML for 30 days, metadata only after
  - Backlinks: Keep active backlinks in PostgreSQL, historical in MongoDB
  - API logs: Keep 30 days in PostgreSQL, archive to S3 after
```

---

## 4. API Layer Design

### 4.1 API Architecture

**Protocol:** REST API with optional GraphQL endpoint  
**Format:** JSON  
**Authentication:** JWT tokens + API keys  
**Versioning:** URL-based (`/api/v1/`, `/api/v2/`)

### 4.2 API Endpoints

#### **4.2.1 Keyword Research API**

```
POST /api/v1/keywords/search
Description: Search for keyword data
Authentication: Required (JWT or API key)
Rate Limit: 100/min (Pro), 500/min (Agency)

Request:
{
    "keyword": "running shoes",
    "country": "US",  // ISO 3166-1 alpha-2
    "language": "en",
    "device": "desktop",  // desktop, mobile, tablet
    "include_related": true,
    "include_questions": true,
    "include_trends": true
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "normalized": "running shoes",
        "metrics": {
            "search_volume": 110000,
            "search_volume_trend": "up",  // up, down, stable
            "cpc": {
                "min": 0.85,
                "max": 2.50,
                "avg": 1.25,
                "currency": "USD"
            },
            "competition": {
                "score": 0.78,
                "level": "high"  // low, medium, high
            },
            "difficulty_score": 65,  // 0-100
            "opportunity_score": 42  // 0-100 (custom metric)
        },
        "trends": {
            "last_12_months": [
                {"month": "2024-02", "value": 95},
                {"month": "2024-03", "value": 100},
                ...
            ],
            "year_over_year": 8.5  // % change
        },
        "related_keywords": [
            {
                "keyword": "best running shoes",
                "volume": 90500,
                "relevance": 0.95,
                "type": "similar"
            },
            ...
        ],
        "questions": [
            {
                "question": "what are the best running shoes for beginners",
                "type": "what",
                "frequency": 85
            },
            ...
        ],
        "serp_features": [
            "featured_snippet",
            "people_also_ask",
            "local_pack"
        ],
        "last_updated": "2025-01-15T10:30:00Z"
    },
    "metadata": {
        "cached": true,
        "cache_age_seconds": 3600,
        "sources": ["google_ads", "google_trends"],
        "credits_used": 1
    }
}

Error Responses:
400 Bad Request:
{
    "status": "error",
    "error": {
        "code": "INVALID_COUNTRY",
        "message": "Country code must be ISO 3166-1 alpha-2",
        "field": "country"
    }
}

429 Too Many Requests:
{
    "status": "error",
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Try again in 45 seconds",
        "retry_after": 45
    }
}

402 Payment Required:
{
    "status": "error",
    "error": {
        "code": "QUOTA_EXCEEDED",
        "message": "Monthly quota exceeded. Upgrade plan to continue",
        "quota_limit": 1000,
        "quota_used": 1000,
        "reset_date": "2025-02-01T00:00:00Z"
    }
}
```

```
GET /api/v1/keywords/{keyword_id}/suggestions
Description: Get related keywords and suggestions
Authentication: Required

Query Parameters:
- type: related|questions|broader|narrower (default: all)
- limit: 1-100 (default: 50)
- min_volume: minimum search volume filter
- max_difficulty: maximum difficulty score filter

Response (200 OK):
{
    "status": "success",
    "data": {
        "suggestions": [
            {
                "keyword": "best running shoes for flat feet",
                "search_volume": 22000,
                "difficulty_score": 58,
                "relevance_score": 0.88,
                "type": "narrower"
            },
            ...
        ],
        "total": 247,
        "returned": 50
    }
}
```

```
POST /api/v1/keywords/bulk
Description: Bulk keyword lookup (up to 100 keywords)
Authentication: Required
Rate Limit: 10/min (Pro), 50/min (Agency)

Request:
{
    "keywords": ["running shoes", "hiking boots", ...],
    "country": "US",
    "language": "en",
    "metrics": ["volume", "cpc", "difficulty"]  // optional filter
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "results": [
            {
                "keyword": "running shoes",
                "status": "success",
                "metrics": {...}
            },
            {
                "keyword": "xyz123invalid",
                "status": "not_found",
                "error": "No data available"
            }
        ],
        "summary": {
            "total": 100,
            "successful": 98,
            "failed": 2
        }
    },
    "metadata": {
        "credits_used": 10,
        "processing_time_ms": 1250
    }
}
```

#### **4.2.2 Domain Analysis API**

```
GET /api/v1/domains/{domain}/overview
Description: Get comprehensive domain metrics
Authentication: Required
Rate Limit: 50/min (Pro), 200/min (Agency)

Path Parameters:
- domain: example.com or www.example.com

Query Parameters:
- include_backlinks: true|false (default: false)
- include_top_pages: true|false (default: false)
- include_keywords: true|false (default: false)

Response (200 OK):
{
    "status": "success",
    "data": {
        "domain": "example.com",
        "metrics": {
            "domain_authority": 75,
            "page_authority_avg": 48.5,
            "spam_score": 2,
            "backlinks": {
                "total": 125847,
                "unique_domains": 8542,
                "dofollow": 98234,
                "nofollow": 27613,
                "referring_ips": 7234,
                "new_last_month": 1234,
                "lost_last_month": 456
            },
            "organic": {
                "keywords_count": 45231,
                "traffic_estimate": 850000,
                "traffic_value": 425000.00,
                "traffic_trend": "up",
                "top_keywords_count": 150,
                "keywords_top_3": 1234,
                "keywords_top_10": 4567,
                "keywords_top_100": 18923
            },
            "paid": {
                "keywords_count": 234,
                "traffic_estimate": 12000,
                "traffic_cost": 15000.00
            },
            "content": {
                "pages_indexed": 1547,
                "pages_crawled": 1892,
                "avg_page_speed": 2.3,
                "mobile_friendly_score": 95
            }
        },
        "competitors": [
            {
                "domain": "competitor1.com",
                "authority": 72,
                "keyword_overlap": 1234,
                "similarity_score": 0.78
            },
            ...
        ],
        "last_updated": "2025-01-15T08:00:00Z"
    }
}
```

```
GET /api/v1/domains/{domain}/backlinks
Description: Get backlink data for domain
Authentication: Required

Query Parameters:
- page: 1-1000 (default: 1)
- limit: 10-100 (default: 50)
- type: all|dofollow|nofollow (default: all)
- sort: authority|date_found|anchor_text (default: authority)
- order: desc|asc (default: desc)
- min_authority: 0-100 (filter)
- only_active: true|false (default: true)

Response (200 OK):
{
    "status": "success",
    "data": {
        "backlinks": [
            {
                "source_url": "https://source.com/article",
                "source_domain": "source.com",
                "source_authority": 68,
                "target_url": "https://example.com/page",
                "anchor_text": "click here",
                "link_type": "dofollow",
                "first_seen": "2024-06-15T00:00:00Z",
                "last_seen": "2025-01-15T00:00:00Z",
                "http_status": 200,
                "is_active": true
            },
            ...
        ],
        "pagination": {
            "page": 1,
            "limit": 50,
            "total": 125847,
            "pages": 2517
        }
    }
}
```

```
GET /api/v1/domains/{domain}/top-pages
Description: Get top-performing pages
Authentication: Required

Query Parameters:
- page: 1-100 (default: 1)
- limit: 10-100 (default: 20)
- sort: traffic|keywords|backlinks (default: traffic)
- metric: organic|paid|all (default: organic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "pages": [
            {
                "url": "https://example.com/best-products",
                "title": "Best Products 2025",
                "page_authority": 52,
                "organic_traffic": 85000,
                "organic_keywords": 1234,
                "backlinks": 456,
                "social_shares": 1200,
                "traffic_value": 42500.00,
                "top_keywords": [
                    {
                        "keyword": "best products",
                        "position": 2,
                        "volume": 22000,
                        "traffic_estimate": 8800
                    },
                    ...
                ]
            },
            ...
        ],
        "pagination": {...}
    }
}
```

```
GET /api/v1/domains/{domain}/organic-keywords
Description: Get ranking keywords for domain
Authentication: Required

Query Parameters:
- page: 1-1000
- limit: 10-100
- position: 1-100 (filter)
- min_volume: minimum search volume
- sort: position|volume|traffic (default: traffic)

Response (200 OK):
{
    "status": "success",
    "data": {
        "keywords": [
            {
                "keyword": "running shoes",
                "position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "search_volume": 110000,
                "traffic_estimate": 8800,
                "traffic_value": 11000.00,
                "serp_features": ["featured_snippet"]
            },
            ...
        ],
        "summary": {
            "total_keywords": 45231,
            "top_3": 1234,
            "top_10": 4567,
            "top_100": 18923
        },
        "pagination": {...}
    }
}
```

#### **4.2.3 SERP Analysis API**

```
POST /api/v1/serp/analyze
Description: Get SERP analysis for keyword
Authentication: Required
Rate Limit: 50/min

Request:
{
    "keyword": "running shoes",
    "country": "US",
    "language": "en",
    "device": "desktop",
    "location": "New York, NY",  // optional for local searches
    "num_results": 100  // 10-100, default: 10
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "total_results": 234000000,
        "serp_features": [
            {
                "type": "featured_snippet",
                "position": 0,
                "domain": "example.com",
                "url": "https://example.com/guide",
                "content_preview": "Running shoes are..."
            },
            {
                "type": "people_also_ask",
                "questions": [
                    "What are the best running shoes?",
                    "How to choose running shoes?",
                    ...
                ]
            },
            {
                "type": "local_pack",
                "businesses": [...]
            }
        ],
        "organic_results": [
            {
                "position": 1,
                "title": "Best Running Shoes 2025",
                "url": "https://example.com/running-shoes",
                "domain": "example.com",
                "domain_authority": 75,
                "description": "Discover the best...",
                "rich_snippet": {
                    "type": "product",
                    "rating": 4.5,
                    "reviews": 1200,
                    "price": "$129.99"
                },
                "backlinks": 1234,
                "referring_domains": 456,
                "estimated_traffic": 35000
            },
            ...
        ],
        "paid_results": [
            {
                "position": "top1",
                "title": "Running Shoes Sale",
                "url": "https://shop.com/running",
                "domain": "shop.com",
                "description": "50% off all running shoes"
            },
            ...
        ],
        "analysis": {
            "difficulty_score": 68,
            "opportunity_score": 45,
            "avg_domain_authority": 72.5,
            "avg_backlinks": 8542,
            "content_length_avg": 2850,
            "content_recommendations": [
                "Include product comparisons",
                "Add video content",
                "Target featured snippet opportunity"
            ]
        },
        "last_updated": "2025-01-15T10:30:00Z"
    }
}
```

```
GET /api/v1/serp/features
Description: Get SERP features statistics
Authentication: Required

Query Parameters:
- keyword: specific keyword or keyword_id
- country: US, UK, etc.
- date_range: last_7_days|last_30_days|last_90_days

Response (200 OK):
{
    "status": "success",
    "data": {
        "features_present": [
            {
                "feature": "featured_snippet",
                "frequency": 85,  // % of time present
                "domains_winning": [
                    {"domain": "example.com", "count": 45},
                    ...
                ]
            },
            {
                "feature": "people_also_ask",
                "frequency": 92
            },
            {
                "feature": "local_pack",
                "frequency": 12
            }
        ],
        "feature_history": [
            {
                "date": "2025-01-15",
                "features": ["featured_snippet", "people_also_ask", "images"]
            },
            ...
        ]
    }
}
```

#### **4.2.4 Rank Tracking API**

```
POST /api/v1/tracking/projects
Description: Create new tracking project
Authentication: Required

Request:
{
    "project_id": 123,  // existing project
    "name": "My Website Tracking",
    "target_domain": "example.com",
    "check_frequency": "daily",  // daily, weekly, monthly
    "keywords": [
        {
            "keyword": "running shoes",
            "target_url": "https://example.com/running-shoes",
            "tags": ["product", "priority-high"]
        },
        ...
    ]
}

Response (201 Created):
{
    "status": "success",
    "data": {
        "tracking_project_id": 456,
        "keywords_added": 50,
        "next_check_at": "2025-01-16T00:00:00Z",
        "estimated_credits_per_check": 50
    }
}
```

```
GET /api/v1/tracking/projects/{project_id}/rankings
Description: Get ranking data for tracked keywords
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD (default: 30 days ago)
- date_to: YYYY-MM-DD (default: today)
- tags: filter by tags (comma-separated)
- position_change: improved|declined|unchanged|new|lost
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "rankings": [
            {
                "keyword": "running shoes",
                "current_position": 5,
                "previous_position": 7,
                "position_change": 2,
                "ranking_url": "https://example.com/running-shoes",
                "best_position": 3,
                "worst_position": 15,
                "average_position": 6.8,
                "history": [
                    {"date": "2025-01-15", "position": 5},
                    {"date": "2025-01-14", "position": 6},
                    ...
                ],
                "serp_features": ["featured_snippet"],
                "visibility_score": 85  // 0-100
            },
            ...
        ],
        "summary": {
            "total_keywords": 50,
            "improved": 12,
            "declined": 8,
            "unchanged": 28,
            "new": 2,
            "lost": 0,
            "avg_position": 15.4,
            "visibility_score": 72
        }
    }
}
```

```
GET /api/v1/tracking/rankings/{keyword_id}/history
Description: Get detailed ranking history
Authentication: Required

Query Parameters:
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- granularity: daily|weekly|monthly

Response (200 OK):
{
    "status": "success",
    "data": {
        "keyword": "running shoes",
        "domain": "example.com",
        "history": [
            {
                "date": "2025-01-15",
                "position": 5,
                "ranking_url": "https://example.com/running-shoes",
                "serp_features": ["featured_snippet"],
                "competitors_above": [
                    {"domain": "competitor.com", "position": 1},
                    ...
                ]
            },
            ...
        ],
        "statistics": {
            "best_position": 3,
            "worst_position": 15,
            "average_position": 6.8,
            "position_changes": 23,
            "days_tracked": 90,
            "trend": "improving"  // improving, declining, stable
        }
    }
}
```

#### **4.2.5 Trends & Analytics API**

```
GET /api/v1/trends/keywords
Description: Get trending keywords
Authentication: Required

Query Parameters:
- country: US, UK, etc.
- category: all|shopping|sports|technology|...
- timeframe: today|week|month
- min_volume: minimum search volume
- limit: 10-100

Response (200 OK):
{
    "status": "success",
    "data": {
        "trending_keywords": [
            {
                "keyword": "ai chatbot",
                "search_volume": 246000,
                "volume_change_percent": 350,
                "trend_score": 95,
                "related_topics": ["artificial intelligence", "chatgpt"],
                "category": "technology"
            },
            ...
        ],
        "generated_at": "2025-01-15T10:00:00Z"
    }
}
```

```
POST /api/v1/analysis/content-gap
Description: Compare content gaps between domains
Authentication: Required
Rate Limit: 20/min

Request:
{
    "source_domain": "example.com",
    "competitor_domains": ["competitor1.com", "competitor2.com"],
    "country": "US",
    "min_volume": 1000,
    "max_difficulty": 70,
    "limit": 100
}

Response (200 OK):
{
    "status": "success",
    "data": {
        "opportunities": [
            {
                "keyword": "best running shoes for beginners",
                "search_volume": 22000,
                "difficulty_score": 58,
                "gap_score": 85,  // 0-100 (higher = better opportunity)
                "source_position": null,  // not ranking
                "competitors": [
                    {
                        "domain": "competitor1.com",
                        "position": 3,
                        "url": "...",
                        "page_authority": 45
                    },
                    {
                        "domain": "competitor2.com",
                        "position": 7,
                        "url": "...",
                        "page_authority": 38
                    }
                ],
                "opportunity_reasons": [
                    "Competitors ranking with lower authority",
                    "High search volume with medium difficulty",
                    "Related to existing content on your site"
                ]
            },
            ...
        ],
        "summary": {
            "total_opportunities": 247,
            "high_priority": 45,
            "medium_priority": 128,
            "low_priority": 74,
            "estimated_traffic_potential": 125000
        }
    }
}
```

### 4.3 Pagination Strategy

All list endpoints use **cursor-based pagination** for performance:

```
GET /api/v1/keywords/search?page=1&limit=50

Response:
{
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 50,
        "total": 1247,
        "pages": 25,
        "has_next": true,
        "has_prev": false,
        "next_page": 2,
        "prev_page": null
    },
    "links": {
        "first": "/api/v1/keywords/search?page=1&limit=50",
        "last": "/api/v1/keywords/search?page=25&limit=50",
        "next": "/api/v1/keywords/search?page=2&limit=50",
        "prev": null
    }
}
```

For very large datasets (backlinks, SERP history), use **cursor pagination**:

```
GET /api/v1/domains/{domain}/backlinks?cursor=abc123&limit=100

Response:
{
    "data": [...],
    "pagination": {
        "cursor": "def456",
        "has_more": true,
        "limit": 100
    },
    "links": {
        "next": "/api/v1/domains/{domain}/backlinks?cursor=def456&limit=100"
    }
}
```

### 4.4 Filtering & Sorting

**Standard filters across endpoints:**
- `min_volume`: Minimum search volume
- `max_volume`: Maximum search volume
- `min_difficulty`: Minimum difficulty score
- `max_difficulty`: Maximum difficulty score
- `country`: Country code(s) - comma-separated
- `language`: Language code(s)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Standard sorting:**
- `sort`: Field to sort by
- `order`: asc|desc

Example:
```
GET /api/v1/keywords/search?
    keyword=shoes&
    min_volume=10000&
    max_difficulty=60&
    country=US,CA&
    sort=volume&
    order=desc&
    page=1&
    limit=50
```

### 4.5 Caching Strategy

```
Cache-Control Headers:
- Keyword data: max-age=86400 (24 hours)
- Domain overview: max-age=43200 (12 hours)
- SERP data: max-age=21600 (6 hours)
- Ranking data: max-age=3600 (1 hour)
- Trending data: max-age=600 (10 minutes)

ETag Support:
- Include ETag header in responses
- Support If-None-Match requests
- Return 304 Not Modified when appropriate

Example Response Headers:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=86400, public
ETag: "abc123def456"
X-Cache: HIT
X-Cache-Age: 3600
```

---

## 5. Crawler & Data Sources

### 5.1 Data Source Integration

#### **5.1.1 Google APIs**

**Google Ads Keyword Planner API**
```python
Purpose: Search volume, CPC, competition data
Rate Limit: 15,000 requests/day
Cost: Free with Google Ads account
Data Freshness: Updated monthly

Integration:
- OAuth 2.0 authentication
- REST API calls
- Batch requests (up to 100 keywords)
- Response caching (30 days)

Data Retrieved:
- Monthly search volume
- Competition level (low/medium/high)
- Suggested bid (CPC)
- Historical data (12 months)
- Related keywords
```

**Google Search Console API**
```python
Purpose: Verified site ranking data, clicks, impressions
Rate Limit: 1,200 requests/day
Cost: Free
Data Freshness: 2-3 days delay

Integration:
- OAuth 2.0 with Search Console verification
- Query for ranking data, impressions, clicks
- Filter by country, device, search appearance

Data Retrieved:
- Keyword rankings for verified sites
- Click-through rates
- Impressions
- Average position
```

**Google Trends API (Unofficial)**
```python
Purpose: 12-month trend data, related queries
Rate Limit: 1,500 requests/hour
Cost: Free (via pytrends library)
Data Freshness: Real-time

Integration:
- Python pytrends library
- Rotating proxies to avoid blocks
- Delayed requests (2-5 seconds)

Data Retrieved:
- Interest over time (0-100 scale)
- Related topics and queries
- Regional interest
- Rising keywords
```

#### **5.1.2 Bing Webmaster Tools API**

```python
Purpose: Alternative search data, Bing-specific metrics
Rate Limit: 5,000 requests/month
Cost: Free
Data Freshness: Daily updates

Integration:
- API key authentication
- REST API

Data Retrieved:
- Keyword rankings
- Traffic data
- Backlink data (limited)
- Page-level metrics
```

#### **5.1.3 Third-Party SEO APIs**

**DataForSEO API**
```python
Purpose: Comprehensive SERP data, backlinks, metrics
Rate Limit: Based on subscription
Cost: Pay-per-request ($0.001 - $0.02 per request)
Data Freshness: Real-time for SERP, daily for backlinks

Data Retrieved:
- SERP results with rich data
- Backlink profiles
- Keyword difficulty scores
- Domain metrics
- Historical data
```

**SEMrush API** (Alternative)
```python
Purpose: Keyword data, competition analysis
Cost: $199-$499/month + API credits
Data Retrieved:
- Keyword metrics
- Domain analytics
- Competitor analysis
- Backlink data
```

### 5.2 Headless Browser Crawling

For SERP scraping when APIs are insufficient:

```python
Technology Stack:
- Selenium with Chrome/Firefox headless
- Playwright (modern alternative, faster)
- Puppeteer (Node.js option)

Proxy Integration:
- Bright Data (Luminati) residential proxies
- Oxylabs datacenter & residential proxies
- ScraperAPI (handles proxies + CAPTCHA)

CAPTCHA Handling:
- 2Captcha API integration
- Anti-Captcha service
- Automatic retry with new proxy
- Fallback to human verification queue

User Agent Rotation:
- Random desktop user agents
- Mobile user agents for mobile SERP
- Update monthly from real browser stats
```

#### **5.2.1 SERP Crawler Implementation**

```python
# Pseudo-code for SERP crawler

class SERPCrawler:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        
    async def crawl_serp(self, keyword, country, device):
        # Select appropriate proxy
        proxy = self.proxy_manager.get_proxy(country)
        
        # Configure browser
        browser = await self.launch_browser(
            proxy=proxy,
            user_agent=self.get_user_agent(device),
            headless=True
        )
        
        try:
            # Navigate to Google search
            page = await browser.new_page()
            search_url = self.build_search_url(keyword, country)
            await page.goto(search_url, wait_until='networkidle')
            
            # Check for CAPTCHA
            if await self.detect_captcha(page):
                solved = await self.captcha_solver.solve(page)
                if not solved:
                    raise CaptchaError("Failed to solve CAPTCHA")
            
            # Extract SERP data
            serp_data = await self.extract_serp_data(page)
            
            # Take screenshot for archive
            screenshot = await page.screenshot(full_page=True)
            
            return {
                'results': serp_data,
                'screenshot': screenshot,
                'timestamp': datetime.utcnow(),
                'proxy_used': proxy.id
            }
            
        except Exception as e:
            # Mark proxy as failed
            self.proxy_manager.mark_failed(proxy)
            raise
            
        finally:
            await browser.close()
    
    async def extract_serp_data(self, page):
        # Extract organic results
        organic = await page.eval("""
            () => Array.from(document.querySelectorAll('.g')).map(el => ({
                position: Array.from(el.parentNode.children).indexOf(el) + 1,
                title: el.querySelector('h3')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.VwiC3b')?.textContent,
                rich_snippet: extractRichSnippet(el)
            }))
        """)
        
        # Extract SERP features
        featured_snippet = await page.querySelector('.ifM9O')
        people_also_ask = await page.querySelectorAll('.related-question-pair')
        local_pack = await page.querySelector('.rllt__details')
        
        # Extract paid ads
        ads = await page.eval("""
            () => Array.from(document.querySelectorAll('.uEierd')).map(el => ({
                position: 'top' + (Array.from(el.parentNode.children).indexOf(el) + 1),
                title: el.querySelector('.CCgQ5')?.textContent,
                url: el.querySelector('a')?.href,
                description: el.querySelector('.MUxGbd')?.textContent
            }))
        """)
        
        return {
            'organic': organic,
            'ads': ads,
            'features': {
                'featured_snippet': featured_snippet,
                'people_also_ask': people_also_ask,
                'local_pack': local_pack
            }
        }
```

### 5.3 Crawler Scheduler

```python
# Celery beat schedule for periodic crawls

CELERYBEAT_SCHEDULE = {
    'crawl-high-priority-keywords': {
        'task': 'crawlers.tasks.crawl_keywords',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
        'args': ({'priority': 'high'},)
    },
    'crawl-tracked-keywords-daily': {
        'task': 'crawlers.tasks.crawl_tracked_keywords',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'args': ({'frequency': 'daily'},)
    },
    'refresh-domain-backlinks': {
        'task': 'crawlers.tasks.refresh_backlinks',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'args': ()
    },
    'update-keyword-trends': {
        'task': 'crawlers.tasks.update_trends',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),  # Monthly
        'args': ()
    }
}
```

### 5.4 Proxy Management System

```python
class ProxyManager:
    def __init__(self):
        self.redis = Redis()
        self.proxy_pool = []
        
    def load_proxies(self):
        # Load from providers: Bright Data, Oxylabs, etc.
        proxies = [
            {'ip': '1.2.3.4:8080', 'country': 'US', 'type': 'residential'},
            {'ip': '5.6.7.8:8080', 'country': 'UK', 'type': 'datacenter'},
            ...
        ]
        self.proxy_pool = proxies
    
    def get_proxy(self, country='US', exclude_failed=True):
        # Get least recently used proxy for country
        candidates = [p for p in self.proxy_pool if p['country'] == country]
        
        if exclude_failed:
            # Filter out proxies that failed recently
            candidates = [p for p in candidates 
                         if not self.is_in_cooldown(p['ip'])]
        
        # Sort by last used time
        candidates.sort(key=lambda p: self.get_last_used(p['ip']))
        
        if not candidates:
            raise NoProxyAvailable(f"No proxies available for {country}")
        
        selected = candidates[0]
        self.mark_used(selected['ip'])
        return selected
    
    def mark_used(self, proxy_ip):
        self.redis.set(f'proxy:last_used:{proxy_ip}', time.time())
        self.redis.incr(f'proxy:usage_count:{proxy_ip}')
    
    def mark_failed(self, proxy, reason='unknown'):
        # Put proxy in cooldown for 5 minutes
        self.redis.setex(
            f'proxy:cooldown:{proxy["ip"]}',
            300,  # 5 minutes
            reason
        )
        self.redis.incr(f'proxy:failure_count:{proxy["ip"]}')
        
        # If too many failures, remove from pool
        failures = int(self.redis.get(f'proxy:failure_count:{proxy["ip"]}') or 0)
        if failures > 10:
            self.remove_proxy(proxy['ip'])
    
    def is_in_cooldown(self, proxy_ip):
        return self.redis.exists(f'proxy:cooldown:{proxy_ip}')
    
    def get_last_used(self, proxy_ip):
        return float(self.redis.get(f'proxy:last_used:{proxy_ip}') or 0)
    
    def health_check(self, proxy):
        # Test proxy connectivity
        try:
            response = requests.get(
                'https://api.ipify.org?format=json',
                proxies={'https': f'http://{proxy["ip"]}'},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    async def periodic_health_check(self):
        # Run every 5 minutes to check all proxies
        for proxy in self.proxy_pool:
            if not self.health_check(proxy):
                self.mark_failed(proxy, 'health_check_failed')
```

### 5.5 CAPTCHA Handling Strategy

```python
class CaptchaSolver:
    def __init__(self):
        self.twocaptcha_api_key = settings.TWOCAPTCHA_API_KEY
        
    async def solve(self, page, captcha_type='recaptcha_v2'):
        if captcha_type == 'recaptcha_v2':
            return await self.solve_recaptcha_v2(page)
        elif captcha_type == 'recaptcha_v3':
            return await self.solve_recaptcha_v3(page)
        elif captcha_type == 'image':
            return await self.solve_image_captcha(page)
    
    async def solve_recaptcha_v2(self, page):
        # Extract site key
        site_key = await page.evaluate("""
            () => document.querySelector('[data-sitekey]')?.getAttribute('data-sitekey')
        """)
        
        if not site_key:
            return False
        
        # Send to 2Captcha service
        task_id = self.create_captcha_task(
            site_key=site_key,
            page_url=page.url
        )
        
        # Wait for solution (can take 30-60 seconds)
        solution = self.wait_for_solution(task_id, timeout=120)
        
        if solution:
            # Inject solution into page
            await page.evaluate(f"""
                {% raw %}
                () => {{
                    document.getElementById('g-recaptcha-response').innerHTML = '{solution}';
                    document.querySelector('form').submit();
                }}{% endraw %}
                "
            """)
            return True
        
        return False
    
    def create_captcha_task(self, site_key, page_url):
        response = requests.post(
            'https://2captcha.com/in.php',
            data={
                'key': self.twocaptcha_api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': page_url,
                'json': 1
            }
        )
        return response.json()['request']
    
    def wait_for_solution(self, task_id, timeout=120):
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(
                'https://2captcha.com/res.php',
                params={
                    'key': self.twocaptcha_api_key,
                    'action': 'get',
                    'id': task_id,
                    'json': 1
                }
            )
            result = response.json()
            
            if result['status'] == 1:
                return result['request']
            
            time.sleep(5)
        
        return None
```

---

## 6. Ranking & Analytics Engine

### 6.1 Keyword Difficulty Algorithm

```python
def calculate_keyword_difficulty(keyword_data, serp_data):
    """
    Calculate keyword difficulty score (0-100)
    Higher = more difficult to rank
    
    Factors:
    1. Competition level from Google Ads (weight: 20%)
    2. Domain authority of top 10 results (weight: 40%)
    3. Backlink profile of top 10 (weight: 30%)
    4. SERP features present (weight: 10%)
    """
    
    # Factor 1: Competition level
    competition_score = keyword_data['competition'] * 100  # 0-100
    
    # Factor 2: Domain authority
    top_10_domains = serp_data['organic_results'][:10]
    avg_domain_authority = sum(d['domain_authority'] for d in top_10_domains) / 10
    
    # Factor 3: Backlinks
    avg_backlinks = sum(d['backlinks_count'] for d in top_10_domains) / 10
    backlink_score = min(100, (avg_backlinks / 1000) * 100)  # Normalize
    
    # Factor 4: SERP features
    serp_features_count = len(serp_data['serp_features'])
    serp_feature_score = min(100, serp_features_count * 15)
    
    # Weighted calculation
    difficulty = (
        competition_score * 0.20 +
        avg_domain_authority * 0.40 +
        backlink_score * 0.30 +
        serp_feature_score * 0.10
    )
    
    return round(difficulty, 2)
```

### 6.2 Opportunity Score Algorithm

```python
def calculate_opportunity_score(keyword_data, serp_data, user_domain_data):
    """
    Calculate opportunity score (0-100)
    Higher = better opportunity for ranking
    
    Factors:
    1. Search volume (high volume = more opportunity)
    2. Low difficulty (easier to rank)
    3. Low competition from strong domains
    4. User's domain strength relative to competitors
    5. Traffic value (CPC * volume)
    6. Trend direction (rising = more opportunity)
    """
    
    # Factor 1: Search volume score
    volume = keyword_data['search_volume']
    volume_score = min(100, (volume / 100000) * 100)  # Normalize to 100k
    
    # Factor 2: Difficulty score (inverse)
    difficulty = keyword_data['difficulty_score']
    difficulty_score = 100 - difficulty
    
    # Factor 3: Competition gap
    user_authority = user_domain_data['domain_authority']
    avg_competitor_authority = sum(
        d['domain_authority'] for d in serp_data['organic_results'][:10]
    ) / 10
    
    authority_gap = avg_competitor_authority - user_authority
    competition_score = max(0, 100 - authority_gap)
    
    # Factor 4: Traffic value
    traffic_value = keyword_data['cpc_avg'] * volume
    value_score = min(100, (traffic_value / 10000) * 100)
    
    # Factor 5: Trend score
    trend = keyword_data.get('trend_direction', 'stable')
    trend_score = {
        'rising': 100,
        'stable': 50,
        'declining': 20
    }.get(trend, 50)
    
    # Weighted calculation
    opportunity = (
        volume_score * 0.25 +
        difficulty_score * 0.30 +
        competition_score * 0.25 +
        value_score * 0.10 +
        trend_score * 0.10
    )
    
    return round(opportunity, 2)
```

### 6.3 Domain Authority Algorithm

```python
def calculate_domain_authority(domain_data):
    """
    Calculate domain authority (0-100)
    Similar to Moz's DA or Ahrefs DR
    
    Factors:
    1. Total backlinks (log scale)
    2. Unique referring domains (log scale)
    3. Quality of referring domains
    4. Link velocity (new vs lost)
    5. Organic traffic estimate
    6. Number of ranking keywords
    """
    
    # Factor 1: Total backlinks (log scale for diminishing returns)
    backlinks = domain_data['total_backlinks']
    backlink_score = min(100, math.log10(backlinks + 1) * 20)
    
    # Factor 2: Unique referring domains
    referring_domains = domain_data['unique_referring_domains']
    referring_score = min(100, math.log10(referring_domains + 1) * 25)
    
    # Factor 3: Quality of backlinks (avg authority of referring domains)
    avg_referring_authority = domain_data['avg_referring_domain_authority']
    quality_score = avg_referring_authority
    
    # Factor 4: Link velocity
    new_links_month = domain_data['new_backlinks_last_month']
    lost_links_month = domain_data['lost_backlinks_last_month']
    velocity = (new_links_month - lost_links_month) / max(1, backlinks) * 100
    velocity_score = min(100, max(0, 50 + velocity * 10))
    
    # Factor 5: Organic traffic
    organic_traffic = domain_data['organic_traffic_estimate']
    traffic_score = min(100, math.log10(organic_traffic + 1) * 15)
    
    # Factor 6: Ranking keywords
    ranking_keywords = domain_data['organic_keywords_count']
    keyword_score = min(100, math.log10(ranking_keywords + 1) * 20)
    
    # Weighted calculation
    authority = (
        backlink_score * 0.25 +
        referring_score * 0.30 +
        quality_score * 0.20 +
        velocity_score * 0.05 +
        traffic_score * 0.10 +
        keyword_score * 0.10
    )
    
    return round(authority, 2)
```

### 6.4 Trend Analysis Engine

```python
class TrendAnalyzer:
    def analyze_keyword_trend(self, historical_data):
        """
        Analyze 12-month trend data
        Returns: trend_direction, trend_strength, seasonality
        """
        
        # Extract monthly values
        months = sorted(historical_data.keys())
        values = [historical_data[m] for m in months]
        
        # Calculate linear regression
        slope, intercept = self.linear_regression(range(len(values)), values)
        
        # Determine trend direction
        if slope > 5:
            direction = 'rising'
        elif slope < -5:
            direction = 'declining'
        else:
            direction = 'stable'
        
        # Calculate trend strength (0-100)
        strength = min(100, abs(slope) * 2)
        
        # Detect seasonality
        seasonality = self.detect_seasonality(values)
        
        # Calculate volatility
        volatility = np.std(values) / np.mean(values) * 100
        
        return {
            'direction': direction,
            'strength': strength,
            'seasonality': seasonality,
            'volatility': volatility,
            'forecast_next_month': intercept + slope * len(values)
        }
    
    def detect_seasonality(self, values):
        """
        Detect seasonal patterns (monthly, quarterly, annual)
        """
        if len(values) < 12:
            return None
        
        # Check for quarterly pattern
        q1_avg = np.mean(values[0:3] + values[3:6] + values[6:9] + values[9:12])
        # ... more complex seasonality detection
        
        return {
            'has_seasonality': True,
            'pattern': 'quarterly',
            'peak_months': [6, 7, 8]  # Summer peak
        }
    
    def linear_regression(self, x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        return slope, intercept
```

### 6.5 Content Gap Analysis Algorithm

```python
def analyze_content_gap(source_domain, competitor_domains, filters):
    """
    Find keyword opportunities where competitors rank but source doesn't
    """
    
    # Get all keywords competitors rank for
    competitor_keywords = set()
    for competitor in competitor_domains:
        keywords = fetch_competitor_keywords(competitor, filters)
        competitor_keywords.update(keywords)
    
    # Get keywords source domain ranks for
    source_keywords = set(fetch_domain_keywords(source_domain))
    
    # Find gaps (keywords only competitors have)
    gap_keywords = competitor_keywords - source_keywords
    
    # Score each gap keyword
    opportunities = []
    for keyword in gap_keywords:
        # Get keyword data
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        # Calculate scores
        difficulty = calculate_keyword_difficulty(keyword_data, serp_data)
        opportunity = calculate_opportunity_score(
            keyword_data, 
            serp_data,
            fetch_domain_data(source_domain)
        )
        
        # Calculate gap score
        # Higher when multiple competitors rank highly
        competitor_positions = [
            pos for comp in competitor_domains 
            for pos in get_keyword_position(comp, keyword)
            if pos
        ]
        
        if competitor_positions:
            avg_competitor_position = sum(competitor_positions) / len(competitor_positions)
            gap_score = (
                opportunity * 0.5 +
                (100 - difficulty) * 0.3 +
                (100 - avg_competitor_position * 10) * 0.2
            )
        else:
            gap_score = 0
        
        opportunities.append({
            'keyword': keyword,
            'difficulty': difficulty,
            'opportunity': opportunity,
            'gap_score': gap_score,
            'competitor_positions': competitor_positions,
            'volume': keyword_data['search_volume'],
            'cpc': keyword_data['cpc_avg']
        })
    
    # Sort by gap score
    opportunities.sort(key=lambda x: x['gap_score'], reverse=True)
    
    return opportunities
```

### 6.6 Machine Learning for Keyword Clustering

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

class KeywordClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def cluster_keywords(self, keywords, n_clusters=10):
        """
        Group similar keywords into topic clusters
        """
        
        # Vectorize keywords using TF-IDF
        keyword_texts = [kw['keyword'] for kw in keywords]
        tfidf_matrix = self.vectorizer.fit_transform(keyword_texts)
        
        # Apply K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Reduce dimensionality for visualization
        pca = PCA(n_components=2)
        coords = pca.fit_transform(tfidf_matrix.toarray())
        
        # Group keywords by cluster
        clusters = {}
        for i, keyword in enumerate(keywords):
            cluster_id = cluster_labels[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'keywords': [],
                    'total_volume': 0,
                    'avg_difficulty': 0,
                    'center': coords[i].tolist()
                }
            
            clusters[cluster_id]['keywords'].append(keyword)
            clusters[cluster_id]['total_volume'] += keyword['search_volume']
        
        # Calculate cluster statistics and labels
        for cluster_id, cluster_data in clusters.items():
            keywords_in_cluster = cluster_data['keywords']
            
            # Calculate average difficulty
            cluster_data['avg_difficulty'] = sum(
                kw['difficulty_score'] for kw in keywords_in_cluster
            ) / len(keywords_in_cluster)
            
            # Generate cluster label (most common terms)
            cluster_label = self.generate_cluster_label(
                [kw['keyword'] for kw in keywords_in_cluster]
            )
            cluster_data['label'] = cluster_label
        
        return clusters
    
    def generate_cluster_label(self, keywords):
        # Extract most common words
        word_freq = {}
        for keyword in keywords:
            for word in keyword.split():
                if len(word) > 3:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 2-3 words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        return ' '.join(word for word, _ in top_words)
```

### 6.7 Predictive Analytics

```python
class RankingPredictor:
    def predict_ranking_potential(self, target_url, keyword, current_ranking):
        """
        Predict likelihood of ranking improvement
        Uses historical data and ML model
        """
        
        # Extract features
        features = self.extract_features(target_url, keyword, current_ranking)
        
        # Load trained model (e.g., Random Forest or XGBoost)
        model = self.load_model()
        
        # Predict probability of improvement
        prediction = model.predict_proba([features])[0]
        
        # Estimate time to rank in top 10
        estimated_days = self.estimate_time_to_rank(features, prediction)
        
        return {
            'probability_top_10': prediction[1],
            'probability_top_3': prediction[2] if len(prediction) > 2 else 0,
            'estimated_days_to_top_10': estimated_days,
            'confidence': self.calculate_confidence(features),
            'recommended_actions': self.generate_recommendations(features)
        }
    
    def extract_features(self, target_url, keyword, current_ranking):
        page_data = fetch_page_data(target_url)
        keyword_data = fetch_keyword_data(keyword)
        serp_data = fetch_serp_data(keyword)
        
        return {
            'current_position': current_ranking or 100,
            'page_authority': page_data['page_authority'],
            'domain_authority': page_data['domain_authority'],
            'backlinks_count': page_data['backlinks_count'],
            'content_length': page_data['content_length'],
            'keyword_density': page_data['keyword_density'],
            'keyword_difficulty': keyword_data['difficulty_score'],
            'search_volume': keyword_data['search_volume'],
            'avg_competitor_authority': serp_data['avg_domain_authority'],
            'serp_features_count': len(serp_data['serp_features']),
            'has_featured_snippet': 'featured_snippet' in serp_data['serp_features']
        }
    
    def generate_recommendations(self, features):
        recommendations = []
        
        if features['content_length'] < 1500:
            recommendations.append({
                'priority': 'high',
                'action': 'Increase content length',
                'details': f'Current: {features["content_length"]} words. Target: 2000+ words',
                'impact': 'medium'
            })
        
        if features['backlinks_count'] < 50:
            recommendations.append({
                'priority': 'high',
                'action': 'Build more backlinks',
                'details': f'Current: {features["backlinks_count"]}. Target: 100+ backlinks',
                'impact': 'high'
            })
        
        if features['keyword_density'] < 0.5:
            recommendations.append({
                'priority': 'medium',
                'action': 'Optimize keyword usage',
                'details': 'Include target keyword more naturally in content',
                'impact': 'low'
            })
        
        return recommendations
```

---

## 7. User System

### 7.1 Authentication & Authorization

```python
# JWT token structure
{
    "user_id": 12345,
    "email": "user@example.com",
    "plan": "pro",
    "permissions": ["keyword_search", "domain_analysis", "rank_tracking"],
    "iat": 1705320000,
    "exp": 1705406400  # 24 hour expiry
}

# API Key structure
{
    "key_id": "ak_live_abc123xyz789",
    "user_id": 12345,
    "name": "Production API Key",
    "permissions": ["keyword_search", "serp_analysis"],
    "rate_limit": 500,  # requests per minute
    "created_at": "2025-01-01T00:00:00Z",
    "last_used_at": "2025-01-15T10:30:00Z"
}
```

### 7.2 Subscription Plans

```yaml
Plans:
  Free:
    price: $0/month
    features:
      keyword_searches: 10/day
      domain_analyses: 3/day
      serp_checks: 10/day
      tracked_keywords: 0
      historical_data: 7 days
      api_access: false
      export: false
      team_members: 1
      
  Pro:
    price: $99/month
    features:
      keyword_searches: 100/day (3000/month)
      domain_analyses: 50/day
      serp_checks: 100/day
      tracked_keywords: 500
      rank_checks_frequency: daily
      historical_data: 90 days
      api_access: true
      api_calls: 10,000/month
      export: true (CSV, Excel)
      team_members: 3
      reports: 10/month
      
  Agency:
    price: $299/month
    features:
      keyword_searches: unlimited
      domain_analyses: unlimited
      serp_checks: unlimited
      tracked_keywords: 5000
      rank_checks_frequency: daily
      historical_data: 2 years
      api_access: true
      api_calls: 100,000/month
      export: true (CSV, Excel, API)
      team_members: 10
      reports: unlimited
      white_label: true
      priority_support: true
      
  Enterprise:
    price: Custom
    features:
      everything_unlimited: true
      dedicated_account_manager: true
      custom_integrations: true
      on_premise_option: true
      sla_guarantee: 99.9%
```

### 7.3 Quota Management

```python
class QuotaManager:
    def check_quota(self, user_id, action_type):
        """
        Check if user has quota remaining for action
        Returns: (allowed: bool, remaining: int, reset_at: datetime)
        """
        
        # Get user plan
        user = fetch_user(user_id)
        plan = PLANS[user.plan_type]
        
        # Get quota limits
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        quota_used = redis.get(quota_key) or 0
        quota_limit = plan['features'][f'{action_type}']
        
        # Check if unlimited
        if quota_limit == 'unlimited':
            return (True, -1, None)
        
        # Check limit
        allowed = int(quota_used) < int(quota_limit)
        remaining = max(0, int(quota_limit) - int(quota_used))
        reset_at = datetime.combine(date.today() + timedelta(days=1), datetime.min.time())
        
        return (allowed, remaining, reset_at)
    
    def consume_quota(self, user_id, action_type, amount=1):
        """
        Consume quota for action
        """
        quota_key = f'quota:{user_id}:{action_type}:{date.today()}'
        
        # Increment usage
        new_usage = redis.incr(quota_key, amount)
        
        # Set expiry to end of day if first use
        if new_usage == amount:
            redis.expireat(quota_key, datetime.combine(
                date.today() + timedelta(days=1),
                datetime.min.time()
            ))
        
        # Log usage
        log_quota_usage(user_id, action_type, amount)
        
        return new_usage
```

### 7.4 Role-Based Access Control (RBAC)

```python
ROLES = {
    'owner': {
        'permissions': [
            'manage_project',
            'manage_team',
            'view_billing',
            'manage_billing',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'admin': {
        'permissions': [
            'manage_team',
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data',
            'api_access'
        ]
    },
    'editor': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'rank_tracking',
            'export_data'
        ]
    },
    'viewer': {
        'permissions': [
            'keyword_research',
            'domain_analysis',
            'view_rankings'
        ]
    }
}

def check_permission(user_id, project_id, permission):
    # Get user's role in project
    membership = fetch_project_membership(user_id, project_id)
    
    if not membership:
        return False
    
    # Check if role has permission
    role_permissions = ROLES[membership.role]['permissions']
    return permission in role_permissions
```

---

## 8. Dashboard & UI Modules

### 8.1 Dashboard Components

#### **8.1.1 Keyword Explorer Module**

```
Components:
├── Search Bar
│   ├── Keyword input with autocomplete
│   ├── Country selector (dropdown with flags)
│   ├── Language selector
│   └── Device type selector (desktop/mobile/tablet)
│
├── Results Table
│   ├── Columns: Keyword, Volume, CPC, Competition, Difficulty, Trend
│   ├── Sortable columns
│   ├── Filterable (volume range, difficulty range)
│   ├── Bulk select for export
│   └── Add to project button
│
├── Keyword Details Panel (expandable row)
│   ├── 12-month trend chart
│   ├── Related keywords list
│   ├── Question keywords
│   ├── SERP features present
│   └── Top 10 ranking URLs
│
└── Sidebar Filters
    ├── Search volume range slider
    ├── Difficulty range slider
    ├── Competition level checkboxes
    ├── SERP features filters
    └── Keyword intent filters (informational, commercial, transactional)

Features:
- Real-time search with debounce (300ms)
- Export to CSV/Excel
- Save search history
- Favorite keywords
- Bulk keyword upload (CSV)
```

#### **8.1.2 Domain Overview Module**

```
Layout:
┌─────────────────────────────────────────────────────────────┐
│ Domain Input & Analysis                                      │
│ [example.com                              ] [Analyze]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Authority: 75│ Backlinks:   │ Org Keywords:│ Est. Traffic:│
│              │ 125,847      │ 45,231       │ 850,000/mo   │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Traffic Trend (Last 12 Months) - Line Chart                 │
│ [Interactive chart showing organic traffic over time]        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Top Organic Keywords         │ Top Pages                     │
│ [Sortable table]             │ [Sortable table]              │
│ - Keyword                    │ - URL                         │
│ - Position                   │ - Traffic                     │
│ - Volume                     │ - Keywords                    │
│ - Traffic                    │ - Backlinks                   │
└──────────────────────────────┴──────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────┐
│ Backlink Growth              │ Competitors                   │
│ [Area chart]                 │ [List with metrics]           │
│ New vs Lost backlinks        │ - Domain                      │
│                              │ - Authority                   │
│                              │ - Keyword Overlap             │
└──────────────────────────────┴──────────────────────────────┘

Tabs:
- Overview
- Organic Keywords
- Top Pages
- Backlinks
- Competitors
- Historical Data
```

#### **8.1.3 SERP Overview Module**

```
Components:
├── SERP Search
│   ├── Keyword input
│   ├── Location selector (with map)
│   ├── Device type tabs
│   └── Analyze button
│
├── SERP Preview
│   ├── Visual SERP representation
│   ├── Organic results (1-100)
│   ├── Paid ads highlighted
│   ├── SERP features marked
│   └── Each result expandable for details
│
├── SERP Analysis
│   ├── Difficulty score gauge
│   ├── Opportunity score gauge
│   ├── Avg domain authority
│   ├── Avg backlinks
│   ├── Content length avg
│   └── SERP features breakdown
│
├── Competitor Analysis Table
│   ├── Competitor Analysis Table
│   ├── Position, Domain, DA, Backlinks, Content Length
│   ├── Compare button (multi-select)
│   └── Export to PDF
│
└── Content Recommendations
    ├── Suggested content length
    ├── Topics to cover
    ├── Keywords to include
    └── SERP feature opportunities

Features:
- Side-by-side SERP comparison (desktop vs mobile)
- Historical SERP data (change tracking)
- Screenshot archive
- SERP feature trend analysis
```

#### **8.1.4 Rank Tracker Module**

```
Dashboard View:
┌─────────────────────────────────────────────────────────────┐
│ Tracking Overview                                            │
│ ┌──────────┬──────────┬──────────┬──────────┐              │
│ │ Total    │ Improved │ Declined │ Unchanged│              │
│ │ Keywords │   12     │    8     │    30    │              │
│ │   50     │  ↑ 24%   │  ↓ 16%   │   60%    │              │
│ └──────────┴──────────┴──────────┴──────────┘              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Visibility Score Trend (Last 30 Days)                       │
│ [Line chart showing overall visibility over time]           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Tracked Keywords                                             │
│ ┌──────────┬─────────┬─────────┬──────────┬────────────┐   │
│ │ Keyword  │ Current │ Previous│ Change   │ Best/Worst │   │
│ ├──────────┼─────────┼─────────┼──────────┼────────────┤   │
│ │ shoes    │    5    │    7    │ ↑ 2 🟢  │  3 / 15    │   │
│ │ boots    │   15    │   12    │ ↓ 3 🔴  │  8 / 20    │   │
│ │ sandals  │    8    │    8    │   -     │  6 / 12    │   │
│ └──────────┴─────────┴─────────┴──────────┴────────────┘   │
│ [View Chart] [View SERP] [Compare Competitors]              │
└─────────────────────────────────────────────────────────────┘

Features:
- Daily/weekly/monthly check frequency
- Email alerts for rank changes
- Tag-based filtering
- Competitor comparison view
- Export reports (PDF, CSV)
- Share tracking links with clients
```

#### **8.1.5 Backlink Analysis Module**

```
Components:
├── Backlink Overview Stats
│   ├── Total backlinks
│   ├── Referring domains
│   ├── New/Lost (last 30 days)
│   └── Follow/Nofollow ratio
│
├── Backlink Growth Chart
│   └── Historical backlink acquisition
│
├── Backlinks Table
│   ├── Columns: Source URL, Target URL, Anchor Text, DA, Type, Date
│   ├── Filters: Follow type, Date range, Domain authority
│   ├── Search by domain or anchor text
│   └── Export functionality
│
├── Top Referring Domains
│   └── List of domains with most backlinks
│
├── Anchor Text Distribution
│   └── Pie chart or word cloud
│
└── Backlink Quality Analysis
    ├── Spam score distribution
    ├── Geographic distribution
    └── Link type breakdown

Features:
- Disavow file generator
- Competitor backlink comparison
- Link building opportunity finder
- Broken backlink detector
```

#### **8.1.6 Content Gap Analysis Module**

```
Workflow:
1. Input your domain
2. Add competitor domains (up to 5)
3. Set filters (volume, difficulty)
4. Run analysis

Results View:
┌─────────────────────────────────────────────────────────────┐
│ Content Gap Opportunities                                    │
│                                                              │
│ Filters: [Min Volume: 1000] [Max Difficulty: 70] [Apply]   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Opportunity Keywords                                         │
│ ┌──────────────┬────────┬────────┬──────────────────────┐   │
│ │ Keyword      │ Volume │ Diff   │ Competitors Ranking  │   │
│ ├──────────────┼────────┼────────┼──────────────────────┤   │
│ │ running tips │ 22,000 │   58   │ C1(#3), C2(#7)      │   │
│ │ shoe care    │ 18,000 │   45   │ C1(#2), C2(#5), C3  │   │
│ └──────────────┴────────┴────────┴──────────────────────┘   │
│ [Add to Project] [Create Content Brief] [Export]            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Keyword Overlap Venn Diagram                                │
│ [Visual representation of keyword overlap between domains]   │
└─────────────────────────────────────────────────────────────┘

Features:
- Content brief generator
- Priority scoring
- Estimated traffic potential
- Topic clustering
```

#### **8.1.7 Project Management Module**

```
Project Dashboard:
├── Project List (sidebar)
│   ├── Project name
│   ├── Target domain
│   └── Quick stats
│
├── Project Overview
│   ├── Saved keywords (count)
│   ├── Tracked keywords (count)
│   ├── Domains analyzed
│   └── Team members
│
├── Recent Activity Feed
│   └── Timeline of actions and changes
│
└── Quick Actions
    ├── Add keywords
    ├── Set up tracking
    ├── Invite team member
    └── Generate report

Features:
- Multi-project support
- Project templates
- Team collaboration
- Activity logs
- Project notes
```

#### **8.1.8 Reporting Module**

```
Report Builder:
┌─────────────────────────────────────────────────────────────┐
│ Create New Report                                            │
│                                                              │
│ Report Type:                                                │
│ ○ Keyword Research Report                                   │
│ ○ Domain Overview Report                                    │
│ ● Rank Tracking Report                                      │
│ ○ Backlink Analysis Report                                  │
│ ○ Custom Report                                             │
│                                                              │
│ Date Range: [Last 30 Days ▼]                               │
│                                                              │
│ Include:                                                    │
│ ☑ Executive Summary                                         │
│ ☑ Ranking Changes Chart                                     │
│ ☑ Keyword Performance Table                                 │
│ ☑ Competitor Comparison                                     │
│ ☑ Recommendations                                           │
│                                                              │
│ Branding (Agency Plan):                                     │
│ [Your Logo] [Primary Color] [Company Name]                 │
│                                                              │
│ [Preview Report] [Generate PDF] [Schedule Email]            │
└─────────────────────────────────────────────────────────────┘

Scheduled Reports:
- Daily/weekly/monthly schedules
- Email to multiple recipients
- Auto-generated on specific dates
- White-label branding
```

### 8.2 UI/UX Best Practices

```yaml
Design Principles:
  - Data-heavy but not overwhelming
  - Progressive disclosure (expandable sections)
  - Visual hierarchy (important metrics prominent)
  - Real-time updates where appropriate
  - Responsive design (desktop-first, mobile-friendly)
  - Dark mode support

Performance:
  - Lazy loading for large tables
  - Virtual scrolling for 1000+ rows
  - Skeleton screens during data fetch
  - Optimistic UI updates
  - Background data refresh

Accessibility:
  - WCAG 2.1 AA compliance
  - Keyboard navigation
  - Screen reader support
  - Sufficient color contrast
  - Alt text for charts/images
```

---

## 9. Scalability, Performance & Security

### 9.1 Scalability Architecture

#### **9.1.1 Horizontal Scaling Strategy**

```yaml
Application Tier:
  - Stateless services (easy to scale)
  - Auto-scaling groups (AWS ASG or K8s HPA)
  - Scale triggers:
    * CPU > 70%
    * Memory > 80%
    * Request queue depth > 100
  - Min instances: 3 (HA across AZs)
  - Max instances: 50 (cost limit)

Database Tier:
  - PostgreSQL with read replicas
    * 1 primary (writes)
    * 3-5 read replicas (queries)
    * Connection pooling (PgBouncer)
  - MongoDB sharded cluster
    * 3 config servers
    * 3+ shard servers
    * 2 mongos routers
  - Redis Cluster
    * 6+ nodes (3 masters, 3 replicas)
    * Automatic failover

Worker Tier:
  - Celery workers with auto-scaling
  - Scale based on queue depth
  - Different worker pools:
    * CPU-intensive: 4 workers per instance
    * I/O-intensive: 10 workers per instance
  - Spot instances for cost savings

Cache Tier:
  - Multi-layer caching
  - CDN for static assets (CloudFlare)
  - Redis for application cache
  - Application-level cache (in-memory)
```

#### **9.1.2 Load Balancing**

```
Cloud Architecture:

                    ┌─────────────────────┐
                    │   CloudFlare CDN    │
                    │   (DDoS protection) │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Application Load   │
                    │     Balancer        │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐  ┌──────────▼────────┐  ┌────────▼──────┐
│   API Gateway  │  │   API Gateway     │  │  API Gateway  │
│   Instance 1   │  │   Instance 2      │  │  Instance 3   │
│   (us-east-1a) │  │   (us-east-1b)    │  │  (us-east-1c) │
└───────┬────────┘  └──────────┬────────┘  └────────┬──────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Service Mesh      │
                    │   (Microservices)   │
                    └─────────────────────┘

Load Balancing Algorithm:
- Round-robin with health checks
- Sticky sessions for WebSocket
- Weighted routing for gradual rollouts
- Geographic routing for global users
```

#### **9.1.3 Database Optimization**

```sql
-- Index optimization
CREATE INDEX CONCURRENTLY idx_keywords_country_lang_volume 
ON keywords(country, language, search_volume DESC);

-- Partial indexes for common queries
CREATE INDEX idx_active_backlinks 
ON backlinks(target_domain_id, last_seen_at DESC) 
WHERE is_active = true;

-- Covering indexes to avoid table lookups
CREATE INDEX idx_keywords_search_covering 
ON keywords(keyword_normalized, country, language) 
INCLUDE (search_volume, difficulty_score);

-- Query optimization
-- Use EXPLAIN ANALYZE to identify slow queries
-- Add indexes based on actual query patterns
-- Use materialized views for complex aggregations

-- Materialized view for domain metrics summary
CREATE MATERIALIZED VIEW domain_metrics_summary AS
SELECT 
    d.domain_id,
    d.domain_name,
    dm.domain_authority,
    COUNT(DISTINCT b.source_domain_id) as unique_referring_domains,
    COUNT(b.backlink_id) as total_backlinks,
    COUNT(DISTINCT dok.keyword_id) as organic_keywords_count
FROM domains d
LEFT JOIN domain_metrics dm ON d.domain_id = dm.domain_id 
    AND dm.metric_date = CURRENT_DATE
LEFT JOIN backlinks b ON d.domain_id = b.target_domain_id 
    AND b.is_active = true
LEFT JOIN domain_organic_keywords dok ON d.domain_id = dok.domain_id 
    AND dok.position_date = CURRENT_DATE
GROUP BY d.domain_id, d.domain_name, dm.domain_authority;

-- Refresh materialized view nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY domain_metrics_summary;

-- Partitioning for time-series data
CREATE TABLE ranking_history (
    history_id BIGSERIAL,
    tracked_keyword_id BIGINT,
    check_date DATE NOT NULL,
    position INT,
    PRIMARY KEY (history_id, check_date)
) PARTITION BY RANGE (check_date);

-- Create monthly partitions
CREATE TABLE ranking_history_2025_01 
PARTITION OF ranking_history 
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

#### **9.1.4 Caching Strategy (Detailed)**

```python
# Multi-level cache implementation

class CacheManager:
    def __init__(self):
        self.l1_cache = LRUCache(maxsize=1000)  # In-memory
        self.l2_cache = RedisClient()  # Redis
        self.l3_cache = CDNClient()  # CloudFlare
    
    def get(self, key, fetch_func=None, ttl=3600):
        # L1: Check in-memory cache
        value = self.l1_cache.get(key)
        if value is not None:
            metrics.increment('cache.l1.hit')
            return value
        
        # L2: Check Redis
        value = self.l2_cache.get(key)
        if value is not None:
            metrics.increment('cache.l2.hit')
            # Promote to L1
            self.l1_cache.set(key, value)
            return value
        
        # L3: Check CDN (for static data)
        if self.is_cdn_cacheable(key):
            value = self.l3_cache.get(key)
            if value is not None:
                metrics.increment('cache.l3.hit')
                # Promote to L2 and L1
                self.l2_cache.setex(key, ttl, value)
                self.l1_cache.set(key, value)
                return value
        
        # Cache miss - fetch from source
        if fetch_func:
            metrics.increment('cache.miss')
            value = fetch_func()
            
            # Store in all cache levels
            self.l1_cache.set(key, value)
            self.l2_cache.setex(key, ttl, value)
            
            if self.is_cdn_cacheable(key):
                self.l3_cache.set(key, value, ttl)
            
            return value
        
        return None
    
    def invalidate(self, key):
        # Invalidate all cache levels
        self.l1_cache.delete(key)
        self.l2_cache.delete(key)
        self.l3_cache.purge(key)

# Cache warming strategy
def warm_cache():
    # Pre-populate cache with popular data
    popular_keywords = get_popular_keywords(limit=1000)
    
    for keyword in popular_keywords:
        cache_key = f"keyword:{keyword.id}"
        data = fetch_keyword_data(keyword.id)
        cache_manager.set(cache_key, data, ttl=86400)
```

### 9.2 Performance Optimization

#### **9.2.1 Database Query Optimization**

```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@localhost/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Batch operations
def bulk_insert_keywords(keywords):
    # Instead of individual inserts, use bulk operations
    session.bulk_insert_mappings(Keyword, keywords)
    session.commit()

# Use pagination efficiently
def get_keywords_paginated(page, limit=50):
    # Use keyset pagination for large datasets
    last_id = request.args.get('last_id', 0)
    
    keywords = session.query(Keyword)\
        .filter(Keyword.id > last_id)\
        .order_by(Keyword.id)\
        .limit(limit)\
        .all()
    
    return {
        'keywords': keywords,
        'next_cursor': keywords[-1].id if keywords else None
    }

# Eager loading to avoid N+1 queries
def get_keywords_with_metrics():
    keywords = session.query(Keyword)\
        .options(joinedload(Keyword.metrics))\
        .options(joinedload(Keyword.trends))\
        .all()
    
    return keywords
```

#### **9.2.2 API Response Optimization**

```python
# Compression
from flask import Flask, make_response
import gzip

@app.after_request
def compress_response(response):
    if response.status_code < 200 or response.status_code >= 300:
        return response
    
    if 'gzip' in request.headers.get('Accept-Encoding', ''):
        response.direct_passthrough = False
        
        if response.mimetype.startswith('application/json'):
            gzip_buffer = BytesIO()
            gzip_file = gzip.GzipFile(
                mode='wb',
                fileobj=gzip_buffer
            )
            gzip_file.write(response.data)
            gzip_file.close()
            
            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Length'] = len(response.data)
    
    return response

# Response field filtering
@app.route('/api/v1/keywords/<keyword_id>')
def get_keyword(keyword_id):
    # Allow clients to specify which fields they need
    fields = request.args.get('fields', '').split(',')
    
    keyword = fetch_keyword(keyword_id)
    
    if fields:
        # Return only requested fields
        response_data = {
            field: getattr(keyword, field) 
            for field in fields 
            if hasattr(keyword, field)
        }
    else:
        response_data = keyword.to_dict()
    
    return jsonify(response_data)
```

#### **9.2.3 Async Processing**

```python
# Use async/await for I/O operations
import asyncio
import aiohttp

async def fetch_multiple_sources(keyword):
    async with aiohttp.ClientSession() as session:
        # Fetch from multiple APIs concurrently
        tasks = [
            fetch_google_ads(session, keyword),
            fetch_google_trends(session, keyword),
            fetch_third_party_api(session, keyword)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        combined_data = {}
        for result in results:
            if isinstance(result, dict):
                combined_data.update(result)
        
        return combined_data

# Queue background jobs
@app.route('/api/v1/keywords/search', methods=['POST'])
def search_keyword():
    keyword = request.json['keyword']
    
    # Quick cache check
    cached = cache_manager.get(f'keyword:{keyword}')
    if cached:
        return jsonify(cached)
    
    # Queue background job for fresh data
    job_id = str(uuid.uuid4())
    celery_app.send_task(
        'tasks.fetch_keyword_data',
        args=[keyword, job_id],
        priority=1
    )
    
    return jsonify({
        'status': 'processing',
        'job_id': job_id,
        'estimated_time': 30
    }), 202
```

### 9.3 Security Implementation

#### **9.3.1 Authentication Security**

```python
# JWT implementation with security best practices
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id, email, plan):
    payload = {
        'user_id': user_id,
        'email': email,
        'plan': plan,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24),
        'jti': str(uuid.uuid4())  # Unique token ID for revocation
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    # Store token in Redis for revocation capability
    redis.setex(
        f'token:{payload["jti"]}',
        86400,  # 24 hours
        user_id
    )
    
    return token

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        
        # Check if token is revoked
        if not redis.exists(f'token:{payload["jti"]}'):
            raise AuthenticationError('Token revoked')
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise AuthenticationError('Token expired')
    except jwt.JWTError:
        raise AuthenticationError('Invalid token')

def revoke_token(token):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
    redis.delete(f'token:{payload["jti"]}')
```

#### **9.3.2 API Security**

```python
# Rate limiting with sliding window
def check_rate_limit(user_id, endpoint, limit=100, window=60):
    key = f'ratelimit:{user_id}:{endpoint}'
    now = time.time()
    
    # Remove old requests outside the window
    redis.zremrangebyscore(key, 0, now - window)
    
    # Count requests in current window
    request_count = redis.zcard(key)
    
    if request_count >= limit:
        # Get oldest request timestamp
        oldest = redis.zrange(key, 0, 0, withscores=True)
        if oldest:
            retry_after = int(oldest[0][1] + window - now)
            raise RateLimitExceeded(
                f'Rate limit exceeded. Retry after {retry_after} seconds'
            )
    
    # Add current request
    redis.zadd(key, {str(uuid.uuid4()): now})
    redis.expire(key, window)
    
    return {
        'limit': limit,
        'remaining': limit - request_count - 1,
        'reset': int(now + window)
    }

# Input validation
from pydantic import BaseModel, validator, constr

class KeywordSearchRequest(BaseModel):
    keyword: constr(min_length=1, max_length=200)
    country: constr(regex='^[A-Z]{2}# 🎯 Keyword Research & SEO Analysis Platform
## Complete System Design Document