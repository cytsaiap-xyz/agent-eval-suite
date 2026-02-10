# Problem 12: PowerPoint Presentation Generation

## Difficulty: Hard (Agentic)
## Expected Tool Calls: 12-25
## Skills Required: pptx creation, data visualization

## Task

Generate a professional PowerPoint presentation from structured data and specifications.

## Input Files

1. `presentation_spec.json` - Presentation structure and content
2. `sales_data.csv` - Data for charts
3. `brand_guidelines.json` - Colors, fonts, logo specs

## Requirements

Create `quarterly_review.pptx` with:

### Slide Structure (10 slides minimum)

1. **Title Slide**
   - Company name
   - Presentation title
   - Date and presenter name

2. **Agenda Slide**
   - Bulleted list of topics

3. **Executive Summary**
   - Key metrics in boxes/shapes
   - High-level takeaways

4. **Revenue Overview**
   - Bar chart comparing quarters
   - YoY growth percentage

5. **Regional Performance**
   - Pie chart of revenue by region
   - Key insights as bullet points

6. **Product Analysis**
   - Table with product metrics
   - Highlight top performer

7. **Customer Metrics**
   - Line chart showing NPS trend
   - Satisfaction callout box

8. **Challenges & Opportunities**
   - Two-column layout
   - Icons or shapes for visual interest

9. **Recommendations**
   - Numbered list
   - Priority indicators

10. **Q&A / Thank You**
    - Contact information
    - Company logo

### Design Requirements

- Consistent color scheme from brand_guidelines.json
- Proper font hierarchy (title, subtitle, body)
- Charts must be editable (not images)
- Slide numbers on all slides except title
- Company logo in footer/corner

### Chart Requirements

- Bar chart: Quarterly revenue comparison
- Pie chart: Regional breakdown
- Line chart: NPS trend over time
- All charts must have:
  - Clear titles
  - Legend
  - Data labels
  - Consistent colors

## Evaluation Criteria

| Criterion | Points |
|-----------|--------|
| All 10 slides present | 15 |
| Title slide correct | 5 |
| Charts render correctly | 20 |
| Tables formatted properly | 10 |
| Brand colors applied | 10 |
| Fonts consistent | 10 |
| Slide numbers present | 5 |
| Content matches spec | 15 |
| Overall professional look | 10 |
| **Total** | **100** |

## Hints

- Use python-pptx library
- Charts are created with chart_data objects
- Shapes can contain text frames
- Master slides control consistent formatting
- Colors use RGBColor objects
