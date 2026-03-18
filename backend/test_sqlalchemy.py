from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from env
database_url = os.getenv('DATABASE_URL')
print(f"Connecting with: {database_url}")

try:
    # Create engine
    engine = create_engine(database_url)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy connection successful!")
        
        # Check if we can see tables
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"Current tables: {tables}")
        
except Exception as e:
    print(f"❌ Error: {e}")