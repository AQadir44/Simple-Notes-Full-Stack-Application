from .models import Note, Todo
from .schemas import NoteBaseSchema, ListNoteResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


# Search , Result Limiting , Pagination
# [...] get all records
@router.get('/')
def get_notes(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1)*limit

    notes = db.query(Note).filter(
        Note.title.contains(search)
    ).limit(limit).offset(skip).all()

    return {
        "status": 'success',
        'results': len(notes),
        "notes": notes
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteBaseSchema, db: Session = Depends(get_db)):

    note = Note(**payload.model_dump())

    db.add(note)

    db.commit()

    db.refresh(note)

    return {
        "status": 'success',
        "notes": note
    }


@router.patch('/{note_id}', status_code=status.HTTP_202_ACCEPTED)
def create_note(note_id : str , payload: NoteBaseSchema, db: Session = Depends(get_db)):

    note_query = db.query(Note).filter(Note.id == note_id)
    db_note = note_query.first()
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f'No note with this id : {note_id}')
    
    update_data = payload.model_dump(exclude_unset=True)
    
    note_query.filter(Note.id == note_id).update(update_data , synchronize_session=False)
    
    db.commit()
    
    db.refresh(db_note)
    return {
        "status": 'success',
        "notes": db_note
    }


@router.get('/{note_id}')
def get_post(note_id: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {note_id} found")
    return {"status": "success", "note": note}

@router.delete('/{note_id}')
def delete_post(note_id: str, db: Session = Depends(get_db)):
    note_query = db.query(Note).filter(Note.id == note_id)
    note = note_query.first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {id} found')
    note_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)