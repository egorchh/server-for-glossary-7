from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from .migrations import run_migrations
from typing import List

app = FastAPI(title="Глоссарий API")

@app.on_event("startup")
async def startup_event():
    run_migrations()

database.Base.metadata.create_all(bind=database.engine)

@app.get("/terms/", response_model=List[models.Term])
def get_terms(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    terms = db.query(schemas.TermModel).offset(skip).limit(limit).all()
    return terms

@app.get("/terms/{term}", response_model=models.Term)
def get_term(term: str, db: Session = Depends(database.get_db)):
    db_term = db.query(schemas.TermModel).filter(schemas.TermModel.term == term).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return db_term

@app.post("/terms/", response_model=models.Term)
def create_term(term: models.TermCreate, db: Session = Depends(database.get_db)):
    db_term = schemas.TermModel(**term.dict())
    db.add(db_term)
    try:
        db.commit()
        db.refresh(db_term)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Термин уже существует")
    return db_term

@app.put("/terms/{term}", response_model=models.Term)
def update_term(term: str, term_update: models.TermUpdate, db: Session = Depends(database.get_db)):
    db_term = db.query(schemas.TermModel).filter(schemas.TermModel.term == term).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    
    update_data = term_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_term, key, value)
    
    try:
        db.commit()
        db.refresh(db_term)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при обновлении")
    return db_term

@app.delete("/terms/{term}")
def delete_term(term: str, db: Session = Depends(database.get_db)):
    db_term = db.query(schemas.TermModel).filter(schemas.TermModel.term == term).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    
    db.delete(db_term)
    db.commit()
    return {"message": "Термин успешно удален"} 