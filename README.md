# DOM2React

Convert traditional HTML, CSS, and JavaScript websites into modern React + Vite projects.

DOM2React is a Python-based website migration tool designed to convert static websites into React applications with reusable components, page routing, styles, and copied assets.

## Features

- Convert HTML pages into React JSX
- Convert multiple HTML files into React pages
- Generate reusable components from common HTML sections
- Convert common HTML attributes to JSX syntax
- Copy CSS files and static assets
- Preserve original JavaScript files for manual migration
- Generate a React + Vite project structure
- Support React Router for multi-page websites

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

Run the converter:

```bash
python dom2react.py ./my-website --output ./my-react-app
```

Then install and start the generated React project:

```bash
cd my-react-app
npm install
npm run dev
```

## Project structure

```text
DOM2React/
├── dom2react.py
├── README.md
└── ...
```

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
