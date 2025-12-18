# Customer Pulse 🩺

An AI-Powered Customer Health Scoring Platform designed for modern Customer Success teams. It aggregates signals from emails, meetings, and contracts to provide a real-time health score, enabling proactive churn prevention.

---

## 🏗 Infrastructure & Tech Stack

### Backend
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.9+) - High-performance async API.
*   **Database**: [PostgreSQL](https://www.postgresql.org/) 15 - Relational data persistence.
*   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) 2.0 - Database abstraction.
*   **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database schema version control.
*   **Task Scheduling**: [APScheduler](https://apscheduler.readthedocs.io/) - Background jobs for daily health score recalculation.
*   **AI Integration**: Modular `LLMClientFactory` supporting OpenAI, Anthropic, and Google Gemini.

### Frontend
*   **Framework**: [React](https://react.dev/) 18 + [Vite](https://vitejs.dev/) - Blazing fast SPA architecture.
*   **Language**: TypeScript - Type-safe development.
*   **Styling**: [Tailwind CSS](https://tailwindcss.com/) + [Shadcn UI](https://ui.shadcn.com/) - Premium, responsive component library.
*   **State Management**: React Query (TanStack) - Server state management.

### Deployment
*   **Containerization**: Docker & Docker Compose - consistent local and production environments.

---

## 📂 Project Structure

```bash
/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/routes/     # API Endpoints (v1)
│   │   ├── core/           # Config, Security, Database
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   └── services/       # Business Logic (Health Calc, Intelligence)
│   ├── migrations/         # Alembic versions
│   └── scripts/            # Seed & Maintenance utilities
│
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Route-based views
│   │   ├── services/       # API Clients (Axios)
│   │   └── types/          # TypeScript Interfaces
│   └── public/             # Static assets
│
└── docker-compose.yml      # Orchestration config
```

---

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   *OR* Python 3.9+ and Node.js 18+ for local dev.

### Option 1: Docker (Recommended)
1.  **Configure Environment**:
    Create `.env` in the root:
    ```env
    DATABASE_URL=postgresql://user:password@db:5432/customer_pulse
    SECRET_KEY=dev_secret_key_change_in_prod
    FERNET_KEY=<generate_using_fernet>
    ```

2.  **Launch**:
    ```bash
    docker-compose up -d --build
    ```
    *   Frontend: `http://localhost`
    *   API Documentation: `http://localhost:8000/docs`

### Option 2: Local Development
**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing & Validation
*   **API Tests**: `python backend/scripts/debug_api.py` (Connectivity check)
*   **Seed Data**: `python backend/scripts/seed_demo.py` (Populates demo accounts)

## 🔐 Security
*   **API Key Encryption**: All LLM provider keys are encrypted at rest using Fernet (symmetric encryption).
*   **CORS**: Configured strict origin policies for production, open for dev.

## � License
Private & Proprietary.
