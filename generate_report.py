from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import date

OUTPUT = "/home/user/Drop-Studio-/WSS26_Performance_Report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

W = A4[0] - 4*cm  # usable width

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=20,
    textColor=colors.HexColor("#1a1a2e"),
    spaceAfter=6,
    alignment=TA_CENTER,
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=11,
    textColor=colors.HexColor("#555555"),
    spaceAfter=4,
    alignment=TA_CENTER,
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontSize=13,
    textColor=colors.HexColor("#ffffff"),
    backColor=colors.HexColor("#1a1a2e"),
    spaceBefore=14,
    spaceAfter=6,
    leftIndent=-6,
    rightIndent=-6,
    borderPad=6,
)
subsection_style = ParagraphStyle(
    "Subsection",
    parent=styles["Heading3"],
    fontSize=11,
    textColor=colors.HexColor("#1a1a2e"),
    spaceBefore=10,
    spaceAfter=4,
    borderPad=2,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=9,
    textColor=colors.HexColor("#333333"),
    spaceAfter=4,
)
note_style = ParagraphStyle(
    "Note",
    parent=styles["Normal"],
    fontSize=8,
    textColor=colors.HexColor("#888888"),
    spaceAfter=4,
    leftIndent=10,
)

# Table helpers
HEADER_BG   = colors.HexColor("#1a1a2e")
ALT_ROW_BG  = colors.HexColor("#f4f4f8")
WHITE       = colors.white
BORDER      = colors.HexColor("#cccccc")
RED_ALERT   = colors.HexColor("#c0392b")
ORANGE      = colors.HexColor("#e67e22")

