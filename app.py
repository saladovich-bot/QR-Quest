from flask import Flask, render_template, request, redirect, session
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
        "name": "Secure Chat Messaging System",
        "question": "من الذي مصرح له برؤية محتوى الرسالة في المشروع؟",
        "options": ["لا شيء مما ذكر", "مدير السيرفر", "صاحب التطبيق"],
        "answer": "لا شيء مما ذكر",
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
    "booth_14": {
        "name": "Multimedia",
        "question": "أي تنسيق من التالي يُستخدم غالبًا للصور التي تحتاج خلفية شفافة؟",
        "options": ["JPG", "PNG", "MP3"],
        "answer": "PNG",
        "letter": "B"
    },
    "booth_15": {
        "name": "IOT Forensics",
        "question": "?ما هي صيغة الملفات المستخرجة من الكاميرات في مشروعنا",
        "options": [".RAW", ".PCAP", "MP4 AVI MOV UVRD"],
        "answer": "MP4 AVI MOV UVRD",
        "letter": "?"
    },
    "booth_16": {
        "name": "SDN IDS",
        "question": "ما اسم البروتوكول الذي يستخدمه الكنترولر ONOS للتواصل مع السوتشات و التحكم فيها؟",
        "options": ["OpenFlow", "MQTT", "Zigbee"],
        "answer": "OpenFlow",
        "letter": "?"
    },
    "booth_17": {
        "name": "Voxeli.ai",
        "question": "ما الشيء الذي لا يستطيع الذكاء الاصطناعي استنساخه بالكامل؟",
        "options": ["الصورة", "الصوت", "الخيال"],
        "answer": "الخيال",
        "letter": "?"
    },
    "booth_18": {
        "name": "Elixir",
        "question": "ما معنى إلكسير؟",
        "options": ["سُمّ قاتل", "شيء يبعث النشاط أو يمنع الأمل و الحيوية", "معدن نفيس"],
        "answer": "شيء يبعث النشاط أو يمنع الأمل و الحيوية",
        "letter": "?"
    },
    "booth_19": {
        "name": "Flomaster Ahmar",
        "question": "Question coming soon...",
        "options": ["السحر", "لا شيء مما ذكر", "الحقيقة وراء السحر"],
        "answer": "الحقيقة وراء السحر",
        "letter": "?"
    },
    "booth_20": {
        "name": "UniStudy",
        "question": "ما هو القسم الذي يحوّل الطالب من محرد مستفيد الي شخص مساهم يشارك زملاءه بالملخصات و الامتحانات؟",
        "options": ["قسم المجتمع/قسم مرفقاتي", "قسم الجدول الدراسي", "قسم المحاضرات"],
        "answer": "قسم المجتمع/قسم مرفقاتي",
        "letter": "?"
    },
    "booth_21": {
        "name": "Smart Elderly Management System",
        "question": "What is the main goal of our project?",
        "options": ["Control", "Profit", "Care"],
        "answer": "Care",
        "letter": "?"
    },
    "booth_22": {
        "name": "File integrity monitoring system",
        "question": "شو الفنكشن الاساسي الي بقوم فيه مشروعنا؟",
        "options": ["نسخ ملفاتك احتياطياً", "مراقبة ملفاتك الحساسة", "تشفير ملفاتك تلقائياً"],
        "answer": "مراقبة ملفاتك الحساسة",
        "letter": "?"
    },
    "booth_23": {
        "name": "UniSooq",
        "question": "هل هناك حاجة لسوق مخصص للطلاب فقط؟",
        "options": ["لا", "نعم", "-"],
        "answer": "نعم",
        "letter": "?"
    },
    "booth_24": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_25": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_26": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_27": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_28": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_29": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_30": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_31": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_32": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_33": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_34": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_35": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_36": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_37": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_38": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_39": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "booth_40": {
        "name": "Booth name",
        "question": "Question coming soon...",
        "options": ["Option A", "Option B", "Option C"],
        "answer": "Option A",
        "letter": "?"
    },
    "final": {
        "name": "Final Challenge",
        "question": "What is the name of our university club?",
        "options": ["Code Club", "Tech Club", "IT Club"],
        "answer": "IT Club",
        "letter": "R"
    }
}

from quest import update_leaderboard, load_participants_from_sheets, save_participant_to_sheets

participants = load_participants_from_sheets()

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
        
        save_participant_to_sheets(student_id, participants[student_id])
        update_leaderboard(participants)
    
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
        y = 10 + row * 8
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