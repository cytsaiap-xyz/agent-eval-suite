#!/usr/bin/env python3
"""
Generate the sample PDF for P14.
Requires: pip install reportlab
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os


def create_annual_report():
    doc = SimpleDocTemplate(
        "annual_report.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )

    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )

    story = []

    # Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("TechCorp Industries", title_style))
    story.append(Paragraph("Annual Report 2024", styles['Heading2']))
    story.append(Spacer(1, inch))
    story.append(Paragraph("Driving Innovation, Delivering Value", body_style))
    story.append(PageBreak())

    # Letter to Shareholders
    story.append(Paragraph("Letter to Shareholders", heading1_style))
    story.append(Paragraph("""
    Dear Shareholders,

    I am pleased to report that 2024 was another outstanding year for TechCorp Industries.
    Despite challenging market conditions, we achieved record revenue of $14.4 million,
    representing a 15% increase over the prior year. Our commitment to innovation and
    customer satisfaction continues to drive sustainable growth.
    """, body_style))

    story.append(Paragraph("""
    Key highlights from 2024 include:
    • Revenue growth of 15% year-over-year
    • Expansion into three new international markets
    • Launch of our flagship Product X
    • Net Promoter Score increased to 72
    • Employee satisfaction at all-time high
    """, body_style))

    story.append(Paragraph("""
    Looking ahead to 2025, we remain focused on executing our strategic initiatives while
    maintaining operational excellence. We are investing in R&D to expand our product
    portfolio and enhance our competitive position.

    Thank you for your continued support and confidence in TechCorp Industries.

    Sincerely,
    Sarah Johnson
    Chief Executive Officer
    """, body_style))
    story.append(PageBreak())

    # Financial Highlights
    story.append(Paragraph("Financial Highlights", heading1_style))
    story.append(Paragraph("""
    TechCorp Industries delivered strong financial performance in 2024, with growth
    across all major metrics. The following table summarizes our key financial results:
    """, body_style))

    # Financial Table 1
    fin_data = [
        ['Metric', '2024', '2023', 'Change'],
        ['Revenue', '$14.4M', '$12.5M', '+15.2%'],
        ['Gross Profit', '$6.3M', '$5.3M', '+20.0%'],
        ['Operating Income', '$2.8M', '$2.1M', '+33.3%'],
        ['Net Income', '$2.0M', '$1.5M', '+33.3%'],
        ['Earnings Per Share', '$1.00', '$0.75', '+33.3%'],
    ]

    fin_table = Table(fin_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1*inch])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(fin_table)
    story.append(Spacer(1, 20))
    story.append(PageBreak())

    # Revenue by Segment
    story.append(Paragraph("Revenue by Business Segment", heading1_style))
    story.append(Paragraph("""
    Our diversified business model continues to provide stability and growth opportunities.
    The following table shows revenue breakdown by business segment:
    """, body_style))

    seg_data = [
        ['Segment', 'Revenue', '% of Total', 'YoY Growth'],
        ['Electronics', '$8.2M', '57%', '+18%'],
        ['Accessories', '$4.1M', '28%', '+12%'],
        ['Tools', '$1.5M', '10%', '+8%'],
        ['Services', '$0.6M', '5%', '+5%'],
        ['Total', '$14.4M', '100%', '+15%'],
    ]

    seg_table = Table(seg_data, colWidths=[1.8*inch, 1.2*inch, 1*inch, 1*inch])
    seg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E8E8E8')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
    ]))
    story.append(seg_table)
    story.append(Spacer(1, 20))
    story.append(PageBreak())

    # Regional Performance
    story.append(Paragraph("Regional Performance", heading1_style))
    story.append(Paragraph("""
    TechCorp operates in five major geographic regions. Our strategic expansion into
    Asia-Pacific markets yielded significant results in 2024.
    """, body_style))

    reg_data = [
        ['Region', 'Revenue', 'Orders', 'Customers', 'Growth'],
        ['North America', '$7.2M', '1,250', '890', '+12%'],
        ['Western Europe', '$4.3M', '720', '520', '+15%'],
        ['APAC', '$2.9M', '480', '380', '+45%'],
        ['Latin America', '$0.8M', '140', '95', '+22%'],
        ['Eastern Europe', '$0.5M', '90', '65', '+18%'],
    ]

    reg_table = Table(reg_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 0.9*inch, 0.8*inch])
    reg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
    ]))
    story.append(reg_table)
    story.append(PageBreak())

    # Operations
    story.append(Paragraph("Operations Overview", heading1_style))

    story.append(Paragraph("Manufacturing", heading2_style))
    story.append(Paragraph("""
    Our manufacturing operations achieved significant improvements in efficiency and
    quality during 2024. Key operational metrics include:
    • Production capacity increased by 25%
    • Defect rate reduced to 0.5%
    • On-time delivery improved to 98%
    • Inventory turns increased to 8x
    """, body_style))

    story.append(Paragraph("Supply Chain", heading2_style))
    story.append(Paragraph("""
    We continued to strengthen our supply chain resilience through supplier diversification
    and strategic inventory positioning. Despite global supply chain challenges, we
    maintained product availability above 95% throughout the year.
    """, body_style))
    story.append(PageBreak())

    # Balance Sheet
    story.append(Paragraph("Balance Sheet Summary", heading1_style))

    bs_data = [
        ['Assets', '2024', '2023'],
        ['Cash and Equivalents', '$4.2M', '$3.1M'],
        ['Accounts Receivable', '$2.8M', '$2.4M'],
        ['Inventory', '$1.9M', '$1.7M'],
        ['Property & Equipment', '$3.5M', '$3.2M'],
        ['Other Assets', '$0.6M', '$0.5M'],
        ['Total Assets', '$13.0M', '$10.9M'],
        ['', '', ''],
        ['Liabilities & Equity', '2024', '2023'],
        ['Accounts Payable', '$1.8M', '$1.5M'],
        ['Accrued Expenses', '$0.9M', '$0.8M'],
        ['Long-term Debt', '$2.0M', '$2.5M'],
        ['Shareholders Equity', '$8.3M', '$6.1M'],
        ['Total Liabilities & Equity', '$13.0M', '$10.9M'],
    ]

    bs_table = Table(bs_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch])
    bs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A5F')),
        ('BACKGROUND', (0, 8), (-1, 8), colors.HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 8), (-1, 8), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
    ]))
    story.append(bs_table)
    story.append(PageBreak())

    # Corporate Information
    story.append(Paragraph("Corporate Information", heading1_style))
    story.append(Paragraph("""
    TechCorp Industries was founded in 2015 with a mission to deliver innovative
    technology solutions that improve people's lives. Headquartered in San Francisco,
    California, we employ over 450 professionals across 12 countries.
    """, body_style))

    story.append(Paragraph("Board of Directors", heading2_style))
    story.append(Paragraph("""
    • Sarah Johnson - Chief Executive Officer
    • Michael Chen - Chief Financial Officer
    • Dr. Emily Rodriguez - Chief Technology Officer
    • James Williams - Independent Director
    • Patricia Lee - Independent Director
    """, body_style))

    story.append(Paragraph("Corporate Headquarters", heading2_style))
    story.append(Paragraph("""
    TechCorp Industries
    100 Innovation Way
    San Francisco, CA 94105
    United States

    Phone: +1 (555) 123-4567
    Email: investors@techcorp.com
    Web: www.techcorp.com
    """, body_style))

    # Build PDF
    doc.build(story)
    print("Created annual_report.pdf")


if __name__ == "__main__":
    create_annual_report()
