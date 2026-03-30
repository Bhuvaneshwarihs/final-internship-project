import pandas as pd
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_dataframe(q, a, res):
    import re
    import pandas as pd

    pattern = r"(### QUESTION \d+.*?)(?=(### QUESTION \d+|$))"

    matches = re.findall(pattern, res, re.DOTALL)
    matches = [m[0] for m in matches]

    rows = []

    for i in range(min(len(q), len(a), len(matches))):
        rows.append({
            "Question": q[i],
            "Answer": a[i],
            "Evaluation": matches[i].strip()
        })

    return pd.DataFrame(rows)

    for i in range(min(len(q), len(a), len(matches))):
        rows.append({
            "Question": q[i],
            "Answer": a[i],
            "Evaluation": matches[i].strip()
        })

    return pd.DataFrame(rows)

def download_csv(df):
    return df.to_csv(index=False).encode()

def generate_pdf(df):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = []

    for _, r in df.iterrows():
        content.append(Paragraph(f"Q: {r['Question']}", styles["Normal"]))
        content.append(Paragraph(f"A: {r['Answer']}", styles["Normal"]))
        content.append(Paragraph(f"{r['Evaluation']}", styles["Normal"]))

    doc.build(content)

    return open("report.pdf", "rb").read()

    # jhgg