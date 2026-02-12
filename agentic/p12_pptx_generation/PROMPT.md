# Task: Generate a Professional PowerPoint Presentation

Create a complete PowerPoint presentation from structured specifications and data using the `/pptx` skill.

## Input Files

1. `presentation_spec.json` - Defines slide structure and content
2. `sales_data.csv` - Data for charts
3. `brand_guidelines.json` - Colors, fonts, layout specs

## Skills Available

You have access to the `/pptx` skill for PowerPoint operations. Use it to:
- Create new presentations from scratch
- Add slides with various layouts
- Insert charts, tables, and formatted text
- Apply professional design principles

Read the skill documentation carefully for:
- Design best practices (color palettes, typography)
- Chart creation patterns
- QA and verification steps

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

## Skill Usage Expectations

This task tests your ability to:
1. **Invoke the /pptx skill** and follow its guidance
2. **Apply design principles** from the skill documentation
3. **Use pptxgenjs patterns** for slide creation
4. **Perform QA verification** as specified in the skill
5. **Create professional visuals** following skill best practices

## Key Skill Concepts to Apply

From the `/pptx` skill, pay attention to:
- Color palette selection (don't default to generic blue)
- Typography guidelines (font sizes, hierarchy)
- Layout options (two-column, icon grids, etc.)
- QA requirements (convert to images, visual inspection)
- Common mistakes to avoid

## Evaluation

Your presentation will be checked for:
- Proper /pptx skill invocation
- All 10 slides present with correct content
- Charts render with correct data
- Brand colors properly applied
- Font consistency
- Professional appearance
- Evidence of QA process
