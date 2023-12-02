
# Talon's imgui gui library is not accessible to screen readers. 
# By using HTML we can create temporary web pages that are accessible to screen readers.

import os
import tempfile
import webbrowser
from talon import cron

STYLE = """
<style>
    body { 
        background-color: #2E3440;
        margin: 0;
        padding: 0;
        font-family: 'Ubuntu Mono', monospace;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        box-sizing: border-box;
    }
    h1, p, h2, h3, ul, ol {
        color: #ECEFF4  ;
        margin: 20px 0;
    }
</style>
"""
import enum, contextlib

class ARIARole(enum.Enum):
    MAIN = "main"
    # roles TODO fill in



class HTMLBuilder:
    def __init__(self):
        self.elements = []

    def _flat_helper(self, text, tag, role=None):
        if role:
            self.elements.append(f"<{tag} role='{role.value}'>{text}</{tag}>")
        else:
            self.elements.append(f"<{tag}>{text}</{tag}>")

    def h1(self, text, role=None):
        self._flat_helper(text, "h1", role)
    
    def h2(self, text, role=None):
        self._flat_helper(text, "h2", role)
    
    def h3(self, text, role=None):
        self._flat_helper(text, "h3", role)

    def p(self, text, role=None):
        self._flat_helper(text, "p", role)
    
    def a(self, text, href, role=None):
        self.elements.append(f"<a href='{href}' role='{role.value}'>{text}</a>" if role else f"<a href='{href}'>{text}</a>")
        
    def _li(self, text):
        self._flat_helper(text, "li")

    def ul(self, *text, role=None):
        self.elements.append(f"<ul role='{role.value}'>" if role else "<ul>")

        for item in text:
            self._li(item)
        self.elements.append("</ul>")


    def ol(self, *text, role=None):
        self.elements.append(f"<ol role='{role.value}'>" if role else "<ol>")
        for item in text:
            self._li(item)
        self.elements.append("</ol>")


    def render(self):
        html_content = '\n'.join(self.elements)
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated HTML</title>
            {STYLE}
        </head>
        <body>
            <div class="container">
                {html_content}
            </div>
        </body>
        </html>
        """

        # Create a temporary file and write the HTML content
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as temp_file:
            temp_file.write(full_html)
            temp_file_path = temp_file.name

        # Open the temporary HTML file in the default web browser
        webbrowser.open(temp_file_path)
        # Delete it automatically after a while
        # cron.after("1000s", lambda: os.remove(temp_file_path))


builder = HTMLBuilder()
builder.h1("Hello World")
builder.h2("Hello World")
builder.h3("Hello World")
builder.ul("Hello", "World")
builder.h1("Article Heading", role=ARIARole.MAIN)
builder.p("This is a paragraph within the article")
builder.ol("Hello", "World")
builder.p("Hello World")
builder.render()

