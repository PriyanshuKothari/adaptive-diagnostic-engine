"""
Seed script: inserts 20 GRE-style questions into MongoDB.
Run with: python -m app.seed.seed_questions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.database import questions_col

QUESTIONS = [
    # ── ALGEBRA (5 questions) ────────────────────────────────────────────────
    {
        "question_id": "q001",
        "text": "If 2x + 3 = 11, what is the value of x?",
        "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
        "correct_answer": "C",
        "difficulty": 0.1,
        "topic": "Algebra",
        "tags": ["linear equations", "basic"],
    },
    {
        "question_id": "q002",
        "text": "Solve for x: x² - 5x + 6 = 0",
        "options": ["A) x = 1, 6", "B) x = 2, 3", "C) x = -2, -3", "D) x = -1, 6"],
        "correct_answer": "B",
        "difficulty": 0.3,
        "topic": "Algebra",
        "tags": ["quadratic", "factoring"],
    },
    {
        "question_id": "q003",
        "text": "If f(x) = 3x² - 2x + 1, what is f(3)?",
        "options": ["A) 22", "B) 24", "C) 26", "D) 28"],
        "correct_answer": "C",
        "difficulty": 0.4,
        "topic": "Algebra",
        "tags": ["functions", "substitution"],
    },
    {
        "question_id": "q004",
        "text": "The sum of three consecutive integers is 99. What is the largest integer?",
        "options": ["A) 31", "B) 32", "C) 33", "D) 34"],
        "correct_answer": "D",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["word problems", "consecutive integers"],
    },
    {
        "question_id": "q005",
        "text": "If |2x - 4| > 6, which of the following is a solution?",
        "options": ["A) x = 2", "B) x = 4", "C) x = -2", "D) x = 3"],
        "correct_answer": "C",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["absolute value", "inequalities"],
    },

    # ── GEOMETRY (4 questions) ───────────────────────────────────────────────
    {
        "question_id": "q006",
        "text": "A circle has a radius of 7. What is its area? (Use π ≈ 3.14)",
        "options": ["A) 43.96", "B) 153.86", "C) 44", "D) 49"],
        "correct_answer": "B",
        "difficulty": 0.2,
        "topic": "Geometry",
        "tags": ["circle", "area"],
    },
    {
        "question_id": "q007",
        "text": "In a right triangle, the two legs are 6 and 8. What is the hypotenuse?",
        "options": ["A) 9", "B) 10", "C) 11", "D) 12"],
        "correct_answer": "B",
        "difficulty": 0.25,
        "topic": "Geometry",
        "tags": ["pythagorean theorem", "right triangle"],
    },
    {
        "question_id": "q008",
        "text": "A rectangle has a perimeter of 36 and a width of 6. What is its area?",
        "options": ["A) 54", "B) 72", "C) 108", "D) 60"],
        "correct_answer": "B",
        "difficulty": 0.45,
        "topic": "Geometry",
        "tags": ["rectangle", "perimeter", "area"],
    },
    {
        "question_id": "q009",
        "text": "Two parallel lines are cut by a transversal. If one co-interior angle is 65°, what is the other?",
        "options": ["A) 65°", "B) 115°", "C) 90°", "D) 125°"],
        "correct_answer": "B",
        "difficulty": 0.6,
        "topic": "Geometry",
        "tags": ["parallel lines", "transversal", "angles"],
    },

    # ── ARITHMETIC & NUMBER THEORY (4 questions) ─────────────────────────────
    {
        "question_id": "q010",
        "text": "What is 15% of 240?",
        "options": ["A) 36", "B) 24", "C) 40", "D) 30"],
        "correct_answer": "A",
        "difficulty": 0.15,
        "topic": "Arithmetic",
        "tags": ["percentage", "basic"],
    },
    {
        "question_id": "q011",
        "text": "What is the least common multiple (LCM) of 12 and 18?",
        "options": ["A) 6", "B) 24", "C) 36", "D) 216"],
        "correct_answer": "C",
        "difficulty": 0.3,
        "topic": "Arithmetic",
        "tags": ["LCM", "number theory"],
    },
    {
        "question_id": "q012",
        "text": "A store marks up an item by 40% and then offers a 20% discount. What is the net % change?",
        "options": ["A) 20% increase", "B) 12% increase", "C) 8% increase", "D) 20% decrease"],
        "correct_answer": "B",
        "difficulty": 0.65,
        "topic": "Arithmetic",
        "tags": ["percentage", "profit-loss"],
    },
    {
        "question_id": "q013",
        "text": "How many prime numbers are between 20 and 40?",
        "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
        "correct_answer": "B",
        "difficulty": 0.5,
        "topic": "Arithmetic",
        "tags": ["prime numbers", "number theory"],
    },

    # ── VOCABULARY (4 questions) ─────────────────────────────────────────────
    {
        "question_id": "q014",
        "text": "Choose the word most similar in meaning to EPHEMERAL:",
        "options": ["A) Permanent", "B) Fleeting", "C) Ancient", "D) Massive"],
        "correct_answer": "B",
        "difficulty": 0.35,
        "topic": "Vocabulary",
        "tags": ["synonyms", "GRE words"],
    },
    {
        "question_id": "q015",
        "text": "Choose the word most opposite in meaning to LOQUACIOUS:",
        "options": ["A) Talkative", "B) Verbose", "C) Taciturn", "D) Gregarious"],
        "correct_answer": "C",
        "difficulty": 0.55,
        "topic": "Vocabulary",
        "tags": ["antonyms", "GRE words"],
    },
    {
        "question_id": "q016",
        "text": "The scientist's conclusions were considered _____ because they lacked empirical support. (Choose best word)",
        "options": ["A) Irrefutable", "B) Tenuous", "C) Compelling", "D) Exhaustive"],
        "correct_answer": "B",
        "difficulty": 0.7,
        "topic": "Vocabulary",
        "tags": ["sentence completion", "GRE words"],
    },
    {
        "question_id": "q017",
        "text": "Which word best describes someone who pretends to have virtues or beliefs they do not have?",
        "options": ["A) Altruist", "B) Pragmatist", "C) Hypocrite", "D) Stoic"],
        "correct_answer": "C",
        "difficulty": 0.2,
        "topic": "Vocabulary",
        "tags": ["definitions", "GRE words"],
    },

    # ── DATA ANALYSIS (3 questions) ──────────────────────────────────────────
    {
        "question_id": "q018",
        "text": "The mean of 5 numbers is 14. If four of the numbers are 10, 12, 16, and 18, what is the fifth?",
        "options": ["A) 12", "B) 14", "C) 10", "D) 16"],
        "correct_answer": "B",
        "difficulty": 0.35,
        "topic": "Data Analysis",
        "tags": ["mean", "statistics"],
    },
    {
        "question_id": "q019",
        "text": "A bag has 4 red and 6 blue balls. What is the probability of drawing 2 red balls in a row without replacement?",
        "options": ["A) 2/15", "B) 4/25", "C) 1/6", "D) 8/45"],
        "correct_answer": "A",
        "difficulty": 0.75,
        "topic": "Data Analysis",
        "tags": ["probability", "combinatorics"],
    },
    {
        "question_id": "q020",
        "text": "In a set of 7 numbers, the median is 9 and the range is 10. If the smallest number is 4, what is the largest?",
        "options": ["A) 13", "B) 14", "C) 15", "D) 16"],
        "correct_answer": "B",
        "difficulty": 0.85,
        "topic": "Data Analysis",
        "tags": ["median", "range", "statistics"],
    },
]


def seed():
    existing = questions_col.count_documents({})
    if existing >= 20:
        print(f"✅ Already seeded ({existing} questions found). Skipping.")
        return

    questions_col.drop()
    questions_col.insert_many(QUESTIONS)
    print(f"✅ Seeded {len(QUESTIONS)} questions into MongoDB.")


if __name__ == "__main__":
    seed()
