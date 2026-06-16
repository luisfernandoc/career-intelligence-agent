# Career Intelligence Agent

Career Intelligence Agent is an AI-powered assistant designed to help professionals analyze job opportunities, identify skill gaps, prepare for interviews, and build a long-term professional knowledge base.

The project combines Large Language Models (LLMs), structured persistence, and career insights to provide personalized recommendations for interview preparation and career growth.

---

## Features

### Job Analysis

Analyze a resume against a target job description.

- Match score calculation
- Strength identification
- Skill gap detection
- Interview risk assessment
- Personalized recommendations

### Interview Question Generation

Generate interview questions tailored to:

- Candidate experience
- Job requirements
- Technical stack
- Target role

### Answer Evaluation

Evaluate interview responses and provide:

- Feedback
- Areas for improvement
- Communication assessment
- Suggested stronger answers

### Study Plan Generation

Generate personalized study plans based on identified skill gaps.

Includes:

- Preparation priorities
- Daily learning suggestions
- Practice exercises
- Project recommendations

### Professional Memory

Store and track:

- Job analyses
- Generated questions
- Interview evaluations
- Study plans

### Career Insights

Automatically identify:

- Recurring skill gaps
- Most common strengths
- Recommended learning focus areas
- Career preparation trends

---

## Architecture

```text
Client
   │
   ▼
FastAPI API
   │
   ▼
Routes Layer
   │
   ▼
Services Layer
   │
   ▼
Provider Factory
   │
   ├── Groq Provider
   │
   └── OpenAI Provider
           │
           ▼
          LLM
```

### Persistence Layer

```text
SQLite
   │
   ├── Job Analyses
   ├── Interview Questions
   ├── Answer Evaluations
   ├── Study Plans
   └── Skill Insights
```

---

## Current Endpoints

### System

| Method | Endpoint |
|----------|----------|
| GET | `/health` |

### Analysis

| Method | Endpoint |
|----------|----------|
| POST | `/analyze-job` |
| POST | `/generate-questions` |
| POST | `/evaluate-answer` |
| POST | `/study-plan` |

### History

| Method | Endpoint |
|----------|----------|
| GET | `/history/job-analyses` |
| GET | `/history/questions` |
| GET | `/history/evaluations` |
| GET | `/history/study-plans` |

### Insights

| Method | Endpoint |
|----------|----------|
| GET | `/insights/skill-gaps` |
| GET | `/insights/top-strengths` |
| GET | `/insights/career-summary` |

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

### AI

- Groq
- OpenAI-compatible architecture
- LLM Provider Abstraction

### Database

- SQLite

### Development

- Uvicorn
- python-dotenv

---

## Design Decisions

### Provider Abstraction

The application uses a provider-based architecture to avoid coupling business logic to a specific LLM vendor.

Current providers:

- Groq
- OpenAI

Future providers:

- Ollama
- Gemini
- Anthropic

### Structured Persistence

Career data is stored in SQLite to enable:

- Historical analysis
- Trend detection
- Skill tracking
- Future retrieval systems

### Skill Insights

Skill strengths and gaps are stored separately from raw LLM responses.

This enables:

- Long-term tracking
- Aggregation
- Career recommendations
- Future agent reasoning

---

## Roadmap

### Phase 1 — Functional MVP ✅

- [x] Job analysis
- [x] Interview question generation
- [x] Answer evaluation
- [x] Study plan generation
- [x] Multi-provider LLM architecture

### Phase 2 — Professional Memory ✅

- [x] SQLite persistence
- [x] Historical records
- [x] Skill tracking
- [x] Career insights
- [x] Recurring gap detection

### Phase 3 — Career Knowledge Base

- [x] Manual document ingestion
- [x] File upload ingestion
- [X] Embeddings
- [X] ChromaDB integration
- [X] Career memory retrieval
- [ ] PDF support
- [ ] DOCX support
- [ ] Repository ingestion
- [ ] Resume knowledge base
- [ ] Interview notes retrieval

### Phase 4 — Interview Simulator

- [ ] Mock interview sessions
- [ ] Multi-question interviews
- [ ] Session summaries
- [ ] Progress tracking

### Phase 5 — Agent Architecture

- [ ] Tool calling
- [ ] Memory search tools
- [ ] Career reasoning workflows
- [ ] Automated preparation plans

### Phase 6 — Frontend

- [ ] React application
- [ ] Dashboard
- [ ] Career analytics
- [ ] Interview simulator UI

---

## Future Vision

Career Intelligence Agent aims to evolve into a personal career operating system capable of:

- Understanding professional history
- Tracking strengths and weaknesses
- Preparing users for interviews
- Recommending learning paths
- Acting as a long-term career copilot

---

## Example Insight

```json
{
  "top_skill_gaps": [
    {
      "skill": "vector databases",
      "count": 5
    },
    {
      "skill": "rust",
      "count": 4
    }
  ],
  "recommended_focus": [
    "vector databases",
    "rust",
    "aws"
  ]
}
```

---

## Author

Luis Fernando Cuevas Alvarez
