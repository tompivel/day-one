import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.append(backend_path)

print(f"Testing import from: {backend_path}")

try:
    from main import app
    print("Backend import successful!")
except Exception as e:
    print(f"Backend import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
