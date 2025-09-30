# FIFA Agent API ⚽

API développée en **FastAPI** pour s'entraîner à l'examen d'Agent FIFA.  
Elle permet de réviser via **flashcards interactives**, de lancer des **examens blancs** et d'obtenir des **corrections détaillées**.

---

## 🚀 Fonctionnalités

- **Mode Entraînement** : questions aléatoires via `/entrainement/{session_id}`  
- **Mode Correction** : validation des réponses via `/corriger`  
- **Examens Blancs** : simulation de 20 questions chronométrées via `/exam/{session_id}`  
- **Score Final** : résultats et pourcentage via `/exam/score/{session_id}`  

---

## 📂 Fichiers inclus
- `FIFA_Agent_Flashcards_API.py` → code source de l’API  
- `FIFA_Agent_Flashcards.json` → base de données des questions/réponses  
- `requirements.txt` → dépendances Python (FastAPI, Uvicorn)

---

## 🔧 Installation locale

### 1. Cloner le projet
```bash
git clone https://github.com/Alfergus93/fifa-agent-api.git
cd fifa-agent-api
