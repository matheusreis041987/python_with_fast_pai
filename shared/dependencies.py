from shared.database import SessionLocal


#forma de recuperar o db - abre e fecha a session com o DB
def get_db():
    db = SessionLocal()
    try:
        yield db #O yield funciona de forma parecida com um return, mas permite que o código continue executando depois.
    finally:
        db.close()