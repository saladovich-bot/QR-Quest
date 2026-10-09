from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "qr_quest_secret_2024"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
# Локальный запуск по http: должно быть False. Для Railway (https) верни True.
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 86400


booths = {
    "booth_1": {
        "name": "Ice Breaker - Find Someone Who",
        "question": "ما الهدف الأساسي من لعبة Find Someone Who؟",
        "options": ["التعارف على أشخاص جدد", "حل أصعب مسألة برمجة", "الفوز بأسرع وقت فقط"],
        "answer": "التعارف على أشخاص جدد",
        "letter": "W"
    },
    "booth_2": {
        "name": "AI Prompt Battle",
        "question": "شو المطلوب منك في لعبة AI Prompt Battle؟",
        "options": ["تصمم موقع إلكتروني", "تكتب وصفاً لـ ChatGPT ليعطيك أفضل صورة", "تكتب كود بلغة Python"],
        "answer": "تكتب وصفاً لـ ChatGPT ليعطيك أفضل صورة",
        "letter": "E"
    },
    "booth_3": {
        "name": "IT Hunting Battle",
        "question": "كم عدد أفراد الفريق الواحد في IT Hunting Battle؟",
        "options": ["من 8 إلى 10 طلاب", "طالب واحد فقط", "من 2 إلى 4 طلاب"],
        "answer": "من 2 إلى 4 طلاب",
        "letter": "L"
    },
    "booth_4": {
        "name": "Multimedia",
        "question": "أي امتداد من التالي يُستخدم للأغاني والملفات الصوتية؟",
        "options": ["PNG", "MP4", "MP3"],
        "answer": "MP3",
        "letter": "C"
    },
    "booth_5": {
        "name": "Artificial Intelligence",
        "question": "ماذا تعني كلمة AI؟",
        "options": ["Artificial Intelligence", "Automatic Internet", "Advanced Information"],
        "answer": "Artificial Intelligence",
        "letter": "O"
    },
    "booth_6": {
        "name": "IT Majors",
        "question": "أي تخصص من التالي يهتم بحماية الأنظمة والمعلومات من الاختراق؟",
        "options": ["Multimedia", "Cybersecurity", "Networks"],
        "answer": "Cybersecurity",
        "letter": "M"
    },
    "booth_7": {
        "name": "IT Majors",
        "question": "أي تخصص من التالي يهتم ببناء الروبوتات والأجهزة الذكية؟",
        "options": ["Robotics", "Graphic Design", "Web Hosting"],
        "answer": "Robotics",
        "letter": "E"
    },
    "final": {
        "name": "Final",
        "question": "ما الكلمة التي تكوّنت من الحروف التي جمعتها؟",
        "options": ["WELCOME", "WELCOMS", "WALCOME"],
        "answer": "WELCOME"
    },
}

from quest import update_leaderboard, load_participants_from_sheets, save_participant_to_sheets

participants = load_participants_from_sheets()


@app.route("/", methods=["GET", "POST"])
def register():
    if "student_id" in session:
        if session["student_id"] in participants:
            return redirect("/welcome")
        # Устаревший cookie (игрока нет на сервере) - сбрасываем сессию
        session.clear()

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

    if booth_id not in booths or booth_id == "final":
        return redirect("/welcome")

    score = participants[student_id]["score"]
    already_answered = booth_id in participants[student_id]["answers"]
    result = None

    if request.method == "POST" and not already_answered:
        answer = request.form["answer"]
        if answer == booths[booth_id]["answer"]:
            participants[student_id]["answers"][booth_id] = True
            participants[student_id]["score"] += 1
            result = "correct"
        else:
            participants[student_id]["answers"][booth_id] = False
            result = "wrong"
        score = participants[student_id]["score"]

        save_participant_to_sheets(student_id, participants[student_id])
        update_leaderboard(participants)

    booth_list = [(bid, bdata) for bid, bdata in booths.items() if bid != "final"]
    cols = 3
    total_rows = (len(booth_list) + cols - 1) // cols
    row_step = 70 / (total_rows - 1) if total_rows > 1 else 0
    map_places = []
    for i, (bid, bdata) in enumerate(booth_list):
        row = i // cols
        col = i % cols

        if row % 2 == 0:
            x = 20 + col * 30
        else:
            x = 20 + (cols - 1 - col) * 30
        y = 15 + row * row_step
        map_places.append({
            "id": i + 1,
            "booth_id": bid,
            "name": bdata["name"],
            "letter": bdata["letter"],
            "x": x,
            "y": y
        })

    return render_template("question.html",
        booth_name=booths[booth_id]["name"],
        question=booths[booth_id]["question"],
        options=booths[booth_id]["options"],
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
    if student_id not in participants:
        return redirect("/")
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
        if answer == booths["final"]["answer"]:
            participants[student_id]["answers"]["final"] = True
            participants[student_id]["score"] += 1
            result = "correct"
        else:
            participants[student_id]["answers"]["final"] = False
            result = "wrong"
        score = participants[student_id]["score"]
        save_participant_to_sheets(student_id, participants[student_id])
        update_leaderboard(participants)

    return render_template("final.html",
        booths=booths,
        name=session["name"],
        score=score,
        already_answered=already_answered,
        result=result
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)