import os
import gzip
import shutil
import subprocess
from datetime import datetime
import boto3
from config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)
        
        if settings.USE_S3_BACKUP:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_KEY
            )

    def create_backup(self):
        """Create a database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.sql'
        backup_path = os.path.join(self.backup_dir, backup_file)
        
        try:
            if 'postgresql' in settings.DATABASE_URL:
                self._backup_postgres(backup_path)
            else:
                self._backup_sqlite(backup_path)
                
            # Compress the backup
            with open(backup_path, 'rb') as f_in:
                with gzip.open(f'{backup_path}.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Upload to S3 if configured
            if settings.USE_S3_BACKUP:
                self._upload_to_s3(f'{backup_path}.gz')
                
            return f'{backup_path}.gz'
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            raise

    def _backup_postgres(self, backup_path):
        """Create PostgreSQL backup"""
        db_url = settings.DATABASE_URL
        db_info = self._parse_db_url(db_url)
        
        cmd = [
            'pg_dump',
            '-h', db_info['host'],
            '-p', db_info['port'],
            '-U', db_info['user'],
            '-d', db_info['database'],
            '-f', backup_path
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = db_info['password']
        
        subprocess.run(cmd, env=env, check=True)

    def _backup_sqlite(self, backup_path):
        """Create SQLite backup"""
        db_path = settings.DATABASE_URL.replace('sqlite:///', '')
        shutil.copy2(db_path, backup_path)

    def restore_backup(self, backup_path):
        """Restore from backup"""
        try:
            # Decompress if needed
            if backup_path.endswith('.gz'):
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(backup_path[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path = backup_path[:-3]

            if 'postgresql' in settings.DATABASE_URL:
                self._restore_postgres(backup_path)
            else:
                self._restore_sqlite(backup_path)
                
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}")
            raise

    def _upload_to_s3(self, file_path):
        """Upload backup to S3"""
        file_name = os.path.basename(file_path)
        self.s3.upload_file(
            file_path,
            settings.AWS_BUCKET_NAME,
            f'backups/{file_name}'
        )

    @staticmethod
    def _parse_db_url(url):
        """Parse database URL into components"""
        # Simple parsing for demonstration
        # In production, use proper URL parsing
        parts = url.split('//')
        credentials, location = parts[1].split('@')
        user, password = credentials.split(':')
        host, database = location.split('/')
        
        return {
            'user': user,
            'password': password,
            'host': host,
            'port': '5432',
            'database': database
        }