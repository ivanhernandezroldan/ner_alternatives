# NER Alternatives Comparison

This project performs a comparative analysis of different alternatives for Named Entity Recognition (NER) in the clinical domain (diseases, medications, symptoms), implementing and evaluating various approaches and tools available in the market.

## 📋 Table of Contents

- [Description](#description)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Docker](#docker)
- [License](#license)

## 🎯 Description

This repository contains an implementation and comparative analysis of different NER (Named Entity Recognition) solutions. The project includes an interactive web interface developed with Streamlit to visualize and compare the results of different NER models and approaches.

## 📁 Project Structure

```
.
├── src/                    # Source code
│   ├── app/               # Streamlit application
│   └── lib/               # Libraries and utilities
│       ├── utils/         # Utility functions and helpers
│       ├── test/          # Test files
│       ├── models/        # NER models implementations
│       ├── evaluation/    # Evaluation scripts and metrics
│       ├── preprocessing/ # Data preprocessing utilities
│       └── fine_tune/     # Model fine-tuning scripts
├── results/               # Comparative results and analysis
├── resources/             # Additional resources
├── ner_dataset/          # Training and evaluation datasets
├── MASTER_THESIS_REPORT.pdf  # Detailed project documentation
├── requirements.txt       # Project dependencies (Windows)
├── requirements_linux.txt # Project dependencies (Linux)
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore rules
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── .env                 # Environment variables (not included in git)
```

## 📋 Requirements

- Python 3.11.8
- Docker (optional)
- GPU compatible with PyTorch (recommended for better performance)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/[username]/ner_alternatives.git
cd ner_alternatives
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
# For Windows
pip install -r requirements.txt

# For Linux
pip install -r requirements_linux.txt
```

## 💻 Usage

To run the web application:

```bash
streamlit run src/app/app.py
```

The application will be available at `http://localhost:8501`

## 🐳 Docker

The project includes Docker support. To run the application in a container:

1. Build the image:
```bash
docker build -t ner-alternatives .
```

2. Run the container:
```bash
docker run -p 8501:8501 ner-alternatives
```

## 📄 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Developed with ❤️ for the NLP community
