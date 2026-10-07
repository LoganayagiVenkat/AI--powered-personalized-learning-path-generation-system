import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_border(cell, **kwargs):
    """
    Set cell borders
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='000000')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, attr in [("val", "w:val"), ("color", "w:color"), ("sz", "w:sz"), ("space", "w:space")]:
                if key in edge_data:
                    element.set(qn(attr), str(edge_data[key]))

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def style_paragraph(p, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0), align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    for run in p.runs:
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

def add_styled_paragraph(doc, text, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0), align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    return p

def add_heading_1(doc, text):
    return add_styled_paragraph(doc, text, size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=6)

def add_heading_2(doc, text):
    return add_styled_paragraph(doc, text, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)

def add_heading_3(doc, text):
    return add_styled_paragraph(doc, text, size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=4)

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F4F6F9")
    set_cell_border(cell, 
                    top={"sz": 4, "val": "single", "color": "D0D5DD"},
                    bottom={"sz": 4, "val": "single", "color": "D0D5DD"},
                    left={"sz": 4, "val": "single", "color": "D0D5DD"},
                    right={"sz": 4, "val": "single", "color": "D0D5DD"})
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(20, 30, 45)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout_box(doc, title, desc):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, "F9FAFB")
    set_cell_border(cell, 
                    top={"sz": 6, "val": "dashed", "color": "6B7280"},
                    bottom={"sz": 6, "val": "dashed", "color": "6B7280"},
                    left={"sz": 6, "val": "dashed", "color": "6B7280"},
                    right={"sz": 6, "val": "dashed", "color": "6B7280"})
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"[{title}]\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r2 = p.add_run(f"{desc}\n(Screenshot placeholder)")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(90, 90, 90)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def format_table(table, col_widths, headers, data, header_bg="EAECEF"):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        hdr_cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(hdr_cells[i], header_bg)
        set_cell_border(hdr_cells[i],
                        top={"sz": 6, "val": "single", "color": "000000"},
                        bottom={"sz": 6, "val": "single", "color": "000000"},
                        left={"sz": 6, "val": "single", "color": "000000"},
                        right={"sz": 6, "val": "single", "color": "000000"})
        p = hdr_cells[i].paragraphs[0]
        style_paragraph(p, size_pt=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)

    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            row_cells[col_idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_border(row_cells[col_idx],
                            top={"sz": 4, "val": "single", "color": "000000"},
                            bottom={"sz": 4, "val": "single", "color": "000000"},
                            left={"sz": 4, "val": "single", "color": "000000"},
                            right={"sz": 4, "val": "single", "color": "000000"})
            p = row_cells[col_idx].paragraphs[0]
            # align left for second column if it's title
            align = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 1 and len(headers) == 3 else WD_ALIGN_PARAGRAPH.CENTER
            style_paragraph(p, size_pt=10.5, align=align, space_before=3, space_after=3)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_docx_report():
    doc = Document()
    
    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ================= PAGE 1: TITLE PAGE =================
    add_styled_paragraph(doc, "", space_before=20)
    add_styled_paragraph(doc, "AI-Powered Personalized Learning Path Generation System", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=14)
    add_styled_paragraph(doc, "23CS55C - ARTIFICIAL INTELLIGENCE", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8)
    add_styled_paragraph(doc, "MICRO PROJECT REPORT", size_pt=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=40)
    
    add_styled_paragraph(doc, "Submitted by", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=12)
    add_styled_paragraph(doc, "JEYAKIRTHIKA V  -  2312015\nSTUDENT NAME 2  -  23120XX\nSTUDENT NAME 3  -  23120XX", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=60, line_spacing=1.3)
    
    add_styled_paragraph(doc, "Course Instructor", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=40, space_after=20)

    # Marks rubric table (Cover Page: 40 Marks)
    t_cover = doc.add_table(rows=2, cols=5)
    headers_cover = [
        "Innovation and\nProblem statement\n(10 Marks)",
        "Implementation &\nResults\n(10 Marks)",
        "Presentation and\nDocumentation\n(10 Marks)",
        "Viva\n(10 Marks)",
        "Total\n(40 Marks)"
    ]
    data_cover = [["", "", "", "", ""]]
    format_table(t_cover, [1.3, 1.3, 1.4, 1.1, 1.2], headers_cover, data_cover)
    t_cover.rows[1].height = Inches(0.5)

    doc.add_page_break()

    # ================= PAGE 2: TABLE OF CONTENTS =================
    add_styled_paragraph(doc, "TABLE OF CONTENTS", size_pt=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=20)
    
    t_toc = doc.add_table(rows=8, cols=3)
    headers_toc = ["CH NO", "TITLE", "PAGE NO"]
    data_toc = [
        ["1", "INTRODUCTION", "3"],
        ["2", "PROBLEM STATEMENT", "4"],
        ["3", "MODULE DESCRIPTION", "5"],
        ["4", "ARCHITECTURE DIAGRAM", "7"],
        ["5", "CODING & IMPLEMENTATION", "10"],
        ["6", "OUTPUT SCREENSHOTS", "20"],
        ["7", "CONCLUSION", "22"]
    ]
    format_table(t_toc, [1.0, 4.3, 1.2], headers_toc, data_toc)

    doc.add_page_break()

    # ================= PAGE 3: CHAPTER 1 INTRODUCTION =================
    add_heading_1(doc, "CHAPTER 1")
    add_heading_2(doc, "INTRODUCTION")
    
    add_styled_paragraph(doc, "In today's fast-paced digital and technological environment, traditional educational paradigms have long relied on one-size-fits-all curricula that fail to accommodate individual student proficiencies, diverse learning speeds, and evolving industry standards. With the exponential emergence of technical domains such as Artificial Intelligence, Data Science, Machine Learning, and Cloud-Native Software Engineering, learners frequently encounter fragmented materials, redundant introductory content, and unclear prerequisite dependencies. This capstone micro project addresses this critical challenge by engineering an AI-Powered Personalized Learning Path Generation System that dynamically synthesizes custom, mastery-based academic roadmaps tailored to each student's career aspirations and foundational knowledge.")
    
    add_styled_paragraph(doc, "The Gap:", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6)
    add_styled_paragraph(doc, "Conventional Learning Management Systems (LMS) and online course catalogs deliver rigid, linear syllabi that do not adapt to individual learning needs. Students are forced to traverse predefined modules regardless of whether they have already mastered foundational concepts or lack crucial prerequisites. Furthermore, these platforms lack automated diagnostic mechanisms to identify precise technical skill gaps against target career roles (such as AI/ML Engineer, Data Scientist, or Full-Stack Developer). When students struggle or fail assessments, standard systems offer no automated remedial feedback loop, leading to cognitive fatigue, knowledge voids, and high dropout rates.")
    
    add_styled_paragraph(doc, "The Goal :", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6)
    add_styled_paragraph(doc, "The primary objective of this project is to develop an end-to-end, intelligent learning ecosystem that leverages Natural Language Processing (NLP), Directed Acyclic Graph (DAG) topological sequencing, machine learning-driven risk prediction, and automated adaptive feedback. The system evaluates a learner's baseline proficiency through diagnostic benchmarking, computes numerical skill gaps against career benchmark vectors, and synthesizes an optimal prerequisite-respecting curriculum via Kahn's Topological Sort algorithm. In addition, the platform features dynamic quiz-driven remediation, context-aware AI tutoring, and hands-free voice interaction to deliver an adaptive, interactive, and personalized educational journey.")

    doc.add_page_break()

    # ================= PAGE 4: CHAPTER 2 PROBLEM STATEMENT =================
    add_heading_1(doc, "CHAPTER 2")
    add_heading_2(doc, "PROBLEM STATEMENT")

    add_styled_paragraph(doc, "Online education and technical upskilling platforms have become primary avenues for higher education and workforce preparation. However, students and early-career engineers frequently encounter substantial friction in navigating dense, unstructured technical curricula. The core problem lies in the absence of adaptive intelligence in traditional curricula design: learners are treated as homogenous cohorts, receiving identical course paths regardless of varying competencies, background knowledge, and specific target career outcomes.")

    add_styled_paragraph(doc, "This deficiency manifests in several critical areas:", size_pt=12, bold=True, space_before=8, space_after=4)

    p1 = doc.add_paragraph(style='List Bullet')
    p1.paragraph_format.space_after = Pt(4)
    r = p1.add_run("Rigid and Linear Progression Bottlenecks: ")
    r.bold = True
    r.font.name = "Times New Roman"
    p1.add_run("Standard e-learning systems sequence topics chronologically rather than dependency-wise. Students often encounter advanced algorithmic or mathematical concepts without first mastering essential prerequisites (e.g., attempting Deep Neural Networks without understanding Linear Algebra or Gradient Descent), leading to severe cognitive overload.").font.name = "Times New Roman"

    p2 = doc.add_paragraph(style='List Bullet')
    p2.paragraph_format.space_after = Pt(4)
    r = p2.add_run("Absence of Granular Skill-Gap Quantification: ")
    r.bold = True
    r.font.name = "Times New Roman"
    p2.add_run("Existing platforms lack automated diagnostic tools to objectively measure a student's current proficiency vector against real-world target career requirements. Learners cannot pinpoint exactly which skills are critical, moderate, or already met.").font.name = "Times New Roman"

    p3 = doc.add_paragraph(style='List Bullet')
    p3.paragraph_format.space_after = Pt(4)
    r = p3.add_run("Lack of Dynamic Remediation and Feedback Loops: ")
    r.bold = True
    r.font.name = "Times New Roman"
    p3.add_run("In traditional LMS architectures, failing a module test merely yields a numerical score without re-engineering the curriculum. There is no automated mechanism to dynamically insert remedial exercises, reinforce prerequisite concepts, or adjust pacing in real time.").font.name = "Times New Roman"

    p4 = doc.add_paragraph(style='List Bullet')
    p4.paragraph_format.space_after = Pt(6)
    r = p4.add_run("Inflexible Static Pacing and Missing Tutoring Support: ")
    r.bold = True
    r.font.name = "Times New Roman"
    p4.add_run("Students learn at varying velocities, yet static curricula cannot dynamically predict completion timelines or identify high-risk modules. Moreover, without interactive tutoring, students facing conceptual bottlenecks are left without immediate guidance.").font.name = "Times New Roman"

    add_styled_paragraph(doc, "The consequences are profound: suboptimal learning efficiency, knowledge retention deficits, frustration, and demotivation. In an era where data-driven adaptation is paramount, education must shift from static delivery to dynamic personalization. This project bridges this divide by developing an AI-driven educational engineering platform that dynamically analyzes student skill gaps, constructs dependency-validated DAG roadmaps, and provides automated remedial adaptation and interactive tutoring.", space_before=10)

    doc.add_page_break()

    # ================= PAGE 5: CHAPTER 3 MODULE DESCRIPTION =================
    add_heading_1(doc, "CHAPTER 3")
    add_heading_2(doc, "MODULE DESCRIPTION")

    add_styled_paragraph(doc, "The AI-Powered Personalized Learning Path Generation System is structured into six key modules, each handling a specific dimension of the educational pipeline. These modules work collaboratively to transform raw learner diagnostic profiles into an adaptive, dependency-validated learning journey:")

    add_styled_paragraph(doc, "The Student Profiling and Diagnostic Assessment Module captures user career objectives, baseline self-ratings, and diagnostic test responses to construct a multi-dimensional student competency profile.")

    add_styled_paragraph(doc, "The NLP and Curriculum Extraction Module leverages TF-IDF token vectorization and cosine similarity to extract semantic keywords from curriculum topic catalogs and align them mathematically with student goals.")

    add_styled_paragraph(doc, "The Skill-Gap Analysis and Vector Distance Engine compares student proficiency vectors against career benchmark requirements, computing weighted distance scores to identify Critical, Moderate, and Met skill levels.")

    add_styled_paragraph(doc, "The DAG-Based Learning Path Generation and Remediation Module formulates curriculum topics as a Directed Acyclic Graph (DAG) and executes Kahn's Topological Sort algorithm to guarantee that all prerequisite dependencies are satisfied in optimal pedagogical order. It also includes dynamic quiz remediation to inject refresher content upon assessment failure.")

    add_styled_paragraph(doc, "The Interactive Assessment and Mastery Tracking Module delivers timed module quizzes, tracks concept retention, awards continuous learning streaks, and logs completion analytics to keep learners engaged.")

    add_styled_paragraph(doc, "Finally, the Intelligent Tutoring Chatbot and Voice Assistant Module features an NLP-driven conversational agent with intent classification alongside Google Speech Recognition and gTTS audio synthesis for natural, hands-free voice interaction.")

    add_heading_3(doc, "Architectural Foundation:")
    add_styled_paragraph(doc, "The AI-Powered Personalized Learning Path Generation System is built upon a high-performance, modular full-stack architecture. The frontend is engineered with React 18 and Vite, utilizing Lucide React icons, Recharts for radar and progress analytics, and the HTML5 Web Speech API. The backend is powered by Python Flask structured with modular blueprints. Data persistence is managed via SQLAlchemy ORM supporting MySQL with an automated zero-configuration SQLite fallback (learning_path.db). Core AI and machine learning tasks utilize scikit-learn (TF-IDF vectorizer, Cosine Similarity, K-Means clustering, Random Forest performance prediction), graph algorithms via Python collections, and audio pipelines powered by SpeechRecognition and gTTS.")

    # Functional modules
    add_heading_3(doc, "Functional Modules:")
    add_styled_paragraph(doc, "The system comprises several interconnected functional modules:")
    
    fm_items = [
        ("Student Profiling and Diagnostic Assessment Module: ", "Collects student career goals (e.g., Data Scientist, AI/ML Engineer, Full Stack Developer), processes baseline diagnostic tests, and stores verified proficiency ratings across technical domains."),
        ("NLP and Curriculum Extraction Module: ", "Tokenizes and cleans course syllabi, removes stop words, generates unigram and bigram TF-IDF feature matrices, and computes semantic alignment with student query profiles."),
        ("Skill-Gap Analysis Module: ", "Computes weighted Euclidean-style gap distances against industry-benchmarked career skill sets, classifying each skill into Critical, Moderate, or Met status, and suggests corresponding courses."),
        ("DAG Topological Sequencing Module: ", "Constructs prerequisite dependency adjacency lists and computes in-degrees for each topic. Executes Kahn's algorithm to resolve topic ordering, prioritizing foundational concepts and addressing weak areas first."),
        ("Adaptive Remediation Engine: ", "Dynamically intercepts quiz evaluation results; if a student scores below 60%, the system flags the topic for remedial review and attaches supplementary exercises. Scores of 85% or higher trigger mastery acceleration."),
        ("Intelligent Tutoring Chatbot & Voice Assistant: ", "Implements multi-intent classification (why_recommended, next_topic, concept_explanation, skill_gaps, career_guidance), delivering contextual academic tutoring via chat and voice.")
    ]
    for b_title, b_desc in fm_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(b_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(b_desc).font.name = "Times New Roman"

    add_heading_3(doc, "Operational Flow:")
    add_styled_paragraph(doc, "The operational flow commences when a student registers and selects a target career goal. The student undertakes an initial diagnostic benchmark assessment that establishes their baseline proficiency. The NLP engine calculates TF-IDF representations of all topics and matches them against the student's profile. The DAG Topological Sort sequences the curriculum based on prerequisite dependencies, while the Random Forest predictor projects topic difficulty and pass probabilities. As the student engages with learning content and completes mastery quizzes, the system dynamically updates progress, recalibrating the path and providing remedial assistance when needed, supported continuously by the AI tutoring chatbot and voice assistant.")

    doc.add_page_break()

    # ================= PAGE 7: CHAPTER 4 ARCHITECTURAL DIAGRAM =================
    add_heading_1(doc, "CHAPTER 4")
    add_heading_2(doc, "ARCHITECTURAL DIAGRAM")

    add_heading_3(doc, "4.1 Overview:")
    add_styled_paragraph(doc, "The architecture of the AI-Powered Personalized Learning Path Generation System follows a modular, layered design that separates data processing, AI reasoning, analytics computation, and user interaction. This ensures scalability, maintainability, and ease of updates. The system is built entirely with open-source technologies and runs locally, eliminating dependency on cloud services for core functionality.")

    add_heading_3(doc, "4.2 Architectural Diagram :")
    arch_diagram_text = (
        "+-------------------------------------------------------------------------+\n"
        "|                          User Interface Layer                           |\n"
        "|      [ React 18 SPA ]  [ Recharts Analytics ]  [ Web Speech Voice UI ]  |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                           Application Layer                             |\n"
        "|      [ Flask REST API ] -> Blueprints (Auth, Path, Quiz, Chatbot, etc.) |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                           Processing Layer                              |\n"
        "|  +--------------------+  +--------------------+  +-------------------+  |\n"
        "|  |   DAG Topological  |  |  TF-IDF & Cosine   |  | Skill-Gap Vector  |  |\n"
        "|  |     Sequencing     |  |   NLP Matcher      |  |     Analyzer      |  |\n"
        "|  +--------------------+  +--------------------+  +-------------------+  |\n"
        "|  +--------------------+  +--------------------+  +-------------------+  |\n"
        "|  | Adaptive Remedial  |  | Chatbot Intent     |  | Random Forest ML  |  |\n"
        "|  |   Quiz Engine      |  | Classifier & Audio |  | Predictor Engine  |  |\n"
        "|  +--------------------+  +--------------------+  +-------------------+  |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                              Data Layer                                 |\n"
        "|    [ Users & Profiles ]  [ Career & Skills ]  [ Topics & DAG Prereqs ]   |\n"
        "|               [ SQLite / MySQL with SQLAlchemy ORM ]                    |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     |\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                         Infrastructure Layer                            |\n"
        "|    [ Python 3.x Runtime ]  [ scikit-learn / NumPy ]  [ Speech & gTTS ]  |\n"
        "+-------------------------------------------------------------------------+"
    )
    add_code_block(doc, arch_diagram_text)

    add_heading_3(doc, "4.3 Layer Descriptions")
    
    layers = [
        ("4.3.1 User Interface Layer", "React 18 web interface built with Vite", "Provides interactive dashboard, dynamic DAG roadmap visualizations, skill-gap radar charts, quiz evaluation modals, and floating voice assistant", "React.js, Tailwind/Vanilla CSS, Lucide Icons, Recharts", "Enables students to interact with personalized curricula and track performance effortlessly"),
        ("4.3.2 Application Layer", "Flask REST API routing layer", "Coordinates user requests, executes session validation, routes data between client and AI services", "Python Flask, Flask-CORS, Modular Blueprints", "Serves as the central API gateway and controller for educational operations"),
        ("4.3.3 Processing Layer", "AI Reasoning, Graph Sequencing, and Adaptive Engine", "DAG Sequencing resolves curriculum dependencies via Kahn's algorithm; NLP Engine evaluates semantic relevance via TF-IDF token matrices; Skill Gap Engine computes distance from target career profiles", "scikit-learn, NumPy, NLTK, Python Graph Collections", "Performs core AI reasoning and dynamic curriculum synthesis"),
        ("4.3.4 Data Layer", "Relational Database Models & Store", "Stores user records, career goals, skills, topics, prerequisite links, and generated paths", "SQLAlchemy ORM, SQLite (learning_path.db), MySQL", "Provides persistent, relational storage for student academic history"),
        ("4.3.5 Infrastructure Layer", "AI Runtimes, Audio Models, and Math Engines", "Executes vector mathematics, speech recognition, and audio synthesis", "Python 3.x, SpeechRecognition, Google Text-to-Speech (gTTS)", "Supplies foundational computational and speech processing capabilities")
    ]
    for l_title, comp, func, tech, purp in layers:
        add_styled_paragraph(doc, l_title, size_pt=12, bold=True, space_before=8, space_after=3)
        for bullet_label, bullet_val in [("Component: ", comp), ("Functionality: ", func), ("Technology: ", tech), ("Purpose: ", purp)]:
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(bullet_label)
            r.bold = True
            r.font.name = "Times New Roman"
            p.add_run(bullet_val).font.name = "Times New Roman"

    add_heading_3(doc, "4.4 Data Flow")
    df_steps = [
        "User logs in and selects target career goal via React user interface.",
        "Application layer requests diagnostic assessment and routes baseline scores to processing layer.",
        "TF-IDF & Cosine Similarity vectorize topic catalog and align them with the student query.",
        "Kahn's Topological Sort orders topics strictly according to prerequisite constraints.",
        "Random Forest predictor computes pacing advice and pass probability for each module.",
        "Mastery quiz submissions dynamically trigger remediation or fast-tracking updates.",
        "Interactive progress, charts, and voice explanations are rendered in real time."
    ]
    for idx, step_txt in enumerate(df_steps, 1):
        p = doc.add_paragraph(style='List Number')
        p.paragraph_format.space_after = Pt(3)
        p.add_run(step_txt).font.name = "Times New Roman"

    add_heading_3(doc, "4.5 Key Design Decisions")
    decisions = [
        ("DAG-Based Dependency Resolution: ", "Modeling course topics as a Directed Acyclic Graph prevents circular learning traps and guarantees foundational topics are completed before advanced material."),
        ("Local & Deterministic Algorithm Execution: ", "Core sequencing runs via deterministic graph theory and local scikit-learn models, guaranteeing zero API latency and complete student privacy."),
        ("Dual Database Portability: ", "Implements zero-configuration SQLite fallback if MySQL is unreachable, making testing and deployment instantaneous across environments."),
        ("Explainable AI Recommendations: ", "Every roadmap topic provides explicit, student-readable justification strings explaining prerequisite fulfillment and career alignment."),
        ("Multimodal Learning Modality: ", "Unifies visual charts, structured interactive text, conversational chatbot assistance, and speech audio synthesis.")
    ]
    for d_title, d_desc in decisions:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(d_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(d_desc).font.name = "Times New Roman"

    doc.add_page_break()

    # ================= PAGE 10: CHAPTER 5 CODING AND IMPLEMENTATION =================
    add_heading_1(doc, "CHAPTER 5")
    add_heading_2(doc, "CODING AND IMPLEMENTATION")

    add_heading_3(doc, "5.1 Introduction")
    add_styled_paragraph(doc, "This chapter details the coding and implementation of the AI-Powered Personalized Learning Path Generation System. The system is built using Python with Flask, scikit-learn, and SQLAlchemy on the backend, complemented by a modern React.js frontend. The codebase follows clean software engineering principles, maintaining strict separation between data persistence, AI algorithms, API routing, and user interface components. All code is written in Python 3.x and modern ES6 JavaScript/React.")

    add_heading_3(doc, "5.2 Coding")
    add_styled_paragraph(doc, "The core implementation consists of several Python modules and React components. Below are the key code snippets from the main files.")

    add_styled_paragraph(doc, "5.2.1 Learning Path Generator & DAG Sequencing (backend/ai/learning_path.py):", size_pt=11.5, bold=True, space_before=6, space_after=2)
    code_lp = """import json
