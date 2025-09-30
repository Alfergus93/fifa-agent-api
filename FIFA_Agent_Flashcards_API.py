
from fastapi import FastAPI
from pydantic import BaseModel
import random, json, time

app = FastAPI()

# Charger les flashcards
with open("FIFA_Agent_Flashcards.json", "r", encoding="utf-8") as f:
    flashcards = json.load(f)

# Stockage temporaire des sessions (simple en mémoire)
sessions = {}

class AnswerRequest(BaseModel):
    session_id: str
    question: str
    reponse: str

@app.get("/entrainement/{session_id}")
def entrainement(session_id: str):
    """Retourne une question aléatoire pour l'entraînement."""
    carte = random.choice(flashcards)
    sessions[session_id] = {"question": carte["question"], "answer": carte["answer"], "score": 0}
    return {"question": carte["question"]}

@app.post("/corriger")
def corriger(data: AnswerRequest):
    """Corrige une réponse donnée et renvoie le résultat."""
    session = sessions.get(data.session_id, {})
    if not session:
        return {"error": "Session non trouvée"}
    correcte = session["answer"]
    resultat = "✅ Correct" if data.reponse.lower().strip() == correcte.lower().strip() else "❌ Incorrect"
    if resultat.startswith("✅"):
        session["score"] += 1
    return {
        "question": session["question"],
        "ta_reponse": data.reponse,
        "bonne_reponse": correcte,
        "resultat": resultat,
        "score": session["score"]
    }

@app.get("/exam/{session_id}")
def exam(session_id: str, n_questions: int = 20, duree_minutes: int = 60):
    """Démarre un examen blanc avec un certain nombre de questions."""
    questions = random.sample(flashcards, min(n_questions, len(flashcards)))
    sessions[session_id] = {
        "exam": questions,
        "score": 0,
        "debut": time.time(),
        "limite": duree_minutes * 60
    }
    return {"questions": [q["question"] for q in questions], "limite_minutes": duree_minutes}

class ExamAnswerRequest(BaseModel):
    session_id: str
    question: str
    reponse: str

@app.post("/exam/reponse")
def exam_reponse(data: ExamAnswerRequest):
    """Corrige une réponse d'examen."""
    session = sessions.get(data.session_id, {})
    if not session:
        return {"error": "Session non trouvée"}
    if time.time() - session["debut"] > session["limite"]:
        return {"error": "⏰ Temps écoulé !"}
    for q in session["exam"]:
        if q["question"] == data.question:
            correcte = q["answer"]
            resultat = "✅ Correct" if data.reponse.lower().strip() == correcte.lower().strip() else "❌ Incorrect"
            if resultat.startswith("✅"):
                session["score"] += 1
            return {
                "question": q["question"],
                "ta_reponse": data.reponse,
                "bonne_reponse": correcte,
                "resultat": resultat,
                "score": session["score"]
            }
    return {"error": "Question introuvable dans l'examen"}

@app.get("/exam/score/{session_id}")
def exam_score(session_id: str):
    """Renvoie le score final d'un examen."""
    session = sessions.get(session_id, {})
    if not session or "exam" not in session:
        return {"error": "Examen non trouvé"}
    total = len(session["exam"])
    return {"score": session["score"], "total": total, "pourcentage": (session["score"]/total)*100}
