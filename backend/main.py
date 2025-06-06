from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import json
import mysql.connector
import os
import urllib.parse

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "kastro_exam_db")
    )

@app.get("/", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/select-tool", response_class=HTMLResponse)
async def select_tool(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    email: str = Form(...)
):
    return templates.TemplateResponse("select_tool.html", {
        "request": request,
        "name": name,
        "age": age,
        "gender": gender,
        "email": email
    })

@app.post("/start-exam", response_class=HTMLResponse)
async def start_exam(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    tool: str = Form(...)
):
    tool_name = "AWS" if tool == "aws" else "DevOps"
    question_file = f"questions/{tool}_questions.json"

    try:
        with open(question_file, "r") as f:
            questions = json.load(f)
            random.shuffle(questions)
            selected_questions = questions[:10]
    except FileNotFoundError:
        return HTMLResponse("Question file not found", status_code=404)

    user_data = urllib.parse.quote(json.dumps({
        "name": name,
        "age": age,
        "gender": gender,
        "email": email
    }))

    return templates.TemplateResponse("exam_page.html", {
        "request": request,
        "questions": selected_questions,
        "tool": tool,
        "tool_name": tool_name,
        "user_data": user_data
    })

@app.post("/submit-exam", response_class=HTMLResponse)
async def submit_exam(request: Request):
    form = await request.form()
    user_data = json.loads(urllib.parse.unquote(form.get("user_data", "{}")))
    tool = form.get("tool")
    question_file = f"questions/{tool}_questions.json"

    try:
        with open(question_file, "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        return HTMLResponse("Question file not found", status_code=404)

    answers_dict = {q["id"]: q["answer"] for q in questions}
    score = 0

    for key in form:
        if key.startswith("q"):
            try:
                qid = int(key[1:])
                if form[key] == answers_dict.get(qid):
                    score += 1
            except ValueError:
                pass

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO results (name, age, gender, email, tool, score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_data.get("name"), user_data.get("age"), user_data.get("gender"),
              user_data.get("email"), tool, score))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return HTMLResponse(f"Database error: {e}", status_code=500)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "name": user_data.get("name"),
        "tool": tool.upper() if tool else "UNKNOWN",
        "score": score
    })
