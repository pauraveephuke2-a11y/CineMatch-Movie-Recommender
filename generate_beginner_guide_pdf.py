"""
generate_beginner_guide_pdf.py
Generates a comprehensive, beginner-friendly PDF guide explaining every single file
in the CineMatch project with plain-English analogies, step-by-step workflows,
and code breakdowns.

Outputs:
- C:\\Users\\Nucom\\Desktop\\CineMatch_Beginners_File_Guide.pdf
- C:\\Users\\Nucom\\Projects\\MovieRecommender\\CineMatch_Beginners_File_Guide.pdf
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_DIR = r"C:\Users\Nucom\Projects\MovieRecommender"
DESKTOP_DIR = r"C:\Users\Nucom\Desktop"
PDF_FILENAME = "CineMatch_Beginners_File_Guide.pdf"

PROJECT_PDF = os.path.join(PROJECT_DIR, PDF_FILENAME)
DESKTOP_PDF = os.path.join(DESKTOP_DIR, PDF_FILENAME)


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and 'Page X of Y' footers to every page except cover."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header
        self.drawString(54, 11 * 72 - 36, "CineMatch — Beginner's Guide to Every File & Codebase Architecture")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer
        self.setFont("Helvetica", 8)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "Author: Pauravee Phuke | MIT-WPU Pune | AI & Data Science")
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PROJECT_PDF,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=colors.HexColor('#E50914'), alignment=1, spaceAfter=20
    )
    tagline_style = ParagraphStyle(
        'CoverTagline', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=10, leading=14,
        textColor=colors.HexColor('#64748B'), alignment=1, spaceAfter=28
    )
    h1_style = ParagraphStyle(
        'Head1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=colors.HexColor('#E50914'), spaceBefore=14, spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Head2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=colors.HexColor('#0F172A'), spaceBefore=9, spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=colors.HexColor('#1E293B'), spaceAfter=5
    )
    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=12.5,
        textColor=colors.HexColor('#0369A1'), spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=colors.HexColor('#334155'), leftIndent=12, spaceAfter=3
    )

    story = []

    # ═════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═════════════════════════════════════════════════════════════
    story.append(Spacer(1, 20))
    story.append(Paragraph("CINEMATCH: THE COMPLETE BEGINNER'S CODE GUIDE", title_style))
    story.append(Paragraph("A Clear, Friendly Walkthrough of Every Single File, Script, and Technology", subtitle_style))
    story.append(Paragraph("Written for students, professors, and teammates to understand exactly how the system works without getting lost in jargon.", tagline_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#E50914"), spaceAfter=20))

    meta_data = [
        [Paragraph("<b>Project Name:</b>", body_style), Paragraph("CineMatch — AI Movie Recommender & OTT Streaming Platform", body_style)],
        [Paragraph("<b>Student Author:</b>", body_style), Paragraph("<b>Pauravee Phuke</b> (Division 9, Batch I2)", body_style)],
        [Paragraph("<b>Institution:</b>", body_style), Paragraph("MIT World Peace University (MIT-WPU), Pune", body_style)],
        [Paragraph("<b>Department:</b>", body_style), Paragraph("B.Tech in Artificial Intelligence & Data Science (AI & DS)", body_style)],
        [Paragraph("<b>Live Website:</b>", body_style), Paragraph("<font color='#0284C7'><b>https://pauraveephuke2-a11y.github.io/</b></font>", body_style)],
        [Paragraph("<b>GitHub Code:</b>", body_style), Paragraph("<font color='#0284C7'><b>https://github.com/pauraveephuke2-a11y/cinematch</b></font>", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[130, 340])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>What Is in This Guide?</b>", h2_style))
    story.append(Paragraph("1. <b>The Big Picture:</b> How all the files connect like a modern digital movie studio.<br/>"
                           "2. <b>File-by-File Breakdown:</b> What each file does, plain-English analogies, and key code.<br/>"
                           "3. <b>The 2 Main Faces of CineMatch:</b> The Python Streamlit app vs. the live GitHub Pages OTT web app.<br/>"
                           "4. <b>How the AI Works:</b> TF-IDF and Cosine Similarity explained like matching flavors of ice cream.<br/>"
                           "5. <b>Payment & Streaming:</b> How the UPI QR system and video player operate safely.", body_style))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 1: THE BIG PICTURE
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("1. THE BIG PICTURE: HOW EVERYTHING CONNECTS", h1_style))
    story.append(Paragraph(
        "Think of CineMatch like a <b>modern high-tech cinema</b>. To run smoothly, it needs three main departments:",
        body_style
    ))
    story.append(Paragraph("• <b>The Storage Room (Data):</b> Holds the movie catalogs, descriptions, ratings, and posters (<code>movies.csv</code>, <code>user_ratings.csv</code>).", bullet_style))
    story.append(Paragraph("• <b>The Brain / Kitchen (Machine Learning & Python):</b> Studies movie flavors, plots, and user tastes to decide which films match (<code>recommender.py</code>, <code>collaborative_filter.py</code>).", bullet_style))
    story.append(Paragraph("• <b>The Theater Screens (User Interfaces):</b> Where people browse, watch trailers, buy subscriptions, and discover movies (<code>index.html</code> for the live web app, <code>app.py</code> for the Python dashboard).", bullet_style))

    story.append(Spacer(1, 4))

    # Summary table of all files
    map_data = [
        [Paragraph("<b>File Name</b>", body_style), Paragraph("<b>Category</b>", body_style), Paragraph("<b>One-Sentence Beginner Summary</b>", body_style)],
        [Paragraph("<b>index.html</b>", body_style), Paragraph("Frontend (Live)", body_style), Paragraph("The complete Netflix-style OTT website that visitors see and interact with.", body_style)],
        [Paragraph("<b>movies.csv</b>", body_style), Paragraph("Data", body_style), Paragraph("The movie spreadsheet containing 30 films with ratings, genres, and posters.", body_style)],
        [Paragraph("<b>user_ratings.csv</b>", body_style), Paragraph("Data", body_style), Paragraph("A table of simulated user scores used for collaborative filtering experiments.", body_style)],
        [Paragraph("<b>app.py</b>", body_style), Paragraph("Python App", body_style), Paragraph("A Python Streamlit dashboard with a movie roulette game and quiz.", body_style)],
        [Paragraph("<b>recommender.py</b>", body_style), Paragraph("AI Core", body_style), Paragraph("The Python script that calculates mathematical cosine similarity between movies.", body_style)],
        [Paragraph("<b>collaborative_filter.py</b>", body_style), Paragraph("AI Core", body_style), Paragraph("Predicts what you like by finding people who share your movie taste.", body_style)],
        [Paragraph("<b>launch_public.py</b>", body_style), Paragraph("Networking", body_style), Paragraph("Shares your local Python app to any smartphone via a Cloudflare secure link.", body_style)],
        [Paragraph("<b>verify_live.py</b>", body_style), Paragraph("Testing", body_style), Paragraph("A robot browser that tests the live website and clicks buttons automatically.", body_style)],
        [Paragraph("<b>build_full_academic_report.py</b>", body_style), Paragraph("Tools", body_style), Paragraph("Builds the formal Word and PDF reports for university submission.", body_style)],
    ]
    t_map = Table(map_data, colWidths=[120, 90, 260])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_map)

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 2: THE DATA FILES
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("2. THE DATA FILES: WHAT FEEDS THE SYSTEM", h1_style))

    story.append(Paragraph("File 1: <code>movies.csv</code>", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> This is an Excel-style comma-separated table that acts as our database. It contains 30 carefully curated world-class movies.<br/>"
        "<b>What columns are in it?</b><br/>"
        "• <code>title</code>: Name of the film (e.g., <i>Inception</i>, <i>3 Idiots</i>, <i>Dangal</i>).<br/>"
        "• <code>genre</code>: Category (e.g., Sci-Fi, Action, Comedy, Drama).<br/>"
        "• <code>rating</code>: The IMDb score out of 10 (e.g., 8.8).<br/>"
        "• <code>mood</code>: Emotional vibe (e.g., <i>Mind-Bending 🧠</i>, <i>Heartwarming 🥺</i>, <i>Adrenaline 💥</i>).<br/>"
        "• <code>stars</code>: Leading actors (e.g., Leonardo DiCaprio, Aamir Khan).<br/>"
        "• <code>overview</code>: A 2-sentence summary of the story.<br/>"
        "• <code>poster</code>: Direct internet URL to official high-resolution studio poster artwork.<br/>"
        "<b>Simple Analogy:</b> This is the menu of our movie restaurant. Without it, the chefs (algorithms) wouldn't know what they are serving!",
        body_style
    ))

    story.append(Paragraph("File 2: <code>user_ratings.csv</code>", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> A table of 140+ simulated ratings from different users (User 1, User 2, User 3...) rating movies on a scale of 1 to 10.<br/>"
        "<b>Why is it needed?</b> It trains our <b>Collaborative Filtering</b> algorithm. By seeing that 'User 1' and 'User 3' both gave 10/10 to <i>Interstellar</i> and <i>Inception</i>, the computer realizes they have identical taste and recommends other movies they each watched.",
        body_style
    ))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 3: THE LIVE PRODUCTION WEBSITE (INDEX.HTML)
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("3. THE LIVE WEB PLATFORM: <code>index.html</code>", h1_style))
    story.append(Paragraph(
        "<b>What is it?</b> This is the crown jewel of the project. It is a complete, single-file Over-The-Top (OTT) streaming platform inspired by Netflix and Disney+ Hotstar. Anyone with a browser on an iPhone, Android, or laptop can open it instantly.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Why is it built as a 'Single-File App'?</b><br/>"
        "Normally, websites need complicated servers, Node.js packages, and third-party script libraries. But Indian cellular carriers (like Jio and Airtel) often block third-party CDNs. To make CineMatch 100% unbreakable, the entire HTML structure, CSS styling, and JavaScript logic are bundled cleanly into one file with zero external dependencies!",
        body_style
    ))

    story.append(Paragraph("What Happens Inside <code>index.html</code> (Section by Section):", h2_style))
    story.append(Paragraph("1. <b>The Dark Cinema Theme (CSS):</b> Deep obsidian background (<code>#07070b</code>) with Netflix-red highlights (<code>#e50914</code>) and golden VIP accents (<code>#ffd700</code>).", bullet_style))
    story.append(Paragraph("2. <b>Hero Spotlight Billboard:</b> When you open the page, a massive 88vh billboard showcases a top trending movie with 1280px high-res background art and a 'Watch Now' button.", bullet_style))
    story.append(Paragraph("3. <b>Movie Carousels:</b> Smooth horizontally scrolling rows (Trending, Top Rated, Indian Blockbusters, Hollywood Hits).", bullet_style))
    story.append(Paragraph("4. <b>Mood Selector Quiz:</b> Click 'Mind-Bending' or 'Laugh Out Loud' and the catalog instantly rearranges to match your vibe.", bullet_style))
    story.append(Paragraph("5. <b>Cinema Video Modal:</b> Clicking any movie opens a popup cinema player. It supports multi-server switching (Server 1: YouTube HD, Server 2: Fast CDN, Server 3: Free Web Stream Aggregator).", bullet_style))
    story.append(Paragraph("6. <b>UPI Payment Gateway:</b> Click 'Upgrade VIP' to choose a pass (Mobile ₹149, Standard ₹499, VIP ₹699). It creates a real dynamic QR code for Axis Bank UPI ID <code>7499525420@axl</code>, accepts the demo payment, and showers the screen in confetti!", bullet_style))
    story.append(Paragraph("7. <b>Client-Side AI Engine:</b> Type any movie in the search box. In less than 3 milliseconds, JavaScript calculates vector overlap and tells you the top 6 films with the closest match!", bullet_style))

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 4: THE MACHINE LEARNING ENGINES
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("4. THE MACHINE LEARNING ENGINES: HOW THE AI THINKS", h1_style))

    story.append(Paragraph("File 3: <code>recommender.py</code> (Content-Based Filtering)", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> The Python engine that analyzes movie features (genre, plot words, actors, mood) to recommend similar films.<br/>"
        "<b>How it works (The 3-Step Recipe):</b><br/>"
        "1. <b>Soup Creation:</b> For each movie, it creates a text 'soup': <code>'Sci-Fi Mind-Bending Leonardo DiCaprio dream thief corporate secrets'</code>.<br/>"
        "2. <b>TF-IDF Vectorizer:</b> Converts words into numbers. Common words like 'the' are ignored. Rare, important words like 'wormhole' or 'wrestler' get heavy mathematical scores.<br/>"
        "3. <b>Cosine Similarity:</b> Measures the angle between two movies. If the angle is 0 degrees, the cosine is 1.0 (exact match). If the angle is 90 degrees, the cosine is 0.0 (completely different).",
        body_style
    ))

    story.append(Paragraph("File 4: <code>collaborative_filter.py</code> (People-Like-You Filtering)", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> Instead of looking at movie descriptions, this script looks at <i>human behavior</i>.<br/>"
        "<b>Simple Analogy:</b> If your best friend has the exact same taste in music as you, and they tell you about a new song they loved, you will probably love it too! This script mathematically calculates who your 'taste twins' are from the rating matrix.",
        body_style
    ))

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 5: THE PYTHON WEB DASHBOARD (APP.PY)
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("5. THE PYTHON ANALYTICAL DASHBOARD: <code>app.py</code>", h1_style))
    story.append(Paragraph(
        "<b>What is it?</b> While <code>index.html</code> is designed as a public consumer streaming site, <code>app.py</code> is the interactive Python dashboard built using <b>Streamlit</b>.<br/>"
        "<b>Why did we build both?</b><br/>"
        "In university evaluations, professors love to see Python data exploration! <code>app.py</code> lets students and professors interactively inspect similarity scores, view bar charts, spin the 'Movie Roulette' wheel, and take a 30-second personality quiz.",
        body_style
    ))
    story.append(Paragraph("Key Features in <code>app.py</code>:", h2_style))
    story.append(Paragraph("• <b>Movie Roulette:</b> Can't decide what to watch? Hit 'Spin Roulette' and it selects a certified masterpiece with balloons and confetti.", bullet_style))
    story.append(Paragraph("• <b>30-Second Quiz:</b> Asks 3 fun questions (Who are you with? What's your energy level? How much time do you have?) and computes your ideal movie.", bullet_style))
    story.append(Paragraph("• <b>Live Watchlist:</b> Add films to your personal list and export them directly to WhatsApp with 1 click.", bullet_style))

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 6: NETWORKING, TESTING & AUTOMATION TOOLS
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("6. NETWORKING, TESTING & AUTOMATION SCRIPTS", h1_style))

    story.append(Paragraph("File 6: <code>launch_public.py</code> (Cloudflare Quick Tunnel)", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> A Python script that creates a free, secure global HTTPS internet link for your local Python Streamlit app.<br/>"
        "<b>Why is it amazing?</b> Normally, to let someone on their phone view your project, you'd need to pay for cloud servers, configure routers, or port-forward. <code>launch_public.py</code> runs Cloudflare in the background, gives you a URL like <code>https://something.trycloudflare.com</code>, and generates a 1-tap WhatsApp link so you can text it to anyone!",
        body_style
    ))

    story.append(Paragraph("File 7: <code>verify_live.py</code> (Automated Robot Tester)", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> An automated testing script built with <b>Playwright</b>.<br/>"
        "<b>How it works:</b> It launches an invisible headless browser, visits the live website, clicks the Bank button, tests the UPI payment modal, checks mobile phone dimensions (iPhone 14 / 390px), takes 7 proof screenshots, and verifies that there are zero bugs or crashes.",
        body_style
    ))

    story.append(Paragraph("File 8: <code>build_full_academic_report.py</code> (Report Compiler)", h2_style))
    story.append(Paragraph(
        "<b>What is it?</b> A Python program using <code>python-docx</code> and <code>reportlab</code> that automatically writes and styles the formal academic reports submitted to MIT-WPU professors.",
        body_style
    ))

    # ═════════════════════════════════════════════════════════════
    # CHAPTER 7: SUMMARY CHEAT SHEET FOR PRESENTATIONS
    # ═════════════════════════════════════════════════════════════
    story.append(Paragraph("7. PRESENTATION CHEAT SHEET: HOW TO EXPLAIN THIS IN 60 SECONDS", h1_style))
    story.append(Paragraph(
        "If your professor or judge asks: <i>'What did you build and how does it work?'</i>, here is the perfect beginner-friendly answer:",
        body_style
    ))
    story.append(Paragraph(
        "<i>'We built CineMatch — an AI-powered movie recommendation and streaming platform. We combined Natural Language Processing (TF-IDF) and Cosine Similarity to mathematically understand film plots, genres, and moods. On the frontend, we built an industry-standard Netflix-style Over-The-Top web app deployed live on GitHub Pages with an embedded cinema player and an operational UPI-only subscription gateway (Axis Bank). On the backend, we built Python algorithms and a Streamlit dashboard with a movie roulette game and automated Playwright testing.'</i>",
        callout_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Beginner Guide PDF Generated: {PROJECT_PDF}")

    shutil.copy2(PROJECT_PDF, DESKTOP_PDF)
    print(f"[OK] Beginner Guide PDF Copied to Desktop: {DESKTOP_PDF}")


if __name__ == "__main__":
    build_pdf()
