# 🧠 Adaptive Diagnostic Engine

A 1-Dimension Adaptive Testing system that dynamically selects GRE-style questions based on a student's estimated ability using **Item Response Theory (IRT)** — Rasch Model. Built with FastAPI, MongoDB, and Groq (Llama 3) for AI-powered personalized study plans.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- MongoDB running locally (`mongod`)
- A free [Groq API key](https://console.groq.com/) (takes 30 seconds, no credit card needed)

### 2. Clone & Install

```bash
git clone https://github.com/PriyanshuKothari/adaptive-diagnostic-engine.git
cd adaptive-diagnostic-engine

pip install -r requirements.txt
```

### 3. Configure Environment

creat `.env`:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=adaptive_engine
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Seed the Database

```bash
python -m app.seed.seed_questions
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

---

## 📡 API Endpoints

### Sessions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/sessions/start` | Start a new test session |
| `GET`  | `/sessions/{session_id}` | Get current session state |

**POST /sessions/start** — Body:
```json
{ "student_name": "Alice" }
```
**Response:**
```json
{
  "session_id": "uuid-here",
  "student_name": "Alice",
  "ability": 0.5,
  "questions_answered": 0,
  "is_complete": false
}
```

---

### Questions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/questions/next?session_id=<id>` | Get the next adaptive question |

**Response:**
```json
{
  "question_id": "q004",
  "text": "The sum of three consecutive integers is 99...",
  "options": ["A) 31", "B) 32", "C) 33", "D) 34"],
  "difficulty": 0.5,
  "topic": "Algebra",
  "tags": ["word problems"]
}
```

---

### Answers
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/answers/submit` | Submit an answer, get IRT update |

**POST /answers/submit** — Body:
```json
{
  "session_id": "uuid-here",
  "question_id": "q004",
  "selected_answer": "D"
}
```

**Response (mid-session):**
```json
{
  "is_correct": true,
  "correct_answer": "D",
  "new_ability": 0.62,
  "questions_answered": 5,
  "is_complete": false,
  "study_plan": null
}
```

**Response (session complete — 10 questions):**
```json
{
  "is_correct": false,
  "correct_answer": "B",
  "new_ability": 0.54,
  "questions_answered": 10,
  "is_complete": true,
  "study_plan": "STEP 1: Strengthen Algebra Skills\nAction: Practice 20 quadratic equations daily...\n..."
}
```

---

## 🧮 Adaptive Algorithm Explained

### Model: Rasch IRT (1-Parameter Logistic)

The system uses the **Rasch Model** from Item Response Theory to estimate student ability.

**Probability of a correct answer:**

```
P(correct | θ, b) = 1 / (1 + e^(-(θ - b)))
```

Where:
- `θ` (theta) = student ability score (0.1 to 1.0)
- `b` = question difficulty (0.1 to 1.0)

**Ability Update (Online Gradient Step):**

After each response, ability is updated using the score residual:

```
θ_new = θ_old + learning_rate × (response - P(correct | θ, b))
```

- `response` = 1 if correct, 0 if incorrect
- `learning_rate` = 0.3 (tunable)
- `P(correct | θ, b)` = expected probability from Rasch model

This is mathematically equivalent to a gradient ascent step on the log-likelihood, giving a principled update that shrinks as ability converges.

**Next Question Selection:**

The system selects the unanswered question whose difficulty is closest to the current `θ`:

```
argmin_q |q.difficulty - θ|
```

This maximises **Fisher Information** at the student's current ability estimate — the core principle of Computer Adaptive Testing (CAT).

### Example Flow
```
Start:  θ = 0.5 → select question with difficulty ≈ 0.5
✓ Correct → θ increases (e.g. 0.62) → next question difficulty ≈ 0.62
✗ Wrong  → θ decreases (e.g. 0.54) → next question difficulty ≈ 0.54
... (10 questions total)
```

---

## 🤖 AI Log — How AI Tools Were Used

### Tools Used
- **Claude (Anthropic)** — Architecture planning, IRT math explanation, Pydantic model design
- **Cursor.ai** — Code generation for boilerplate routes and MongoDB queries
- **Groq (Llama 3)** — Runtime AI inference for generating personalized study plans

### What AI Accelerated
1. **IRT formula verification** — Used Claude to verify the Rasch model update equation and confirm the gradient-step interpretation was mathematically sound
2. **MongoDB schema design** — Claude suggested embedding `answer_history` in the session document vs. a separate collection (chose embedded for read performance on 10-item sessions)
3. **Seed data generation** — Used AI to generate 20 GRE-style questions with calibrated difficulty scores across 5 topics
4. **Groq prompt engineering** — Iterated on the study plan prompt to get structured, actionable 3-step output

### Challenges AI Couldn't Fully Solve
1. **Difficulty calibration** — AI suggested question difficulties but real-world IRT requires empirical data from student responses to calibrate `b` values properly. The seed difficulties are expert estimates, not statistically derived
2. **Groq response consistency** — LLM output format (STEP 1/2/3) required a specific prompt structure; raw output occasionally deviated and needed format enforcement
3. **Edge cases in IRT clamping** — Deciding on `ABILITY_MIN = 0.1` vs `0.0` required thinking through what happens when a student gets every question wrong

---

## 📁 Project Structure

```
adaptive-diagnostic-engine/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # MongoDB connection
│   ├── models/
│   │   ├── question.py      # Question & QuestionOut schemas
│   │   └── session.py       # UserSession, AnswerRecord schemas
│   ├── routes/
│   │   ├── sessions.py      # POST /sessions/start, GET /sessions/{id}
│   │   ├── questions.py     # GET /questions/next
│   │   └── answers.py       # POST /answers/submit
│   ├── services/
│   │   ├── irt.py           # Rasch model IRT logic
│   │   └── llm.py           # Groq study plan generation
│   └── seed/
│       └── seed_questions.py # 20 GRE questions seeder
├── .env
├── requirements.txt
└── README.md
```

---

## 🗄️ MongoDB Schema

### `questions` collection
```json
{
  "question_id": "q001",
  "text": "If 2x + 3 = 11, what is x?",
  "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
  "correct_answer": "C",
  "difficulty": 0.1,
  "topic": "Algebra",
  "tags": ["linear equations", "basic"]
}
```

### `user_sessions` collection
```json
{
  "session_id": "uuid",
  "student_name": "Alice",
  "ability": 0.62,
  "questions_asked": ["q001", "q004", "..."],
  "answer_history": [
    {
      "question_id": "q001",
      "topic": "Algebra",
      "difficulty": 0.1,
      "is_correct": true,
      "ability_after": 0.62
    }
  ],
  "is_complete": false,
  "started_at": "2025-01-01T10:00:00Z",
  "completed_at": null
}
```
