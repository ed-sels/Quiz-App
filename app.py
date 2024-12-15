from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Quiz Data
QUIZ_DATA = {
    "questions": [
        {"text": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
        {"text": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"text": "What is the largest planet in our solar system?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter"},
    ]
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
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

    # If there are no more questions, redirect to results page
    if current_question_index >= len(QUIZ_DATA["questions"]):
        return redirect(url_for("results"))

    # Get the current question data
    question = QUIZ_DATA["questions"][current_question_index]
    return render_template("quiz.html", question=question, question_number=current_question_index + 1, total_questions=len(QUIZ_DATA["questions"]))

@app.route("/results")
def results():
    user_answers = session.get("answers", [])
    correct_answers = 0

    # Compare user answers with the correct answers
    for i, question in enumerate(QUIZ_DATA["questions"]):
        if i < len(user_answers) and user_answers[i] == question["answer"]:
            correct_answers += 1

    score = (correct_answers / len(QUIZ_DATA["questions"])) * 100
    return render_template("results.html", score=score, user_answers=user_answers, questions=QUIZ_DATA["questions"])


@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("quiz"))

if __name__ == "__main__":
    app.run(debug=True)
