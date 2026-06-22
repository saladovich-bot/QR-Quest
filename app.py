from flask import Flask, render_template, request, redirect, session
from quest import update_leaderboard
import os

app = Flask(__name__)
app.secret_key = "qr_quest_secret_2024"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 86400


booths = {
    "booth_1": {
        "name": "FindIt Campus",
        "question": "What is the main purpose of the FindIt Campus application?",
        "options": ["CampusNavigation", "EventScheduling", "LostAndFound"],
        "answer": "LostAndFound",
        "letter": "I"
    },
    "booth_2": {
        "name": "نفشة وطن - HomeLand In a Pattern",
        "question": "ما هي التقنية المستخدمة في المشروع للحفاظ على التراث الفلسطيني رقمياً؟",
        "options": ["الموشن جرافيك", "الواقع الافتراضي", "الذكاء الاصطناعي"],
        "answer": "الموشن جرافيك",
        "letter": "T"
    },
    "booth_3": {
        "name": "Ivestpress",
        "question": "بيستهدف أشخاص مهنتهم في سوق العمل بحاجة لتوثيق الأخبار وتصوير الأحداث، فمن المستخدمون للمنصة؟",
        "options": ["المحامون", "المدرسون", "الصحفيون" ],
        "answer": "الصحفيون",
        "letter": "C"
    },
    "booth_4": {
        "name": "Tracely",
        "question": "رفيقك وقت الضياع ودليلك وقت السفر، بيعرف وين كنت ووين رايح، ودائماً بلحقك... شو هو؟",
        "options": ["Bluetooth", "GPS", "WiFi"],
        "answer": "GPS",
        "letter": "L"
    },
    "booth_5": {
        "name": "Eyeland",
        "question": "ما هي التقنية التي تسمح للطفل بتجربة النظارات على وجهه داخل التطبيق؟",
        "options": ["الواقع المعزز (AR)", "الواقع الافتراضي (VR)", "معالجة الصور (IP)"],
        "answer": "الواقع المعزز (AR)",
        "letter": "U"
    },
    "booth_6": {
        "name": "Social Media & Mental Health",
        "question": "ما مجال الذكاء الاصطناعي الذي يندرج المشروع ضمنه؟",
        "options": ["Expert Systems", "Deep Learning", "Fuzzy Logic"],
        "answer": "Deep Learning",
        "letter": "B"
    },
    "booth_7": {
        "name": "Green AAUP",
        "question": "ما الشيء الذي يجب على اللاعب إنقاذه؟",
        "options": ["البيئة", "المدينة", "الحيوانات"],
        "answer": "البيئة",
        "letter": "M"
    },
    "booth_8": {
        "name": "Catalyst Lab",
        "question": "كيف يخزن Catalyst Lab التفاعلات المحفوظة (Favourite) لتعمل بدون إنترنت؟",
        "options": ["Session Storage", "Cloud Storage", "Local Storage"],
        "answer": "Local Storage",
        "letter": "A"
    },
    "booth_9": {
        "name": "No More Cheaters",
        "question": "What framework is used for the frontend?",
        "options": ["Vue", "Angular", "React"],
        "answer": "React",
        "letter": "Z"
    },
    "booth_10": {
        "name": "No More Cheaters",
        "question": "What foundational deep learning architecture does the YOLO model rely on?",
        "options": ["CNN", "RNN", "GAN"],
        "answer": "CNN",
        "letter": "E"
    },
    "booth_11": {
        "name": "EduNext",
        "question": "ليش سمّينا مشروعنا EduNext؟",
        "options": ["تطوير المناهج" , "مستقبل التعليم", "التعلم الذكي"],
        "answer": "مستقبل التعليم",
        "letter": "S"
    },
    "booth_12": {
        "name": "Smart Bus System",
        "question": "ما الرمز الذي يمسحه الراكب لدفع أجرة الحافلة إلكترونياً؟",
        "options": ["NFC", "Barcode", "QR"],
        "answer": "QR",
        "letter": "T"
    },
    "booth_13": {
        "name": "رحلة إلى القدس",
        "question": "ما هي العناصر التراثية التي يجمعها اللاعب؟",
        "options": ["الزهور والأعشاب والتوابل" , "سعف النخيل والقمح وأغصان الزيتون", "الحجارة والخزف والفخار"],
        "answer": "سعف النخيل والقمح وأغصان الزيتون",
        "letter": "A"
    },
    "final": {
        "name": "Final Challenge",
        "question": "What is the name of our university club?",
        "options": ["Code Club", "Tech Club", "IT Club"],
        "answer": "IT Club",
        "letter": "R"
    }
}

import json
import os

def load_participants():
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as f:
                content = f.read()
                if content.strip():
                    return json.loads(content)
        except:
            pass
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
        if answer == booths[booth_id]["answer"]:
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)