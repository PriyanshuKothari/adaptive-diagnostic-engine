"""
Groq LLM Service — Personalized Study Plan Generator
------------------------------------------------------
Sends student performance data to Groq (Llama 3) and returns
a structured 3-step study plan based on weak topics and ability score.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from typing import List
from app.models.session import AnswerRecord

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _build_performance_summary(
    ability: float,
    answer_history: List[AnswerRecord],
) -> str:
    """Build a human-readable summary of student performance."""
    total = len(answer_history)
    correct = sum(1 for a in answer_history if a.is_correct)
    accuracy = round((correct / total) * 100, 1) if total > 0 else 0

    # Aggregate by topic
    topic_stats: dict[str, dict] = {}
    for record in answer_history:
        t = record.topic
        if t not in topic_stats:
            topic_stats[t] = {"correct": 0, "total": 0}
        topic_stats[t]["total"] += 1
        if record.is_correct:
            topic_stats[t]["correct"] += 1

    topic_lines = []
    weak_topics = []
    for topic, stats in topic_stats.items():
        acc = round((stats["correct"] / stats["total"]) * 100, 1)
        topic_lines.append(f"  - {topic}: {stats['correct']}/{stats['total']} correct ({acc}%)")
        if acc < 60:
            weak_topics.append(topic)

    summary = f"""
Student Performance Summary:
- Final Ability Score (theta): {ability:.3f} / 1.0
- Overall Accuracy: {correct}/{total} ({accuracy}%)
- Performance by Topic:
{chr(10).join(topic_lines)}
- Identified Weak Topics (< 60% accuracy): {', '.join(weak_topics) if weak_topics else 'None'}
    """.strip()

    return summary, weak_topics


def generate_study_plan(ability: float, answer_history: List[AnswerRecord]) -> str:
    """
    Call Groq API to generate a personalized 3-step study plan.
    Returns the plan as a formatted string.
    """
    summary, weak_topics = _build_performance_summary(ability, answer_history)

    prompt = f"""
You are an expert GRE tutor. A student just completed an adaptive diagnostic test.
Here is their performance data:

{summary}

Based on this data, generate a personalized 3-step study plan to help this student improve.
Each step should:
1. Target a specific weak area identified above
2. Include a concrete action (e.g., "Practice 20 quadratic equations daily")
3. Suggest a specific resource or method

Format your response as:
STEP 1: [Title]
Action: [Specific action]
Resource: [Suggested resource]

STEP 2: [Title]
Action: [Specific action]
Resource: [Suggested resource]

STEP 3: [Title]
Action: [Specific action]
Resource: [Suggested resource]

Keep each step concise and actionable.
    """.strip()

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a concise, expert GRE tutor who gives actionable study advice.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=600,
    )

    return response.choices[0].message.content
