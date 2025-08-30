import mysql.connector

# Ganti dengan user dan password MySQL lo
db_config = {
    'user': 'root', 
    'password': 'MySQLNafiRKA123',
    'host': '127.0.0.1'
}

# Nama database dan tabel yang akan dibuat
DATABASE_NAME = 'customer_db'
TABLE_NAME = 'customer_predictions'

# Kode untuk membuat koneksi dan cursor
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Membuat database jika belum ada
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    print(f"Database '{DATABASE_NAME}' berhasil dibuat atau sudah ada.")
    
    # Koneksi ulang dengan database yang baru dibuat
    conn.database = DATABASE_NAME

    # Membuat tabel jika belum ada
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Year_Birth INT,
        Income INT,
        Kidhome INT,
        Teenhome INT,
        Recency INT,
        MntWines INT,
        MntFruits INT,
        MntMeatProducts INT,
        MntFishProducts INT,
        MntSweetProducts INT,
        MntGoldProds INT,
        NumDealsPurchases INT,
        NumWebPurchases INT,
        NumCatalogPurchases INT,
        NumStorePurchases INT,
        NumWebVisitsMonth INT,
        AcceptedCmp3 INT,
        AcceptedCmp4 INT,
        AcceptedCmp5 INT,
        AcceptedCmp1 INT,
        AcceptedCmp2 INT,
        Complain INT,
        Response INT,
        cluster_id INT
    )
    """
    cursor.execute(create_table_query)
    print(f"Tabel '{TABLE_NAME}' berhasil dibuat atau sudah ada.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Setup database selesai!")

except mysql.connector.Error as err:
    print(f"Ada yang salah: {err}")