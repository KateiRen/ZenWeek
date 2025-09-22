import os
import shutil
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_FILE = os.getenv('PROD_DATABASE_URI', 'prod.sqlite3').strip('"')

BACKUP_DIR = 'backups'
WEEKLY_DIR = os.path.join(BACKUP_DIR, 'weekly')
MAX_WEEKLY_BACKUPS = 5



def backup_db(target_dir=BACKUP_DIR, prefix='prod'):
    if not os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' not found.")
        return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(target_dir, f"{prefix}_{timestamp}.sqlite3")
    shutil.copy2(DB_FILE, backup_file)
    print(f"Backup created: {backup_file}")
def weekly_backup():
    backup_db(target_dir=WEEKLY_DIR, prefix='weekly')
    # Prune old backups, keep only the last MAX_WEEKLY_BACKUPS
    backups = [f for f in os.listdir(WEEKLY_DIR) if f.endswith('.sqlite3')]
    backups.sort(reverse=True)
    if len(backups) > MAX_WEEKLY_BACKUPS:
        for old in backups[MAX_WEEKLY_BACKUPS:]:
            os.remove(os.path.join(WEEKLY_DIR, old))
            print(f"Deleted old backup: {old}")


def list_backups():
    if not os.path.exists(BACKUP_DIR):
        print("No backups found.")
        return []
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.sqlite3')]
    backups.sort(reverse=True)
    for idx, fname in enumerate(backups, 1):
        print(f"{idx}: {fname}")
    return backups


def restore_db():
    backups = list_backups()
    if not backups:
        print("No backups to restore.")
        return
    try:
        choice = int(input("Enter the number of the backup to restore: "))
        if not (1 <= choice <= len(backups)):
            print("Invalid selection.")
            return
        backup_file = os.path.join(BACKUP_DIR, backups[choice - 1])
        shutil.copy2(backup_file, DB_FILE)
        print(f"Database restored from {backup_file}")
    except ValueError:
        print("Invalid input.")


def print_usage():
    print("Usage: python backup_restore.py [backup|restore|list|weekly]")


def main():
    if len(sys.argv) != 2:
        print_usage()
        return
    cmd = sys.argv[1].lower()
    if cmd == 'backup':
        backup_db()
    elif cmd == 'restore':
        restore_db()
    elif cmd == 'list':
        list_backups()
    elif cmd == 'weekly':
        weekly_backup()
    else:
        print_usage()


if __name__ == '__main__':
    main()
