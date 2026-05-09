import re
import random


def get_response(user_input):
    user_input = user_input.strip().lower()

    # ─────────────────────────────────────────────
    # RESPONSE POOLS
    # ─────────────────────────────────────────────

    greeting_responses = [
        "Hello! How can I assist you today? 😊",
        "Hi there! Need help with your academics?",
        "Hey! What would you like to know?",
        "Good to see you! How can I help?",
        "Welcome to Student Help Desk! Ask me anything.",
    ]

    farewell_responses = [
        "Goodbye! Have a great day! 👋",
        "See you later! Study well!",
        "Take care! Best of luck with your studies!",
        "Bye! Don't forget to revise your notes!",
    ]

    thanks_responses = [
        "You're welcome! 😊",
        "Happy to help!",
        "Anytime! Feel free to ask more questions.",
        "Glad I could assist!",
    ]

    fallback_responses = [
        "Sorry, I didn't understand that. Could you rephrase? 🤔",
        "I'm not sure about that. Try asking differently.",
        "Hmm, I don't have an answer for that yet. Ask about timetable, exams, or assignments!",
        "That's outside my current knowledge. Try asking about academics!",
    ]

    # ─────────────────────────────────────────────
    # RULE-BASED MATCHING  (100 + rules)
    # ─────────────────────────────────────────────

    rules = [
        # ── Greetings ──────────────────────────────────────────────────────
        (r"\b(hi|hello|hey|good morning|good evening|good afternoon|howdy|sup|what'?s up)\b",
         greeting_responses),

        # ── Farewells ──────────────────────────────────────────────────────
        (r"\b(bye|goodbye|see you|exit|quit|take care|later|farewell)\b",
         farewell_responses),

        # ── Thanks ─────────────────────────────────────────────────────────
        (r"\b(thank(s| you)|thx|ty|cheers)\b",
         thanks_responses),

        # ── Timetable / Schedule ───────────────────────────────────────────
        (r"\b(timetable|time.?table)\b",
         ["Your timetable is available on the college portal.",
          "Today's timetable: Math at 9 AM, Science at 11 AM, English at 1 PM.",
          "Please check the noticeboard or portal for your weekly timetable."]),

        (r"\b(schedule|class timing|routine|class schedule)\b",
         ["Your class schedule starts at 9 AM.",
          "Classes run Monday–Saturday, 9 AM to 4 PM.",
          "Check the portal for your personalised schedule."]),

        (r"\b(next (class|lecture))\b",
         ["Your next class is in one hour. Check your timetable!",
          "The upcoming lecture is Mathematics at 11 AM.",
          "Your next session starts at 2 PM."]),

        (r"\b(when (is|are) (the )?class(es)?|upcoming class)\b",
         ["Classes are scheduled as per the timetable on the portal.",
          "Your upcoming class is at 11 AM today.",
          "Check the portal for today's class timing."]),

        (r"\b(first (class|lecture)|morning (class|lecture))\b",
         ["The first class starts at 9 AM.",
          "Morning lectures begin at 9:00 AM sharp.",
          "First period starts at 9 AM every weekday."]),

        (r"\b(last (class|lecture)|evening class)\b",
         ["The last class ends at 4 PM.",
          "Evening lectures conclude by 4:30 PM.",
          "Your final period of the day ends at 4 PM."]),

        # ── Exams (subject-specific BEFORE generic) ────────────────────────
        (r"\b(math(ematics)?.*exam|exam.*math(ematics)?)\b",
         ["Math exam is on 12th March at 10 AM.",
          "Mathematics paper is scheduled for 12th March.",
          "Prepare well! Math exam is on 12th March."]),

        (r"\b(science.*exam|exam.*science|physics.*exam|chemistry.*exam)\b",
         ["Science exam is on 14th March.",
          "Physics paper: 14th March. Chemistry paper: 16th March.",
          "Science exams begin 14th March — revise all chapters!"]),

        (r"\b(english.*exam|exam.*english)\b",
         ["English exam is on 18th March.",
          "Your English paper is scheduled for 18th March.",
          "English exam: 18th March. Focus on grammar and essays."]),

        (r"\b(computer.*exam|exam.*computer)\b",
         ["Computer Science exam is on 20th March.",
          "Your CS paper is on 20th March.",
          "Computer exam: 20th March — revise algorithms and programs."]),

        (r"\b(history.*exam|exam.*history|social.*exam)\b",
         ["History exam is on 22nd March.",
          "Social Studies paper is on 22nd March.",
          "History exam on 22nd March — focus on dates and events."]),

        # ── Generic exams ──────────────────────────────────────────────────
        (r"\b(exam|test|assessment|paper|quiz|viva)\b",
         ["Exams start from 10th March. Check the exam timetable!",
          "The next test is scheduled for Monday.",
          "Exams are coming up — stay focused and study hard! 📚",
          "Check the notice board or portal for detailed exam schedule."]),

        (r"\b(exam (date|schedule|timetable)|when (is|are) (the )?exam)\b",
         ["Exam dates are posted on the college portal.",
          "Exams start 10th March — check the portal for the full schedule.",
          "Please visit the admin office for a printed exam schedule."]),

        (r"\b(exam (result|marks|score|grade))\b",
         ["Results are usually declared within 2 weeks of the exam.",
          "Check the college portal for your exam results.",
          "Results will be published on the notice board and portal."]),

        (r"\b(exam (hall|centre|venue|room))\b",
         ["Exam hall allotment will be posted two days before the exam.",
          "Check the notice board for your exam hall number.",
          "Hall tickets will mention your exam centre details."]),

        (r"\b(hall ticket|admit card)\b",
         ["Hall tickets are available on the college portal one week before exams.",
          "Download your admit card from the student portal.",
          "Contact the admin office if you haven't received your hall ticket."]),

        # ── Assignments / Projects ─────────────────────────────────────────
        (r"\b(assignment|homework|task)\b",
         ["Your next assignment is due on 25th February.",
          "Make sure to submit your homework on time.",
          "Check your subject portal for pending assignments."]),

        (r"\b(project)\b",
         ["Your project submission is due at end of month.",
          "You have one pending group project. Check with your team!",
          "Project guidelines are available on the college portal."]),

        (r"\b(deadline|due date|last date|submit by|submission date)\b",
         ["The submission deadline is this Friday at 5 PM.",
          "Last date for submission is 25th February.",
          "Don't miss the deadline — submit before 5 PM on the due date."]),

        (r"\b(pending (assignment|task|work)|incomplete (assignment|work))\b",
         ["You have 2 pending assignments. Check the portal!",
          "Please complete your pending tasks before the deadline.",
          "Log into the portal to see all pending assignments."]),

        (r"\b(submit|submission|how to submit)\b",
         ["Submit your assignments via the college portal or directly to your teacher.",
          "Submissions can be done online or handed to the class representative.",
          "Upload your work to the assignment section on the portal."]),

        # ── Teachers / Faculty ─────────────────────────────────────────────
        (r"\b(who teaches|teacher for|faculty for|who is (the )?teacher)\b",
         ["Mr. Sharma teaches Mathematics.",
          "Science is taught by Ms. Gupta.",
          "Please check your timetable for faculty details."]),

        (r"\b(teacher|faculty|professor|lecturer|instructor)\b",
         ["You can contact your teacher via the college portal.",
          "Faculty contact details are available on the college website.",
          "Reach out to your class teacher for academic guidance."]),

        (r"\b(teacher.*(email|contact|phone)|contact.*teacher)\b",
         ["Teacher emails are available on the college portal under Faculty Directory.",
          "Contact your teacher at their official college email ID.",
          "Visit the portal → Faculty → Contact for teacher details."]),

        (r"\b(hod|head of department)\b",
         ["The HOD of Computer Science is Dr. Mehta.",
          "Please visit the department office to meet the HOD.",
          "HOD contact is available on the department's page on the portal."]),

        (r"\b(principal|director)\b",
         ["The principal's office is on the 2nd floor, Room 201.",
          "You can meet the principal during office hours: 10 AM – 12 PM.",
          "Contact the principal's office at principal@college.com."]),

        # ── Attendance ─────────────────────────────────────────────────────
        (r"\b(attendance|present|absent)\b",
         ["Your attendance is available on the college portal.",
          "Maintain at least 75% attendance to be eligible for exams.",
          "Check the portal for your subject-wise attendance."]),

        (r"\b(attendance (percentage|percent|%)|how much attendance)\b",
         ["You need 75% attendance to sit for exams.",
          "Check your current attendance on the student portal.",
          "Attendance below 75% may result in exam detainment."]),

        (r"\b(low attendance|shortage (of )?attendance|attendance shortage)\b",
         ["Low attendance may result in exam ban. Please apply for condonation.",
          "Contact your class teacher if you have an attendance shortage.",
          "Condonation for attendance is granted only in medical emergencies."]),

        (r"\b(leave|leave application|apply.*leave)\b",
         ["Submit leave applications to your class teacher in advance.",
          "Leave forms are available at the admin office.",
          "Medical leave requires a doctor's certificate."]),

        # ── Fees ──────────────────────────────────────────────────────────
        (r"\b(fee|fees|tuition|payment)\b",
         ["Fee details are available on the college portal.",
          "You can pay fees online via the student portal.",
          "Fee payment deadline is the 10th of every month."]),

        (r"\b(fee (due|pending|amount)|how much.*fee)\b",
         ["Log into the portal to view your pending fee amount.",
          "Fee receipts and dues are visible under the Finance section.",
          "Contact the accounts office for fee-related queries."]),

        (r"\b(scholarship)\b",
         ["Scholarship forms are available at the admin office.",
          "Apply for scholarships before the last date on the notice board.",
          "Check government scholarship portals for eligibility."]),

        (r"\b(refund|fee refund)\b",
         ["Refund requests should be submitted to the accounts office.",
          "Fee refund policy details are available on the portal.",
          "Refunds are processed within 30 working days."]),

        # ── Library ────────────────────────────────────────────────────────
        (r"\b(library|books?|borrow|return)\b",
         ["The library is open from 8 AM to 6 PM on weekdays.",
          "You can borrow up to 3 books for 14 days.",
          "Return books on time to avoid late fees."]),

        (r"\b(library (timing|hours|open|close))\b",
         ["Library hours: Monday–Friday 8 AM to 6 PM, Saturday 9 AM to 1 PM.",
          "The library is closed on Sundays and public holidays.",
          "Library opens at 8 AM — reach early for a good seat!"]),

        (r"\b(e.?book|digital (book|library)|online (book|resource))\b",
         ["E-books are accessible via the college portal under Digital Library.",
          "Access e-resources using your student login credentials.",
          "NPTEL and other resources are linked in the portal."]),

        # ── Hostel ────────────────────────────────────────────────────────
        (r"\b(hostel|dorm|dormitory|accommodation)\b",
         ["Hostel admission forms are available at the admin office.",
          "Hostel fees must be paid before the semester starts.",
          "Contact the hostel warden at hostel@college.com."]),

        (r"\b(hostel (mess|food|canteen|meal))\b",
         ["Hostel mess serves breakfast at 7:30 AM, lunch at 12:30 PM, dinner at 7:30 PM.",
          "Monthly mess fees are included in the hostel charges.",
          "Raise any mess-related complaints with the hostel warden."]),

        # ── Transport ─────────────────────────────────────────────────────
        (r"\b(bus|transport|vehicle|college bus)\b",
         ["College bus routes are posted on the notice board.",
          "Bus pass applications are available at the transport office.",
          "Contact the transport office at transport@college.com."]),

        # ── Results / Marks ───────────────────────────────────────────────
        (r"\b(result|marks|score|grade|report card|marksheet)\b",
         ["Results are published on the college portal after evaluation.",
          "Check your marks on the student portal under Results section.",
          "Marksheets can be collected from the exam section."]),

        (r"\b(pass|fail|passing (marks|percentage))\b",
         ["The passing marks are 40% in each subject.",
          "You need at least 40% to pass. Good luck! 💪",
          "Passing criteria: 40% in theory and 50% in practicals."]),

        (r"\b(rank|topper|merit)\b",
         ["Merit list is posted on the notice board after results.",
          "Top rankers are announced at the annual prize distribution.",
          "Check the portal for class rank after exam results."]),

        (r"\b(revaluation|rechecking|re.?evaluation)\b",
         ["Apply for revaluation within 7 days of result declaration.",
          "Revaluation forms are available at the exam section.",
          "Revaluation fee is ₹500 per subject."]),

        # ── Syllabus / Notes ──────────────────────────────────────────────
        (r"\b(syllabus|curriculum|topics?)\b",
         ["Syllabus is available on the college portal under Academics.",
          "Download your semester syllabus from the portal.",
          "Ask your subject teacher for the detailed syllabus."]),

        (r"\b(notes?|study material|handout|pdf)\b",
         ["Study materials and notes are uploaded on the portal by teachers.",
          "Check the subject page on the portal for uploaded notes.",
          "Ask your class representative for shared study materials."]),

        (r"\b(important (question|topic)|guess paper)\b",
         ["Important questions are shared by teachers before exams — attend classes!",
          "Focus on previous year papers for important topics.",
          "Check the portal for teacher-uploaded important questions."]),

        # ── Internship / Placement ────────────────────────────────────────
        (r"\b(internship)\b",
         ["Internship opportunities are posted on the placement portal.",
          "Contact the Training & Placement cell for internship guidance.",
          "Apply for internships through the college portal or T&P office."]),

        (r"\b(placement|campus (drive|interview|recruitment))\b",
         ["Campus placement drives are announced on the placement portal.",
          "Register on the placement portal to be notified of drives.",
          "Contact T&P office at placement@college.com."]),

        (r"\b(resume|cv|curriculum vitae)\b",
         ["Get your resume reviewed at the T&P office.",
          "Resume-building workshops are held every semester — watch the notice board.",
          "Keep your resume updated before placement season begins."]),

        # ── College Events / Activities ───────────────────────────────────
        (r"\b(event|fest|festival|cultural|annual (day|function))\b",
         ["College fest details are posted on the notice board and portal.",
          "Annual day is usually held in February — stay tuned for announcements.",
          "Register for college events through the student activities portal."]),

        (r"\b(workshop|seminar|webinar|conference)\b",
         ["Upcoming workshops are listed on the college portal.",
          "Register for seminars through the Events section on the portal.",
          "Attend workshops to earn extra credit — check the portal!"]),

        (r"\b(club|society|extracurricular)\b",
         ["Join clubs via the student activities portal.",
          "Cultural, technical, and sports clubs are open for enrollment.",
          "Club meetings are held on Fridays after 4 PM."]),

        (r"\b(sport|cricket|football|basketball|kabaddi)\b",
         ["Sports trials are held in the first week of the semester.",
          "Join the sports club via the student activities portal.",
          "Practice sessions are from 5 PM to 7 PM on the college ground."]),

        # ── Admin / Office ────────────────────────────────────────────────
        (r"\b(office|admin(istration)?|reception)\b",
         ["The admin office is open from 9 AM to 5 PM on weekdays.",
          "Visit the admin office on the ground floor for official queries.",
          "Admin contact: admin@college.com | 9876543210"]),

        (r"\b(contact (info|number|us|details)|phone number|helpline)\b",
         ["Admin: 9876543210 | Email: support@college.com",
          "Reach us at admin@college.com for any queries.",
          "Helpdesk number: 9876543210 — available 9 AM to 5 PM."]),

        (r"\b(certificate|bonafide|character certificate)\b",
         ["Bonafide certificates are issued from the admin office within 2 working days.",
          "Submit a written application at the admin office for certificates.",
          "Character certificates are issued at the end of the academic year."]),

        (r"\b(id card|identity card|student id)\b",
         ["Lost ID cards can be reissued from the admin office for ₹100.",
          "Carry your student ID at all times on campus.",
          "New ID cards are issued in the first week of every academic year."]),

        (r"\b(college (timing|hours|open|close)|when (does|is) college (open|close))\b",
         ["College is open Monday–Saturday, 8:30 AM to 5:30 PM.",
          "College remains closed on Sundays and public holidays.",
          "Administrative office hours: 9 AM to 5 PM."]),

        # ── Portal / Online ───────────────────────────────────────────────
        (r"\b(portal|online portal|student portal|login)\b",
         ["Access the student portal at portal.college.com.",
          "Use your enrollment number and date of birth to log in first time.",
          "For portal issues, contact IT support at it@college.com."]),

        (r"\b(password|forgot password|reset password)\b",
         ["Use the 'Forgot Password' option on the portal login page.",
          "Contact IT support at it@college.com to reset your password.",
          "Password reset link is sent to your registered email."]),

        (r"\b(app|mobile app|college app)\b",
         ["The college mobile app is available on Play Store and App Store.",
          "Search 'College Name' on Play Store to download the app.",
          "Use the app for timetable, results, and announcements."]),

        # ── Health / Medical ──────────────────────────────────────────────
        (r"\b(medical|health|sick|doctor|nurse|clinic|dispensary)\b",
         ["The college medical centre is open from 9 AM to 4 PM.",
          "Visit the campus clinic on the ground floor for medical assistance.",
          "In emergencies, call the medical helpline: 9876500000."]),

        # ── Canteen / Food ────────────────────────────────────────────────
        (r"\b(canteen|cafeteria|food|lunch|breakfast|snack)\b",
         ["The college canteen is open from 8 AM to 6 PM.",
          "Canteen menu is available at the counter.",
          "Meal timings: Breakfast 8–9 AM, Lunch 12–2 PM, Snacks 4–5 PM."]),

        # ── WiFi / Internet ───────────────────────────────────────────────
        (r"\b(wifi|wi.fi|internet|network)\b",
         ["Connect to 'CollegeWiFi' using your student ID and password.",
          "WiFi is available in classrooms, library, and hostel.",
          "For WiFi issues, contact IT support at it@college.com."]),

        # ── Exam Preparation ──────────────────────────────────────────────
        (r"\b(how to (study|prepare|revise)|study tips?|preparation tips?)\b",
         ["Make a timetable, revise daily, and solve previous papers! 📚",
          "Break your syllabus into small chunks and revise one section daily.",
          "Focus on weak topics first, then revise strong ones. All the best! 💪"]),

        (r"\b(previous (year|paper)|past paper|old paper|sample paper)\b",
         ["Previous year papers are available in the library and on the portal.",
          "Practicing old papers is one of the best exam strategies!",
          "Download sample papers from the Exam section on the portal."]),

        # ── Help / Bot info ───────────────────────────────────────────────
        (r"\b(help|support|assist|guide)\b",
         ["I can help with timetable, exams, assignments, attendance, fees, and more!",
          "Ask me about your academic schedule, deadlines, or college information.",
          "I'm here to assist you! Type your question anytime. 😊"]),

        (r"\b(what can you do|your features|your services|capabilities)\b",
         ["I can answer questions about: timetable, exams, assignments, attendance, fees, library, hostel, events, and more!",
          "I help students with academic queries, schedules, and college information.",
          "Ask me anything about college life! 🎓"]),

        (r"\b(who (are you|made you|created you)|what are you)\b",
         ["I'm the Student Help Desk Chatbot — here to assist you 24/7! 🤖",
          "I'm a rule-based chatbot built to answer student queries.",
          "I'm your virtual academic assistant. Ask me anything!"]),

        # ── Motivational ──────────────────────────────────────────────────
        (r"\b(motivat|stressed?|anxious|worried|nervous|scared.*exam)\b",
         ["You've got this! 💪 Believe in yourself and keep studying.",
          "Stay calm, prepare well, and trust the process. You'll do great!",
          "Take a short break, breathe, then get back to studying. You can do it! 🌟"]),

        (r"\b(bored|boring|nothing to do)\b",
         ["Try exploring college clubs or working on a personal project! 🚀",
          "Use free time to revise your notes or read ahead!",
          "Boredom is a great time to study something new. Check the e-library!"]),
    ]

    # Match rules in order
    for pattern, responses in rules:
        if re.search(pattern, user_input, re.I):
            return random.choice(responses)

    return random.choice(fallback_responses)
