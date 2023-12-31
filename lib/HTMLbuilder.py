
# Talon's imgui gui library is not accessible to screen readers. 
# By using HTML we can create temporary web pages that are accessible to screen readers.

import tempfile
import webbrowser
import enum


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

class ARIARole(enum.Enum):
    MAIN = "main"
    BANNER = "banner"
    NAV = "navigation"
    FOOTER = "contentinfo"
    # TODO other roles?

class HTMLBuilder:

    '''
    Easily build HTML pages and add aria roles to elements
    in order to make them accessible to screen readers.
    '''

    def __init__(self):
        self.elements = []
        self.doc_title = "Generated Help Page from Talon"

    def _flat_helper(self, text, tag, role=None):
        if role:
            self.elements.append(f"<{tag} role='{role.value}'>{text}</{tag}>")
        else:
            self.elements.append(f"<{tag}>{text}</{tag}>")

    def title(self, text):
        self.doc_title = text

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
            <title>{self.doc_title}</title>
            {STYLE}
        </head>
        <body>
            <div class="container">
                {html_content}
            </div>
        </body>
        </html>
        """

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as temp_file:
            temp_file.write(full_html)
            temp_file_path = temp_file.name

        webbrowser.open(temp_file_path)

# API Demo
# builder = HTMLBuilder()
# builder.title("Generated Help Page from Talon")
# builder.h1("Banner Heading", role=ARIARole.BANNER)
# builder.h1("Header 1 for the page")
# builder.h2("Header 2")
# builder.h3("Smaller Header 3")
# builder.ul("Bullet 1", "Bullet number two")
# builder.p("This is a paragraph within the article", role=ARIARole.MAIN)
# builder.h2("Navigation Heading", role=ARIARole.NAV)
# builder.p("This is a paragraph within the article")
# builder.ol("First element: Hello", "Second one: World")
# builder.p("This is labeled as an aria footer within the article", role=ARIARole.FOOTER)
# builder.render()

