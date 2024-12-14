import os
from alembic.config import Config
from alembic import command
from pathlib import Path

def run_migrations():
    Path("./data").mkdir(exist_ok=True)
    
    alembic_cfg = Config("alembic.ini")
    
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Error during migration: {e}")
        raise 