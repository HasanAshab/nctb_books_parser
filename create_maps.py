import os
import importlib.util
import sys
import urllib3


def run_map_makers():
    map_makers_dir = 'map_makers'
    
    # Get all Python files from map_makers directory
    files = [f for f in os.listdir(map_makers_dir) if f.endswith('.py')]
    print(f"Running {len(files)} map makers...")
    # Run each file
    for filename in files:
        filepath = os.path.join(map_makers_dir, filename)
        module_name = filename[:-3]  # Remove .py extension
        
        # Load and execute the module
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run_map_makers()
