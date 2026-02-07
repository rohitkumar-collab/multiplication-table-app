from flask import Flask, render_template, request, jsonify, send_file
import random
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

app = Flask(__name__)

# File to store analytics
ANALYTICS_FILE = "analytics.json"

def load_analytics():
    """Load analytics data from file"""
    try:
        if os.path.exists(ANALYTICS_FILE):
            with open(ANALYTICS_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading analytics: {e}")
    return {}

def save_analytics(data):
    """Save analytics data to file"""
    try:
        with open(ANALYTICS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving analytics: {e}")

def update_analytics(number):
    """Update analytics when a table is generated"""
    analytics = load_analytics()
    num_str = str(number)
    if num_str not in analytics:
        analytics[num_str] = 0
    analytics[num_str] += 1
    save_analytics(analytics)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        table = None
        num = None
        start_range = 1
        end_range = 10
        
        if request.method == "POST":
            num = int(request.form.get("number", 1))
            start_range = int(request.form.get("start_range", 1))
            end_range = int(request.form.get("end_range", 10))
            
            # Validate ranges
            if start_range < 1:
                start_range = 1
            if end_range < start_range:
                end_range = start_range + 10
            if end_range > 100:
                end_range = 100
            
            table = [(num, i, num * i) for i in range(start_range, end_range + 1)]
            update_analytics(num)
        
        analytics = load_analytics()
        top_tables = sorted(analytics.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return render_template("index.html", table=table, num=num, start_range=start_range, 
                             end_range=end_range, top_tables=top_tables)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template("index.html", table=None, num=None, start_range=1, 
                             end_range=10, top_tables=[])

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Quiz mode route"""
    if request.method == "POST":
        return render_template("quiz.html")
    return render_template("quiz.html")

@app.route("/api/quiz-question", methods=["GET"])
def get_quiz_question():
    """Generate a random quiz question"""
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    answer = num1 * num2
    return jsonify({
        "num1": num1,
        "num2": num2,
        "answer": answer
    })

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    """Generate and download multiplication table as PDF"""
    num = int(request.form.get("number"))
    start_range = int(request.form.get("start_range", 1))
    end_range = int(request.form.get("end_range", 10))
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77d2'),
        spaceAfter=30,
        alignment=1
    )
    
    # Title
    title = Paragraph(f"Multiplication Table for {num}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Create table data
    table_data = [["Number", f"{num} ×", "Result"]]
    for i in range(start_range, end_range + 1):
        table_data.append([str(i), "×", str(num * i)])
    
    # Create table
    table = Table(table_data, colWidths=[1.5*inch, 1*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77d2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"multiplication_table_{num}.pdf", mime_type="application/pdf")

@app.route("/analytics")
def analytics():
    """Show analytics page"""
    analytics_data = load_analytics()
    top_tables = sorted(analytics_data.items(), key=lambda x: x[1], reverse=True)
    total_queries = sum(analytics_data.values())
    
    return render_template("analytics.html", top_tables=top_tables, total_queries=total_queries)

if __name__ == "__main__":
    # For production, debug is set to False, and host is set to '0.0.0.0' to allow external access
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

# Expose app for gunicorn
wsgi_app = app