from fasthtml.fastapp import FastHTML
from fastapi.responses import HTMLResponse # FastHTML is built on Starlette/FastAPI
import os

# Determine the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static") # Conventionally, static files are in a 'static' folder
INDEX_HTML_PATH = os.path.join(BASE_DIR, "index.html")

# Initialize FastHTML application
# By default, FastHTML will look for a 'static' directory.
# If avatar.png is in the root, index.html will try to fetch /avatar.png
# We need to make sure such files are served.
# We can add a specific route for files in the root if necessary, or move them to 'static'
# and update index.html paths.

app = FastHTML(static_dir='.') # Serve static files from the current directory (includes avatar.png if in root)

@app.get("/")
async def get_index():
    try:
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, media_type="text/html")
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found</h1>", status_code=404, media_type="text/html")
    except Exception as e:
        return HTMLResponse(content=f"<h1>An error occurred: {str(e)}</h1>", status_code=500, media_type="text/html")

@app.get("/skills-content")
async def get_skills_content():
    # This data could come from a database or other dynamic source in a real app
    skills_data = [
        {"name": "Nuxt.js", "level": "Intermediate", "width": "90%", "color": "var(--color-trans-pink)"},
        {"name": "Web Design (Tailwindcss)", "level": "Still learning", "width": "75%", "color": "var(--color-trans-blue)"},
        {"name": "Pixel Art", "level": "Novice", "width": "60%", "color": "#70D870"},
        {"name": "Game Development (Godot)", "level": "Beginner", "width": "40%", "color": "#D8B870"},
    ]

    html_content = '<div class="space-y-5 p-4">'
    for skill in skills_data:
        html_content += f"""
        <div id="skill-{skill['name'].lower().replace(' ', '').replace('(', '').replace(')', '')}-container">
            <div class="flex justify-between items-center mb-1">
                <p class="pixel-art-font text-[var(--color-text-secondary)] text-lg font-medium">{skill['name']}</p>
                <p class="pixel-art-font text-[var(--color-text-primary)] text-sm font-medium">{skill['level']}</p>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {skill['width']}; background-color: {skill['color']};"></div>
            </div>
        </div>
        """
    html_content += '</div>'

    return HTMLResponse(content=html_content, media_type="text/html")

# To run this app:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Run with uvicorn: uvicorn main:app --reload

# Note: If avatar.png is meant to be in a /static/ directory,
# then index.html should reference it as /static/avatar.png
# and the FastHTML call would be app = FastHTML() assuming a 'static' folder exists.
# For now, app = FastHTML(static_dir='.') will serve files from the root.
# This means if index.html requests "avatar.png", the server will look for "avatar.png" in the root.
