import PyPDF2

# Common skills (IT + Non-IT)

SKILLS = [
    # IT
    "Python", "Java", "C", "C++", "HTML", "CSS", "JavaScript",
    "React", "Angular", "Node.js", "SQL", "MySQL", "MongoDB",

    # Data
    "Excel", "Power BI", "Tableau", "Machine Learning", "Data Analysis",

    # HR
    "Recruitment", "Payroll", "Employee Relations",

    # Finance
    "Accounting", "Tally", "GST", "Bookkeeping",

    # Marketing
    "SEO", "Google Ads", "Social Media Marketing", "Content Writing",

    # Design
    "Photoshop", "Illustrator", "Figma", "Canva",

    # Mechanical
    "AutoCAD", "SolidWorks", "ANSYS",

    # Civil
    "STAAD Pro", "Revit",

    # Electrical
    "PLC", "SCADA",

    # Healthcare
    "Patient Care", "Nursing", "Medical Coding",

    # Sales
    "Sales", "Customer Service", "CRM",

    # Soft Skills
    "Communication", "Leadership", "Teamwork",
    "Problem Solving", "Time Management"
]


def parse_resume(uploaded_file):
    """Extract text from PDF resume."""

    reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    return resume_text


def extract_skills(resume_text):
    """Extract matching skills from resume."""

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)

    return found_skills


def calculate_resume_score(found_skills):
    """Simple resume score based on skills."""

    count = len(found_skills)

    if count >= 10:
        return 10
    elif count >= 8:
        return 9
    elif count >= 6:
        return 8
    elif count >= 4:
        return 7
    elif count >= 2:
        return 6
    else:
        return 5