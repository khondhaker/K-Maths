import random
import io
from flask import Flask, request, make_response, render_template_string
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.lib import colors # Import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Math (Pre-K/G1)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen py-12">
    <div class="w-full max-w-md bg-white rounded-lg shadow-xl p-8">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
            Visual Math Generator
        </h1>
        <p class="text-center text-gray-600 mb-6">For K and Grade 1 (Numbers 0-10)</p>
        <p class="text-center text-gray-600 mb-6">Developed by Khondhaker Al Momin</p>
        
        <form action="/generate" method="POST">
            <div class="space-y-6">
                <div>
                    <label for="operation" class="block text-sm font-medium text-gray-700 mb-1">
                        Operation
                    </label>
                    <select id="operation" name="operation" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="+">Addition (+)</option>
                        <option value="-">Subtraction (-)</option>
                    </select>
                </div>
                
                <!-- 2. Page Count Option Added -->
                <div>
                    <label for="page_count" class="block text-sm font-medium text-gray-700 mb-1">
                        Pages
                    </label>
                    <select id="page_count" name="page_count" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="1">1 Page (18 Problems)</option>
                        <option value="2">2 Pages (36 Problems)</option>
                    </select>
                </div>
            </div>

            <div class="mt-8">
                <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-300">
                    Create Practice Sheet
                </button>
            </div>
        </form>
    </div>
