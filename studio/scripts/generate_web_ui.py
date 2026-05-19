import json
import os
import sys

def generate_web_ui(json_path, output_path):
    if not os.path.exists(json_path):
        print(f"Error: JSON file {json_path} not found.")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    caption = data.get('prose_content', '') or data.get('content', {}).get('caption', '')
    paragraphs = [p for p in caption.split('\n') if p.strip()]

    theme = data.get('metadata', {}).get('theme', 'Adaptation')

    # HTML template with premium glassmorphism dark mode styling
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LND Studio - Web Reader</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f1115;
            --text-color: #e2e8f0;
            --accent-color: #8b5cf6;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.15), transparent 25%);
            background-attachment: fixed;
            color: var(--text-color);
            line-height: 1.8;
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }}

        .container {{
            max-width: 800px;
            width: 100%;
            margin: 40px 20px;
            padding: 50px 60px;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: fadeIn 0.8s ease-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        header {{
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 1px solid var(--glass-border);
        }}

        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            margin: 0 0 15px 0;
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }}

        .metadata-pill {{
            display: inline-block;
            padding: 6px 16px;
            background: rgba(139, 92, 246, 0.1);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 9999px;
            font-size: 0.85rem;
            color: #c4b5fd;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .prose-content {{
            font-size: 1.15rem;
            color: #cbd5e1;
        }}

        .prose-content p {{
            margin-bottom: 24px;
            text-align: justify;
            transition: color 0.3s ease;
        }}

        .prose-content p:hover {{
            color: #f8fafc;
        }}

        /* Styling dialogue differently */
        .dialogue {{
            color: #e2e8f0;
            font-weight: 400;
            padding-left: 20px;
            border-left: 3px solid var(--accent-color);
            margin: 30px 0;
            font-size: 1.2rem;
            background: linear-gradient(90deg, rgba(139, 92, 246, 0.05) 0%, transparent 100%);
            padding-top: 10px;
            padding-bottom: 10px;
        }}

        .sfx {{
            font-weight: 600;
            font-style: italic;
            color: #f472b6;
            text-align: center;
            margin: 30px 0;
            letter-spacing: 0.05em;
        }}

        @media (max-width: 768px) {{
            .container {{
                margin: 20px 10px;
                padding: 30px 20px;
            }}
            h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>I'll Collect Your Semen 4</h1>
            <div class="metadata-pill">Theme: {theme}</div>
        </header>
        <div class="prose-content">
"""

    for p in paragraphs:
        if p.startswith('「') and p.endswith('」'):
            html_content += f'            <div class="dialogue">{p}</div>\n'
        elif p.startswith('「'):
             html_content += f'            <div class="dialogue">{p}</div>\n'
        elif p.startswith('***') and p.endswith('***'):
            html_content += f'            <div class="sfx">{p}</div>\n'
        elif p.startswith('***'):
            html_content += f'            <div class="sfx">{p}</div>\n'
        else:
            html_content += f'            <p>{p}</p>\n'

    html_content += """        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Web UI successfully generated at: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate Web UI from LND Studio JSON output')
    parser.add_argument('--input', default='../../_out_lnd/gooner-alchemist/I_Will_Collect_Your_Semen_Series/artifact/draft-prose.json', help='Path to draft-prose.json')
    parser.add_argument('--output', default='../../_out_lnd/gooner-alchemist/I_Will_Collect_Your_Semen_Series/artifact/reader.html', help='Path to output HTML file')
    
    args = parser.parse_args()
    
    # Resolve paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, args.input)
    output_path = os.path.join(script_dir, args.output)
    
    generate_web_ui(input_path, output_path)
