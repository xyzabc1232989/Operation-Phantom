import subprocess
import os
import re
import math

def check_password_with_assembly(password):
    """
    Truly integrated: Calls the compiled Assembly .exe file
    The Assembly program does the actual password analysis
    """
    
    print(f"[ASSEMBLY INTEGRATION] Analyzing: {password}")
    
    # Get the path to the Assembly executable
    exe_path = os.path.join(os.path.dirname(__file__), 'password_checker.exe')
    
    # Check if the .exe exists
    if not os.path.exists(exe_path):
        print(f"[ERROR] Assembly EXE not found at: {exe_path}")
        print("[FALLBACK] Using Python implementation (Assembly not available)")
        return analyze_with_python(password)
    
    try:
        # Run the Assembly program and send password to it
        # Use CREATE_NO_WINDOW to hide the console window
        import subprocess
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 6  # SW_MINIMIZE
        
        process = subprocess.Popen(
            [exe_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo
        )
        
        # Send the password and get output
        stdout, stderr = process.communicate(input=password + '\n', timeout=3)
        
        print(f"[ASSEMBLY OUTPUT] {stdout}")
        
        # Parse the Assembly output
        result = parse_assembly_output(stdout, password)
        
        if result:
            print(f"[ASSEMBLY RESULT] Score: {result['strength']}%, Time: {result['crack_time']}")
            return result
        else:
            print("[ERROR] Failed to parse Assembly output, using Python fallback")
            return analyze_with_python(password)
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Assembly program timed out")
        return analyze_with_python(password)
    except Exception as e:
        print(f"[ERROR] Running Assembly: {e}")
        return analyze_with_python(password)

def parse_assembly_output(output, password):
    """Parse the Assembly output with full words"""
    try:
        lines = output.split('\n')
        for line in lines:
            if 'RESULT:' in line:
                # Extract after RESULT:
                data = line.split('RESULT:')[1].strip()
                parts = data.split('|')
                
                if len(parts) >= 3:
                    # Parse score
                    score = int(parts[0]) if parts[0].isdigit() else 50
                    
                    # Parse crack time (already in full word format)
                    crack_time = parts[1].strip()
                    
                    # Parse weaknesses (comma separated)
                    weaknesses = []
                    if len(parts) >= 3 and parts[2] != 'NONE':
                        weak_parts = parts[2].split(',')
                        weaknesses = [w.strip() for w in weak_parts if w.strip()]
                    
                    # Calculate entropy
                    import math
                    import re
                    charset_size = 0
                    if re.search(r'[a-z]', password): charset_size += 26
                    if re.search(r'[A-Z]', password): charset_size += 26
                    if re.search(r'[0-9]', password): charset_size += 10
                    if re.search(r'[^a-zA-Z0-9]', password): charset_size += 33
                    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
                    
                    return {
                        'score': min(4, score // 25),
                        'strength': score,
                        'crack_time': crack_time,
                        'weaknesses': weaknesses[:3],
                        'entropy': round(entropy, 1),
                        'length': len(password)
                    }
    except Exception as e:
        print(f"Parse error: {e}")
    
    return None

def calculate_entropy(password):
    """Calculate password entropy"""
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset_size += 33
    
    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
    return round(entropy, 1)

def analyze_with_python(password):
    """Fallback Python implementation (same logic as Assembly)"""
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    length = len(password)
    
    # Calculate score (matching Assembly logic)
    score = 0
    
    # Length scoring
    if length >= 13: score += 30
    elif length >= 11: score += 25
    elif length >= 9: score += 20
    elif length >= 8: score += 15
    elif length >= 6: score += 10
    else: score += 5
    
    # Character type scoring
    if has_upper: score += 20
    if has_lower: score += 20
    if has_digit: score += 15
    if has_special: score += 15
    
    score = min(100, score)
    
    # Crack time
    if score >= 80: crack_time = 'Years'
    elif score >= 60: crack_time = 'Months'
    elif score >= 40: crack_time = 'Days'
    elif score >= 20: crack_time = 'Hours'
    else: crack_time = 'Minutes'
    
    # Weaknesses
    weaknesses = []
    if length < 8: weaknesses.append('Too short')
    if not has_upper: weaknesses.append('No uppercase letters')
    if not has_lower: weaknesses.append('No lowercase letters')
    if not has_digit: weaknesses.append('No numbers')
    if not has_special: weaknesses.append('No special characters')
    
    return {
        'score': min(4, score // 25),
        'strength': score,
        'crack_time': crack_time,
        'weaknesses': weaknesses[:3],
        'entropy': calculate_entropy(password),
        'length': length
    }