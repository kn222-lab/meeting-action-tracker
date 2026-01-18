from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Request,
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Request

from app.database import get_db
from app.models.meeting import Meeting
from app.models.action import Action
from app.schemas.meeting import MeetingCreate
from app.schemas.action import (
    ActionCreate,
    ActionResponse,
    ActionUpdate,
)
from fastapi.responses import HTMLResponse

from fastapi import Form
from fastapi.responses import RedirectResponse

from datetime import datetime, date
from starlette.middleware.sessions import SessionMiddleware


# --------------------
# App setup
# --------------------
app = FastAPI()

# static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# templates
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",  # 開発用でOK
)

# --------------------
# Root
# --------------------
@app.get("/")
def root():
    return {"message": "Meeting Action Tracker is running"}

# ==================================================
# API: Meetings
# ==================================================
@app.post("/meetings")
def create_meeting(
    meeting: MeetingCreate,
    db: Session = Depends(get_db)
):
    new_meeting = Meeting(
        title=meeting.title,
        meeting_date=meeting.meeting_date
    )
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


@app.get("/meetings")
def get_meetings(db: Session = Depends(get_db)):
    return db.query(Meeting).order_by(Meeting.meeting_date.desc()).all()


@app.get(
    "/meetings/{meeting_id}/actions",
    response_model=List[ActionResponse]
)
def get_actions_by_meeting(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return (
        db.query(Action)
        .filter(Action.meeting_id == meeting_id)
        .order_by(Action.due_date)
        .all()
    )

# ==================================================
# API: Actions
# ==================================================
@app.post("/actions")
def create_action(
    action: ActionCreate,
    db: Session = Depends(get_db)
):
    new_action = Action(
        meeting_id=action.meeting_id,
        content=action.content,
        due_date=action.due_date
    )
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action


@app.get("/actions", response_model=List[ActionResponse])
def get_actions(
    meeting_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Action)
    if meeting_id is not None:
        query = query.filter(Action.meeting_id == meeting_id)
    return query.all()


@app.patch("/actions/{action_id}")
def update_action(
    action_id: int,
    data: ActionUpdate,
    db: Session = Depends(get_db)
):
    action = db.query(Action).filter(Action.id == action_id).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")

    if data.content is not None:
        action.content = data.content
    if data.due_date is not None:
        action.due_date = data.due_date
    if data.status is not None:
        action.status = data.status

    db.commit()
    db.refresh(action)
    return action


@app.patch("/actions/{action_id}/complete")
def complete_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    action = db.query(Action).filter(Action.id == action_id).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")

    action.status = "完了"
    db.commit()
    db.refresh(action)
    return action


@app.delete("/actions/{action_id}")
def delete_action(
    action_id: int,
    db: Session = Depends(get_db)
):
    action = db.query(Action).filter(Action.id == action_id).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")

    db.delete(action)
    db.commit()
    return {"message": "Action deleted"}

# ==================================================
# UI Pages
# ==================================================
@app.get("/ui/meetings")
def meetings_page(
    request: Request,
    db: Session = Depends(get_db)
):
    meetings = db.query(Meeting).order_by(Meeting.meeting_date.desc()).all()
    return templates.TemplateResponse(
        "meetings.html",
        {
            "request": request,
            "meetings": meetings,
        }
    )


@app.get("/ui/meetings/{meeting_id}", response_class=HTMLResponse)
def meeting_detail_page(
    meeting_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")

    actions = (
        db.query(Action)
        .filter(Action.meeting_id == meeting_id)
        .order_by(Action.due_date)
        .all()
    )

    return templates.TemplateResponse(
        "meeting_detail.html",
        {
            "request": request,
            "meeting": meeting,
            "actions": actions,
        }
    )


@app.post("/ui/meetings/{meeting_id}/actions")
def create_action_ui(
    meeting_id: int,
    content: str = Form(...),
    due_date: str = Form(...),
    db: Session = Depends(get_db)
):
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()

    action = Action(
        meeting_id=meeting_id,
        content=content,
        due_date=due_date_obj,
        status="未着手"
    )

    db.add(action)
    db.commit()

    return RedirectResponse(
        url=f"/ui/meetings/{meeting_id}",
        status_code=303
    )



@app.post("/ui/meetings")
def create_meeting_ui(
    title: str = Form(...),
    meeting_date: str = Form(...),
    db: Session = Depends(get_db)
):
    meeting = Meeting(
        title=title,
        meeting_date=datetime.strptime(meeting_date, "%Y-%m-%d").date()
    )
    db.add(meeting)
    db.commit()

    return RedirectResponse("/ui/meetings", status_code=303)


@app.post("/ui/actions/{action_id}/toggle")
def toggle_action_status(
    action_id: int,
    db: Session = Depends(get_db)
):
    action = db.query(Action).get(action_id)
    if action:
        action.status = "完了" if action.status != "完了" else "未着手"
        db.commit()

    return RedirectResponse(
        f"/ui/meetings/{action.meeting_id}",
        status_code=303
    )


@app.post("/ui/actions/{action_id}/delete")
def delete_action_ui(
    action_id: int,
    db: Session = Depends(get_db)
):
    action = db.query(Action).get(action_id)
    if action:
        meeting_id = action.meeting_id
        db.delete(action)
        db.commit()
        return RedirectResponse(f"/ui/meetings/{meeting_id}", status_code=303)

    return RedirectResponse("/ui/meetings", status_code=303)


@app.post("/ui/meetings/{meeting_id}/delete")
def delete_meeting_ui(
    meeting_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # ① 先にアクション削除
    db.query(Action).filter(Action.meeting_id == meeting_id).delete()

    # ② 会議削除
    db.delete(meeting)
    db.commit()

    # フラッシュメッセージ
    request.session["flash"] = "会議を削除しました"

    return RedirectResponse(
        url="/ui/meetings",
        status_code=303
    )

