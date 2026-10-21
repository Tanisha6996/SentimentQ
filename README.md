
# SentimentQ 🧠⚛️

**Quantum Computing × Natural Language Processing for Mental Health Tweet Analysis**

SentimentQ combines **Grover's quantum search algorithm** with **VADER sentiment analysis** to explore the identification and sentiment analysis of mental-health-related tweets.

The project investigates how quantum search techniques can complement classical NLP workflows, bringing together quantum computing, text processing, and sentiment analysis.

## 🎯 Objectives

- Explore the application of quantum computing to large-scale text search.
- Implement Grover's algorithm for searching relevant records.
- Apply VADER sentiment analysis to mental-health-related tweets.
- Investigate the intersection of quantum computing and Natural Language Processing (NLP).
- Evaluate the performance of the search workflow on a dataset containing over 3 million tweets.

## ⚙️ Methodology

### 1. Quantum Search using Grover's Algorithm

Grover's algorithm is a quantum search algorithm that uses amplitude amplification to locate target states in an unstructured search space. Its theoretical query complexity is quadratic in the number of candidates, compared with classical exhaustive search.

In SentimentQ, Grover's algorithm is applied to the search component of the mental-health tweet analysis workflow.

### 2. Sentiment Analysis using VADER

VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon- and rule-based sentiment analysis tool designed for social media text.

It estimates sentiment polarity and intensity, enabling the analysis of textual content without requiring a separately trained deep-learning model.

### 3. Integrating Quantum Search and NLP

The project combines quantum search techniques with classical sentiment analysis to explore the identification and interpretation of relevant tweets.

This hybrid approach investigates the potential role of quantum algorithms in search-intensive text-analysis workflows.

## 🚀 Performance Results

The project reported a reduction in processing time for a dataset containing over **3 million tweets**.

| Metric | Reported result |
|---|---:|
| Dataset size | Over 3 million tweets |
| Original processing time | 32 seconds |
| New processing time | 0.01 seconds |

The speedup is calculated as the ratio of the original processing time to the new processing time.

**Benchmark note:** These figures represent the reported timings for the implemented workflow. The measured operation, execution environment, and whether quantum circuit simulation, hardware execution, and preprocessing are included should be documented when reporting the result as an end-to-end performance improvement.

## 🛠️ Technologies Used

- **Python**
- **Qiskit**: Quantum computing and quantum circuit implementation
- **VADER Sentiment**: Lexicon-based sentiment analysis
- **NumPy**: Numerical computation

## 📦 Getting Started

### Clone the Repository

```bash
git clone https://github.com/Tanisha6996/SentimentQ.git
cd SentimentQ
```

### Install Dependencies

Install the libraries required by the implementation. For example:

```bash
pip install numpy qiskit vaderSentiment
```

Additional dependencies or specific package versions may be required depending on the source files.

### Run the Project

Open the relevant Python script or Jupyter Notebook in the repository and follow the execution instructions provided in the code.

## ⚠️ Limitations

- Practical quantum performance depends on the search formulation, oracle construction, execution platform, and associated overhead.
- The reported speedup should be interpreted in the context of the specific benchmark performed.
- VADER estimates linguistic sentiment and does not diagnose or determine an individual's mental health.
- Social media text can be ambiguous, context-dependent, and noisy.

## 🔭 Future Directions

- Compare the quantum search workflow with classical search baselines under equivalent conditions.
- Evaluate performance across different dataset sizes.
- Investigate the effects of circuit simulation and quantum execution overhead.
- Explore alternative NLP methods for analysing social media text.

## 👩‍💻 Author

**Tanisha Das**

[GitHub Profile](https://github.com/Tanisha6996)

---

*An exploration of quantum algorithms and classical NLP for large-scale text analysis.*
