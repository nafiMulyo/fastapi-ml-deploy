import joblib 
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware # Tambahin ini

# Load pipeline yang sudah dilatih
try:
    pipeline = joblib.load('pipeline.joblib')
except FileNotFoundError:
    raise RuntimeError("pipeline.joblib not found. Pastikan file berada di direktori yang sama.")

# Kita gunakan daftar kolom yang sudah pasti benar,
# sesuai dengan saat kita melatih model.
FEATURE_COLS = [
    "Year_Birth", "Income", "Kidhome", "Teenhome", "Recency", "MntWines", 
    "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", 
    "MntGoldProds", "NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", 
    "NumStorePurchases", "NumWebVisitsMonth", "AcceptedCmp3", "AcceptedCmp4", 
    "AcceptedCmp5", "AcceptedCmp1", "AcceptedCmp2", "Complain", "Response"
]

# Tambahin kredensial MySQL lo di sini
db_config = {
    'user': 'root', 
    'password': 'MySQLNafiRKA123',
    'host': '127.0.0.1',
    'database': 'customer_db'
}

# Definisikan FastAPI app
app = FastAPI()

# Bagian baru yang harus lo tambahin: CORS Middleware
origins = ["*"] # Izinkan semua origin. Untuk deployment, ganti dengan URL spesifik.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Izinkan semua metode HTTP (GET, POST, dll)
    allow_headers=["*"], # Izinkan semua header
)

# Definisikan Pydantic model
class CustomerData(BaseModel):
    Year_Birth: int
    Income: int
    Kidhome: int
    Teenhome: int
    Recency: int
    MntWines: int
    MntFruits: int
    MntMeatProducts: int
    MntFishProducts: int
    MntSweetProducts: int
    MntGoldProds: int
    NumDealsPurchases: int
    NumWebPurchases: int
    NumCatalogPurchases: int
    NumStorePurchases: int
    NumWebVisitsMonth: int
    AcceptedCmp3: int
    AcceptedCmp4: int
    AcceptedCmp5: int
    AcceptedCmp1: int
    AcceptedCmp2: int
    Complain: int
    Response: int

@app.get('/')
def home():
    return {"message": "Customer Segmentation API mlaku boskuuu."}

@app.post('/predict')
def predict_customer(data: CustomerData):
    """
    Endpoint untuk prediksi cluster pelanggan.
    """
    try:
        # Konversi Pydantic model ke DataFrame dan pastikan urutan kolomnya benar
        df = pd.DataFrame([data.model_dump()])
        df = df[FEATURE_COLS]
        
        # Lakukan prediksi
        pred = pipeline.predict(df)
        cluster_id = int(pred[0])
        
        # Mulai proses simpan data ke MySQL
        try:
            # Koneksi ke database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Buat query SQL
            cols = FEATURE_COLS + ['cluster_id']
            placeholders = ', '.join(['%s'] * len(cols))
            query = f"INSERT INTO customer_predictions ({', '.join(cols)}) VALUES ({placeholders})"
            
            # Siapkan data
            values = [data.model_dump().get(col) for col in FEATURE_COLS]
            values.append(cluster_id)
            
            # Kirim perintah SQL dan simpan perubahan
            cursor.execute(query, tuple(values))
            conn.commit()
            
            cursor.close()
            conn.close()

            return {"cluster": cluster_id, "message": "Data berhasil diprediksi dan disimpan di MySQL."}
            
        except mysql.connector.Error as db_err:
            return {"error": str(db_err), "message": "Prediksi berhasil, tapi ada error saat menyimpan data ke database."}
        
    except Exception as e:
        return {"error": str(e), "message": "Terjadi error saat melakukan prediksi."}

@app.get('/data')
def get_all_data():
    """
    Endpoint untuk mengambil semua data dari tabel customer_predictions.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) # Menggunakan dictionary=True agar hasilnya dalam bentuk key-value pair
        
        query = "SELECT * FROM customer_predictions"
        cursor.execute(query)
        
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()

        return {"data": data}
    
    except mysql.connector.Error as db_err:
        return {"error": str(db_err), "message": "Gagal mengambil data dari database."}
