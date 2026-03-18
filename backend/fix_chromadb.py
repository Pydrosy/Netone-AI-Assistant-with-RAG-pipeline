import os
import sys

# Path to chromadb __init__.py
venv_path = sys.prefix
chromadb_init = os.path.join(venv_path, 'Lib', 'site-packages', 'chromadb', '__init__.py')

if os.path.exists(chromadb_init):
    print(f"Found chromadb at: {chromadb_init}")
    
    # Read the file
    with open(chromadb_init, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the patch at the very beginning
    patch_code = '''import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

'''
    
    if patch_code not in content:
        # Write patched file
        with open(chromadb_init, 'w', encoding='utf-8') as f:
            f.write(patch_code + content)
        print("✅ Patched chromadb successfully!")
    else:
        print("✅ chromadb already patched")
else:
    print(f"❌ Could not find chromadb at: {chromadb_init}")
