#!/usr/bin/env python3
"""
Database Setup Script for NetOne AI Assistant
Run this script to create all tables and initial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import engine, Base
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        
        # Log connection info (without password)
        logger.info(f"Connecting to: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE} as {settings.MYSQL_USER}")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully!")
        
        # Optional: Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables in database: {tables}")
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        raise

def drop_tables():
    """Drop all tables (use with caution!)"""
    try:
        logger.warning("⚠️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Tables dropped successfully!")
    except Exception as e:
        logger.error(f"❌ Error dropping tables: {e}")
        raise

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database setup for NetOne AI Assistant")
    parser.add_argument("--reset", action="store_true", help="Reset database (drop and recreate)")
    parser.add_argument("--create", action="store_true", help="Create tables only")
    
    args = parser.parse_args()
    
    # Test connection first
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection test passed!")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.error("Please check your .env file and MySQL server")
        sys.exit(1)
    
    if args.reset:
        drop_tables()
        create_tables()
    elif args.create:
        create_tables()
    else:
        logger.info("No action specified. Use --create or --reset")
        logger.info("Example: python setup_database.py --create")
        logger.info("Example: python setup_database.py --reset")

if __name__ == "__main__":
    main()