from collections import defaultdict, deque
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.models.models import User, StudentProfile, CareerGoal, Topic, Prerequisite, LearningPath, LearningPathTopic

def generate_personalized_learning_path(db: Session, user_id: int) -> dict:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first() if profile else db.query(CareerGoal).first()
    all_topics = db.query(Topic).all()

    # TF-IDF & Cosine Similarity Content Matching
    topic_corpus = [f"{t.title} {t.category} {t.description}" for t in all_topics]
    student_query = f"{career_goal.target_role} {career_goal.title} {career_goal.description}"
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(topic_corpus + [student_query])
    cos_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
    similarity_map = {all_topics[i].id: float(cos_similarities[i]) for i in range(len(all_topics))}

    # Build DAG Adjacency List & In-Degrees
    prereq_records = db.query(Prerequisite).all()
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    for pr in prereq_records:
        adj[pr.prerequisite_topic_id].append(pr.topic_id)
        in_degree[pr.topic_id] += 1

    # Kahn's Topological Sort
    queue = deque([t.id for t in all_topics if in_degree[t.id] == 0])
    ordered_topic_ids = []
    while queue:
        curr_id = queue.popleft()
        ordered_topic_ids.append(curr_id)
        for dependent_id in adj[curr_id]:
            in_degree[dependent_id] -= 1
            if in_degree[dependent_id] == 0:
                queue.append(dependent_id)

    return {"status": "success", "total_topics": len(ordered_topic_ids), "ordered_ids": ordered_topic_ids}"""
    add_code_block(doc, code_lp)

    add_styled_paragraph(doc, "5.2.2 Skill Gap Analysis Engine (backend/ai/skill_gap.py):", size_pt=11.5, bold=True, space_before=6, space_after=2)
    code_sg = """import json
