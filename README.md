# AI-Powered HR Hiring Backend

This project is a backend API for automating HR hiring and candidate evaluation workflows, powered by OpenAI's language models. It streamlines job description generation, resume screening, question generation, answer evaluation, and feedback email creation—all with the help of AI.

---

## Features

* Job Description Generator: Automatically generates tailored job descriptions.
* Resume Screening & Fit Scoring: Evaluates candidate resumes against job requirements.
* Screening Question Generator: Crafts relevant interview questions.
* Candidate Answer Evaluation: Assesses and scores candidate responses.
* Feedback Email Generator: Produces personalized acceptance/rejection emails.

---

## Stack

* Backend: Python, Flask
* AI Integration: OpenAI API (via openai-python SDK)
* Testing: pytest, unittest.mock
* Containerization: Docker (optional)
* Env Management: python-dotenv

---

## Getting Started

### 1. Clone the Repo

```
git clone [https://github.com/your-username/ai-hiring-backend.git](https://github.com/your-username/ai-hiring-backend.git)
cd ai-hiring-backend
```

---

### 2. Install Dependencies

Using venv:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following:
```
OPENAI\_API\_KEY=sk-xxxxxx         # Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
OPENAI\_MODEL=gpt-4o              # Or your preferred model
DEBUG=True
```
Note: Never commit your `.env` file to source control.

---

### 4. Run the Application

```
export FLASK\_APP=app
export FLASK\_ENV=development
flask run
```

The API will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

### 5. Using Docker (Optional)

Build the Docker image:
```
docker build -t ai-hiring-backend .
```

Run the container:
```
docker run --env-file .env -p 5000:5000 ai-hiring-backend
```
Docker will look for your `.env` file in the context directory.

---

### 6. API Endpoints

Here are the main routes (assume prefix `/`):

* POST `/generate-jd`: Generate job description.
  JSON body: `{ "title": "Backend Engineer", "seniority": "Senior", "skills": \["Python"], "location": "Remote" }`

* POST `/screen-resume`: Resume screening.
  multipart/form-data: resume file + job\_description (text)

* POST `/generate-questions`: Screening questions.
  JSON body: `{ "title": "Frontend Engineer", "skills": \["React"] }`

* POST `/evaluate`: Evaluate answers.
  JSON body: `{ "questions": "...", "answers": "..." }`

* POST `/generate-feedback`: Generate feedback email.
  JSON body: `{ "candidate\_name": "Jane", "job\_title": "Designer", "outcome": "rejected", "tone": "friendly" }`

---

### 7. Testing

All tests use pytest and mock OpenAI API calls for cost-effective, fast, and offline testing.

To run tests:
```
make pytest

# or, manually:

pytest
```

* Unit tests for openai\_service.py are fully mocked.
* Route tests (test\_ai\_routes.py) use Flask’s test client with mocks for all service functions.

---

## Mocking/OpenAI API

* All critical OpenAI calls are mocked during testing (no actual API calls are made in test runs).
* If you want to run integration tests against the real API, remove the mocks in the tests.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Open a Pull Request.

---

## License

MIT (or your choice)

---

Author:
Ahnaf Khan
Built for portfolio and practical AI HR automation!

