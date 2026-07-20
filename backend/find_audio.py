
import os

# Generate a script to find the actual file
script = '''
import os

# Check multiple possible locations
possible_paths = [
    "downloads/dQw4w9WgXcQ.mp3",
    "downloads/dQw4w9WgXcQ.webm",
    "downloads/dQw4w9WgXcQ.m4a",
    "downloads/dQw4w9WgXcQ.opus",
    "./downloads/dQw4w9WgXcQ.mp3",
    "../downloads/dQw4w9WgXcQ.mp3",
    os.path.join(os.getcwd(), "downloads", "dQw4w9WgXcQ.mp3"),
]

print("Checking possible audio file paths:")
print("-" * 50)

for p in possible_paths:
    exists = os.path.exists(p)
    size = os.path.getsize(p) if exists else 0
    print(f"  {p}")
    print(f"    Exists: {exists}  |  Size: {size} bytes")
    print()

# Also list ALL files in downloads folder
downloads_dir = os.path.join(os.getcwd(), "downloads")
print(f"\\nAll files in '{downloads_dir}':")
print("-" * 50)
if os.path.exists(downloads_dir):
    for f in os.listdir(downloads_dir):
        fpath = os.path.join(downloads_dir, f)
        size = os.path.getsize(fpath)
        print(f"  {f}  ({size} bytes)")
else:
    print("  downloads/ directory does not exist!")
'''

print(script)
