import argparse
import re
import shutil
from pathlib import Path
from html.parser import HTMLParser


class HTMLToJSX(HTMLParser):
    """Convert common HTML syntax into JSX."""

    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr",
        "img", "input", "link", "meta", "param",
        "source", "track", "wbr"
    }

    ATTR_REPLACEMENTS = {
        "class": "className",
        "for": "htmlFor",
        "tabindex": "tabIndex",
        "readonly": "readOnly",
        "maxlength": "maxLength",
        "cellpadding": "cellPadding",
        "cellspacing": "cellSpacing",
        "colspan": "colSpan",
        "rowspan": "rowSpan",
        "autofocus": "autoFocus",
        "autocomplete": "autoComplete",
        "contenteditable": "contentEditable",
        "spellcheck": "spellCheck",
        "crossorigin": "crossOrigin",
        "srcset": "srcSet",
    }

    EVENT_RE = re.compile(r"^on([a-z]+)$", re.IGNORECASE)

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        self.output.append("<" + tag)

        for name, value in attrs:
            name = name.lower()
            name = self.ATTR_REPLACEMENTS.get(name, name)

            match = self.EVENT_RE.match(name)
            if match:
                event_name = match.group(1).capitalize()
                name = "on" + event_name

                if value:
                    value = value.replace('"', '\\"')
                    self.output.append(
                        f' {name}={{() => {{ {value}; }}}}'
                    )
                continue

            if value is None:
                self.output.append(f" {name}={{true}}")
            else:
                value = value.replace("{", "&#123;")
                value = value.replace("}", "&#125;")
                self.output.append(f' {name}="{value}"')

        if tag in self.VOID_TAGS:
            self.output.append(" />")
        else:
            self.output.append(">")
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag not in self.VOID_TAGS:
            self.output.append(f"</{tag}>")
            self.depth = max(0, self.depth - 1)

    def handle_data(self, data):
        self.output.append(data)

    def handle_comment(self, data):
        self.output.append(f"{{/* {data} */}}")

    def get_jsx(self):
        return "".join(self.output).strip()


def extract_body(html):
    """Remove the document wrapper and keep the body content."""
    match = re.search(
        r"<body[^>]*>(.*?)</body>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return html.strip()


def extract_css_links(html):
    """Find external CSS files referenced by HTML."""
    return re.findall(
        r'<link[^>]+href=["\']([^"\']+\.css)["\']',
        html,
        flags=re.IGNORECASE
    )


def remove_scripts(html):
    """Remove script tags from the HTML body."""
    return re.sub(
        r"<script\b[^>]*>.*?</script>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )


def convert_html_to_jsx(html):
    html = extract_body(html)
    html = remove_scripts(html)

    parser = HTMLToJSX()
    parser.feed(html)

    return parser.get_jsx()


def copy_assets(source_dir, output_dir):
    """Copy common website assets into public/."""
    public_dir = output_dir / "public"
    public_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.iterdir():
        if item.name in {
            "index.html",
            "src",
            "node_modules",
            ".git",
            "dist"
        }:
            continue

        if item.is_dir():
            destination = public_dir / item.name
            shutil.copytree(item, destination, dirs_exist_ok=True)

        elif item.suffix.lower() in {
            ".css", ".js", ".jsx", ".html", ".htm"
        }:
            continue

        else:
            shutil.copy2(item, public_dir / item.name)


def find_css_file(source_dir, html):
    """Find the first CSS file referenced by HTML."""
    links = extract_css_links(html)

    for link in links:
        css_path = source_dir / link
        if css_path.exists():
            return css_path

    css_files = list(source_dir.glob("*.css"))
    return css_files[0] if css_files else None


def create_react_project(source_dir, output_dir):
    source_dir = Path(source_dir).resolve()
    output_dir = Path(output_dir).resolve()

    html_file = source_dir / "index.html"

    if not html_file.exists():
        raise FileNotFoundError(
            "index.html was not found in the input folder."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    src_dir = output_dir / "src"
    src_dir.mkdir(exist_ok=True)

    html = html_file.read_text(encoding="utf-8")
    jsx = convert_html_to_jsx(html)

    css_file = find_css_file(source_dir, html)

    if css_file:
        css = css_file.read_text(encoding="utf-8")
    else:
        css = "/* Add your CSS here */\n"

    app_jsx = f'''import "./App.css";

function App() {{
  return (
    <>
      {jsx}
    </>
  );
}}

export default App;
'''

    main_jsx = '''import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
'''

    package_json = '''{
  "name": "converted-react-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^6.0.0"
  }
}
'''

    vite_config = '''import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()]
});
'''

    index_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Converted React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
'''

    (src_dir / "App.jsx").write_text(app_jsx, encoding="utf-8")
    (src_dir / "main.jsx").write_text(main_jsx, encoding="utf-8")
    (src_dir / "App.css").write_text(css, encoding="utf-8")
    (output_dir / "package.json").write_text(package_json, encoding="utf-8")
    (output_dir / "vite.config.js").write_text(vite_config, encoding="utf-8")
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    copy_assets(source_dir, output_dir)

    js_files = list(source_dir.glob("*.js"))

    if js_files:
        legacy_dir = output_dir / "legacy-js"
        legacy_dir.mkdir(exist_ok=True)

        for js_file in js_files:
            shutil.copy2(js_file, legacy_dir / js_file.name)

    print(f"React project created: {output_dir}")
    print("Next steps:")
    print(f"  cd {output_dir}")
    print("  npm install")
    print("  npm run dev")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a basic HTML/CSS/JS website into a React project."
    )

    parser.add_argument(
        "input",
        help="Folder containing index.html"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="converted-react-app",
        help="Output React project folder"
    )

    args = parser.parse_args()

    create_react_project(args.input, args.output)


if __name__ == "__main__":
    main()
