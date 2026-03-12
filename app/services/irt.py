"""
IRT (Item Response Theory) — Rasch Model Implementation
--------------------------------------------------------
The Rasch model defines the probability that a student with ability θ (theta)
answers a question of difficulty b correctly as:

    P(correct | θ, b) = 1 / (1 + exp(-(θ - b)))

This is a logistic function. When θ > b, probability > 0.5 (student likely correct).
When θ < b, probability < 0.5 (student likely incorrect).

Ability Update (MLE-inspired gradient step):
After each response, we update θ using the score residual:

    θ_new = θ_old + learning_rate * (response - P(correct | θ, b))

Where:
    - response = 1 if correct, 0 if incorrect
    - learning_rate controls how aggressively ability is revised
    - This is a simplified online update (no full Fisher scoring for simplicity)

Next Question Selection:
    Pick the question whose difficulty b is closest to the current θ,
    from questions not yet seen. This maximizes information at the current ability level.
"""

import math
from typing import List, Optional

LEARNING_RATE: float = 0.3      # How fast ability updates per question
MAX_QUESTIONS: int = 10         # End session after this many questions
ABILITY_MIN: float = 0.1        # Clamp theta lower bound
ABILITY_MAX: float = 1.0        # Clamp theta upper bound


def probability_correct(theta: float, difficulty: float) -> float:
    """Rasch model: P(correct | theta, difficulty)."""
    return 1.0 / (1.0 + math.exp(-(theta - difficulty)))


def update_ability(theta: float, difficulty: float, is_correct: bool) -> float:
    """
    Update student ability using gradient step on log-likelihood.
    residual = observed - expected
    theta_new = theta + lr * residual
    """
    response: int = 1 if is_correct else 0
    p: float = probability_correct(theta, difficulty)
    residual: float = response - p
    new_theta: float = theta + LEARNING_RATE * residual
    # Clamp to valid range
    return round(max(ABILITY_MIN, min(ABILITY_MAX, new_theta)), 4)


def select_next_question(
    current_ability: float,
    all_questions: List[dict],
    asked_ids: List[str],
) -> Optional[dict]:
    """
    Choose the unanswered question whose difficulty is closest to current ability.
    This maximises Fisher information at the student's current theta.
    """
    available = [q for q in all_questions if q["question_id"] not in asked_ids]
    if not available:
        return None
    # Sort by absolute distance between difficulty and theta
    return min(available, key=lambda q: abs(q["difficulty"] - current_ability))


def session_is_complete(questions_asked_count: int) -> bool:
    return questions_asked_count >= MAX_QUESTIONS