from sqlalchemy.orm import Session
from backend.models.models import StudentProfile, CareerGoal, Skill, StudentSkill, Topic, SkillGap

LEVEL_MAP = {"none": 0, "beginner": 1, "intermediate": 2, "advanced": 3}

def analyze_student_skill_gaps(db: Session, user_id: int) -> dict:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    career_goal = db.query(CareerGoal).filter(CareerGoal.id == profile.career_goal_id).first()
    required_skills = json.loads(career_goal.required_skills_json or "[]")
    
    student_skills_records = db.query(StudentSkill).filter(StudentSkill.user_id == user_id).all()
    user_skill_levels = {ss.skill.name.lower(): ss.current_level for ss in student_skills_records if ss.skill}

    gaps_result = []
    total_required = 0
    total_earned = 0

    for item in required_skills:
        skill_name = item.get("skill_name", "")
        req_val = LEVEL_MAP.get(item.get("required_level", "Intermediate").lower(), 2)
        curr_val = LEVEL_MAP.get(user_skill_levels.get(skill_name.lower(), "Beginner").lower(), 1)
        gap_diff = req_val - curr_val
        
        status = "Critical" if gap_diff >= 2 else "Moderate" if gap_diff == 1 else "Met"
        total_required += req_val
        total_earned += min(curr_val, req_val)

        gaps_result.append({
            "skill_name": skill_name,
            "required_val": req_val,
            "current_val": curr_val,
            "gap_status": status
        })

    readiness = round((total_earned / max(total_required, 1)) * 100, 1)
    return {"target_career": career_goal.title, "readiness_percentage": readiness, "gaps": gaps_result}"""
    add_code_block(doc, code_sg)

    add_styled_paragraph(doc, "5.2.3 NLP Intent Classifier (backend/ai/nlp.py):", size_pt=11.5, bold=True, space_before=6, space_after=2)
    code_nlp = """import re
