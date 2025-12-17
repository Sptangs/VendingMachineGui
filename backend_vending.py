import mysql.connector
from typing import Dict, Any, Tuple, Optional

class VendingBackend:
    """Backend untuk operasi vending machine (transaksi pembelian)"""
    
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
    
    def get_all_products(self) -> Dict[str, Any]:
        """Mendapatkan semua produk untuk ditampilkan di vending machine"""
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
        """Mendapatkan detail produk berdasarkan ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, namaProduk, harga, gambar FROM products WHERE id=%s", 
                (product_id,)
            )
            product = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if product:
                return {
                    'success': True,
                    'id': product[0],
                    'nama': product[1],
                    'harga': product[2],
                    'gambar': product[3] if len(product) > 3 else None
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
    
    def process_purchase(self, product_id: int, coin: int) -> Dict[str, Any]:
        """Memproses transaksi pembelian"""
        try:
            if coin < 1000:
                return {
                    'success': False,
                    'message': 'Koin minimum adalah 1000'
                }
            
            product_result = self.get_product_by_id(product_id)
            
            if not product_result['success']:
                return product_result
            
            nama = product_result['nama']
            harga = product_result['harga']
            
            if coin < harga:
                return {
                    'success': False,
                    'message': f'Uang kurang Rp {harga - coin}',
                    'kurang': harga - coin
                }

            kembalian = coin - harga
            return {
                'success': True,
                'message': f'Berhasil membeli {nama}',
                'nama_produk': nama,
                'harga': harga,
                'coin': coin,
                'kembalian': kembalian
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def validate_coin(self, coin: int) -> Dict[str, Any]:
        """Validasi koin yang dimasukkan"""
        try:
            if coin < 1000:
                return {
                    'valid': False,
                    'message': 'Koin minimum adalah Rp 1000'
                }
            
            return {
                'valid': True,
                'coin': coin
            }
        except:
            return {
                'valid': False,
                'message': 'Format koin tidak valid'
            }
    
    def validate_product_id(self, product_id: int) -> Dict[str, Any]:
        """Validasi ID produk"""
        try:
            product_result = self.get_product_by_id(product_id)
            
            if product_result['success']:
                return {
                    'valid': True,
                    'product_id': product_id
                }
            else:
                return {
                    'valid': False,
                    'message': 'ID produk tidak ditemukan'
                }
        except:
            return {
                'valid': False,
                'message': 'Format ID produk tidak valid'
            }