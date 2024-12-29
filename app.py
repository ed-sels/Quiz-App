from flask import Flask, render_template, request, redirect, url_for, session, flash
import openai

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OpenAI API key (replace with your actual key)
openai.api_key = "your_openai_api_key"

# Static Quiz Data
QUIZ_DATA = {
    "questions": [
        {"text": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
        {"text": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"text": "What is the largest planet in our solar system?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter"},
    ]
}

# AI-based question generator function
def generate_ai_question():
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                "Generate a trivia question with 4 multiple-choice options. "
                "Format the response as follows:\n"
                "Question: [Insert question here]\n"
                "Options: [Option1, Option2, Option3, Option4]\n"
                "Answer: [Correct Option]"
            ),
            max_tokens=150,
            temperature=0.7,
        )
        result = response.choices[0].text.strip()
        lines = result.split("\n")
        question = lines[0].split(": ")[1]
        options = lines[1].split(": ")[1].strip("[]").split(", ")
        answer = lines[2].split(": ")[1]

        return {"text": question, "options": options, "answer": answer}
    except Exception as e:
        return {"error": f"Error generating question: {str(e)}"}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    # Decide which mode to use (static or AI-generated)
    mode = session.get("quiz_mode", "static")

    if "current_question" not in session:
        session["current_question"] = 0
        session["answers"] = []

    if request.method == "POST":
        # Store user's answer
        answer = request.form.get("answer")
        session["answers"].append(answer)

        # Move to the next question
        session["current_question"] += 1

    current_question_index = session["current_question"]

    # Static Mode
    if mode == "static":
        # If there are no more questions, redirect to results page
        if current_question_index >= len(QUIZ_DATA["questions"]):
            return redirect(url_for("results"))

        # Get the current question data
        question = QUIZ_DATA["questions"][current_question_index]
        return render_template(
            "quiz.html",
            question=question,
            question_number=current_question_index + 1,
            total_questions=len(QUIZ_DATA["questions"]),
        )

    # AI Mode
    if mode == "ai":
        if current_question_index >= len(session.get("ai_questions", [])):
            return redirect(url_for("results"))

        # Fetch AI-generated question if not already done
        if current_question_index == len(session.get("ai_questions", [])):
            ai_question = generate_ai_question()
            if "error" in ai_question:
                flash(ai_question["error"], "danger")
                return redirect(url_for("quiz"))
            ai_questions = session.get("ai_questions", [])
            ai_questions.append(ai_question)
            session["ai_questions"] = ai_questions

        question = session["ai_questions"][current_question_index]
        return render_template(
            "quiz.html",
            question=question,
            question_number=current_question_index + 1,
            total_questions=len(session.get("ai_questions", [])),
        )

@app.route("/results")
def results():
    user_answers = session.get("answers", [])
    mode = session.get("quiz_mode", "static")
    questions = QUIZ_DATA["questions"] if mode == "static" else session.get("ai_questions", [])
    correct_answers = 0

    # Compare user answers with the correct answers
    for i, question in enumerate(questions):
        if i < len(user_answers) and user_answers[i] == question["answer"]:
            correct_answers += 1

    score = (correct_answers / len(questions)) * 100 if questions else 0
    return render_template("results.html", score=score, user_answers=user_answers, questions=questions)

@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))

@app.route("/set_mode/<string:mode>")
def set_mode(mode):
    if mode not in ["static", "ai"]:
        flash("Invalid mode selected!", "danger")
        return redirect(url_for("home"))
    session["quiz_mode"] = mode
    session["current_question"] = 0
    session["answers"] = []
    session["ai_questions"] = [] if mode == "ai" else None
    return redirect(url_for("quiz"))

if __name__ == "__main__":
    app.run(debug=True)
