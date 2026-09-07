# DOM2React

Convert traditional HTML, CSS, and JavaScript websites into modern React + Vite projects.

DOM2React is a Python-based website migration tool designed to convert multi-page static websites into React applications with reusable components, page routing, styles, and copied assets.

## Features

- Convert HTML pages into React JSX
- Convert multiple HTML files into React pages
- Generate reusable components from common HTML sections
- Convert common HTML attributes to JSX syntax
- Copy CSS files and static assets
- Preserve original JavaScript files for manual migration
- Generate a React + Vite project structure
- Support React Router for multi-page websites

## Planned conversion structure

```text
input-website/
├── index.html
├── about.html
├── contact.html
├── css/
├── js/
└── images/
```

Output:

```text
converted-react-app/
├── index.html
├── package.json
├── vite.config.js
├── public/
│   └── images/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Navbar.jsx
│   │   └── Footer.jsx
│   └── pages/
│       ├── Home.jsx
│       ├── About.jsx
│       └── Contact.jsx
└── legacy-js/
```

## Requirements

- Python 3.9 or newer
- Node.js and npm

## Installation

Clone the repository:

```bash
git clone https://github.com/vyasanbmathew2008/DOM2React.git
cd DOM2React
```

## Usage

The planned command-line interface is:

```bash
python html_to_react.py ./my-website --output ./my-react-app
```

Then install the generated React project dependencies:

```bash
cd my-react-app
npm install
npm run dev
```

## Conversion example

Input:

```html
<section id="hero">
  <h1>Welcome</h1>
  <p>This is my website.</p>
</section>
```

Generated React component:

```jsx
function Hero() {
  return (
    <section id="hero">
      <h1>Welcome</h1>
      <p>This is my website.</p>
    </section>
  );
}

export default Hero;
```

## JavaScript migration

HTML and CSS can usually be converted automatically, but JavaScript that directly manipulates the DOM may require manual migration to React state, props, and effects.

For example, DOM manipulation such as:

```js
document.getElementById("message").innerText = "Hello";
```

is normally rewritten using React state:

```jsx
const [message, setMessage] = useState("");
```

DOM2React preserves original JavaScript files when automatic conversion is not safe.

## Project status

DOM2React is under development. The goal is to provide reliable automatic conversion for static websites while keeping generated React code readable and easy to edit.

## Roadmap

- [ ] Multi-page HTML conversion
- [ ] Automatic reusable component detection
- [ ] React Router generation
- [ ] CSS and asset path conversion
- [ ] Inline event-handler conversion
- [ ] Better JavaScript-to-React migration
- [ ] Configuration file for custom component names
- [ ] CLI options and conversion reports
- [ ] Conversion validation and error reporting

## Contributing

Contributions, suggestions, and issue reports are welcome. Please open an issue or submit a pull request.

## License

This project is currently unlicensed. Add a license before distributing the project publicly.
