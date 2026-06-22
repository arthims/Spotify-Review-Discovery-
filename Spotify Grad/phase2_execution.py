import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def call_groq(prompt, system="You are an expert UX Researcher."):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        model=MODEL,
        temperature=0.7,
    )
    return response.choices[0].message.content

def phase2_execution():
    print("Starting Phase 2 Execution...")
    ensure_dir("data/phase2")

    # 2.1 Methodology - Generate Interview Guide
    print("Generating Interview Protocol...")
    protocol_prompt = """
    We are building a new AI-native feature for Spotify to improve music discovery and reduce repetitive listening ("the echo chamber"). 
    We want to interview the "High-Engagement, Low-Discovery" user persona (listens to a lot of music but struggles to find new songs).
    Please draft a semi-structured interview guide with:
    1. A screener to ensure we have the right persona.
    2. 5-7 core questions exploring their frustrations with the current recommendation algorithm, how they currently try to discover music, and what their ideal discovery experience would look like.
    """
    interview_protocol = call_groq(protocol_prompt)
    with open("data/phase2/interview_protocol.md", "w") as f:
        f.write(interview_protocol)
    print("Saved interview protocol.")

    # 2.2 Data Synthesis - Generate Mock Transcripts
    print("Generating Mock Transcripts for 5 Users...")
    transcripts = []
    for i in range(1, 6):
        print(f"  Generating Transcript {i}...")
        transcript_prompt = f"""
        Act as User {i}, a Spotify user who fits the "High-Engagement, Low-Discovery" profile. You listen to music for 20+ hours a week, but you feel stuck listening to the same artists and playlists. You want to discover new music but the algorithm just keeps playing things you already know.
        
        Write a raw, realistic interview transcript (interviewer and user) based on the following themes:
        - Frustration with 'Discover Weekly' or 'Radio' playing safe, familiar songs.
        - Workarounds you use (like searching Reddit for playlists or going incognito).
        - A desire for more control over the vibe or mood of the recommendations.
        
        Make it conversational and about 400 words.
        """
        transcript = call_groq(transcript_prompt, system="You are a realistic user participant in a UX research interview.")
        transcripts.append(f"### User {i} Transcript\n{transcript}\n")
    
    combined_transcripts = "\n".join(transcripts)
    with open("data/phase2/mock_transcripts.md", "w") as f:
        f.write(combined_transcripts)
    print("Saved mock transcripts.")

    # 2.2 Data Synthesis - Synthesize Findings
    print("Synthesizing Findings from Transcripts...")
    synthesis_prompt = f"""
    You are a Lead UX Researcher. Here are 5 interview transcripts from Spotify users who fit the "High-Engagement, Low-Discovery" profile.
    
    {combined_transcripts}
    
    Synthesize these transcripts and provide:
    1. Key Themes & Frustrations (What is broken with the current algorithm?)
    2. User Workarounds (How do they currently try to fix the problem?)
    3. Root Cause Hypothesis (Why is the current system failing them?)
    4. Opportunity Area for an AI solution (How can an LLM/AI feature solve this?)
    
    Format the output as a clean, professional Markdown report.
    """
    synthesis_report = call_groq(synthesis_prompt)
    with open("data/phase2/synthesis_report.md", "w") as f:
        f.write(synthesis_report)
    print("Saved synthesis report.")
    print("Phase 2 Execution Complete!")

if __name__ == "__main__":
    phase2_execution()
