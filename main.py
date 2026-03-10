from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
import schemas
import auth


# Linea para asegurar que las tablas se creen al iniciar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vendor Management System")

# Funcion para conectar y cerrar la conexion a la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint 1: Obtiene la lista de todos los contratistas
@app.get("/contractors", response_model=list[schemas.Contractor])
def list_contractors(db: Session = Depends(get_db)):
    return db.query(models.Contractor).all()

# Endpoint 2: Crea un contratista con datos dinamicos desde la web
@app.post("/contractors/", response_model=schemas.Contractor)
def create_contractor(contractor: schemas.ContractorCreate, db: Session = Depends(get_db)):
    # Convertir los datos que recibimos (Pydantic) a modelo de base de datos (SQLAlchemy)
    nuevo_contratista = models.Contractor(**contractor.model_dump())

    db.add(nuevo_contratista)
    db.commit()
    db.refresh(nuevo_contratista)
    return nuevo_contratista

# Endpoint 3: Review del contratista
@app.post("/reviews/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Criterios de la review
    nueva_review = models.Review(**review.model_dump())
    db.add(nueva_review)
    db.commit()
    db.refresh(nueva_review)
    return nueva_review

# Endpoint 4: Permite al usuario editar/borrar informacion
@app.put("/contractors/{contractor_id}", response_model=schemas.Contractor)
def update_contractor(contractor_id: int, contractor_data: schemas.ContractorUpdate, db: Session = Depends(get_db)):
    # Busca al contratista por su ID
    db_contractor = db.query(models.Contractor).filter(models.Contractor.id == contractor_id).first()

    # Cuando no exista, lanza error 404
    if not db_contractor:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contratista no encontrado")
    
    # Actualizar solo los campos que el usuario envio
    update_data = contractor_data.model_dump(exclude_unset=True) # Solo toma lo que no es None
    for key, value in update_data.items():
        setattr(db_contractor, key, value) # Esto es como hacer db_contractor.name = value

    # Guardar cambios
    db.commit()
    db.refresh(db_contractor)
    return db_contractor

@app.delete("/contractors/{contractor_id}")
def delete_contractor(contractor_id: int, db: Session = Depends(get_db)):
    # Busca al contratista
    db_contractor = db.query(models.Contractor).filter(models.Contractor.id == contractor_id).first()

    # Cuando no exista, lanza error 404
    if not db_contractor:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Contratista no encontrado")
    
    # Borrar la sesion y confirmar en la DB
    db.delete(db_contractor)
    db.commit()

    return {"message": f"Contratista con ID {contractor_id} eliminado exitosamente."}

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hashear la contraseña antes de cualquier otra cosa
    hashed_pwd = auth.get_password_hash(user.password) # <-- Hash

    # Crea el objeto de usuario usando el hash, no la clave plana
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )

    # Guarda en la base de datos
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="El usuario o email ya existe") #TODO Cambia el idioma del texto a ingles
    
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca al usuario por username
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # Verifica si existe y si la contraseña es correcta
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Incorrect username of password")
    
    # Si todo esta bien, fabricar el token
    access_token = auth.create_acess_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}