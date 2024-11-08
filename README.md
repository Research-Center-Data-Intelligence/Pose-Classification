# Project Setup

## Frontend
Navigate to the `frontend/` directory, install the dependencies, and run it:

```bash
npm install
npm run dev
```

## Backend API
### 1. Create and Activate Virtual Environment
Navigate to the `backend/` directory, create a virtual environment, and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
on Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies
After activating the virtual environment, install the required packages for the backend:
```bash
pip install -r requirements.txt
```


### 3. Run the Backend API
To run the backend API:
```bash
uvicorn api:app --reload
```

## Model
Navigate to the `model/` directory, create a virtual environment, and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```
on Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies
After activating the virtual environment, install the required packages for the model:
```bash
pip install -r requirements.txt
```