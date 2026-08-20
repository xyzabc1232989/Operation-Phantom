import statistics
import hashlib

def analyze(keystrokes, phrase):
    if not keystrokes or len(keystrokes) < 2:
        return {
            'signature': None,
            'wpm': 0,
            'accuracy': 0,
            'consistency': 0,
            'latencies': []
        }
    
    # Calculate typing speed (WPM)
    # Average word length ~5 chars, so WPM = (chars / 5) / (time_in_seconds / 60)
    total_chars = len(keystrokes)
    if total_chars > 0:
        start_time = keystrokes[0]['timestamp']
        end_time = keystrokes[-1]['timestamp']
        duration_sec = (end_time - start_time) / 1000  # ms to sec
        wpm = (total_chars / 5) / (duration_sec / 60) if duration_sec > 0 else 0
    else:
        wpm = 0
    
    # Calculate latencies between consecutive keys
    latencies = []
    for i in range(1, len(keystrokes)):
        latency = keystrokes[i]['timestamp'] - keystrokes[i-1]['timestamp']
        latencies.append(latency)
    
    # Calculate consistency (inverse of standard deviation of latencies)
    if len(latencies) > 1:
        std_dev = statistics.stdev(latencies)
        mean_latency = statistics.mean(latencies)
        consistency = max(0, 100 - (std_dev / max(mean_latency, 1)) * 50)
        consistency = min(100, consistency)
    else:
        consistency = 50
    
    # Calculate accuracy based on backspace count
    backspaces = sum(1 for k in keystrokes if k.get('key') == 'Backspace')
    accuracy = max(0, 100 - (backspaces / max(total_chars, 1)) * 100)
    
    # Generate unique digital signature
    signature_data = f"{phrase}_{wpm}_{consistency}_{accuracy}_{latencies[:10]}"
    signature_hash = hashlib.sha256(signature_data.encode()).hexdigest()[:8]
    signature = f"KS-{signature_hash.upper()}"
    
    return {
        'signature': signature,
        'wpm': round(wpm, 1),
        'accuracy': round(accuracy, 1),
        'consistency': round(consistency, 1),
        'latencies': [round(l, 2) for l in latencies[:20]]  # Return first 20 for display
    }