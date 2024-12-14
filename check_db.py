from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./data/glossary.db")

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM terms"))
    print("\nСписок всех терминов:")
    for row in result:
        print(f"ID: {row[0]}, Термин: {row[1]}, Описание: {row[2]}") 