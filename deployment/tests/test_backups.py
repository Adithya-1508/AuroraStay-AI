def test_backup_restore_script_paths() -> None:
    # Verifies standard paths for bash backup shell utilities exist in deployment folders
    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert os.path.exists(os.path.join(base_dir, "backups", "db_backup.sh"))
    assert os.path.exists(os.path.join(base_dir, "backups", "qdrant_backup.sh"))
    assert os.path.exists(os.path.join(base_dir, "restore", "db_restore.sh"))
    assert os.path.exists(os.path.join(base_dir, "restore", "qdrant_restore.sh"))
