from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from typing import List

from skin_cancer import predict_benmal
from skin_cancer import predict_disease_type

app = FastAPI()

# CORS configuration (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider limiting this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="lunarinspector_db"
        )
        return conn
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))

# POST endpoint to upload an image
@app.post("/upload_image/")
async def upload_image(
    file: UploadFile = File(...),
    user: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    uv: float = Form(...),
    polution: float = Form(...),
    state: str = Form(...)
):
    try:
        # Ensure the file is an image (basic check)
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

        # Save the file to the local filesystem
        file_location = f"images/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Insert the data into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO lunar_images (route, user, lat, lon, uv, polution, state)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (file_location, user, lat, lon, uv, polution, state))
        conn.commit()
        cursor.close()
        conn.close()


        prediction = predict_benmal(file_location)
        disease_type = {}
        if prediction == "maligno":
            disease_type = predict_disease_type(file_location)
        

        return {"filename": file.filename, "file_path": file_location, "skin_cancer": prediction, "disease_type":disease_type}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/get_images")
def get_images():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()  # Get a new connection for each request
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM lunar_images")  # Replace with your actual table name
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
