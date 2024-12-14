from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
from .migrations import run_migrations
from typing import List

app = FastAPI(
    title="Глоссарий API",
    description="""
    API сервис для управления глоссарием терминов. 
    
    ## Возможности
    
    * Получение списка всех терминов
    * Поиск термина по ключевому слову
    * Добавление новых терминов
    * Обновление существующих терминов
    * Удаление терминов
    
    ## Использование
    
    Документация доступна в двух форматах:
    * `/docs` - Swagger UI
    * `/redoc` - ReDoc
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

@app.on_event("startup")
async def startup_event():
    run_migrations()

database.Base.metadata.create_all(bind=database.engine)

@app.get(
    "/terms/",
    response_model=List[models.Term],
    summary="Получить список всех терминов",
    description="Возвращает список всех терминов в глоссарии с возможностью пагинации",
    response_description="Список терминов с их описаниями"
)
def get_terms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """
    Получить список всех терминов с пагинацией:
    
    - **skip**: количество пропускаемых терминов
    - **limit**: максимальное количество возвращаемых терминов
    """
    terms = db.query(schemas.TermModel).offset(skip).limit(limit).all()
    return terms

@app.get(
    "/terms/{term}",
    response_model=models.Term,
    summary="Получить информацию о термине",
    description="Возвращает подробную информацию о конкретном термине",
    responses={
        404: {
            "description": "Термин не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Термин не найден"}
                }
            }
        }
    }
)
def get_term(term: str, db: Session = Depends(database.get_db)):
    """
    Получить информацию о конкретном термине:
    
    - **term**: искомый термин
    """
    db_term = db.query(schemas.TermModel).filter(schemas.TermModel.term == term).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    return db_term

@app.post(
    "/terms/",
    response_model=models.Term,
    summary="Создать новый термин",
    description="Добавляет новый термин в глоссарий",
    status_code=201,
    responses={
        400: {
            "description": "Термин уже существует",
            "content": {
                "application/json": {
                    "example": {"detail": "Термин уже существует"}
                }
            }
        }
    }
)
def create_term(term: models.TermCreate, db: Session = Depends(database.get_db)):
    """
    Создать новый термин в глоссарии:
    
    - **term**: термин для добавления
    - **description**: описание термина
    """
    db_term = schemas.TermModel(**term.dict())
    db.add(db_term)
    try:
        db.commit()
        db.refresh(db_term)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Термин уже существует")
    return db_term

@app.put(
    "/terms/{term}",
    response_model=models.Term,
    summary="Обновить термин",
    description="Обновляет информацию о существующем термине",
    responses={
        404: {"description": "Термин не найден"},
        400: {"description": "Ошибка при обновлении"}
    }
)
def update_term(
    term: str,
    term_update: models.TermUpdate,
    db: Session = Depends(database.get_db)
):
    """
    Обновить существующий термин:
    
    - **term**: термин для обновления
    - **term_update**: новые данные для термина
    """
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

@app.delete(
    "/terms/{term}",
    summary="Удалить термин",
    description="Удаляет термин из глоссария",
    responses={
        404: {"description": "Термин не найден"},
        200: {
            "description": "Термин успешно удален",
            "content": {
                "application/json": {
                    "example": {"message": "Термин успешно удален"}
                }
            }
        }
    }
)
def delete_term(term: str, db: Session = Depends(database.get_db)):
    """
    Удалить термин из глоссария:
    
    - **term**: термин для удаления
    """
    db_term = db.query(schemas.TermModel).filter(schemas.TermModel.term == term).first()
    if db_term is None:
        raise HTTPException(status_code=404, detail="Термин не найден")
    
    db.delete(db_term)
    db.commit()
    return {"message": "Термин успешно удален"} 