def make_table(data, col_widths, highlight_rows=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND",  (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  8),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("ALIGN",       (0, 1), (0, -1),  "LEFT"),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, ALT_ROW_BG]),
        ("GRID",        (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if highlight_rows:
        for r in highlight_rows:
            style_cmds.append(("TEXTCOLOR", (0, r), (-1, r), RED_ALERT))
            style_cmds.append(("FONTNAME",  (0, r), (-1, r), "Helvetica-Bold"))
    t.setStyle(TableStyle(style_cmds))
    return t

story = []

# ── HEADER ──────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Achilles Stores", title_style))
story.append(Paragraph("New Arrivals Summer 2026 — WSS26 Performance Report", subtitle_style))
story.append(Paragraph(f"Period: May 5 – May 9, 2026  |  Generated: {date.today().strftime('%B %d, %Y')}", subtitle_style))
story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor("#1a1a2e"), spaceAfter=10))

# ── SECTION 1 — STORE OVERVIEW ───────────────────────────────────────────────
story.append(Paragraph("  1.  Store-Wide Sales Overview (Last 5 Days)", section_style))

sales_data = [
    ["Date", "Orders", "Gross Sales (EGP)", "Net Sales (EGP)", "AOV (EGP)"],
    ["May 5, 2026",  "110", "288,482",   "272,754",  "2,623"],
    ["May 6, 2026",  "97",  "256,133",   "256,133",  "2,641"],
    ["May 7, 2026",  "94",  "256,164",   "256,164",  "2,725"],
    ["May 8, 2026",  "103", "239,840",   "234,003",  "2,329"],
    ["May 9, 2026",  "92",  "216,751",   "216,751",  "2,356"],
    ["TOTAL",        "496", "1,257,370", "1,235,805","2,535 avg"],
]
cw = [W*0.20, W*0.12, W*0.24, W*0.24, W*0.20]
t = make_table(sales_data, cw, highlight_rows=[6])
story.append(t)
story.append(Paragraph(
    "★ Revenue declined ~16% from May 5 to May 9. May 5 was the strongest day.",
    note_style
))

# ── SECTION 2 — CUSTOMER BEHAVIOUR ──────────────────────────────────────────
story.append(Paragraph("  2.  Customer Behaviour", section_style))

cust_data = [
    ["Date", "Total Customers", "Returning Customers", "Return Rate"],
    ["May 5, 2026", "105", "39", "37.1%"],
    ["May 6, 2026", "96",  "37", "38.5%"],
    ["May 7, 2026", "91",  "28", "30.8%"],
    ["May 8, 2026", "99",  "46", "46.5%"],
    ["May 9, 2026", "90",  "32", "35.6%"],
]
cw2 = [W*0.22, W*0.26, W*0.26, W*0.26]
story.append(make_table(cust_data, cw2, highlight_rows=[4]))
story.append(Paragraph(
    "★ Average return rate 37.7%. May 8 spike to 46.5% indicates strong loyalty. "
    "Note: store uses COD — Shopify checkout conversion metrics do not reflect actual completed orders.",
    note_style
))

# ── SECTION 3 — SESSION FUNNEL ───────────────────────────────────────────────
story.append(Paragraph("  3.  Session & Conversion Funnel", section_style))

sess_data = [
    ["Date", "Sessions", "Cart Adds", "Completed Orders", "Conv. Rate"],
    ["May 5", "5,650", "364", "14", "0.25%"],
    ["May 6", "5,620", "330",  "9", "0.16%"],
    ["May 7", "5,958", "354", "18", "0.30%"],
    ["May 8", "6,525", "404", "19", "0.29%"],
    ["May 9", "5,770", "364",  "9", "0.16%"],
    ["TOTAL", "29,919","1,816","69", "—"],
]
cw3 = [W*0.16, W*0.18, W*0.18, W*0.24, W*0.24]
story.append(make_table(sess_data, cw3, highlight_rows=[6]))
story.append(Paragraph(
    "★ Low conversion rate is expected with COD model — Shopify tracks card checkout completions only. "
    "Cart add rate (~6%) shows real purchase intent.",
    note_style
))

# ── SECTION 4 — TOP PRODUCTS ─────────────────────────────────────────────────
story.append(Paragraph("  4.  Top 10 Products Store-Wide", section_style))

top_data = [
    ["Product", "Gross Sales (EGP)", "Orders"],
    ["Woven Mesh Mary Jane Flats - Brown",             "58,869", "31"],
    ["Square Toe Thong Heeled Mules - Black",           "50,970", "30"],
    ["Studded Sandals - Brown",                         "33,980", "20"],
    ["Strappy Caged Slingback Stiletto - Metallic Bronze","31,984","16"],
    ["Studded Sandals - Café",                          "27,184", "16"],
    ["Beaded Lattice Slip-On Mules - Gold",             "26,990", "10"],
    ["Woven Basket Mary Jane Flats - Beige",            "24,687", "13"],
    ["Woven Mesh Mary Jane Flats - Black",              "24,687", "13"],
    ["Woven Basket Mary Jane Flats - Brown",            "24,687", "13"],
    ["Studded Sandals - Black",                         "23,786", "14"],
]
cw4 = [W*0.62, W*0.24, W*0.14]
story.append(make_table(top_data, cw4))

# ── SECTION 5 — WSS26 LOWEST BY SALES ───────────────────────────────────────
story.append(Paragraph("  5.  WSS26 — Lowest Performing by Sales (Last 5 Days)", section_style))
story.append(Paragraph("Products with only 1 order — weakest revenue in the collection:", subsection_style))

low_sales_data = [
    ["Product", "Gross Sales (EGP)", "Orders"],
    ["Braided Knot Flat Slides - Beige",        "1,299", "1"],
    ["Flat Thong Sandals Gold Oval Ring - Beige","1,299", "1"],
    ["Flat Thong Sandals Gold Oval Ring - Black","1,299", "1"],
    ["Raffia Slides With Round Buckle - Baby Blue","1,299","1"],
    ["Suede Slides Fringe Stones - Café",        "1,499", "1"],
    ["Suede Slides Fringe Stones - Brown",        "1,499", "1"],
    ["Suede Slides Fringe Stones - Black",        "1,499", "1"],
    ["Suede Slides Fringe Stones - Beige",        "1,499", "1"],
    ["Suede Fringe Flat Sandals - Beige",         "1,599", "1"],
    ["Suede Fringe Flat Sandals - Brown",         "1,599", "1"],
    ["Slingback Platform Pumps - Beige",          "1,699", "1"],
    ["Patent Bow Heeled Mules - Maroon",          "1,699", "1"],
    ["Strappy Bow Kitten Heel Mules - Black",     "1,699", "1"],
    ["Patent Kitten Bow Heels - Maroon",          "1,699", "1"],
    ["Patent Kitten Bow Heels - Beige",           "1,699", "1"],
]
cw5 = [W*0.62, W*0.24, W*0.14]
story.append(make_table(low_sales_data, cw5))

# ── SECTION 6 — DEAD STOCK ───────────────────────────────────────────────────
story.append(Paragraph("  6.  WSS26 — Dead Stock Alert (0 Units Sold, High Inventory)", section_style))
story.append(Paragraph(
    "These products have significant stock on hand but zero sales in the last 5 days. "
    "Immediate action recommended.",
    body_style
))

dead_data = [
    ["Product", "Stock On Hand", "Units Sold", "Sell-Through"],
    ["Closed Platform Pumps - Beige",                   "80", "0", "0%"],
    ["Round Toe Platform Ankle Strap Pumps - Beige",    "80", "0", "0%"],
    ["Suede Fringe Platform Sandals - Black",            "80", "0", "0%"],
    ["Round Toe Platform Ankle Strap Pumps - Maroon",   "79", "0", "0%"],
    ["Suede Fringe Flat Sandals - Black",               "79", "0", "0%"],
    ["Suede Fringe Platform Sandals - Café",            "79", "0", "0%"],
    ["Asymmetric Strappy Stiletto Gold Disc - Black",   "79", "0", "0%"],
    ["Patent Kitten Slingback Pumps - Beige",           "79", "0", "0%"],
    ["Patent Kitten Slingback Pumps - Maroon",          "79", "0", "0%"],
    ["Patent Kitten Slingback Pumps - Black",           "76", "0", "0%"],
    ["Patent Kitten Slingback Pumps - Brown",           "76", "0", "0%"],
    ["Asymmetric Strappy Stiletto Gold Disc - Beige",   "76", "0", "0%"],
    ["Strappy Thong Heel Sandals - Brown",              "76", "0", "0%"],
    ["Sneakers Gold Buckle Strap - Brown",              "60", "0", "0%"],
    ["Sneakers Gold Buckle Strap - Camel",              "60", "0", "0%"],
    ["Sneakers Gold Buckle Strap - Black",              "60", "0", "0%"],
    ["Sneakers Gold Buckle Strap - Beige",              "59", "0", "0%"],
    ["Leather Tassel Loafers - Beige",                  "60", "0", "0%"],
    ["Mesh Rhinestone Sneakers - Brown",                "60", "0", "0%"],
    ["Mesh Rhinestone Sneakers - Black",                "60", "0", "0%"],
    ["Patent Bow Heeled Mules - Beige",                 "60", "0", "0%"],
    ["Patent Bow Heeled Mules - Black",                 "60", "0", "0%"],
    ["Strappy Bow Kitten Heel Mules - Maroon",          "60", "0", "0%"],
    ["Strappy Bow Kitten Heel Mules - Beige",           "58", "0", "0%"],
    ["Double-Buckle Patent Slingback Pumps - Café",     "45", "0", "0%"],
    ["Double-Buckle Patent Slingback Pumps - Beige",    "44", "0", "0%"],
    ["Double-Buckle Patent Slingback Pumps - Black",    "43", "0", "0%"],
    ["Notched Peep-Toe Slip-On Mules - Black",          "41", "0", "0%"],
    ["Wrap-Strap Patent Heeled Sandals - Café",         "32", "0", "0%"],
    ["Wide-Band Buckle Slip-On Mules - Black",          "30", "0", "0%"],
    ["Pointed D'Orsay Ankle-Strap Pumps - Black",       "30", "0", "0%"],
    ["Thong Cabochon Stiletto Heels - Black",            "30", "0", "0%"],
    ["Patent Crisscross Mules with Gold Ring - Black",  "28", "0", "0%"],
    ["Triple-Strap Pointed Patent Pumps - Brown",       "28", "0", "0%"],
    ["Wide-Band Buckle Slip-On Mules - Beige",          "28", "0", "0%"],
    ["Suede Crisscross Flatform Sandals - Black",       "28", "0", "0%"],
    ["Pointed D'Orsay Ankle-Strap Pumps - Beige",       "26", "0", "0%"],
]
cw6 = [W*0.56, W*0.16, W*0.14, W*0.14]
story.append(make_table(dead_data, cw6, highlight_rows=list(range(1, 14))))

# ── SECTION 7 — KEY RECOMMENDATIONS ─────────────────────────────────────────
story.append(Paragraph("  7.  Key Recommendations", section_style))

recs = [
    ("Revenue Decline", "Store revenue fell ~16% day-over-day. Investigate what drove May 5 peak (paid ads, email blast) and replicate."),
    ("Patent Kitten Slingback Pumps", "4 colorways × ~78 units = ~312 units of dead stock. Run an urgent discount or bundle promotion."),
    ("Platform Styles", "Closed Platform Pumps, Round Toe Platform Ankle Strap Pumps & Suede Fringe Platform Sandals total 240+ idle units. Consider repositioning with content or influencer seeding."),
    ("Sneakers Gold Buckle Strap", "All 4 colorways at 0 sales (~240 units). May need better product photography or a targeted campaign."),
    ("Suede Slides Fringe Stones", "Entire 4-color line at 1 order each. Low price point (EGP 1,499) — test a flash sale or 2-for-1 offer."),
    ("COD Note", "Shopify conversion metrics understate actual performance since COD orders bypass standard checkout tracking. Use order count as the primary KPI."),
]
for title, text in recs:
    story.append(Paragraph(f"<b>{title}:</b> {text}", body_style))
    story.append(Spacer(1, 2))

story.append(HRFlowable(width=W, thickness=1, color=BORDER, spaceBefore=14, spaceAfter=6))
story.append(Paragraph("Achilles Stores — Confidential Internal Report", note_style))

doc.build(story)
print(f"PDF saved to: {OUTPUT}")
