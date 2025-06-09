![Get lost in this](istockphoto-672841286-612x612.jpg)

# simple_server

Generates a maze in an N x N x N cube of rooms and allows a user to navigate through the maze.

- Uses a cypher for room URLs to prevent cheating by manually editing URLs to skip through the maze.
- Guarantees only one solution from the start point to the end point.
- Save and load mazes.

---

## Table of Contents

- [Future Plans](#future-plans)
- [Disclaimer](#disclaimer)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Running the Tests](#running-the-tests)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Future Plans

- [ ] See the [issue log](https://github.com/ErikPohl444/simple_server/issues) for planned enhancements and bug fixes.

---

## Disclaimer

This project is under active development. Details and functionality might change as it evolves.

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.x installed on your system.
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Installing

1. Clone the repository:

   ```bash
   git clone https://github.com/ErikPohl444/simple_server.git
   cd simple_server
   ```

2. (Optional but recommended) Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

To run with Docker:

```bash
docker build -t simple_server .
docker run -p 8080:8080 simple_server
```

---

## Running the Tests

Tests are underway.  Check back soon.

---

## Technologies Used

- Python 3.x
- Flask
- Jinja2
- numpy
- Docker (optional)
- Unittest (for testing)

---

## Contributing

I'm excited to receive pull requests! For now, there are no strict contribution guidelines. Feel free to fork the repo, make your changes, and submit a pull request.

See the [Contribution Guidelines](CONTRIBUTING.md) for more details.

---

## Authors

| Author name | Author Email             | Entry date  |
|-------------|-------------------------|-------------|
| Erik Pohl   | erik.pohl.444@gmail.com | 06/08/2025  |

See the list of [contributors](https://github.com/ErikPohl444/simple_server/graphs/contributors) who have participated in this project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to everyone who has motivated me to learn more.
