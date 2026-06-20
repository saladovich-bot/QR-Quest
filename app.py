from flask import Flask, render_template, request, redirect, session
from quest import update_leaderboard

app = Flask(__name__)
app.secret_key = "qr_quest_secret"


booths = {
    "booth_1": {"name": "AI & Machine Learning", "question": "What is the most popular programming language for AI?", "answer": "python", "letter": "I"},
    "booth_2": {"name": "Cybersecurity", "question": "What do we call software that protects your computer from attacks?", "answer": "firewall", "letter": "T"},
    "booth_3": {"name": "Networking", "question": "What connects computers together in a local network?", "answer": "router", "letter": "C"},
    "booth_4": {"name": "Database", "question": "What language is used to query databases?", "answer": "sql", "letter": "L"},
    "booth_5": {"name": "Web Development", "question": "What language styles web pages?", "answer": "css", "letter": "U"},
    "booth_6": {"name": "Operating Systems", "question": "What is the most popular open source OS?", "answer": "linux", "letter": "B"},
    "booth_7": {"name": "Cloud Computing", "question": "What does AWS stand for?", "answer": "amazon web services", "letter": "M"},
    "booth_8": {"name": "Data Science", "question": "What library is used for data analysis in Python?", "answer": "pandas", "letter": "A"},
    "booth_9": {"name": "Machine Learning", "question": "What is the process of a model learning from data called?", "answer": "training", "letter": "Z"},
    "booth_10": {"name": "Programming Basics", "question": "What do we call a variable that cannot be changed?", "answer": "constant", "letter": "E"},
    "booth_11": {"name": "Algorithms", "question": "What sorting algorithm divides the list in half each time?", "answer": "merge sort", "letter": "S"},
    "booth_12": {"name": "Hardware", "question": "What does CPU stand for?", "answer": "central processing unit", "letter": "T"},
    "booth_13": {"name": "Software Engineering", "question": "What is the most popular version control system?", "answer": "git", "letter": "A"},
    "booth_14": {"name": "Mobile Development", "question": "What language is used to develop iOS apps?", "answer": "swift", "letter": "R"},
    "booth_15": {"name": "Robotics", "question": "What does IoT stand for?", "answer": "internet of things", "letter": "T"},
    "booth_16": {"name": "Game Development", "question": "What is the most popular game engine?", "answer": "unity", "letter": "S"},
    "booth_17": {"name": "Blockchain", "question": "What is the first cryptocurrency?", "answer": "bitcoin", "letter": "U"},
    "booth_18": {"name": "AR & VR", "question": "What does VR stand for?", "answer": "virtual reality", "letter": "P"},
    "booth_19": {"name": "UI/UX Design", "question": "What does UX stand for?", "answer": "user experience", "letter": "E"},
    "booth_20": {"name": "Open Source", "question": "What is the most popular open source platform for code hosting?", "answer": "github", "letter": "R"},
    "final": {"name": "Final Challenge", "question": "What is the name of our university club?", "answer": "it club", "letter": "!"}
}

import json
import os

def load_participants():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {}

def save_participants():
    with open("data.json", "w") as f:
        json.dump(participants, f)

participants = load_participants()

@app.route("/", methods=["GET", "POST"])
def register():
    if "student_id" in session:
        return redirect("/welcome")
    
    if request.method == "POST":
        name = request.form["name"]
        student_id = request.form["student_id"]
        email = request.form["email"]
        
        session["name"] = name
        session["student_id"] = student_id
        session["email"] = email
      
        if student_id not in participants:
            participants[student_id] = {
                "name": name,
                "email": email,
                "answers": {},
                "score": 0
            }
        
        return redirect("/welcome")
    
    return render_template("register.html")


@app.route("/booth/<booth_id>", methods=["GET", "POST"])
def booth(booth_id):
    if "student_id" not in session:
        return redirect("/")
    
    student_id = session["student_id"]
    
    if student_id not in participants:
        return redirect("/")
    
    if booth_id not in booths:
        return redirect("/welcome")
    
    score = participants[student_id]["score"]
    already_answered = booth_id in participants[student_id]["answers"]
    result = None
    
    if request.method == "POST" and not already_answered:
        answer = request.form["answer"]
        if answer.lower().strip().replace(" ", "") == booths[booth_id]["answer"].replace(" ", ""):
            participants[student_id]["answers"][booth_id] = True
            participants[student_id]["score"] += 1
            result = "correct"
        else:
            participants[student_id]["answers"][booth_id] = False
            result = "wrong"
        score = participants[student_id]["score"]
        save_participants()
        print("Updating leaderboard...")
        update_leaderboard(participants)
        print("Leaderboard updated!")
    
    booth_list = [(bid, bdata) for bid, bdata in booths.items() if bid != "final"]
    cols = 4
    map_places = []
    for i, (bid, bdata) in enumerate(booth_list):
        row = i // cols
        col = i % cols
        
        if row % 2 == 0:
            x = 10 + col * 22
        else:
            x = 10 + (cols - 1 - col) * 22
        y = 10 + row * 20
        map_places.append({
            "id": i+1,
            "booth_id": bid,
            "name": bdata["name"],
            "letter": bdata["letter"],
            "x": x,
            "y": y
        })

    return render_template("question.html",
        booth_name=booths[booth_id]["name"],
        question=booths[booth_id]["question"],
        score=score,
        already_answered=already_answered,
        result=result,
        answered_booths=participants[student_id]["answers"],
        map_places=map_places
    )

@app.route("/welcome")
def welcome():
    if "student_id" not in session:
        return redirect("/")
    student_id = session["student_id"]
    return render_template("welcome.html",
        name=session["name"],
        score=participants[student_id]["score"]
    )

@app.route("/final", methods=["GET", "POST"])
def final():
    if "student_id" not in session:
        return redirect("/")
    
    student_id = session["student_id"]
    
    if student_id not in participants:
        return redirect("/")
    
    score = participants[student_id]["score"]
    already_answered = "final" in participants[student_id]["answers"]
    result = None
    
    if request.method == "POST" and not already_answered:
        answer = request.form["answer"]
        if answer.lower().strip().replace(" ", "") == booths["final"]["answer"].replace(" ", ""):
            participants[student_id]["answers"]["final"] = True
            participants[student_id]["score"] += 1
            result = "correct"
        else:
            participants[student_id]["answers"]["final"] = False
            result = "wrong"
        score = participants[student_id]["score"]
        save_participants()
        update_leaderboard(participants)
    
    return render_template("final.html",
        booths=booths,
        name=session["name"],
        score=score,
        already_answered=already_answered,
        result=result
    )



if __name__ == "__main__":
    app.run(debug=True)