from sklearn.feature_extraction.text import TfidfVectorizer

def parse_chatbot_intent(query: str) -> dict:
    q = query.lower()
    if any(k in q for k in ["why recommend", "why did you suggest"]):
        return {"intent": "why_recommended", "confidence": 0.92}
    if any(k in q for k in ["what should i learn next", "next topic"]):
        return {"intent": "next_topic", "confidence": 0.89}
    if any(k in q for k in ["explain", "what is", "how does"]):
        return {"intent": "concept_explanation", "confidence": 0.90}
    if any(k in q for k in ["weak", "gap", "struggling"]):
        return {"intent": "skill_gaps", "confidence": 0.88}
    return {"intent": "general_tutoring", "confidence": 0.75}"""
    add_code_block(doc, code_nlp)

    add_styled_paragraph(doc, "5.2.4 Adaptive Quiz Interceptor (backend/ai/learning_path.py):", size_pt=11.5, bold=True, space_before=6, space_after=2)
    code_adapt = """def adapt_learning_path_on_quiz(db: Session, user_id: int, quiz_id: int, percentage: float, topic_id: int) -> dict:
    path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
    current_lpt = db.query(LearningPathTopic).filter(
        LearningPathTopic.learning_path_id == path.id,
        LearningPathTopic.topic_id == topic_id
    ).first()

    if current_lpt:
        current_lpt.score = percentage
        if percentage < 60.0:
            current_lpt.status = "review_needed"
            current_lpt.is_adaptive_addition = True
            action = f"Adaptive Remediation: Scored {percentage}%. Added review exercises."
        else:
            current_lpt.status = "completed"
            action = f"Mastery Achieved: Scored {percentage}%. Unlocked downstream modules."
        db.commit()
    return {"action": action, "topic_id": topic_id, "score": percentage}"""
    add_code_block(doc, code_adapt)

    add_styled_paragraph(doc, "5.2.5 Speech Recognition Pipeline (backend/voice/speech_to_text.py):", size_pt=11.5, bold=True, space_before=6, space_after=2)
    code_stt = """import io
