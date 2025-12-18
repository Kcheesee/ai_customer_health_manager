# Customer Pulse - Product Specification Document
## AI-Powered Customer Health Scoring Platform

**Version:** 1.0  
**Date:** December 11, 2024  
**Author:** Kareem Primo  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [User Roles & Permissions](#3-user-roles--permissions)
4. [Core Features](#4-core-features)
5. [Data Models](#5-data-models)
6. [Health Scoring Algorithm](#6-health-scoring-algorithm)
7. [Keyword Lexicon](#7-keyword-lexicon)
8. [API Routes](#8-api-routes)
9. [UI Wireframes](#9-ui-wireframes)
10. [LLM Integration](#10-llm-integration)
11. [Integrations Architecture](#11-integrations-architecture)
12. [Technical Stack](#12-technical-stack)
13. [Task Breakdown](#13-task-breakdown)

---

## 1. Executive Summary

### Problem Statement
Existing customer success platforms (Gainsight, ChurnZero, Totango) cost $18K-50K/year and excel at structured data aggregation but are weak at:
- Processing unstructured inputs (meeting notes, email threads, call transcripts)
- Explaining the "why" behind health scores with narrative context
- Automating the CSM Pulse input that remains manual everywhere

### Solution
Customer Pulse is an AI-powered customer health scoring platform that:
- Ingests messy inputs (emails, notes, contracts) and extracts structured signals
- Uses keyword pre-filtering to reduce LLM costs by 60-70%
- Provides narrative explanations and actionable recommendations
- Supports Enterprise License Agreements (ELAs) with multi-office structures
- Includes federal/compliance signal detection (FedRAMP, HIPAA, 508, ATO)

### Target Users
- Customer Success Managers (CSMs)
- Account Executives (AEs)
- CS Leadership / Managers

---

## 2. Product Overview

### Core Value Proposition
Transform unstructured customer communications into actionable health insights with AI-powered analysis, proactive alerts, and strategic recommendations.

### Key Differentiators
| Feature | Traditional Platforms | Customer Pulse |
|---------|----------------------|----------------|
| Unstructured data processing | Manual entry required | AI-powered parsing |
| Health explanations | Score only | Narrative + recommendations |
| Cost | $18K-50K/year | Self-hosted / low cost |
| Federal compliance signals | Generic | Built-in (FedRAMP, HIPAA, 508, ATO) |
| Setup complexity | Weeks of implementation | Minutes to start |

### MVP Scope
**Included in v1.0:**
- ✅ Email chain input (copy/paste or file upload)
- ✅ Manual notes input
- ✅ Contract fields (manual + AI-assisted parsing)
- ✅ 6-pillar health scoring with decay
- ✅ Keyword pre-filter + LLM analysis
- ✅ Account dashboard with timeline
- ✅ Portfolio overview with filtering
- ✅ Multi-office ELA support (tabs)
- ✅ In-app notifications
- ✅ Follow-up reminders
- ✅ Role-based access (CSM vs AE)

**Roadmap (v1.5+):**
- 📅 Gmail OAuth integration (auto-sync)
- 📅 Google Calendar integration
- 📄 Contract PDF auto-parsing
- 📊 Reporting/exports (PDF, CSV)
- 🔔 Email notifications
- 🔔 Slack integration
- 📹 Zoom/Teams transcript import
- 🔗 Salesforce/HubSpot integration
- 📱 Mobile app with push notifications

---

## 3. User Roles & Permissions

### Role Definitions

| Role | Description | Access Level |
|------|-------------|--------------|
| **Admin** | System administrator | Full access, user management, settings |
| **Manager** | CS/Sales leadership | View all accounts, team dashboards, reports |
| **CSM** | Customer Success Manager | Own accounts + shared accounts, full edit |
| **AE** | Account Executive | Own accounts, limited edit (contracts, contacts) |

### Permission Matrix

| Action | Admin | Manager | CSM | AE |
|--------|-------|---------|-----|-----|
| View own accounts | ✅ | ✅ | ✅ | ✅ |
| View all accounts | ✅ | ✅ | ❌ | ❌ |
| Edit account details | ✅ | ✅ | ✅ | ✅ |
| Add/edit contracts | ✅ | ✅ | ✅ | ✅ |
| Add notes/inputs | ✅ | ✅ | ✅ | ❌ |
| View team dashboard | ✅ | ✅ | ❌ | ❌ |
| Manage users | ✅ | ❌ | ❌ | ❌ |
| Configure settings | ✅ | ❌ | ❌ | ❌ |
| Export reports | ✅ | ✅ | ✅ | ❌ |

---

## 4. Core Features

### 4.1 Account Management

#### Account Types
- **Standard Account**: Single entity, single point of contact
- **ELA Parent Account**: Enterprise License Agreement with multiple child offices
- **ELA Child Office**: Individual office under an ELA

#### Account Fields
```
- account_name: string (required)
- account_type: enum [standard, ela_parent, ela_child]
- parent_account_id: UUID (for ela_child only)
- account_email: string (dedicated CC email for email filtering)
- industry: string
- tier: enum [enterprise, mid_market, smb, startup]
- owner_id: UUID (CSM assignment)
- ae_id: UUID (AE assignment)
- created_at: datetime
- updated_at: datetime
```

### 4.2 Contract Management

#### Contract Types
- SaaS Subscription
- Consulting/SOW
- Master Service Agreement (MSA)
- Enterprise License Agreement (ELA)

#### Contract Fields
```
Core Identifiers:
- contract_name: string
- contract_type: enum
- account_id: UUID
- status: enum [draft, active, pending_renewal, expired, terminated]

Dates & Terms:
- effective_date: date
- end_date: date
- term_length: enum [monthly, quarterly, annual, multi_year, project]
- auto_renewal: boolean
- notice_period_days: integer
- non_renewal_deadline: date (calculated: end_date - notice_period_days)

Financial:
- total_contract_value: decimal
- arr: decimal
- mrr: decimal
- payment_terms: enum [net_30, net_60, auto_charge]
- billing_frequency: enum [monthly, quarterly, annual, milestone]
- pricing_model: enum [flat_rate, per_user, usage_based, tiered]

Scope:
- licensed_seats: integer
- products_modules: string[] (array of product names)
- deliverables_summary: text

Contacts:
- primary_signer: string
- economic_buyer: string

Risk Indicators:
- sla_committed: text
- termination_notes: text
- early_termination_penalty: boolean
- competitor_clause: boolean

Compliance (Federal):
- fedramp_required: boolean
- fisma_level: enum [low, moderate, high, none]
- hipaa_required: boolean
- section_508_required: boolean
- ato_status: enum [active, pending, expired, none]
- ato_expiry_date: date
```

### 4.3 Input Methods

#### Email Input (MVP)
- Copy/paste email thread into text area
- Upload .eml or .msg file
- System extracts: sender, recipients, date, subject, body
- Associates with account via account_email match or manual selection

#### Notes Input
- Free-text note entry
- Note type classification: meeting_note, call_note, internal_note, qbr_note
- Optional: attendees, date override, sentiment override

#### Future: Gmail OAuth Sync
- Connect Gmail account
- Filter emails by account_email (CC'd account alias)
- Auto-sync options: hourly, every_6_hours, daily
- Historical depth: 6 months default, up to 3 years
- Manual sync trigger available

### 4.4 Health Scoring

Six pillars with configurable weights:

| Pillar | Default Weight | Measures |
|--------|---------------|----------|
| Engagement Frequency | 20% | Meeting cadence, response times, communication volume |
| Communication Sentiment | 20% | Tone/mood of interactions, positivity ratio |
| Request Patterns | 15% | Type & volume (support vs feature vs escalation) |
| Relationship Depth | 15% | Champion strength, stakeholder breadth |
| Product Satisfaction | 15% | Expressed satisfaction, complaint frequency |
| Expansion Readiness | 15% | Growth signals, upsell indicators |

#### Scoring Scale
- **Green (Healthy):** 70-100
- **Yellow (Watch):** 50-69
- **Red (At Risk):** 0-49

#### Decay Logic
- No new communication in X days → score decays
- Configurable "check-in" interval per account (default: 14 days)
- Decay rate: -2 points per day after check-in threshold
- Floor: Score cannot decay below 30 (prevents false emergencies)

### 4.5 Alerts & Notifications

#### Alert Types
| Alert | Trigger | Priority |
|-------|---------|----------|
| Health Drop | Score drops >10 points in 7 days | High |
| Churn Risk Keywords | Critical keywords detected | Critical |
| Renewal Approaching | Within notice period | High |
| Non-Renewal Deadline | 7 days before deadline | Critical |
| Follow-up Overdue | Commitment not fulfilled | Medium |
| No Contact Decay | Exceeds check-in interval | Medium |
| Champion Change | Key contact departure detected | High |
| Expansion Signal | Positive expansion keywords | Low (opportunity) |

#### Notification Channels (MVP: In-app only, others stubbed)
- In-app notifications (bell icon, notification center)
- Email digest (daily/weekly summary) - stub
- Real-time email alerts (critical only) - stub
- Slack integration - stub
- Mobile push - stub

### 4.6 Follow-up Reminders

#### Trigger Detection
System scans inputs for commitment language:
```
Commitment phrases:
- "I'll send", "I'll get back", "will follow up"
- "by end of week", "by Friday", "tomorrow", "next week"
- "let me check", "circle back", "reconnect"

Request phrases:
- "can you send", "please provide", "need from you"
- "awaiting", "pending your", "action required"
```

#### Reminder Logic
- Extract commitment with deadline (explicit or inferred)
- Create reminder entry
- Alert if deadline passes without completion
- User can mark complete or snooze

---

## 5. Data Models

### 5.1 Entity Relationship Diagram (Simplified)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │   Account    │       │   Contract   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id           │──┐    │ id           │──────▶│ id           │
│ email        │  │    │ name         │       │ account_id   │
│ name         │  │    │ type         │       │ status       │
│ role         │  ├───▶│ owner_id     │       │ end_date     │
│ password_hash│  │    │ ae_id        │       │ ...          │
└──────────────┘  │    │ parent_id    │       └──────────────┘
                  │    │ account_email│
                  │    └──────────────┘
                  │           │
                  │           ▼
                  │    ┌──────────────┐       ┌──────────────┐
                  │    │    Input     │       │HealthScore  │
                  │    ├──────────────┤       ├──────────────┤
                  │    │ id           │       │ id           │
                  │    │ account_id   │──────▶│ account_id   │
                  │    │ type         │       │ overall      │
                  │    │ content      │       │ engagement   │
                  │    │ created_by   │       │ sentiment    │
                  └───▶│ signals      │       │ requests     │
                       └──────────────┘       │ relationship │
                                              │ satisfaction │
                                              │ expansion    │
                                              │ calculated_at│
                                              └──────────────┘
```

### 5.2 Full Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'manager', 'csm', 'ae')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('standard', 'ela_parent', 'ela_child')),
    parent_account_id UUID REFERENCES accounts(id),
    account_email VARCHAR(255), -- The CC alias for email filtering
    industry VARCHAR(100),
    tier VARCHAR(50) CHECK (tier IN ('enterprise', 'mid_market', 'smb', 'startup')),
    owner_id UUID REFERENCES users(id),
    ae_id UUID REFERENCES users(id),
    check_in_interval_days INTEGER DEFAULT 14,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contacts (stakeholders at customer)
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    title VARCHAR(255),
    role_type VARCHAR(50) CHECK (role_type IN ('champion', 'economic_buyer', 'technical', 'end_user', 'executive', 'other')),
    is_primary BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contracts
CREATE TABLE contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    contract_name VARCHAR(255) NOT NULL,
    contract_type VARCHAR(50) NOT NULL CHECK (contract_type IN ('saas_subscription', 'consulting_sow', 'msa', 'ela')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('draft', 'active', 'pending_renewal', 'expired', 'terminated')),
    
    -- Dates
    effective_date DATE NOT NULL,
    end_date DATE NOT NULL,
    term_length VARCHAR(50),
    auto_renewal BOOLEAN DEFAULT true,
    notice_period_days INTEGER DEFAULT 30,
    
    -- Financial
    total_contract_value DECIMAL(15, 2),
    arr DECIMAL(15, 2),
    mrr DECIMAL(15, 2),
    payment_terms VARCHAR(50),
    billing_frequency VARCHAR(50),
    pricing_model VARCHAR(50),
    
    -- Scope
    licensed_seats INTEGER,
    products_modules TEXT[], -- Array of product names
    deliverables_summary TEXT,
    
    -- Contacts
    primary_signer VARCHAR(255),
    economic_buyer VARCHAR(255),
    
    -- Risk
    sla_committed TEXT,
    termination_notes TEXT,
    early_termination_penalty BOOLEAN DEFAULT false,
    competitor_clause BOOLEAN DEFAULT false,
    
    -- Compliance
    fedramp_required BOOLEAN DEFAULT false,
    fisma_level VARCHAR(50) DEFAULT 'none',
    hipaa_required BOOLEAN DEFAULT false,
    section_508_required BOOLEAN DEFAULT false,
    ato_status VARCHAR(50) DEFAULT 'none',
    ato_expiry_date DATE,
    
    -- Metadata
    document_url TEXT, -- Link to stored contract file
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inputs (emails, notes, etc.)
CREATE TABLE inputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    input_type VARCHAR(50) NOT NULL CHECK (input_type IN ('email', 'meeting_note', 'call_note', 'internal_note', 'qbr_note', 'document')),
    
    -- Content
    subject VARCHAR(500),
    content TEXT NOT NULL,
    content_date TIMESTAMP, -- When the interaction occurred
    
    -- Email-specific
    sender_email VARCHAR(255),
    sender_name VARCHAR(255),
    recipients TEXT[], -- Array of email addresses
    thread_id VARCHAR(255), -- For grouping email chains
    
    -- Note-specific
    attendees TEXT[],
    
    -- Processing
    is_processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Signal Extractions (keyword matches + LLM analysis)
CREATE TABLE signal_extractions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    input_id UUID REFERENCES inputs(id) NOT NULL,
    
    -- Keyword scan results (no LLM)
    churn_signals TEXT[], -- Matched keywords
    positive_signals TEXT[],
    action_signals TEXT[],
    compliance_signals TEXT[],
    keyword_severity VARCHAR(50), -- critical, high, medium, low
    
    -- LLM analysis (only if warranted)
    llm_analyzed BOOLEAN DEFAULT false,
    sentiment_score INTEGER, -- -100 to 100
    sentiment_label VARCHAR(50), -- very_negative, negative, neutral, positive, very_positive
    summary TEXT,
    action_items TEXT[],
    commitments_detected TEXT[], -- "I'll send X by Y"
    stakeholders_mentioned TEXT[],
    topics TEXT[],
    
    -- Scores contribution
    engagement_impact INTEGER, -- -10 to +10
    sentiment_impact INTEGER,
    request_impact INTEGER,
    relationship_impact INTEGER,
    satisfaction_impact INTEGER,
    expansion_impact INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Health Scores (point-in-time snapshots)
CREATE TABLE health_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    
    -- Overall
    overall_score INTEGER NOT NULL, -- 0-100
    overall_status VARCHAR(50) NOT NULL, -- green, yellow, red
    
    -- Pillar scores
    engagement_score INTEGER,
    sentiment_score INTEGER,
    request_score INTEGER,
    relationship_score INTEGER,
    satisfaction_score INTEGER,
    expansion_score INTEGER,
    
    -- Trend
    previous_score INTEGER,
    score_change INTEGER,
    trend_direction VARCHAR(50), -- up, down, stable
    
    -- AI Assessment
    ai_summary TEXT, -- "What's happening"
    ai_recommendations TEXT[], -- Suggested actions
    ai_risks TEXT[], -- Identified risks
    ai_opportunities TEXT[], -- Expansion opportunities
    
    -- Metadata
    triggered_by VARCHAR(50), -- manual, auto_daily, input_added, decay
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    user_id UUID REFERENCES users(id), -- Who should see this
    
    alert_type VARCHAR(100) NOT NULL,
    priority VARCHAR(50) NOT NULL, -- critical, high, medium, low
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Source
    source_type VARCHAR(50), -- health_score, keyword, contract, reminder
    source_id UUID, -- Reference to triggering record
    
    -- Status
    is_read BOOLEAN DEFAULT false,
    is_dismissed BOOLEAN DEFAULT false,
    actioned_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reminders
CREATE TABLE reminders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES accounts(id) NOT NULL,
    user_id UUID REFERENCES users(id) NOT NULL,
    input_id UUID REFERENCES inputs(id), -- Source input if extracted
    
    reminder_type VARCHAR(50) NOT NULL, -- follow_up, commitment, custom
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP NOT NULL,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, completed, snoozed, cancelled
    completed_at TIMESTAMP,
    snoozed_until TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notification Preferences
CREATE TABLE notification_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) UNIQUE NOT NULL,
    
    -- In-app
    in_app_enabled BOOLEAN DEFAULT true,
    
    -- Email (stubbed)
    email_enabled BOOLEAN DEFAULT false,
    email_digest_frequency VARCHAR(50) DEFAULT 'daily', -- daily, weekly, none
    email_realtime_critical BOOLEAN DEFAULT true,
    
    -- Slack (stubbed)
    slack_enabled BOOLEAN DEFAULT false,
    slack_webhook_url TEXT,
    
    -- Mobile push (stubbed)
    push_enabled BOOLEAN DEFAULT false,
    push_token TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LLM Configuration (BYOK - Bring Your Own Key)
CREATE TABLE llm_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) UNIQUE NOT NULL,
    
    -- Active provider selection
    active_provider VARCHAR(50) NOT NULL DEFAULT 'anthropic',
    -- Options: anthropic, openai, google, xai, perplexity
    
    -- Model selection per provider (users can customize)
    anthropic_model VARCHAR(100) DEFAULT 'claude-sonnet-4-20250514',
    openai_model VARCHAR(100) DEFAULT 'gpt-4o',
    google_model VARCHAR(100) DEFAULT 'gemini-1.5-pro',
    xai_model VARCHAR(100) DEFAULT 'grok-2-latest',
    perplexity_model VARCHAR(100) DEFAULT 'llama-3.1-sonar-large-128k-online',
    
    -- API Keys (encrypted at rest - see security notes)
    -- These are encrypted using Fernet symmetric encryption
    -- Key stored in environment variable, never in DB
    anthropic_api_key_encrypted TEXT,
    openai_api_key_encrypted TEXT,
    google_api_key_encrypted TEXT,
    xai_api_key_encrypted TEXT,
    perplexity_api_key_encrypted TEXT,
    
    -- Key validation status (checked on save)
    anthropic_key_valid BOOLEAN DEFAULT false,
    openai_key_valid BOOLEAN DEFAULT false,
    google_key_valid BOOLEAN DEFAULT false,
    xai_key_valid BOOLEAN DEFAULT false,
    perplexity_key_valid BOOLEAN DEFAULT false,
    
    -- Usage tracking (for user's awareness)
    total_tokens_used INTEGER DEFAULT 0,
    total_requests INTEGER DEFAULT 0,
    last_request_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Activity Log (audit trail)
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    account_id UUID REFERENCES accounts(id),
    
    action VARCHAR(100) NOT NULL, -- created, updated, deleted, viewed, exported
    entity_type VARCHAR(50) NOT NULL, -- account, contract, input, health_score
    entity_id UUID,
    
    details JSONB, -- Additional context
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_accounts_owner ON accounts(owner_id);
CREATE INDEX idx_accounts_parent ON accounts(parent_account_id);
CREATE INDEX idx_accounts_email ON accounts(account_email);
CREATE INDEX idx_contracts_account ON contracts(account_id);
CREATE INDEX idx_contracts_end_date ON contracts(end_date);
CREATE INDEX idx_inputs_account ON inputs(account_id);
CREATE INDEX idx_inputs_date ON inputs(content_date);
CREATE INDEX idx_health_scores_account ON health_scores(account_id);
CREATE INDEX idx_health_scores_date ON health_scores(calculated_at);
CREATE INDEX idx_alerts_user ON alerts(user_id);
CREATE INDEX idx_alerts_unread ON alerts(user_id, is_read) WHERE is_read = false;
CREATE INDEX idx_reminders_user_due ON reminders(user_id, due_date) WHERE status = 'pending';
```

---

## 6. Health Scoring Algorithm

### 6.1 Score Calculation

```python
def calculate_health_score(account_id: UUID) -> HealthScore:
    """
    Calculate overall health score from 6 pillars.
    Each pillar: 0-100, weighted to overall.
    """
    
    # Get recent signals (last 90 days)
    signals = get_signals_for_account(account_id, days=90)
    
    # Calculate pillar scores
    engagement = calculate_engagement_score(account_id, signals)
    sentiment = calculate_sentiment_score(signals)
    requests = calculate_request_score(signals)
    relationship = calculate_relationship_score(account_id, signals)
    satisfaction = calculate_satisfaction_score(signals)
    expansion = calculate_expansion_score(signals)
    
    # Apply weights (configurable)
    weights = get_account_weights(account_id)  # Default or custom
    
    overall = (
        engagement * weights['engagement'] +      # 0.20
        sentiment * weights['sentiment'] +        # 0.20
        requests * weights['requests'] +          # 0.15
        relationship * weights['relationship'] +  # 0.15
        satisfaction * weights['satisfaction'] +  # 0.15
        expansion * weights['expansion']          # 0.15
    )
    
    # Apply decay if no recent communication
    overall = apply_decay(account_id, overall)
    
    # Determine status
    status = 'green' if overall >= 70 else 'yellow' if overall >= 50 else 'red'
    
    return HealthScore(
        overall_score=round(overall),
        overall_status=status,
        engagement_score=engagement,
        sentiment_score=sentiment,
        # ... etc
    )
```

### 6.2 Pillar Calculations

#### Engagement Score
```python
def calculate_engagement_score(account_id, signals):
    """
    Measures: communication frequency, response times, meeting cadence
    """
    base_score = 50
    
    # Communication volume (last 30 days)
    comms_count = count_communications(account_id, days=30)
    if comms_count >= 10: base_score += 20
    elif comms_count >= 5: base_score += 10
    elif comms_count == 0: base_score -= 30
    
    # Response time trends
    avg_response_days = get_avg_response_time(account_id)
    if avg_response_days <= 1: base_score += 15
    elif avg_response_days <= 3: base_score += 5
    elif avg_response_days > 7: base_score -= 15
    
    # Meeting frequency
    meetings_this_month = count_meetings(account_id, days=30)
    expected_meetings = get_expected_meeting_cadence(account_id)
    if meetings_this_month >= expected_meetings: base_score += 15
    elif meetings_this_month == 0: base_score -= 20
    
    return max(0, min(100, base_score))
```

#### Sentiment Score
```python
def calculate_sentiment_score(signals):
    """
    Aggregate sentiment from all signals.
    """
    if not signals:
        return 50  # Neutral default
    
    # Weight recent signals more heavily
    weighted_sum = 0
    weight_total = 0
    
    for signal in signals:
        days_ago = (now() - signal.created_at).days
        weight = max(0.1, 1 - (days_ago / 90))  # Decay over 90 days
        
        # Normalize sentiment_score from -100/+100 to 0-100
        normalized = (signal.sentiment_score + 100) / 2
        
        weighted_sum += normalized * weight
        weight_total += weight
    
    return round(weighted_sum / weight_total) if weight_total > 0 else 50
```

### 6.3 Decay Logic

```python
def apply_decay(account_id, current_score):
    """
    Apply decay if no communication past check-in interval.
    """
    account = get_account(account_id)
    last_comm_date = get_last_communication_date(account_id)
    
    days_since_comm = (now() - last_comm_date).days
    check_in_interval = account.check_in_interval_days
    
    if days_since_comm <= check_in_interval:
        return current_score
    
    # Decay: -2 points per day past threshold
    days_overdue = days_since_comm - check_in_interval
    decay_amount = days_overdue * 2
    
    # Floor at 30 to prevent false emergencies
    return max(30, current_score - decay_amount)
```

---

## 7. Keyword Lexicon

### 7.1 Churn Risk / Negative Signals

```python
CHURN_SIGNALS = {
    'critical': [
        # Direct churn indicators
        'cancel', 'cancellation', 'cancelling', 'terminate', 'termination',
        'not renewing', "won't renew", 'reconsidering',
        'take our business elsewhere', 'looking at competitors',
        'exploring options', 'evaluating alternatives',
        'end the contract', 'exit', 'off-board', 'wind down',
        'rfp for replacement', 'vendor review',
    ],
    'high': [
        # Frustration
        'frustrated', 'frustrating', 'disappointed', 'disappointing',
        'unacceptable', 'fed up', 'at wit\'s end', 'last straw',
        'deal breaker', 'non-starter',
        # Escalation
        'escalate', 'escalation', 'involve my manager', 'loop in vp',
        'bring in legal', 'c-suite', 'executive sponsor',
        'unresolved', 'still waiting', 'no response', 'ignored',
        'dropped the ball', 'this is the third time', 'yet again',
    ],
    'medium': [
        # Service issues
        'slow response', 'long wait', 'no follow-up', 'ticket still open',
        'support is terrible', "can't get help", 'nobody responds',
        'passed around', 'transferred again', 'sla breach',
        'outage', 'downtime', 'incident', 'service disruption',
        # Product gaps
        'missing feature', "doesn't have", "can't do", 'limitation',
        'workaround', 'competitor has', 'why can\'t you',
        'not intuitive', 'confusing', 'hard to use', 'clunky', 'buggy',
    ]
}
```

### 7.2 Positive / Expansion Signals

```python
POSITIVE_SIGNALS = {
    'expansion': [
        'expand', 'expansion', 'add more', 'additional licenses',
        'more seats', 'other departments', 'other teams',
        'roll out to', 'enterprise-wide', 'new use case',
        'another project', 'phase 2', 'next phase',
        'budget approved', 'funding secured', 'ready to move forward',
        'who else should i talk to', 'introduce you to',
    ],
    'satisfaction': [
        'love', 'great', 'excellent', 'fantastic', 'amazing', 'impressed',
        'happy with', 'pleased with', 'satisfied', 'delighted',
        'exceeded expectations', 'better than expected', 'blown away',
        'exactly what we needed', 'perfect fit', 'game changer',
    ],
    'relationship': [
        'partner', 'partnership', 'strategic', 'long-term', 'trusted',
        'recommend', 'referral', 'reference', 'case study', 'testimonial',
        'renew', 'renewal', 'multi-year', 'extend', 'committed',
        'advocate', 'champion',
    ],
    'value': [
        'roi', 'return on investment', 'paying off', 'saving us',
        'efficiency', 'productivity', 'streamlined', 'automated',
        'results', 'outcomes', 'impact', 'measurable', 'metrics',
        'success', 'successful', 'working well', 'performing',
    ]
}
```

### 7.3 Action Triggers

```python
ACTION_SIGNALS = {
    'commitments_made': [
        "i'll send", "i'll get back", 'will follow up', 'let me check',
        'by end of week', 'by friday', 'tomorrow', 'next week',
        'circle back', 'reconnect', 'touch base', 'schedule time',
    ],
    'requests_pending': [
        'can you send', 'please provide', 'need from you', 'waiting on',
        'awaiting', 'pending your', 'action required', 'your turn',
        'please confirm', 'need approval', 'sign off needed',
    ],
    'meeting_signals': [
        'let\'s schedule', 'set up a call', 'discuss further',
        'qbr', 'business review', 'check-in', 'sync',
        'demo', 'presentation', 'walk-through', 'deep dive',
    ]
}
```

### 7.4 Federal / Compliance Signals

```python
COMPLIANCE_SIGNALS = {
    'fedramp': ['fedramp', 'fed ramp', 'federal risk'],
    'fisma': ['fisma', 'federal information security'],
    'ato': ['ato', 'authorization to operate', 'authority to operate'],
    'hipaa': ['hipaa', 'phi', 'protected health information'],
    'section_508': ['508 compliance', 'section 508', 'accessibility', 'wcag'],
    'security': [
        'security review', 'security assessment', 'pen test',
        'penetration test', 'vulnerability', 'il4', 'il5',
        'govcloud', 'government cloud',
    ],
    'federal_process': [
        'contracting officer', 'cor', 'cotr', 'procurement',
        'task order', 'bpa', 'idiq', 'option year',
        'period of performance', 'clin', 'gsa schedule',
    ]
}
```

### 7.5 Processing Logic

```python
def scan_for_keywords(text: str) -> dict:
    """
    Fast keyword scan before LLM analysis.
    Returns matched signals and severity.
    """
    text_lower = text.lower()
    results = {
        'churn_signals': [],
        'positive_signals': [],
        'action_signals': [],
        'compliance_signals': [],
        'keyword_severity': 'low'
    }
    
    # Check churn signals
    for severity, keywords in CHURN_SIGNALS.items():
        for keyword in keywords:
            if keyword in text_lower:
                results['churn_signals'].append(keyword)
                # Upgrade severity
                if severity == 'critical':
                    results['keyword_severity'] = 'critical'
                elif severity == 'high' and results['keyword_severity'] != 'critical':
                    results['keyword_severity'] = 'high'
                elif results['keyword_severity'] not in ['critical', 'high']:
                    results['keyword_severity'] = 'medium'
    
    # Check positive signals
    for category, keywords in POSITIVE_SIGNALS.items():
        for keyword in keywords:
            if keyword in text_lower:
                results['positive_signals'].append(keyword)
    
    # Check action signals
    for category, keywords in ACTION_SIGNALS.items():
        for keyword in keywords:
            if keyword in text_lower:
                results['action_signals'].append(keyword)
    
    # Check compliance signals
    for category, keywords in COMPLIANCE_SIGNALS.items():
        for keyword in keywords:
            if keyword in text_lower:
                results['compliance_signals'].append(keyword)
    
    return results


def should_analyze_with_llm(keyword_results: dict) -> bool:
    """
    Determine if LLM analysis is warranted based on keyword scan.
    """
    # Always analyze if critical/high severity
    if keyword_results['keyword_severity'] in ['critical', 'high']:
        return True
    
    # Analyze if significant signal count
    total_signals = (
        len(keyword_results['churn_signals']) +
        len(keyword_results['positive_signals']) +
        len(keyword_results['action_signals'])
    )
    if total_signals >= 3:
        return True
    
    # Analyze if compliance signals (important context)
    if keyword_results['compliance_signals']:
        return True
    
    return False
```

---

## 8. API Routes

### 8.1 Authentication

```
POST   /api/auth/register        - Create new user account
POST   /api/auth/login           - Login, receive JWT
POST   /api/auth/logout          - Logout, invalidate token
POST   /api/auth/refresh         - Refresh JWT token
GET    /api/auth/me              - Get current user
PUT    /api/auth/me              - Update current user
POST   /api/auth/password/change - Change password
POST   /api/auth/password/reset  - Request password reset
```

### 8.2 Users (Admin only)

```
GET    /api/users                - List all users
POST   /api/users                - Create user
GET    /api/users/:id            - Get user
PUT    /api/users/:id            - Update user
DELETE /api/users/:id            - Deactivate user
```

### 8.3 Accounts

```
GET    /api/accounts             - List accounts (filtered by role)
POST   /api/accounts             - Create account
GET    /api/accounts/:id         - Get account details
PUT    /api/accounts/:id         - Update account
DELETE /api/accounts/:id         - Archive account
GET    /api/accounts/:id/health  - Get current health score
GET    /api/accounts/:id/health/history - Get health score history
GET    /api/accounts/:id/timeline - Get activity timeline
GET    /api/accounts/:id/children - Get ELA child offices
POST   /api/accounts/:id/children - Add ELA child office
```

### 8.4 Contracts

```
GET    /api/accounts/:id/contracts - List contracts for account
POST   /api/accounts/:id/contracts - Create contract
GET    /api/contracts/:id          - Get contract
PUT    /api/contracts/:id          - Update contract
DELETE /api/contracts/:id          - Delete contract
POST   /api/contracts/parse        - Parse contract PDF (future)
```

### 8.5 Inputs

```
GET    /api/accounts/:id/inputs    - List inputs for account
POST   /api/accounts/:id/inputs    - Add input (email/note)
GET    /api/inputs/:id             - Get input details
PUT    /api/inputs/:id             - Update input
DELETE /api/inputs/:id             - Delete input
POST   /api/inputs/:id/reprocess   - Reprocess input signals
POST   /api/inputs/upload          - Upload email file (.eml, .msg)
```

### 8.6 Contacts

```
GET    /api/accounts/:id/contacts  - List contacts for account
POST   /api/accounts/:id/contacts  - Add contact
GET    /api/contacts/:id           - Get contact
PUT    /api/contacts/:id           - Update contact
DELETE /api/contacts/:id           - Remove contact
```

### 8.7 Alerts & Notifications

```
GET    /api/alerts                 - List alerts for current user
GET    /api/alerts/unread/count    - Get unread count
PUT    /api/alerts/:id/read        - Mark as read
PUT    /api/alerts/:id/dismiss     - Dismiss alert
POST   /api/alerts/mark-all-read   - Mark all as read
```

### 8.8 Reminders

```
GET    /api/reminders              - List reminders for current user
POST   /api/reminders              - Create reminder
GET    /api/reminders/:id          - Get reminder
PUT    /api/reminders/:id          - Update reminder
PUT    /api/reminders/:id/complete - Mark complete
PUT    /api/reminders/:id/snooze   - Snooze reminder
DELETE /api/reminders/:id          - Delete reminder
```

### 8.9 Dashboard / Portfolio

```
GET    /api/dashboard/portfolio    - Portfolio overview (all accounts)
GET    /api/dashboard/at-risk      - At-risk accounts
GET    /api/dashboard/renewals     - Upcoming renewals
GET    /api/dashboard/stats        - Summary statistics
```

### 8.10 Settings

```
GET    /api/settings/notifications - Get notification preferences
PUT    /api/settings/notifications - Update notification preferences
GET    /api/settings/llm           - Get LLM configuration
PUT    /api/settings/llm           - Update LLM configuration
POST   /api/settings/llm/validate  - Validate an API key
GET    /api/settings/llm/providers - List available providers & models
GET    /api/settings/llm/usage     - Get usage statistics
```

---

## 9. UI Wireframes

### 9.1 Portfolio Dashboard

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CUSTOMER PULSE                              🔔(3)  [Kareem ▼]         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  PORTFOLIO OVERVIEW                          [+ Add Account]       │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                           │ │
│  │  │   12     │ │    5     │ │    3     │     Total: 20 accounts    │ │
│  │  │   🟢     │ │    🟡    │ │    🔴    │     ARR: $4.2M            │ │
│  │  │ Healthy  │ │  Watch   │ │ At Risk  │     Renewals (90d): 6     │ │
│  │  └──────────┘ └──────────┘ └──────────┘                           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  ACCOUNTS                    [Filter ▼] [Sort ▼] [Search 🔍    ]  │ │
│  │  ┌─────────────────────────────────────────────────────────────┐  │ │
│  │  │ 🔴 USDA (ELA)           58 ↓14    Renewal: Dec 31 (20 days) │  │ │
│  │  │    "Meeting frequency dropped, sentiment negative"          │  │ │
│  │  │    └─ NRCS  ●●● └─ FSA  ●●○ └─ ARS  ●○○                    │  │ │
│  │  └─────────────────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────────────────┐  │ │
│  │  │ 🟢 Samsung              91 ↑6     Renewal: Mar 15 (95 days) │  │ │
│  │  │    "Strong engagement, expansion signals detected"          │  │ │
│  │  └─────────────────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────────────────┐  │ │
│  │  │ 🟡 Treasury             74 ↓4     Renewal: Feb 28 (79 days) │  │ │
│  │  │    "Stable but champion (Jane) departed, monitoring"        │  │ │
│  │  └─────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  [Load More...]                                                    │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Account Detail View

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back to Portfolio    USDA                     [+ Add Input] [⚙️]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─ NRCS ─┐ ┌─ FSA ─┐ ┌─ ARS ─┐ ┌─ + Add Office ─┐                    │
│  └────────┘ └───────┘ └───────┘ └────────────────┘                     │
│                                                                         │
│  USDA - NRCS                                                           │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                         │
│  HEALTH: 58 🔴            Trend: ↓14 pts (30 days)                     │
│  ────────────────────────────────────────────────────────────────────   │
│                                                                         │
│  ┌─────────────┬─────────────┬─────────────┐                           │
│  │ Engagement  │ Sentiment   │ Requests    │                           │
│  │     42 🔴   │    38 🔴    │    65 🟡    │                           │
│  │  ↓ from 71  │  ↓ from 62  │  ↓ from 70  │                           │
│  ├─────────────┼─────────────┼─────────────┤                           │
│  │ Relationship│ Satisfaction│ Expansion   │                           │
│  │     55 🟡   │    68 🟡    │    35 🔴    │                           │
│  │  ↓ from 80  │  ─ stable   │  ↓ from 55  │                           │
│  └─────────────┴─────────────┴─────────────┘                           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  AI ASSESSMENT                                    [Regenerate 🔄] │ │
│  │  ─────────────────────────────────────────────────────────────────│ │
│  │  ⚠️ WHAT'S HAPPENING                                              │ │
│  │  Meeting frequency dropped from weekly to monthly since Oct.      │ │
│  │  Last 3 interactions showed frustration about API rate limits.    │ │
│  │  Primary champion (Jane Miller) moved to different department.    │ │
│  │                                                                    │ │
│  │  🔧 RECOMMENDED ACTIONS                                           │ │
│  │  1. Schedule exec sponsor check-in within 7 days                  │ │
│  │  2. Address API limit concerns - escalate to product team         │ │
│  │  3. Identify new champion in current department                   │ │
│  │                                                                    │ │
│  │  💡 EXPANSION: BLOCKED                                            │ │
│  │  Current frustrations make upsell unlikely. Focus on retention    │ │
│  │  and rebuilding relationship first.                               │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  CONTRACT                                              [Edit]      │ │
│  │  MSA FY2024 - Active                                              │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐                        │ │
│  │  │ START     │ │ RENEWAL   │ │ NOTICE BY │                        │ │
│  │  │ Jan 1     │ │ Dec 31    │ │ Dec 1     │                        │ │
│  │  │ 2024      │ │ ⚠️ 20 days│ │ ⏰ PASSED │                        │ │
│  │  └───────────┘ └───────────┘ └───────────┘                        │ │
│  │  TCV: $450K   ARR: $450K   Auto-Renew: ✅   Seats: 500            │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  TIMELINE                                [Filter ▼] [View All →]  │ │
│  │  ─────────────────────────────────────────────────────────────────│ │
│  │  📧 Dec 10 - Email: "Re: API Rate Limit Issues"                   │ │
│  │     Sentiment: 🔴 Negative | Churn signals: "frustrated"          │ │
│  │                                                                    │ │
│  │  📝 Dec 5 - Meeting Note: Weekly Sync                             │ │
│  │     Sentiment: 🟡 Neutral | Action items: 2                       │ │
│  │                                                                    │ │
│  │  📧 Nov 28 - Email: "Jane's Transition"                           │ │
│  │     Sentiment: 🟡 Neutral | Stakeholder change detected           │ │
│  │                                                                    │ │
│  │  🔔 Nov 20 - Alert: No contact in 14 days                         │ │
│  │                                                                    │ │
│  │  📝 Nov 15 - Meeting Note: QBR Review                             │ │
│  │     Sentiment: 🟢 Positive | Expansion signal detected            │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.3 Add Input Modal

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ADD INPUT                                                    [X]       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Input Type:  ○ Email  ○ Meeting Note  ○ Call Note  ○ Internal Note    │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [IF EMAIL SELECTED]                                                    │
│                                                                         │
│  Upload Email:  [Choose File] or paste below                           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ Paste email content here...                                        │ │
│  │                                                                     │ │
│  │ From: jane.miller@usda.gov                                         │ │
│  │ To: kareem@company.com                                             │ │
│  │ CC: usda-account@company.com                                       │ │
│  │ Date: Dec 10, 2024                                                 │ │
│  │ Subject: Re: API Rate Limit Issues                                 │ │
│  │                                                                     │ │
│  │ Hi Kareem,                                                         │ │
│  │                                                                     │ │
│  │ I'm really frustrated with these ongoing API issues...             │ │
│  │                                                                     │ │
│  │                                                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [IF NOTE SELECTED]                                                     │
│                                                                         │
│  Date: [Dec 10, 2024 ▼]                                                │
│                                                                         │
│  Attendees: [Add attendees...]                                         │
│             ┌──────────────────┐                                       │
│             │ Jane Miller      │ [x]                                   │
│             │ Bob Smith        │ [x]                                   │
│             └──────────────────┘                                       │
│                                                                         │
│  Notes:                                                                 │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ Weekly sync call. Jane seemed frustrated about the API rate       │ │
│  │ limits they've been hitting. Bob mentioned they might need to     │ │
│  │ evaluate other solutions if this isn't resolved soon.             │ │
│  │                                                                     │ │
│  │ Action items:                                                       │ │
│  │ - I need to escalate API limits to product by EOW                  │ │
│  │ - Schedule call with their tech team next Tuesday                  │ │
│  │                                                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│                                        [Cancel]  [Save & Process]       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.4 Notification Center

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NOTIFICATIONS                              [Mark All Read] [Settings]  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TODAY                                                                  │
│  ─────────────────────────────────────────────────────────────────────  │
│  ● 🔴 CRITICAL - USDA NRCS                              10:30 AM       │
│    Churn risk keywords detected: "frustrated", "evaluate other"        │
│    [View Account] [Dismiss]                                            │
│                                                                         │
│  ● 🟡 HIGH - Treasury                                    9:15 AM       │
│    Health score dropped 8 points (82 → 74)                             │
│    [View Account] [Dismiss]                                            │
│                                                                         │
│  ○ 🔵 REMINDER - Samsung                                 8:00 AM       │
│    Follow-up due: "Send ROI report by Friday"                          │
│    [Complete] [Snooze] [View]                                          │
│                                                                         │
│  YESTERDAY                                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  ○ 🟡 RENEWAL - J&J                                                    │
│    Contract renewal in 30 days (Jan 10, 2025)                          │
│    [View Contract] [Dismiss]                                           │
│                                                                         │
│  ○ 🔵 INFO - Airbnb                                                    │
│    Expansion signal detected: "roll out to other teams"                │
│    [View Account] [Dismiss]                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.5 LLM Settings Page

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SETTINGS                                                               │
├─────────────────────────────────────────────────────────────────────────┤
│  [Notifications]  [LLM Configuration]  [Account]                        │
│                   ═══════════════════                                   │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  ACTIVE LLM PROVIDER                                              │ │
│  │  ─────────────────────────────────────────────────────────────────│ │
│  │                                                                    │ │
│  │  ○ Claude (Anthropic)     ● GPT-4 (OpenAI)     ○ Gemini (Google) │ │
│  │                                                                    │ │
│  │  ○ Grok (xAI)             ○ Perplexity                            │ │
│  │                                                                    │ │
│  │  Selected: GPT-4 (OpenAI) - gpt-4o                                │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  API KEYS                                          [Show Keys 👁]  │ │
│  │  ─────────────────────────────────────────────────────────────────│ │
│  │                                                                    │ │
│  │  Anthropic (Claude)                                               │ │
│  │  ┌─────────────────────────────────────────────┐                  │ │
│  │  │ sk-ant-••••••••••••••••••••••••••           │  ✅ Valid        │ │
│  │  └─────────────────────────────────────────────┘                  │ │
│  │  Model: [claude-sonnet-4-20250514 ▼]                              │ │
│  │                                                                    │ │
│  │  OpenAI (GPT-4)                                          ⬅ ACTIVE │ │
│  │  ┌─────────────────────────────────────────────┐                  │ │
│  │  │ sk-••••••••••••••••••••••••••••••           │  ✅ Valid        │ │
│  │  └─────────────────────────────────────────────┘                  │ │
│  │  Model: [gpt-4o ▼]                                                │ │
│  │                                                                    │ │
│  │  Google (Gemini)                                                  │ │
│  │  ┌─────────────────────────────────────────────┐                  │ │
│  │  │ Enter API key...                            │  ⚪ Not set      │ │
│  │  └─────────────────────────────────────────────┘                  │ │
│  │  Model: [gemini-1.5-pro ▼]                                        │ │
│  │                                                                    │ │
│  │  xAI (Grok)                                                       │ │
│  │  ┌─────────────────────────────────────────────┐                  │ │
│  │  │ Enter API key...                            │  ⚪ Not set      │ │
│  │  └─────────────────────────────────────────────┘                  │ │
│  │  Model: [grok-2-latest ▼]                                         │ │
│  │                                                                    │ │
│  │  Perplexity                                                       │ │
│  │  ┌─────────────────────────────────────────────┐                  │ │
│  │  │ xai-••••••••••••••••••••                    │  ❌ Invalid      │ │
│  │  └─────────────────────────────────────────────┘                  │ │
│  │  Model: [llama-3.1-sonar-large-128k-online ▼]                     │ │
│  │                                                                    │ │
│  │  ⚠️  Keys are encrypted and stored securely. We never log or      │ │
│  │     share your API keys.                                          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  USAGE THIS MONTH                                                 │ │
│  │  ─────────────────────────────────────────────────────────────────│ │
│  │  Total Requests: 847        Tokens Used: ~124,500                 │ │
│  │  Est. Cost: ~$1.87          Last Request: 2 minutes ago           │ │
│  │                                                                    │ │
│  │  Note: Costs are estimates based on provider pricing. Check your  │ │
│  │  provider dashboard for actual charges.                           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│                                                    [Save Changes]       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 10. LLM Integration

### 10.1 Supported Providers

| Provider | Models | API Style | Notes |
|----------|--------|-----------|-------|
| **Anthropic** | claude-sonnet-4-20250514, claude-opus-4-20250514, claude-haiku-3-5-20241022 | Messages API | Best for nuanced analysis |
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo | Chat Completions | Most widely used |
| **Google** | gemini-1.5-pro, gemini-1.5-flash | Generative AI | Good multimodal support |
| **xAI** | grok-2-latest, grok-2-vision-latest | OpenAI-compatible | Real-time knowledge |
| **Perplexity** | llama-3.1-sonar-large-128k-online | OpenAI-compatible | Built-in web search |

### 10.2 Provider Abstraction

```python
from abc import ABC, abstractmethod
from typing import Optional
from cryptography.fernet import Fernet

# Base class all providers implement
class LLMProvider(ABC):
    """Abstract base for all LLM providers."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        """
        Send prompt to LLM and return response.
        Returns: {"content": str, "tokens_used": int, "model": str}
        """
        pass
    
    @abstractmethod
    async def validate_key(self) -> bool:
        """Test if API key is valid."""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass


class AnthropicProvider(LLMProvider):
    """Claude models via Anthropic API."""
    
    provider_name = "anthropic"
    
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        import anthropic
        
        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        
        message = await client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "content": message.content[0].text,
            "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
            "model": self.model
        }
    
    async def validate_key(self) -> bool:
        try:
            import anthropic
            client = anthropic.AsyncAnthropic(api_key=self.api_key)
            await client.messages.create(
                model="claude-haiku-3-5-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception:
            return False


class OpenAIProvider(LLMProvider):
    """GPT models via OpenAI API."""
    
    provider_name = "openai"
    
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        import openai
        
        client = openai.AsyncOpenAI(api_key=self.api_key)
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "model": self.model
        }
    
    async def validate_key(self) -> bool:
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=self.api_key)
            await client.models.list()
            return True
        except Exception:
            return False


class GoogleProvider(LLMProvider):
    """Gemini models via Google Generative AI."""
    
    provider_name = "google"
    
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        import google.generativeai as genai
        
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=system
        )
        
        response = await model.generate_content_async(prompt)
        
        return {
            "content": response.text,
            "tokens_used": response.usage_metadata.total_token_count,
            "model": self.model
        }
    
    async def validate_key(self) -> bool:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            await model.generate_content_async("Hi")
            return True
        except Exception:
            return False


class XAIProvider(LLMProvider):
    """Grok models via xAI API (OpenAI-compatible)."""
    
    provider_name = "xai"
    
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        import openai
        
        # xAI uses OpenAI-compatible API
        client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "model": self.model
        }
    
    async def validate_key(self) -> bool:
        try:
            import openai
            client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
            await client.chat.completions.create(
                model="grok-2-latest",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False


class PerplexityProvider(LLMProvider):
    """Perplexity models (OpenAI-compatible with web search)."""
    
    provider_name = "perplexity"
    
    async def complete(self, prompt: str, system: Optional[str] = None) -> dict:
        import openai
        
        client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai"
        )
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096
        )
        
        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
            "model": self.model
        }
    
    async def validate_key(self) -> bool:
        try:
            import openai
            client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.perplexity.ai"
            )
            await client.chat.completions.create(
                model="llama-3.1-sonar-small-128k-online",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False


# Factory to get the right provider
class LLMClientFactory:
    """Factory to create LLM client based on user's settings."""
    
    PROVIDERS = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "google": GoogleProvider,
        "xai": XAIProvider,
        "perplexity": PerplexityProvider,
    }
    
    @classmethod
    def create(cls, config: "LLMConfiguration") -> LLMProvider:
        """Create LLM provider from user's configuration."""
        provider_class = cls.PROVIDERS.get(config.active_provider)
        if not provider_class:
            raise ValueError(f"Unknown provider: {config.active_provider}")
        
        api_key = config.get_decrypted_key(config.active_provider)
        model = getattr(config, f"{config.active_provider}_model")
        
        return provider_class(api_key=api_key, model=model)


# Encryption helper for API keys
class KeyEncryption:
    """Encrypt/decrypt API keys using Fernet symmetric encryption."""
    
    def __init__(self, secret_key: str):
        self.fernet = Fernet(secret_key.encode())
    
    def encrypt(self, plaintext: str) -> str:
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        return self.fernet.decrypt(ciphertext.encode()).decode()
```

### 10.3 Using the LLM Client

```python
async def analyze_input(input_id: UUID, user_id: UUID) -> SignalExtraction:
    """Analyze an input using user's configured LLM."""
    
    # Get user's LLM config
    config = await get_llm_config(user_id)
    
    # Create the appropriate provider
    llm = LLMClientFactory.create(config)
    
    # Get input content
    input_data = await get_input(input_id)
    
    # Build prompt (same regardless of provider)
    prompt = build_signal_extraction_prompt(input_data)
    
    # Call LLM (works with any provider!)
    result = await llm.complete(
        prompt=prompt,
        system="You are a customer success analyst..."
    )
    
    # Update usage tracking
    await update_usage_stats(user_id, result["tokens_used"])
    
    # Parse and return
    return parse_extraction_response(result["content"])
```

### 10.4 Processing Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                         INPUT PROCESSING FLOW                         │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 1: KEYWORD SCAN (No LLM - Fast & Free)                         │
│  ─────────────────────────────────────────────────────────────────── │
│  • Scan text for lexicon matches                                     │
│  • Count hits per category (churn, positive, action, compliance)     │
│  • Determine severity level (critical/high/medium/low)               │
│  • Store keyword matches in signal_extractions                       │
│                                                                      │
│  Processing time: <100ms                                             │
│  Cost: $0                                                            │
└──────────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            severity >= medium        severity = low
            OR signals >= 3           AND signals < 3
                    │                       │
                    ▼                       ▼
┌────────────────────────────┐  ┌────────────────────────────┐
│  STEP 2: LLM ANALYSIS      │  │  SKIP LLM                  │
│  ─────────────────────────│  │  ─────────────────────────│
│  • Deep sentiment analysis │  │  • Store keyword results   │
│  • Extract action items    │  │  • Apply default scores    │
│  • Identify stakeholders   │  │  • Mark as processed       │
│  • Generate summary        │  │                            │
│  • Score impact per pillar │  │  Cost: $0                  │
│                            │  │                            │
│  Cost: ~$0.01-0.03/input   │  └────────────────────────────┘
└────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 3: HEALTH RECALCULATION                                        │
│  ─────────────────────────────────────────────────────────────────── │
│  • Aggregate all signals for account                                 │
│  • Calculate 6 pillar scores                                         │
│  • Apply decay if needed                                             │
│  • Generate AI assessment (if score changed significantly)           │
│  • Create alerts if thresholds crossed                               │
└──────────────────────────────────────────────────────────────────────┘
```

### 10.5 LLM Prompt Templates

#### Signal Extraction Prompt

```python
SIGNAL_EXTRACTION_PROMPT = """
You are analyzing customer communication for a B2B SaaS customer success platform.

CONTEXT:
- Account: {account_name}
- Industry: {industry}
- Input Type: {input_type}
- Date: {content_date}

COMMUNICATION:
{content}

KEYWORD SIGNALS ALREADY DETECTED:
- Churn signals: {churn_signals}
- Positive signals: {positive_signals}
- Action signals: {action_signals}
- Compliance signals: {compliance_signals}

ANALYZE AND RETURN JSON:
{{
  "sentiment_score": <-100 to 100>,
  "sentiment_label": "<very_negative|negative|neutral|positive|very_positive>",
  "summary": "<2-3 sentence summary of the communication>",
  "action_items": ["<extracted action items>"],
  "commitments_detected": ["<commitments with deadlines, e.g. 'Send report by Friday'>"],
  "stakeholders_mentioned": ["<names and roles if detectable>"],
  "topics": ["<main topics discussed>"],
  "pillar_impacts": {{
    "engagement": <-10 to 10>,
    "sentiment": <-10 to 10>,
    "requests": <-10 to 10>,
    "relationship": <-10 to 10>,
    "satisfaction": <-10 to 10>,
    "expansion": <-10 to 10>
  }},
  "risk_flags": ["<any risks or concerns>"],
  "opportunity_flags": ["<any expansion or upsell opportunities>"]
}}

Be precise and factual. Only extract what is explicitly stated or strongly implied.
"""
```

#### Health Assessment Prompt

```python
HEALTH_ASSESSMENT_PROMPT = """
You are a senior Customer Success Manager analyzing an account's health.

ACCOUNT: {account_name}
CURRENT HEALTH SCORE: {overall_score}/100 ({status})
PREVIOUS SCORE (30 days ago): {previous_score}/100
TREND: {trend_direction} ({score_change} points)

PILLAR BREAKDOWN:
- Engagement: {engagement_score}/100 (weight: 20%)
- Sentiment: {sentiment_score}/100 (weight: 20%)
- Requests: {request_score}/100 (weight: 15%)
- Relationship: {relationship_score}/100 (weight: 15%)
- Satisfaction: {satisfaction_score}/100 (weight: 15%)
- Expansion: {expansion_score}/100 (weight: 15%)

CONTRACT INFO:
- Renewal Date: {renewal_date}
- Days Until Renewal: {days_to_renewal}
- Contract Value: ${contract_value}
- Auto-Renewal: {auto_renewal}

RECENT SIGNALS (last 30 days):
{recent_signals_summary}

GENERATE ASSESSMENT JSON:
{{
  "whats_happening": "<3-5 bullet points explaining the current situation>",
  "recommended_actions": [
    {{
      "action": "<specific action>",
      "priority": "<high|medium|low>",
      "timeframe": "<when to do it>"
    }}
  ],
  "risks": ["<identified risks>"],
  "opportunities": ["<expansion or improvement opportunities>"],
  "expansion_readiness": "<ready|blocked|neutral>",
  "expansion_notes": "<explanation of expansion readiness>"
}}

Be specific, actionable, and honest. Prioritize retention over expansion if health is poor.
"""
```

### 10.6 Token Estimation & Cost

| Input Type | Avg Tokens | Est. Cost (Claude) |
|------------|------------|-------------------|
| Short email | 500 | $0.0015 |
| Long email thread | 2000 | $0.006 |
| Meeting notes | 800 | $0.0024 |
| Health assessment | 1500 | $0.0045 |

**Estimated monthly cost** (based on 100 accounts, 500 inputs/month):
- With keyword pre-filter (60% skip): ~$4-6/month
- Without pre-filter: ~$10-15/month

---

## 11. Integrations Architecture

### 11.1 Integration Status

| Integration | MVP Status | Implementation |
|-------------|------------|----------------|
| Email input (manual) | ✅ Implemented | Copy/paste, file upload |
| Gmail OAuth | 🔲 Stubbed | OAuth flow ready, sync disabled |
| Google Calendar | 🔲 Stubbed | OAuth shared with Gmail |
| Slack | 🔲 Stubbed | Webhook URL field, no sends |
| Zoom | 🔲 Stubbed | Future transcript import |
| Teams | 🔲 Stubbed | Future transcript import |
| Salesforce | 🔲 Stubbed | Future CRM sync |
| HubSpot | 🔲 Stubbed | Future CRM sync |

### 11.2 Integration Interface

```python
# Abstract integration interface for future implementations
class Integration(ABC):
    """Base class for all integrations."""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Returns: connected, disconnected, error"""
        pass
    
    @abstractmethod
    def connect(self, credentials: dict) -> bool:
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        pass
    
    @abstractmethod
    def sync(self, account_id: UUID) -> list[Input]:
        pass


class GmailIntegration(Integration):
    """Gmail integration - stubbed for MVP."""
    
    def get_name(self) -> str:
        return "Gmail"
    
    def get_status(self) -> str:
        return "disconnected"  # Always disconnected in MVP
    
    def connect(self, credentials: dict) -> bool:
        # TODO: Implement OAuth flow
        raise NotImplementedError("Gmail integration coming soon")
    
    # ... etc


class SlackIntegration(Integration):
    """Slack integration - stubbed for MVP."""
    
    def send_notification(self, webhook_url: str, message: dict) -> bool:
        # TODO: Implement webhook call
        raise NotImplementedError("Slack integration coming soon")
```

### 11.3 Email Parsing (Manual Input)

```python
def parse_email_input(raw_content: str) -> dict:
    """
    Parse pasted email content or uploaded .eml file.
    Extracts headers and body.
    """
    result = {
        'sender_email': None,
        'sender_name': None,
        'recipients': [],
        'subject': None,
        'date': None,
        'body': raw_content
    }
    
    # Try to extract headers from pasted content
    lines = raw_content.split('\n')
    header_patterns = {
        'from': r'^From:\s*(.+)$',
        'to': r'^To:\s*(.+)$',
        'cc': r'^CC:\s*(.+)$',
        'subject': r'^Subject:\s*(.+)$',
        'date': r'^Date:\s*(.+)$',
    }
    
    body_start = 0
    for i, line in enumerate(lines):
        matched = False
        for key, pattern in header_patterns.items():
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                # Extract and store header value
                matched = True
                body_start = i + 1
                break
        
        # Empty line usually separates headers from body
        if not line.strip() and body_start > 0:
            result['body'] = '\n'.join(lines[i+1:])
            break
    
    return result
```

---

## 12. Technical Stack

### 12.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                │
│                     React + TypeScript + Vite                        │
│                        TailwindCSS + shadcn/ui                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ REST API (JSON)
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                 │
│                      FastAPI + Python 3.11+                          │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Routes    │  │  Services   │  │    LLM      │                 │
│  │   (API)     │──│  (Business) │──│  (Claude)   │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│         │                │                                           │
│         │         ┌──────┴──────┐                                   │
│         │         │             │                                   │
│         ▼         ▼             ▼                                   │
│  ┌─────────────────────┐  ┌─────────────────────┐                  │
│  │   SQLAlchemy ORM    │  │  Background Jobs    │                  │
│  │   (Models/Repos)    │  │  (APScheduler)      │                  │
│  └─────────────────────┘  └─────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            DATABASE                                  │
│                           PostgreSQL                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 12.2 Tech Stack Details

| Layer | Technology | Notes |
|-------|------------|-------|
| **Frontend** | React 18 + TypeScript | SPA with React Router |
| | Vite | Build tool |
| | TailwindCSS | Styling |
| | shadcn/ui | Component library |
| | React Query | Data fetching/caching |
| | Zustand | State management |
| **Backend** | FastAPI | Python web framework |
| | Pydantic v2 | Data validation |
| | SQLAlchemy 2.0 | ORM |
| | Alembic | Database migrations |
| | APScheduler | Background jobs |
| | python-jose | JWT authentication |
| | passlib | Password hashing |
| **Database** | PostgreSQL 15+ | Primary database |
| **LLM** | Claude API (Anthropic) | Primary LLM |
| | OpenAI GPT-4 (fallback) | Optional fallback |
| **Deployment** | Render | Cloud hosting |
| | Docker | Containerization |
| | GitHub Actions | CI/CD |

### 12.3 Project Structure

```
customer-pulse/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # shadcn components
│   │   │   ├── accounts/        # Account-related components
│   │   │   ├── dashboard/       # Dashboard components
│   │   │   ├── inputs/          # Input forms/modals
│   │   │   └── layout/          # Layout components
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── AccountDetail.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── Login.tsx
│   │   ├── hooks/               # Custom React hooks
│   │   ├── services/            # API service functions
│   │   ├── stores/              # Zustand stores
│   │   ├── types/               # TypeScript types
│   │   └── utils/               # Utility functions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── accounts.py
│   │   │   │   ├── contracts.py
│   │   │   │   ├── inputs.py
│   │   │   │   ├── alerts.py
│   │   │   │   └── dashboard.py
│   │   │   └── deps.py          # Dependencies (auth, db)
│   │   ├── core/
│   │   │   ├── config.py        # Settings
│   │   │   ├── security.py      # Auth utilities
│   │   │   └── database.py      # DB connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/
│   │   │   ├── health_scoring.py
│   │   │   ├── signal_extraction.py
│   │   │   ├── keyword_scanner.py
│   │   │   ├── llm_client.py
│   │   │   └── notification.py
│   │   ├── jobs/                # Background jobs
│   │   │   ├── scheduler.py
│   │   │   ├── health_recalc.py
│   │   │   └── decay_check.py
│   │   └── main.py              # FastAPI app
│   ├── alembic/                 # Migrations
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## 13. Task Breakdown

### Phase 1: Foundation (Week 1-2)

#### 1.1 Backend Setup
- [ ] Initialize FastAPI project structure
- [ ] Configure PostgreSQL connection
- [ ] Set up Alembic migrations
- [ ] Create base SQLAlchemy models
- [ ] Implement auth endpoints (register, login, logout, refresh)
- [ ] Add JWT middleware
- [ ] Create user CRUD operations

#### 1.2 Frontend Setup
- [ ] Initialize Vite + React + TypeScript project
- [ ] Configure TailwindCSS
- [ ] Install and configure shadcn/ui
- [ ] Set up React Router
- [ ] Create auth pages (login, register)
- [ ] Implement auth context/store
- [ ] Create base layout component

#### 1.3 Database
- [ ] Write initial migration (users table)
- [ ] Add accounts table migration
- [ ] Add contracts table migration
- [ ] Add contacts table migration
- [ ] Add inputs table migration
- [ ] Add signal_extractions table migration
- [ ] Add health_scores table migration
- [ ] Add alerts table migration
- [ ] Add reminders table migration
- [ ] Add indexes

### Phase 2: Core Features (Week 3-4)

#### 2.1 Account Management
- [ ] Account CRUD API endpoints
- [ ] ELA parent/child relationship logic
- [ ] Account list page (frontend)
- [ ] Account detail page (frontend)
- [ ] Add account modal (frontend)
- [ ] ELA office tabs (frontend)

#### 2.2 Contract Management
- [ ] Contract CRUD API endpoints
- [ ] Renewal date calculations
- [ ] Non-renewal deadline logic
- [ ] Contract section UI (frontend)
- [ ] Add/edit contract modal (frontend)

#### 2.3 Input System
- [ ] Input CRUD API endpoints
- [ ] Email parsing utility
- [ ] Note input handling
- [ ] Add input modal (frontend)
- [ ] Timeline component (frontend)

### Phase 3: Intelligence Layer (Week 5-6)

#### 3.1 Keyword Scanner
- [ ] Implement keyword lexicon (Python dict)
- [ ] Create scan_for_keywords() function
- [ ] Add severity determination logic
- [ ] Create should_analyze_with_llm() function
- [ ] Write unit tests for scanner

#### 3.2 LLM Configuration
- [ ] Create LLM configuration Pydantic schemas
- [ ] Implement Fernet encryption for API keys
- [ ] Build provider abstraction base class
- [ ] Implement AnthropicProvider
- [ ] Implement OpenAIProvider
- [ ] Implement GoogleProvider (Gemini)
- [ ] Implement XAIProvider (Grok)
- [ ] Implement PerplexityProvider
- [ ] Create LLMClientFactory
- [ ] Build key validation endpoint
- [ ] Create LLM settings API routes
- [ ] Build LLM settings UI page (frontend)

#### 3.3 LLM Integration
- [ ] Create signal extraction prompt
- [ ] Create health assessment prompt
- [ ] Implement extraction pipeline with provider abstraction
- [ ] Add error handling and retries
- [ ] Implement token counting/cost tracking
- [ ] Add usage statistics tracking

#### 3.4 Health Scoring
- [ ] Implement pillar calculation functions
- [ ] Create overall score aggregation
- [ ] Add decay logic
- [ ] Create health recalculation service
- [ ] Build health score history tracking
- [ ] Create AI assessment generation

### Phase 4: Alerts & Notifications (Week 7)

#### 4.1 Alert System
- [ ] Alert creation service
- [ ] Alert triggers (health drop, keywords, renewal)
- [ ] Alert CRUD API endpoints
- [ ] Notification center UI (frontend)
- [ ] Alert badge/counter (frontend)

#### 4.2 Reminder System
- [ ] Reminder CRUD API endpoints
- [ ] Commitment detection from signals
- [ ] Reminder creation from inputs
- [ ] Reminder list UI (frontend)
- [ ] Complete/snooze functionality

### Phase 5: Dashboard & Polish (Week 8)

#### 5.1 Portfolio Dashboard
- [ ] Dashboard stats API endpoint
- [ ] At-risk accounts endpoint
- [ ] Upcoming renewals endpoint
- [ ] Portfolio overview UI (frontend)
- [ ] Filters and sorting (frontend)
- [ ] Account cards with health indicators

#### 5.2 Background Jobs
- [ ] Set up APScheduler
- [ ] Daily health recalculation job
- [ ] Decay check job
- [ ] Renewal reminder job

#### 5.3 Polish & Testing
- [ ] Error handling throughout
- [ ] Loading states (frontend)
- [ ] Empty states (frontend)
- [ ] Form validation
- [ ] API error responses
- [ ] End-to-end testing

### Phase 6: Deployment (Week 9)

#### 6.1 DevOps
- [ ] Create Dockerfile (backend)
- [ ] Create Dockerfile (frontend)
- [ ] Set up docker-compose for local dev
- [ ] Configure Render services
- [ ] Set up environment variables
- [ ] Configure PostgreSQL on Render
- [ ] Set up CI/CD with GitHub Actions

#### 6.2 Documentation
- [ ] API documentation (auto-generated by FastAPI)
- [ ] README with setup instructions
- [ ] Environment variable documentation
- [ ] User guide (basic)

---

## Appendix A: Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/customer_pulse

# Auth
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Key Encryption (for encrypting user's LLM API keys at rest)
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FERNET_SECRET_KEY=your-fernet-key-here

# LLM (BYOK - Users bring their own keys, stored encrypted in DB)
# No API keys stored here - users configure via Settings > LLM Configuration
# These are optional fallback/default keys for system operations only
# ANTHROPIC_API_KEY=sk-ant-...  # Optional: for system health checks
# OPENAI_API_KEY=sk-...         # Optional: for system health checks

# Email (stubbed)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=

# Slack (stubbed)
SLACK_ENABLED=false

# App
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:5173"]
```

---

## Appendix B: Sample Data

```sql
-- Sample user
INSERT INTO users (email, password_hash, name, role) VALUES
('kareem@example.com', '$2b$12$...', 'Kareem Primo', 'admin');

-- Sample accounts
INSERT INTO accounts (name, account_type, account_email, industry, tier, owner_id) VALUES
('USDA', 'ela_parent', 'usda-account@company.com', 'Government', 'enterprise', '<user_id>'),
('Samsung', 'standard', 'samsung-account@company.com', 'Technology', 'enterprise', '<user_id>');

-- Sample ELA child
INSERT INTO accounts (name, account_type, parent_account_id, account_email, industry, tier, owner_id) VALUES
('USDA - NRCS', 'ela_child', '<usda_id>', 'usda-nrcs@company.com', 'Government', 'enterprise', '<user_id>');
```

---

*End of Specification Document*
