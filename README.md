# Sheepllama-CLI 🐑

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue?logo=python&label=Python%20version%20required)](https://python.org/downloads/)

A blazing fast, minimalist command-line interface (CLI) tool for interacting with the Groq API using ultra-fast Llama models.

---

## 🔒 System Requirements

* **Python Constraints:** This tool **strictly requires Python 3.14 exclusively**. 
* Execution will instantly crash with an error message on 3.10, 3.11, 3.12, 3.13, or 3.15+.

---

## 🛠️ Installation

1. **Clone** the repository and **navigate** to your local project directory:
   ```bash
   git clone https://github.com/GhiQuat5/sheepllama-cli
   cd sheepllama-cli
   ```

2. **Install the package** using your Python 3.14 environment:
   ```bash
   pip install -e .
   ```

3. **Configure your Groq API Key**:
   ```bash
   export GROQ_API_KEY="your-actual-groq-api-key"
   ```

---

## 🚀 Usage

* **Interactive Session:**
  ```bash
  sheepllama
  ```
* **Quick Single Query:**
  ```bash
  sheepllama "Write a quick shell script to clean my system cache."
  ```
* **Piping Logs/Files:**
  ```bash
  cat error.log | sheepllama "Identify why this trace failed"
  ```
