import shutil
from pathlib import Path

def archive_pilot():
    project_root = Path(__file__).parent.parent.parent
    archive_dir = project_root / 'data' / 'processed' / 'archive_pilot_nonconverged'
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_archive = [
        'q1009_forensic_reopt.json',
        'q1009_forensic_cv.json',
        'q1009_forensic_synthetic.json'
    ]
    
    for f_name in files_to_archive:
        src = project_root / 'data' / 'processed' / f_name
        if src.exists():
            dst = archive_dir / f_name
            shutil.copy2(src, dst)
            print(f"Archived {f_name} to {archive_dir}")

if __name__ == '__main__':
    archive_pilot()
