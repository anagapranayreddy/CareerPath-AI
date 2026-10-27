import streamlit as st
import re
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🎯",
    layout="wide"
)
CAREERS = {
    "AI/ML Engineer": {
        "interests": ["Artificial Intelligence", "Problem Solving", "Data"],
        "skills": ["Python", "Machine Learning", "Statistics"],
        "subjects": ["Mathematics", "Computer Science"],
        "activities": ["Building Projects", "Research"],
        "description": "Build intelligent systems that learn from data.",
        "roadmap": [
            "Learn Python fundamentals",
            "Practice NumPy and Pandas",
            "Learn basic statistics and linear algebra",
            "Study machine learning algorithms",
            "Build and evaluate ML projects"
        ],
        "project": "Student performance prediction system"
    },
    "Data Scientist": {
        "interests": ["Data", "Problem Solving", "Research"],
        "skills": ["Python", "Statistics", "Data Analysis"],
        "subjects": ["Mathematics", "Statistics", "Computer Science"],
        "activities": ["Research", "Building Projects"],
        "description": "Analyze data to discover patterns and support decisions.",
        "roadmap": [
            "Learn Python",
            "Practice Pandas and NumPy",
            "Learn statistics and probability",
            "Create charts using visualization tools",
            "Build data analysis and prediction projects"
        ],
        "project": "Student marks data analysis dashboard"
    },
    "Data Analyst": {
        "interests": ["Data", "Business", "Problem Solving"],
        "skills": ["SQL", "Excel", "Data Analysis"],
        "subjects": ["Mathematics", "Business"],
        "activities": ["Research", "Building Projects"],
        "description": "Turn data into useful reports and insights.",
        "roadmap": [
            "Learn Excel basics",
            "Learn SQL queries",
            "Practice Python and Pandas",
            "Learn Power BI or Tableau",
            "Build an interactive dashboard"
        ],
        "project": "College student performance dashboard"
    },
    "Software Developer": {
        "interests": ["Programming", "Problem Solving", "Technology"],
        "skills": ["Python", "Java", "Data Structures"],
        "subjects": ["Computer Science", "Mathematics"],
        "activities": ["Building Projects", "Teamwork"],
        "description": "Design, develop, test, and maintain software.",
        "roadmap": [
            "Learn one programming language well",
            "Practice data structures and algorithms",
            "Learn object-oriented programming",
            "Use Git and GitHub",
            "Build and deploy a complete application"
        ],
        "project": "Library management system"
    },
    "Web Developer": {
        "interests": ["Web Design", "Programming", "Technology"],
        "skills": ["HTML", "CSS", "JavaScript"],
        "subjects": ["Computer Science", "Design"],
        "activities": ["Building Projects", "Creative Work"],
        "description": "Create websites and interactive web applications.",
        "roadmap": [
            "Learn HTML",
            "Practice CSS and responsive design",
            "Learn JavaScript",
            "Understand APIs and backend basics",
            "Build and publish a portfolio website"
        ],
        "project": "Personal portfolio or car rental website"
    },
    "Cybersecurity Analyst": {
        "interests": ["Cybersecurity", "Technology", "Problem Solving"],
        "skills": ["Networking", "Linux", "Security Basics"],
        "subjects": ["Computer Science", "Mathematics"],
        "activities": ["Research", "Problem Solving"],
        "description": "Help protect computers, networks, and information.",
        "roadmap": [
            "Learn computer and networking basics",
            "Practice Linux commands",
            "Understand operating systems",
            "Study security concepts and common threats",
            "Practice in legal cybersecurity labs"
        ],
        "project": "Password strength checker"
    },
    "Cloud Engineer": {
        "interests": ["Cloud Computing", "Technology", "Programming"],
        "skills": ["Linux", "Networking", "Python"],
        "subjects": ["Computer Science"],
        "activities": ["Building Projects", "Problem Solving"],
        "description": "Build and manage applications and services in the cloud.",
        "roadmap": [
            "Learn networking fundamentals",
            "Practice Linux and command-line tools",
            "Learn Git and scripting",
            "Study one cloud platform",
            "Deploy a simple application"
        ],
        "project": "Deploy a personal website to the cloud"
    },
    "UI/UX Designer": {
        "interests": ["Design", "Creativity", "Technology"],
        "skills": ["UI Design", "Wireframing", "User Research"],
        "subjects": ["Design", "Psychology"],
        "activities": ["Creative Work", "Teamwork"],
        "description": "Design digital products that are useful and easy to use.",
        "roadmap": [
            "Learn design principles",
            "Study user needs and usability",
            "Practice wireframes",
            "Learn Figma",
            "Create a case study for an app redesign"
        ],
        "project": "Redesign a college app interface"
    },
    "Business Analyst": {
        "interests": ["Business", "Data", "Problem Solving"],
        "skills": ["Communication", "Excel", "Data Analysis"],
        "subjects": ["Business", "Mathematics"],
        "activities": ["Research", "Teamwork"],
        "description": "Understand business needs and help improve processes.",
        "roadmap": [
            "Learn business analysis basics",
            "Improve communication and documentation",
            "Practice Excel and data analysis",
            "Learn process mapping",
            "Create a sample business requirements document"
        ],
        "project": "Analyze and improve a college registration process"
    },
    "Digital Marketing Specialist": {
        "interests": ["Marketing", "Creativity", "Business"],
        "skills": ["Communication", "Content Creation", "Analytics"],
        "subjects": ["Business", "English"],
        "activities": ["Creative Work", "Research"],
        "description": "Help organizations reach audiences through digital channels.",
        "roadmap": [
            "Learn digital marketing fundamentals",
            "Study content and social media strategy",
            "Learn SEO basics",
            "Practice campaign analytics",
            "Create a sample digital campaign"
        ],
        "project": "Create a social media campaign for a student club"
    }
}
def score_category(selected, target):
    if not target:
        return 0
    return len(set(selected) & set(target)) / len(set(target)) * 100
