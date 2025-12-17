import mysql.connector
from typing import Optional, List, Dict, Any

class AdminBackend:
    """Backend untuk operasi admin (CRUD produk)"""
    
    def __init__(self, host='localhost', database='db_vendingmachine', 
                 user='root', password='', port=3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
    
    def get_connection(self):
        """Membuat koneksi ke database"""
        return mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )
    
    def authenticate_admin(self, username: str, password: str) -> bool:
        """Autentikasi admin"""
        return username == "admin" and password == "123"
    
    def add_product(self,id: float, nama: str, harga: float, gambar: str = None) -> Dict[str, Any]:
        """Menambah produk baru"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if gambar:
                query = "INSERT INTO products (id,namaproduk, harga, gambar) VALUES (%s, %s, %s, %s)"
                data = (id, nama, harga, gambar)
            else:
                query = "INSERT INTO products (id, namaproduk, harga) VALUES (%s, %s, %s)"
                data = (id, nama, harga)
            
            cursor.execute(query, data)
            conn.commit()
            product_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'message': 'Produk berhasil ditambahkan',
                'id': product_id
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def get_all_products(self) -> Dict[str, Any]:
        """Mendapatkan semua produk"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, namaproduk, harga, gambar FROM products")
            products = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'products': products
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'products': []
            }
    
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """Mendapatkan produk berdasarkan ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, namaproduk, harga, gambar FROM products WHERE id=%s", 
                          (product_id,))
            product = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if product:
                return {
                    'success': True,
                    'product': product
                }
            else:
                return {
                    'success': False,
                    'message': 'Produk tidak ditemukan'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def update_product(self, id_lama: int, id_baru: int, 
                      nama_baru: str, harga_baru: float) -> Dict[str, Any]:
        """Update produk"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE products
                SET id=%s, namaProduk=%s, harga=%s
                WHERE id = %s
            """
            data = (id_baru, nama_baru, harga_baru, id_lama)
            cursor.execute(query, data)
            conn.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                return {
                    'success': True,
                    'message': 'Produk berhasil diupdate'
                }
            else:
                return {
                    'success': False,
                    'message': 'Produk tidak ditemukan'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def delete_product(self, product_id: int) -> Dict[str, Any]:
        """Hapus produk"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM products WHERE id=%s"
            cursor.execute(query, (product_id,))
            conn.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            
            if affected_rows > 0:
                return {
                    'success': True,
                    'message': 'Produk berhasil dihapus'
                }
            else:
                return {
                    'success': False,
                    'message': 'Produk tidak ditemukan'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }