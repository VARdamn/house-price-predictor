# House Price Predictor

## Setup

1. **Create virtual environment**

   - **Windows:**
     ```bash
     py -m venv venv
     ```
   - **Linux/MacOS:**
     ```bash
     python3 -m venv venv
     ```

2. **Activate the virtual environment**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/MacOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Install required packages**

   - **Windows:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Linux/MacOS:**
     ```bash
     python3 -m pip install -r requirements.txt
     ```

4. **Create `.env` file and fill it as in `.env.example`**

5. **Run project**

   - **Windows:**
     ```bash
     py main.py
     ```
   - **Linux/MacOS:**
     ```bash
     python3 main.py
     ```

## Linting & formatting

We are using `flake8` for linting and `black` for formatting.

To lint code:
```bash
flake8
```

To format most of issues:
```bash
black .
```
