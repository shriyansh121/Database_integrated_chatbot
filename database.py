import mysql.connector
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from db_config import DB_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            logger.info("Successfully connected to MySQL database")
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to MySQL: {err}")
            self.connection = None
    
    def is_connected(self) -> bool:
        """Check if database connection is active"""
        if self.connection and self.connection.is_connected():
            return True
        return False
    
    def reconnect_if_needed(self):
        """Reconnect if connection is lost"""
        if not self.is_connected():
            logger.info("Reconnecting to database...")
            self.connect()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[pd.DataFrame]:
        """Execute a SQL query and return results as DataFrame"""
        try:
            self.reconnect_if_needed()
            if not self.is_connected():
                logger.error("Cannot execute query: database not connected")
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if results:
                    df = pd.DataFrame(results)
                    return df
                else:
                    return pd.DataFrame()
            else:
                self.connection.commit()
                logger.info(f"Query executed successfully: {cursor.rowcount} rows affected")
                return None
                
        except mysql.connector.Error as err:
            logger.error(f"Error executing query: {err}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def get_table_schema(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """Get schema information for a specific table"""
        try:
            self.reconnect_if_needed()
            if not self.is_connected():
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(f"DESCRIBE {table_name}")
            schema = cursor.fetchall()
            cursor.close()
            return schema
        except mysql.connector.Error as err:
            logger.error(f"Error getting table schema: {err}")
            return None
    
    def get_all_tables(self) -> Optional[List[str]]:
        """Get list of all tables in the database"""
        try:
            self.reconnect_if_needed()
            if not self.is_connected():
                return None
            
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            return tables
        except mysql.connector.Error as err:
            logger.error(f"Error getting tables: {err}")
            return None
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            self.reconnect_if_needed()
            if self.is_connected():
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                return True
            return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

# Global database manager instance
db_manager = DatabaseManager() 