def recommend_careers(interests, skills, subjects, activities):
    results = []
    for name, career in CAREERS.items():
        parts = {
            "Interests": score_category(interests, career["interests"]),
            "Skills": score_category(skills, career["skills"]),
            "Subjects": score_category(subjects, career["subjects"]),
            "Activities": score_category(activities, career["activities"])
        }
        score = (
            parts["Interests"] * 0.40
            + parts["Skills"] * 0.35
            + parts["Subjects"] * 0.15
            + parts["Activities"] * 0.10
        )
        results.append({
            "name": name,
            "score": round(score),
            "parts": parts,
            "career": career
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
def chatbot_reply(question):
    q = question.lower().strip()
    # 1. Greetings
    if any(w in q.split() for w in ["hello", "hi", "hey", "hii", "hai"]):
        return (
            "Hello! Welcome to CareerPath AI. 😊 "
            "I can help you explore careers, skills, learning roadmaps, "
            "projects, and placement preparation. What would you like to know?"
        )
    # 2. Thanks and goodbye
    if any(w in q for w in ["thank you", "thanks", "bye", "goodbye"]):
        if "bye" in q or "goodbye" in q:
            return "Goodbye! Keep learning and building projects. Best wishes for your career!"
        return "You're welcome! Keep exploring your career options. Ask me anytime if you need guidance."
    # 3. About the chatbot
    if "who are you" in q or "what can you do" in q or "help me" in q:
        return (
            "I am the CareerPath AI chatbot. I can guide you about career options, "
            "skills, Python, AI/ML, Data Analysis, Web Development, projects, "
            "learning roadmaps, and placement preparation."
        )
    # 4. Compare careers
    if "compare" in q or "difference" in q:
        return (
            "AI/ML focuses on intelligent models, Data Science focuses on "
            "finding insights from data, and Software Development focuses on "
            "building software applications. Choose based on what you enjoy."
        )
    # 5. Career recommendation
    if (phrase in q for phrase in [
        "best career", "suitable career", "career for me",
        "which career", "recommend a career"
    ]):
        return (
            "Your suitable career depends on your interests, skills, and favorite subjects. "
            "Please complete the Career Assessment page to see your top three career "
            "recommendations and match scores."
        )
    # 6. Beginner-friendly careers
    if "beginner" in q or "easy career" in q:
        return (
            "Beginner-friendly options to explore include Web Developer, Data Analyst, "
            "and Software Developer. Each requires practice. Choose one based on your "
            "interests and start with its basic skills."
        )
    # 7. Learning roadmaps
    if "roadmap" in q or "learn first" in q or "start" in q:
        return (
            "Start with programming fundamentals, practice small problems, "
            "learn the core tools for your chosen field, and build projects. "
            "Use the Learning Roadmap page for career-specific steps."
        )
    # 8. Skills and skill gaps
    if "skill" in q or "gap" in q:
        return (
            "Compare your current skills with the skills needed for your target "
            "career. Learn one missing skill at a time and build a small project "
            "to practice it."
        )
    # 9. Python learning
    if "python" in q:
        return (
            "To learn Python, start with variables, data types, input/output, "
            "conditions, loops, functions, lists, and dictionaries. Then practise "
            "small programs and build a beginner project."
        )
    # 10. AI and Machine Learning
    if "machine learning" in q or "artificial intelligence" in q or "ai/ml" in q or " ai " in f" {q} ":
        return (
            "For AI/ML, begin with Python, NumPy, Pandas, basic statistics, "
            "and then introductory machine learning. Build small projects "
            "before moving to advanced topics."
        )
    # 11. Data Analyst and Data Science
    if "data analyst" in q or "data analysis" in q:
        return (
            "A beginner Data Analyst roadmap is Excel, SQL, data cleaning, "
            "visualization with Power BI or Tableau, and portfolio projects."
        )
    if "data scientist" in q or "data science" in q:
        return (
            "A Data Scientist works with data to discover patterns and build "
            "predictive models. Start with Python, SQL, statistics, data analysis, "
            "visualization, and basic machine learning."
        )
    # 12. Web development
    if "web" in q or "website" in q:
        return (
            "For web development, learn HTML, CSS, JavaScript, responsive "
            "design, and then backend basics. Publish a portfolio project."
        )
    # 13. Software development
    if "software developer" in q or "software development" in q:
        return (
            "A Software Developer builds and maintains applications. Learn one "
            "programming language, practise problem-solving and DSA, understand "
            "Git, and build projects to demonstrate your skills."
        )
    # 14. Cybersecurity
    if "cybersecurity" in q or "cyber security" in q:
        return (
            "Cybersecurity focuses on protecting systems, networks, and data. "
            "Start with computer networks, operating systems, security basics, "
            "and safe practice in authorised learning labs."
        )
    # 15. Cloud computing
    if "cloud" in q:
        return (
            "Cloud Engineers work with online computing, storage, networks, "
            "and cloud services. Learn networking, Linux basics, cloud concepts, "
            "and practise with beginner cloud labs."
        )
    # 16. Projects
    if "project" in q:
        return (
            "Choose a small project that solves a real problem. Beginner ideas "
            "include a portfolio website, expense tracker, student result system, "
            "or data visualisation dashboard. Build, test, and document your work."
        )
    # 17. Placement preparation and interviews
    if "placement" in q or "interview" in q or "resume" in q:
        return (
            "Prepare for placements by practising programming, DSA, aptitude, "
            "communication, and technical interview questions. Build projects, "
            "prepare your resume, and practise explaining your work clearly."
        )
    # 18. Jobs and salary
    if "job" in q or "salary" in q or "package" in q:
        return (
            "Jobs and salaries depend on your skills, location, experience, "
            "projects, and employer. This prototype does not predict hiring "
            "or salary. Check current job listings for realistic requirements."
        )
    # 19. Programming language choice
    if "programming language" in q or "which language" in q:
        return (
            "The best programming language depends on your goal. Python is useful "
            "for AI/ML and data analysis, while JavaScript is important for web "
            "development. Choose one and practise consistently."
        )
    # 20. Study planning
    if "how many hours" in q or "daily study" in q or "study plan" in q:
        return (
            "Start with 30–60 minutes of focused practice each day if your schedule "
            "allows. Divide your time between learning concepts, solving problems, "
            "and building projects. Consistency matters more than long study sessions."
        )
    # 21. Fallback for unrecognised questions
    return (
        "I may not understand that question yet. Try asking me about career choices, "
        "Python, AI/ML, Data Analysis, Web Development, skills, projects, roadmaps, "
        "or placements. You can also use the Career Assessment page for recommendations."
    )
def gemini_chatbot_reply(question):
    if client is None:
        return chatbot_reply(question)

    try:
        response = client.models.generate_content(
           model="gemini-3.5-flash-lite",
            contents=question,
            config={
               "system_instruction": (
    "You are CareerPath AI, a friendly career guidance assistant "
    "for college students. Use simple English and short sentences. "
    "Answer the exact question asked. Keep answers under 200 words. "
    "Use headings and bullet points when useful. "
    "For simple questions, give direct answers. "
    "For roadmaps, give clear numbered steps. "
    "Give practical advice about careers, skills, projects, "
    "internships, resumes, and placements. "
    "Do not repeat the same information unnecessarily. "
    "Do not guarantee jobs or salaries."
),
                "temperature": 0.5,
                "max_output_tokens": 400,
            },
        )

        if response.text:
            print("GEMINI RESPONSE:", response.text)
            return response.text

        return chatbot_reply(question)

    except Exception as e:
        print("Gemini error:", e)
        return chatbot_reply(question)
# Session state
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# Header
st.title("🎯 CareerPath AI")
st.write(
    "Discover career options, identify skill gaps, and create your "
    "personalized learning roadmap."
)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Career Assessment", "Learning Roadmap", "Career Chatbot", "About"]
)
if page == "Career Assessment":
    st.header("🧭 Career Assessment")
    st.write("Select your interests, current skills, subjects, and activities.")
    with st.form("career_form"):
        interests = st.multiselect(
            "What are you interested in?",
            [
                "Artificial Intelligence", "Problem Solving", "Data",
                "Programming", "Technology", "Web Design", "Cybersecurity",
                "Cloud Computing", "Design", "Creativity", "Business",
                "Marketing", "Research"
            ]
        )
        skills = st.multiselect(
            "Which skills do you already have?",
            [
                "Python", "Java", "Machine Learning", "Statistics",
                "Data Analysis", "SQL", "Excel", "Data Structures",
                "HTML", "CSS", "JavaScript", "Networking", "Linux",
                "Security Basics", "UI Design", "Wireframing",
                "User Research", "Communication", "Content Creation",
                "Analytics"
            ]
        )
        subjects = st.multiselect(
            "Which subjects do you enjoy?",
            [
                "Mathematics", "Computer Science", "Statistics",
                "Business", "Design", "Psychology", "English"
            ]
        )
        activities = st.multiselect(
            "Which activities do you prefer?",
            [
                "Building Projects", "Research", "Teamwork",
                "Creative Work", "Problem Solving"
            ]
        )
        submitted = st.form_submit_button("Find My Top Careers")
    if submitted:
        if not (interests or skills or subjects or activities):
            st.warning("Please select at least one option.")
        else:
            st.session_state.recommendations = recommend_careers(
                interests, skills, subjects, activities
            )
            st.session_state.selected_skills = skills
            st.session_state.selected_interests = interests
            st.session_state.selected_subjects = subjects
            st.session_state.selected_activities = activities
    if st.session_state.recommendations:
        st.subheader("🏆 Your Top 3 Career Matches")
        st.caption(
            "Scores show overlap with the built-in career profiles. "
            "They are guidance scores, not probabilities of getting a job."
        )
        for rank, item in enumerate(st.session_state.recommendations[:3], 1):
            st.markdown(f"### {rank}. {item['name']}")
            st.write(item["career"]["description"])
            st.progress(item["score"] / 100)
            st.write(f"**Profile match score: {item['score']}%**")
            st.caption(
                "Interests: " + str(round(item["parts"]["Interests"])) + "% · "
                "Skills: " + str(round(item["parts"]["Skills"])) + "% · "
                "Subjects: " + str(round(item["parts"]["Subjects"])) + "% · "
                "Activities: " + str(round(item["parts"]["Activities"])) + "%"
            )
            st.divider()
elif page == "Learning Roadmap":
    st.header("📚 Personalized Learning Roadmap")
    if st.session_state.recommendations:
        default_career = st.session_state.recommendations[0]["name"]
    else:
        default_career = "AI/ML Engineer"
    career_name = st.selectbox(
        "Choose a career",
        list(CAREERS.keys()),
        index=list(CAREERS.keys()).index(default_career)
    )
    career = CAREERS[career_name]
    st.subheader(career_name)
    st.write(career["description"])
    st.markdown("### Step-by-step roadmap")
    for i, step in enumerate(career["roadmap"], 1):
        st.write(f"{i}. {step}")
    st.markdown("### Beginner project idea")
    st.info(career["project"])
    st.markdown("### Skill-gap analysis")
    current_skills = set(st.session_state.get("selected_skills", []))
    missing = [s for s in career["skills"] if s not in current_skills]
    if missing:
        st.write("Skills to focus on:")
        for skill in missing:
            st.write(f"- {skill}")
    else:
        st.success("Your selected skills cover this profile's listed skills.")
    st.caption(
        "This comparison uses your selected skills and a starter career profile. "
        "It is not a formal assessment of your ability."
    )
elif page == "Career Chatbot":
    st.header("💬 Ask CareerPath AI")
    st.write("Ask about careers, skills, learning plans, or beginner projects.")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input("Example: How do I start learning AI/ML?")
    if prompt:
        
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )
        with st.chat_message("user"):
            st.write(prompt)
        answer = gemini_chatbot_reply(prompt)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
        with st.chat_message("assistant"):
            st.write(answer)
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

elif page == "About":
    st.header("ℹ️ About CareerPath AI")

    st.write(
        "CareerPath AI is an AI-powered career guidance application "
        "that helps students explore career options, identify skill gaps, "
        "and create personalized learning roadmaps."
    )

    st.markdown("""
    ### **Main Features**
    - Career recommendations based on interests, skills, subjects, and activities
    - Career profile match scores
    - Skill-gap analysis
    - Step-by-step learning roadmaps
    - AI-powered career chatbot using Google Gemini

    ### **Technologies Used**
    - Python
    - Streamlit
    - Rule-based recommendation logic
    - Google Gemini API
    - Python Dotenv for API key configuration

    ### **Limitations**
    - Career recommendations depend on predefined career profiles and scoring rules.
    - Match scores are indicative and do not guarantee career success.
    - Gemini responses may occasionally contain inaccurate information.
    - Recommendations provide educational guidance and do not guarantee employment or salary outcomes.
    """)

st.sidebar.divider()
st.sidebar.caption("CareerPath AI | Student Project")
