# Task: Generate a Professional PowerPoint Presentation

Create a complete PowerPoint presentation from structured specifications and data.

## Input Files

1. `presentation_spec.json` - Defines slide structure and content
2. `sales_data.csv` - Data for charts
3. `brand_guidelines.json` - Colors, fonts, layout specs

## Your Task

Generate `quarterly_review.pptx` following the spec exactly.

## Requirements

### Slides to Create (10 total)

1. **Title Slide**
   - Main title, subtitle
   - Presenter name and date
   - Professional layout

2. **Agenda Slide**
   - Bulleted list of 7 topics
   - Clear, readable formatting

3. **Executive Summary**
   - 4 metric boxes (Revenue, Customers, NPS, Markets)
   - Each shows value and change percentage
   - 3 highlight bullet points

4. **Revenue Bar Chart**
   - Bar chart showing Q1-Q4 revenue
   - Proper axis labels
   - Data from sales_data.csv

5. **Regional Pie Chart**
   - Pie chart of revenue by region
   - Legend with percentages
   - Insight bullet points

6. **Product Table**
   - Table with 5 columns, 4 product rows
   - Header row styled differently
   - Highlight top performer

7. **NPS Line Chart**
   - Line chart showing monthly NPS trend
   - 12 data points (Jan-Dec)
   - Trend line visible

8. **Two-Column Challenges/Opportunities**
   - Split layout
   - 4 items each side
   - Visual distinction between columns

9. **Recommendations**
   - Numbered list
   - 5 items with priority indicators
   - Priority colors (High=red, Medium=orange, Low=green)

10. **Thank You/Q&A**
    - Centered layout
    - Contact information

### Design Requirements

- Apply colors from `brand_guidelines.json`
- Use specified fonts and sizes
- Slide numbers on slides 2-10
- Consistent margins
- Professional alignment

### Chart Specifications

All charts must:
- Be editable PowerPoint charts (not images)
- Have clear titles
- Include legends where appropriate
- Use brand colors for data series
- Have readable data labels

## Libraries

```bash
pip install python-pptx
```

## Key python-pptx Patterns

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# Create presentation
prs = Presentation()

# Add slide
slide_layout = prs.slide_layouts[6]  # blank
slide = prs.slides.add_slide(slide_layout)

# Add shape with text
shape = slide.shapes.add_shape(...)
shape.text_frame.text = "Hello"

# Add chart
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', [11.2, 12.1, 13.5, 14.4])
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
).chart
```

## Evaluation

Your presentation will be checked for:
- All 10 slides present with correct content
- Charts render with correct data
- Brand colors properly applied
- Font consistency
- Professional appearance
