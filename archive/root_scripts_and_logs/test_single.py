import sys
from scripts.steps.step_13c_nested_synthetic_adversarial_validation import process_task
if __name__ == '__main__':
    res = process_task(('M3_exact_D', 1, 30))
    print("SUCCESS")
