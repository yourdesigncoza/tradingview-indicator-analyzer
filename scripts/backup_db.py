import os
import subprocess
from datetime import datetime
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalDatabaseBackup:
    def __init__(self):
        # Create backups directory in project root
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Database connection details
        self.db_name = os.getenv("DB_NAME", "your_db_name")
        self.db_user = os.getenv("DB_USER", "your_db_user")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = os.getenv("DB_PORT", "5432")

    def create_backup(self):
        """Create a database backup using pg_dump"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}.sql"
        
        try:
            # Construct pg_dump command
            cmd = [
                "pg_dump",
                "-h", self.db_host,
                "-p", self.db_port,
                "-U", self.db_user,
                "-d", self.db_name,
                "-f", str(backup_path)
            ]
            
            logger.info(f"Creating backup at: {backup_path}")
            
            # Execute pg_dump
            result = subprocess.run(
                cmd,
                env={**os.environ, "PGPASSWORD": os.getenv("DB_PASSWORD", "")},
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Backup created successfully")
                return str(backup_path)
            else:
                logger.error(f"Backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Backup failed with error: {str(e)}")
            return None

    def restore_backup(self, backup_path):
        """Restore database from backup file"""
        try:
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_path}")
                return False
                
            cmd = [
                "psql",
                "-h", self.db_host,
                "-p", self.db_port,
                "-U", self.db_user,
                "-d", self.db_name,
                "-f", backup_path
            ]
            
            logger.info(f"Restoring from backup: {backup_path}")
            
            result = subprocess.run(
                cmd,
                env={**os.environ, "PGPASSWORD": os.getenv("DB_PASSWORD", "")},
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Restore completed successfully")
                return True
            else:
                logger.error(f"Restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Restore failed with error: {str(e)}")
            return False

    def list_backups(self):
        """List all available backups"""
        backups = sorted(self.backup_dir.glob("backup_*.sql"))
        return [str(backup) for backup in backups]

    def cleanup_old_backups(self, keep_last_n=5):
        """Keep only the n most recent backups"""
        backups = sorted(self.backup_dir.glob("backup_*.sql"))
        if len(backups) > keep_last_n:
            for backup in backups[:-keep_last_n]:
                logger.info(f"Removing old backup: {backup}")
                backup.unlink()

def main():
    backup = LocalDatabaseBackup()
    
    # Create new backup
    backup_path = backup.create_backup()
    if backup_path:
        logger.info(f"Backup created at: {backup_path}")
        
        # Cleanup old backups
        backup.cleanup_old_backups()
        
        # List remaining backups
        logger.info("Available backups:")
        for backup_file in backup.list_backups():
            logger.info(backup_file)

if __name__ == "__main__":
    main()