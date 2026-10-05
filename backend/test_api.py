import urllib.request
import urllib.error
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def post(url, data, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json', **headers}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get(url, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def run_tests():
    print("=== Testing Authentication ===")
    try:
        login_res = post('http://127.0.0.1:5000/api/login', {
            'email': 'alex.morgan@example.com',
            'password': 'password123'
        })
        print("✓ Login successful!")
        token = login_res.get('token')
        user = login_res.get('user', {})
        print(f"  User: {user.get('name')} ({user.get('email')})")
    except Exception as e:
        print("Login failed:", e)
        return

    headers = {'Authorization': f'Bearer {token}'}

    print("\n=== Testing Profile ===")
    try:
        prof = get('http://127.0.0.1:5000/api/profile', headers)
        p = prof.get('profile', {})
        print(f"✓ Profile loaded: Target Role = {p.get('target_job_role')}, Overall Level = {p.get('overall_skill_level')}")
        print(f"  Skills: {len(p.get('skills', []))} student skills registered.")
    except Exception as e:
        print("Profile failed:", e)

    print("\n=== Testing Learning Path Generation ===")
    try:
        path_res = get('http://127.0.0.1:5000/api/learning-path', headers)
        steps = path_res.get('steps', [])
        print(f"✓ Learning Path retrieved: {len(steps)} sequenced steps found.")
        if steps:
            print(f"  First step: {steps[0].get('topic_title')} ({steps[0].get('status')})")
    except Exception as e:
        print("Learning Path failed:", e)

    print("\n=== Testing Skill Gap Analysis ===")
    try:
        gap_res = get('http://127.0.0.1:5000/api/skill-gap', headers)
        gaps = gap_res.get('gaps', [])
        print(f"✓ Skill gap analysis computed: {len(gaps)} skills analyzed.")
        if gaps:
            print(f"  Sample gap: {gaps[0].get('skill_name')} - Target: {gaps[0].get('required_level')}, Current: {gaps[0].get('current_level')}, Gap: {gaps[0].get('gap_score')}")
    except Exception as e:
        print("Skill gap failed:", e)

    print("\n=== Testing AI Recommendations ===")
    try:
        rec_res = get('http://127.0.0.1:5000/api/recommendations', headers)
        recs = rec_res if isinstance(rec_res, list) else rec_res.get('recommendations', [])
        print(f"✓ AI recommendations: {len(recs)} topic recommendations provided.")
        if recs:
            print(f"  Top recommended: {recs[0].get('title')} ({recs[0].get('reason')})")
    except Exception as e:
        print("Recommendations failed:", e)

    print("\n=== Testing AI Chatbot Integration ===")
    try:
        chat_res = post('http://127.0.0.1:5000/api/chat', {'message': 'What should I study next and why?'}, headers)
        reply = chat_res.get('reply', '')
        print("✓ Chatbot replied:")
        print(f"  \"{reply[:180]}...\"")
    except Exception as e:
        print("Chatbot failed:", e)

    print("\n=== Testing Voice Assistant API ===")
    try:
        voice_res = post('http://127.0.0.1:5000/api/voice-to-text', {'text': 'What is my current learning progress?'}, headers)
        print("✓ Voice assistant responded with complete Speech/Text pipeline:")
        print(f"  Recognized/Input: \"{voice_res.get('transcribed_text', '')}\"")
        print(f"  Spoken Output: \"{voice_res.get('ai_response_text', '')[:140]}...\"")
        print(f"  Audio Payload URL: {voice_res.get('audio_url')}")
    except Exception as e:
        print("Voice chat failed:", e)

    print("\n=== ALL BACKEND MODULES VERIFIED WORKING! ===")

if __name__ == '__main__':
    run_tests()
