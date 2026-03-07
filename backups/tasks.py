from huey.contrib.djhuey import db_task


@db_task()
def perform_backup_task(backup_pk):
    from backups.models import Backup
    backup = Backup.objects.get(pk=backup_pk)
    backup.perform_backup()
