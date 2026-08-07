import sys
from pathlib import Path

script_dir = Path(__file__).parent
project_root = script_dir.parent.parent
sys.path.append(str(project_root))

def main():
    print("FATAL ERROR: NESTED_SAMPLER_NOT_QUALIFIED")
    print("Cannot run Batch 1. The convergence audit failed.")
    print("The 16-parameter joint continuum model starves dynesty slice sampling.")
    print("A scientific or algorithmic redesign is required.")
    sys.exit(1)

if __name__ == "__main__":
    main()
