import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

categories = [
    ("Tamil", "Pop", "Latest"), ("Tamil", "Pop", "Old"),
    ("Malayalam", "Pop", "Latest"), ("Malayalam", "Pop", "Old"),
    ("Hindi", "Pop", "Latest"), ("Hindi", "Pop", "Old"),
    ("English", "Pop", "Latest"), ("English", "Pop", "Old"),
    ("Telugu", "Pop", "Latest"), ("Telugu", "Pop", "Old"),
    ("English", "Jazz", "Old"), ("English", "Jazz", "Latest"),
    ("Hindi", "Folk", "Latest"), ("Hindi", "Folk", "Old"),
    ("Tamil", "Folk", "Latest"), ("Tamil", "Folk", "Old"),
    ("Malayalam", "Folk", "Latest"), ("Malayalam", "Folk", "Old"),
    ("English", "Folk", "Latest"), ("English", "Folk", "Old"),
    ("Telugu", "Folk", "Latest"), ("Telugu", "Folk", "Old"),
    ("Tamil", "Melody", "Latest"), ("Tamil", "Melody", "Old"),
    ("Telugu", "Melody", "Latest"), ("Telugu", "Melody", "Old"),
    ("Malayalam", "Melody", "Latest"), ("Malayalam", "Melody", "Old"),
    ("Hindi", "Melody", "Latest"), ("Hindi", "Melody", "Old"),
    ("English", "Melody", "Latest"), ("English", "Melody", "Old"),
]

all_tracks = []
track_id = 1

for lang, genre, era in categories:
    prompt = f"""
    Generate 5 real, popular songs that fit exactly these criteria:
    Language: {lang}
    Genre: {genre}
    Era: {era} ('Latest' means post-2015, 'Old' means pre-2010)

    Output STRICTLY a JSON list of objects. Do not include markdown formatting or explanation. Just the raw JSON array.
    Schema:
    [
      {{
        "name": "Song Name",
        "artist": "Artist Name",
        "language": "{lang}",
        "genre": "{genre}",
        "era": "{era}",
        "valence": 0.5, // float 0.0 to 1.0
        "energy": 0.5 // float 0.0 to 1.0
      }}
    ]
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
        content = response.choices[0].message.content
        
        # Clean up markdown if groq adds it
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
            
        tracks = json.loads(content)
        for t in tracks:
            t["id"] = str(track_id)
            track_id += 1
            all_tracks.append(t)
        print(f"Generated {lang} {genre} {era}")
    except Exception as e:
        print(f"Failed for {lang} {genre} {era}: {e}")

with open("src/backend/catalog.json", "w") as f:
    json.dump(all_tracks, f, indent=2)

print(f"Total tracks generated: {len(all_tracks)}")