import speech_recognition as sr

def transcribe_audio_bytes(audio_bytes: bytes) -> dict:
    recognizer = sr.Recognizer()
    try:
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return {"success": True, "text": text}
    except sr.UnknownValueError:
        return {"success": False, "error": "Speech was unintelligible"}
    except Exception as e:
        return {"success": False, "error": str(e)}"""
    add_code_block(doc, code_stt)

    add_heading_3(doc, "5.3 Code Structure:")
    code_tree = """d:/ainlp/
├── backend/
│   ├── ai/
│   │   ├── chatbot.py            # AI Chatbot with intent classification
│   │   ├── clustering.py         # K-Means learner clustering
│   │   ├── learning_path.py      # DAG Topological Sort & path generation
│   │   ├── nlp.py                # TF-IDF & Cosine similarity extraction
│   │   ├── predictor.py          # Random Forest score & timeline predictor
│   │   ├── recommendation.py     # Content-based & collaborative filtering
│   │   └── skill_gap.py          # Skill matrix distance & gap calculation
│   ├── database/
│   │   ├── db.py                 # SQLAlchemy connection with MySQL/SQLite fallback
│   │   ├── learning_path.db      # Local SQLite persistent store
│   │   └── seed_data.py          # Pre-populated careers, skills, topics & quizzes
│   ├── models/
│   │   └── models.py             # Declarative ORM models (Users, Paths, Quizzes)
│   ├── routes/
│   │   ├── auth_routes.py        # /api/register & /api/login
│   │   ├── profile_routes.py     # /api/profile (GET & PUT)
│   │   ├── assessment_routes.py  # Initial diagnostic skill evaluation
│   │   ├── learning_path_routes.py # Personalized DAG roadmap & re-generation
│   │   ├── quiz_routes.py        # Module mastery quizzes & grading
│   │   ├── progress_routes.py    # Time, completions, streak tracking
│   │   ├── skill_gap_routes.py   # Numerical skill gap breakdown
│   │   ├── recommendation_routes.py # AI personalized recommendations
│   │   ├── chatbot_routes.py     # Context-aware educational chatbot
│   │   └── voice_routes.py       # Speech-to-Text & Text-to-Speech pipeline
│   ├── voice/
│   │   ├── speech_to_text.py     # Audio decoding & speech recognition
│   │   └── text_to_speech.py     # Base64 audio synthesis
│   ├── app.py                    # Flask application entry point
│   ├── requirements.txt          # Python dependencies
│   └── test_api.py               # Automated end-to-end REST test suite
├── database/
│   └── schema.sql                # Complete MySQL DDL schema
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FloatingVoiceModal.jsx # Live voice assistant popup
│   │   │   ├── Header.jsx        # Navigation header & user status
│   │   │   └── Sidebar.jsx       # Tab routing sidebar
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx # Analytics, streak, radar, active path
│   │   │   ├── LearningPathPage.jsx # Interactive DAG timeline & filters
│   │   │   ├── SkillAssessmentPage.jsx # Diagnostic benchmark test
│   │   │   ├── SkillGapPage.jsx  # Radar & bar charts of missing skills
│   │   │   ├── TopicsListPage.jsx # Catalog of all courses & topics
│   │   │   ├── TopicLearningPage.jsx # Markdown reader & practice
│   │   │   ├── QuizPage.jsx      # Timed quiz with immediate evaluation
│   │   │   ├── ProgressTrackingPage.jsx # Learning stats & milestones
│   │   │   ├── RecommendationsPage.jsx # AI-curated electives
│   │   │   ├── ChatbotPage.jsx   # Dedicated tutoring chat assistant
│   │   │   └── ProfilePage.jsx   # Career goal & skill level editor
│   │   ├── services/
│   │   │   └── api.js            # Axios/Fetch client with auth headers
│   │   ├── App.jsx               # Main container with tab-based routing
│   │   └── index.css             # Glassmorphic, modern design system
│   ├── package.json
│   └── vite.config.js
├── start_all.bat                 # One-click launch for Windows
├── start_backend.bat             # Launch Python Flask server
└── start_frontend.bat            # Launch React Vite dev server"""
    add_code_block(doc, code_tree)

    add_heading_3(doc, "5.4 VS Code Screenshots:")
    add_styled_paragraph(doc, "Key backend and frontend source files inspected during implementation:")
    vs_items = [
        ("i) learning_path.py: ", "Implementation of Kahn's topological sort and adaptive remediation logic."),
        ("ii) skill_gap.py: ", "Numerical vector distance calculation comparing student ratings against target job profiles."),
        ("iii) nlp.py: ", "Stop-word removal, TF-IDF vectorizer configuration, and multi-intent parsing rules."),
        ("iv) LearningPathPage.jsx: ", "Interactive DAG node rendering with collapsible prerequisite tags and progress badges.")
    ]
    for v_title, v_desc in vs_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(v_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(v_desc).font.name = "Times New Roman"

    add_heading_3(doc, "5.5 Implementation Details:")
    impl_details = [
        ("Environment Setup: ", "Install dependencies using: pip install flask flask-cors sqlalchemy scikit-learn numpy nltk speechrecognition gtts werkzeug, and npm install in frontend."),
        ("Data Preparation & Seeding: ", "Execute python -c \"from backend.database.seed_data import seed_database; seed_database()\" to populate career roles, topics, and quiz databases."),
        ("Running the Application: ", "Launch servers concurrently via start_all.bat (Backend: http://localhost:5000, Frontend: http://localhost:5173)."),
        ("Automated Verification: ", "Execute python backend/test_api.py to validate API integrity.")
    ]
    for i_title, i_desc in impl_details:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(i_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(i_desc).font.name = "Times New Roman"

    doc.add_page_break()

    # ================= PAGE 20: CHAPTER 6 OUTPUT SCREENSHOTS =================
    add_heading_1(doc, "CHAPTER 6")
    add_heading_2(doc, "OUTPUT SCREENSHOTS")

    add_callout_box(doc, "Figure 6.1: Student Analytics Dashboard", "Displays active roadmap progress, overall completion rate, learning streaks, and the comprehensive skills radar chart comparing current proficiencies against target career demands.")
    add_callout_box(doc, "Figure 6.2: Dynamic DAG Personalized Learning Roadmap", "Shows prerequisite-sequenced modules, completion badges, estimated hours, and explicit AI recommendation rationale for each learning node.")
    add_callout_box(doc, "Figure 6.3: Skill-Gap Analysis & Readiness Visualizer", "Visualizes granular skill readiness scores, categorizing competencies into Critical, Moderate, and Met tiers, along with direct course recommendation mappings.")
    add_callout_box(doc, "Figure 6.4: Interactive Topic Reader & Mastery Quiz Interface", "Presents structured learning content with timed diagnostic quizzes and immediate score feedback, including automated remedial recommendations upon score deficits.")
    add_callout_box(doc, "Figure 6.5: Intelligent AI Tutoring Chatbot & Voice Assistant Modal", "Demonstrates real-time conversational assistance, showing concept explanations, roadmap inquiries, and voice-driven interactions.")

    doc.add_page_break()

    # ================= PAGE 22: CHAPTER 7 CONCLUSION =================
    add_heading_1(doc, "CHAPTER 7")
    add_heading_2(doc, "CONCLUSION")

    add_heading_3(doc, "7.1 Summary of the Project:")
    add_styled_paragraph(doc, "The AI-Powered Personalized Learning Path Generation System has been successfully designed, implemented, and validated as an end-to-end educational engineering solution. By combining Natural Language Processing (TF-IDF and Cosine Similarity), Directed Acyclic Graph (DAG) topological sequencing, machine learning-driven risk forecasting, and adaptive remediation, the platform provides personalized, prerequisite-respecting learning pathways that adapt to individual learner needs.")
    
    achievements = [
        "Development of a robust DAG-based topological sequencing engine that eliminates circular dependencies and respects curriculum prerequisites.",
        "Implementation of a vector-based skill gap analysis tool providing actionable, granular readiness metrics against target career roles.",
        "Engineering of an automated adaptive feedback loop that dynamically inserts refresher content upon quiz failure.",
        "Creation of an interactive React frontend paired with an intelligent NLP chatbot and hands-free voice assistant."
    ]
    for ach in achievements:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.add_run(ach).font.name = "Times New Roman"

    add_heading_3(doc, "7.2 Contributions to the Field")
    add_styled_paragraph(doc, "This project contributes significantly to adaptive educational technology by:")
    contribs = [
        ("Democratization of Personalized Education: ", "Delivers adaptive, high-quality tutoring capabilities without requiring expensive private instructional resources."),
        ("Practical Application of Graph Theory & NLP: ", "Demonstrates how Kahn's Topological Sort and TF-IDF can be unified into an efficient curriculum sequencing pipeline."),
        ("Automated Remediation Workflows: ", "Showcases dynamic syllabus adjustment, addressing learning deficits in real time."),
        ("Open-Source Architectural Reference: ", "Establishes a modular full-stack reference design for adaptive educational platforms.")
    ]
    for c_title, c_desc in contribs:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(c_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(c_desc).font.name = "Times New Roman"

    add_heading_3(doc, "7.3 Limitations and Future Work")
    limits = [
        ("Large Language Model (LLM) Integration: ", "Incorporate fine-tuned open-source LLMs (such as LLaMA 3 or Mistral) for deeper conversational explanations."),
        ("Multi-Modal Content Processing: ", "Expand curriculum ingestion to automatically parse lecture videos, PDF textbooks, and code repositories."),
        ("Collaborative Social Learning: ", "Introduce peer-matching algorithms to connect students with complementary skill profiles."),
        ("Mobile Application Deployment: ", "Package the frontend as a cross-platform mobile application using React Native or Flutter.")
    ]
    for l_title, l_desc in limits:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(l_title)
        r.bold = True
        r.font.name = "Times New Roman"
        p.add_run(l_desc).font.name = "Times New Roman"

    add_heading_3(doc, "7.4 Impact on Educational Technology Ecosystem")
    impacts = [
        "Lowers barrier to entry for structured career transitions into AI, Data Science, and Software Engineering.",
        "Reduces learner dropouts by addressing prerequisite gaps early in the study process.",
        "Empowers academic institutions to automate diagnostic profiling and provide targeted student support."
    ]
    for imp in impacts:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.add_run(imp).font.name = "Times New Roman"

    add_heading_3(doc, "7.5 Final Remarks")
    add_styled_paragraph(doc, "The successful realization of this system confirms the effectiveness of combining graph-based dependency modeling with NLP to solve curriculum planning challenges. By moving beyond rigid, linear syllabi, the platform delivers an adaptive educational experience that enhances learner comprehension, retention, and career readiness.")

    add_heading_3(doc, "RUBRICS :")
    t_rubric = doc.add_table(rows=2, cols=7)
    headers_rubric = [
        "Aim &\nAlgorithm\n(10 Marks)",
        "Coding &\nImplementation\n(20 Marks)",
        "Optimization\n(10 Marks)",
        "Output\n(5 Marks)",
        "Time\nManagement\n(5 Marks)",
        "Viva\n(10 Marks)",
        "Total\n(60 Marks)"
    ]
    data_rubric = [["", "", "", "", "", "", ""]]
    format_table(t_rubric, [0.95, 1.25, 1.0, 0.75, 1.05, 0.85, 0.95], headers_rubric, data_rubric)
    t_rubric.rows[1].height = Inches(0.45)

    add_heading_3(doc, "RESULT:")
    add_styled_paragraph(doc, "The AI-Powered Personalized Learning Path Generation System has been successfully implemented and tested, demonstrating robust DAG-based prerequisite curriculum sequencing, accurate numerical skill-gap analysis, adaptive quiz-driven remediation, and intuitive web and voice interfaces. All core functionalities operate with high performance and reliability, establishing an effective AI-powered educational platform.")

    output_path = r"d:\AINLP\MICRO_PROJECT_REPORT.docx"
    doc.save(output_path)
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    build_docx_report()