</body>
</html>
"""

def draw_border(canvas, doc):
    """
    Draws a colorful flower border.
    """
    canvas.saveState()
    
    # --- 1. Define Border Colors ---
    border_colors = [
        colors.blue, colors.red, colors.green, colors.purple,
        colors.orange, colors.darkcyan, colors.magenta, colors.brown
    ]
    num_colors = len(border_colors)

    # --- 2. Background Removed ---
    width, height = letter
    # Page background removed for standard white
    
    # Get margins from the doc template
    left_margin = doc.leftMargin
    right_margin = doc.rightMargin
    top_margin = doc.topMargin
    bottom_margin = doc.bottomMargin

    # Set font
    canvas.setFont('ZapfDingbats', 14)
    
    # --- Symbol to repeat ---
    # \u273F is ✿ (BLACK FLORETTE)
    symbol = '\u273F'
    symbol_width = canvas.stringWidth(symbol, 'ZapfDingbats', 14)
    
    # --- 3. Draw Colorful Top and Bottom Borders ---
    x_positions = []
    current_x = left_margin - symbol_width / 2
    while current_x < (width - right_margin + symbol_width / 2):
        x_positions.append(current_x)
        current_x += symbol_width * 1.5 # Spacing
    
    for i, x in enumerate(x_positions):
        color = border_colors[i % num_colors] # Cycle colors
        canvas.setFillColor(color)
        canvas.drawString(x, height - top_margin + 18, symbol) # Top
        canvas.drawString(x, bottom_margin - 18, symbol)       # Bottom

    # --- 4. Draw Colorful Left and Right Borders ---
    y_positions = []
    current_y = bottom_margin
    while current_y < (height - top_margin + symbol_width):
        y_positions.append(current_y)
        current_y += symbol_width * 1.5 # Spacing

    for i, y in enumerate(y_positions):
        color = border_colors[i % num_colors] # Cycle colors
        canvas.setFillColor(color)
        canvas.drawString(left_margin - 24, y, symbol)  # Left
        canvas.drawString(width - right_margin + 12, y, symbol) # Right

    canvas.restoreState()


def create_worksheet_pdf(op_symbol, page_count):
    """
    Generates the visual math worksheet PDF in memory.
    """
    
    # --- Set Fixed Ranges ---
    top_min, top_max = 0, 10
    bottom_min, bottom_max = 0, 10
    
    all_possible_problems = []
    used_problems = set()
    
    for a in range(top_min, top_max + 1):
        for b in range(bottom_min, bottom_max + 1):
            
            # --- 1. Conditional Rule Change ---
            # Apply rule only for subtraction
            if op_symbol == '-' and a < b:
                continue
                
            problem_pair = (a, b)
            
            if problem_pair not in used_problems:
                all_possible_problems.append(problem_pair)
                used_problems.add(problem_pair)

    if not all_possible_problems:
        return None 

    # --- 2. Page Count Change ---
    num_to_generate = 18 if page_count == 1 else 36
    
    # Ensure we have enough problems, if not, just use what we have
    while len(all_possible_problems) < num_to_generate:
        # If not enough unique problems, we just use the max available
        # To avoid an infinite loop, we'll just use the list we have.
        # For a 0-10 range, we have plenty.
        break 
        
    random.shuffle(all_possible_problems)
    problems = all_possible_problems[:num_to_generate]
    num_problems = len(problems)
    
    # --- Define Color Pairs ---
    color_pairs = [
        (colors.blue, colors.red),
        (colors.green, colors.purple),
        (colors.orange, colors.darkcyan),
        (colors.magenta, colors.brown),
    ]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # --- Add the border function to the document ---
    doc.onFirstPage = draw_border
    doc.onLaterPages = draw_border
    
    story = []
    
    styles = getSampleStyleSheet()
    
    # Style for Name/Date Header
    style_header = styles['Normal']
    style_header.fontName = 'Times-Roman'
    style_header.fontSize = 13
    
    # Style for the problem numbers (e.g., "5", "+ 6")
    style_problem_num = ParagraphStyle(
        'ProblemNum',
        parent=style_header,
        alignment=TA_RIGHT,
        fontSize=17,
    )
    
    # Style for the visual bars (e.g., "{ ||| }")
    style_problem_bars = ParagraphStyle(
        'ProblemBars',
        fontName='Courier', # Monospaced font for even bars
        fontSize=13,
        alignment=TA_LEFT,
        leading=14, # Line spacing
        textColor=black, # Ensure brackets are black
    )
    
    header_data = [
        [Paragraph("Name: ____________________", style_header), Paragraph("Score: ____________________", style_header)]
    ]
    header_table = Table(header_data, colWidths=[3.5 * inch, 3.5 * inch])
    header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (0, 0), (-1, -1), 'LEFT')]))
    story.append(header_table)
    story.append(Spacer(1, 0.4 * inch))

    problem_cells = []
    
    # --- Create each problem cell ---
    for i, (a, b) in enumerate(problems):
        # Get color pair for this problem
        color_top, color_bottom = color_pairs[i % len(color_pairs)]
        
        # Generate bar strings (bars only)
        a_bars = '|' * a
        a_padding = ' ' * (10 - a)
        b_bars = '|' * b
        b_padding = ' ' * (10 - b)

        # Use HTML-like <font> tags to set color *inside* black brackets
        if a == 0:
            a_bar_html = f'{{ {" " * 10} }}'
        else:
            a_bar_html = f'{{ <font color="{color_top.hexval()}">{a_bars}</font>{a_padding} }}'
        
        if b == 0:
            b_bar_html = f'{{ {" " * 10} }}'
        else:
            b_bar_html = f'{{ <font color="{color_bottom.hexval()}">{b_bars}</font>{b_padding} }}'

        # Set number color, keeping operator black
        a_num_html = f'<font color="{color_top.hexval()}">{a}</font>'
        b_num_html = f'{op_symbol} <font color="{color_bottom.hexval()}">{b}</font>' # Operator is now black

        problem_data = [
            [Paragraph(a_num_html, style_problem_num), Paragraph(a_bar_html, style_problem_bars)],
            [Paragraph(b_num_html, style_problem_num), Paragraph(b_bar_html, style_problem_bars)],
        ]
        
        problem_table = Table(problem_data, colWidths=[0.6 * inch, 1.7 * inch])
        problem_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'), # Numbers column
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Bars column
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            # --- 3. Horizontal Line Fix ---
            # Draw a black line under row 1, *only* spanning column 0
            ('LINEBELOW', (0, 1), (0, 1), 1, black), 
            # Add padding below the line for the answer space
            ('BOTTOMPADDING', (0, 1), (1, 1), 8), 
        ]))
        problem_cells.append(problem_table)

    # --- Arrange problems in 3xN grid ---
    # This logic will automatically create as many rows as needed,
    # and SimpleDocTemplate will handle the page break.
    problem_grid_data = []
    empty_row = [None] * 3
    row_heights = []
    problem_row_height = 1.0 * inch # Taller rows for visual problems
    spacer_row_height = 0.4 * inch
    
    num_rows = (num_problems + 2) // 3 # Calculate needed rows (for 3 columns)

    for i in range(num_rows):
        start_index = i * 3
        end_index = min(start_index + 3, num_problems)
        
        row_cells = problem_cells[start_index:end_index]
        
        if len(row_cells) < 3:
            row_cells.extend([None] * (3 - len(row_cells)))
            
        problem_grid_data.append(row_cells)
        row_heights.append(problem_row_height)
        
        # Add a spacer row, but not after the very last row
        if i < (num_rows - 1):
             # Check if we are at the 6th row (index 5) to add extra space for page break
             if (i + 1) % 6 == 0:
                 problem_grid_data.append(empty_row)
                 row_heights.append(0.8 * inch) # Extra space before page break
             else:
                 problem_grid_data.append(empty_row)
                 row_heights.append(spacer_row_height)

    main_grid_table = Table(problem_grid_data, 
                            colWidths=[2.4 * inch] * 3, # 3 wider columns
                            rowHeights=row_heights)
                            
    main_grid_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    
    story.append(main_grid_table)
    
    # --- Build PDF without footer ---
    doc.build(story)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


@app.route('/')
def index():
    """Serves the main HTML dashboard page."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate', methods=['POST'])
def generate_pdf():
    """
    Handles the form submission, generates the PDF,
    and sends it to the user for download.
    """
    try:
        op_symbol = request.form.get('operation')
        # --- 2. Get Page Count ---
        page_count = int(request.form.get('page_count', 1))

        pdf_data = create_worksheet_pdf(op_symbol, page_count)

        if pdf_data is None:
            error_message = (
                "Error: No unique problems could be generated."
            )
            return render_template_string(
                f"""
                <script>
                    alert("{error_message}");
                    window.history.back();
                </script>
                """
            ), 400

        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=visual_math_sheet.pdf'
        
        return response

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return "An error occurred while generating the PDF.", 500


if __name__ == "__main__":
    print("Starting Flask server for Visual Math Sheet...")
    print("Open this URL in your browser: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

