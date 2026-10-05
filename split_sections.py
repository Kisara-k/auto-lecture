"""
Split Key Points and Study Notes sections from output files into a subfolder.
"""
import os
import re

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")
KP_DIR = os.path.join(OUTPUTS_DIR, "key points")
SN_DIR = os.path.join(OUTPUTS_DIR, "study notes")

os.makedirs(KP_DIR, exist_ok=True)
os.makedirs(SN_DIR, exist_ok=True)


def split_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Find the top-level heading (first non-blank line)
    title_line = ""
    for line in lines:
        if line.strip():
            title_line = line
            break

    # Find section boundaries for ## Key Points and ## Study Notes
    key_points_start = study_notes_start = None
    for i, line in enumerate(lines):
        if re.match(r"^## Key Points\s*$", line):
            key_points_start = i
        elif re.match(r"^## Study Notes\s*$", line):
            study_notes_start = i

    if key_points_start is None or study_notes_start is None:
        return False  # skip files missing either section

    key_points_lines = lines[key_points_start:study_notes_start]
    study_notes_lines = lines[study_notes_start:]

    base = os.path.basename(filepath)

    kp_path = os.path.join(KP_DIR, base)
    sn_path = os.path.join(SN_DIR, base)

    with open(kp_path, "w", encoding="utf-8") as f:
        f.write(title_line)
        if not title_line.endswith("\n"):
            f.write("\n")
        f.write("\n")
        f.writelines(key_points_lines)

    with open(sn_path, "w", encoding="utf-8") as f:
        f.write(title_line)
        if not title_line.endswith("\n"):
            f.write("\n")
        f.write("\n")
        f.writelines(study_notes_lines)

    return True


processed = []
skipped = []
quiz_moved = []

quiz_files = [f for f in os.listdir(OUTPUTS_DIR) if f.startswith("q ") and os.path.isfile(os.path.join(OUTPUTS_DIR, f))]
if quiz_files:
    QUIZ_DIR = os.path.join(OUTPUTS_DIR, "quiz")
    os.makedirs(QUIZ_DIR, exist_ok=True)
    for filename in quiz_files:
        src = os.path.join(OUTPUTS_DIR, filename)
        dst = os.path.join(QUIZ_DIR, filename[2:])
        os.rename(src, dst)
        quiz_moved.append(filename)

for filename in sorted(os.listdir(OUTPUTS_DIR)):
    if not filename.endswith(".md"):
        continue
    filepath = os.path.join(OUTPUTS_DIR, filename)
    if os.path.isfile(filepath):
        if split_file(filepath):
            processed.append(filename)
        else:
            skipped.append(filename)

if quiz_moved:
    print(f"Moved {len(quiz_moved)} quiz file(s) to 'quiz/':")
    for f in quiz_moved:
        print(f"  {f} -> {f[2:]}")

print(f"Split {len(processed)} file(s) into 'key points/' and 'study notes/':")
for f in processed:
    print(f"  {f}")
if skipped:
    print(f"\nSkipped (missing Key Points or Study Notes):")
    for f in skipped:
        print(f"  {f}")
