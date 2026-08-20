def calculate_final_score(password_data, typing_data, behavioral_data, usb_data, file_scan):
    # Weighted scoring model
    weights = {
        'password': 0.25,
        'typing': 0.15,
        'behavioral': 0.25,
        'usb': 0.20,
        'files': 0.15
    }
    
    # Get component scores
    password_score = password_data.get('strength', 0) if password_data else 0
    typing_score = typing_data.get('consistency', 0) if typing_data else 0
    behavioral_score = behavioral_data.get('score', 0) if behavioral_data else 50
    usb_score = 100  # Default, will be adjusted based on USB detection
    
    # USB scoring logic
    if usb_data and usb_data.get('detected') and usb_data.get('devices'):
        # Base score for having a USB
        usb_score = 70
        # If we have file scan data
        if file_scan:
            exe_count = file_scan.get('executables', 0)
            hidden_count = file_scan.get('hidden_files', 0) if isinstance(file_scan, dict) else 0
            
            if exe_count > 20:
                usb_score -= 20
            elif exe_count > 5:
                usb_score -= 10
            
            if hidden_count > 10:
                usb_score -= 15
            elif hidden_count > 3:
                usb_score -= 5
    else:
        usb_score = 75  # No USB detected means incomplete assessment
    
    # File score based on suspicious content
    files_score = 100
    if file_scan:
        suspicious_count = file_scan.get('executables', 0) + file_scan.get('scripts', 0)
        if suspicious_count > 20:
            files_score = 40
        elif suspicious_count > 10:
            files_score = 60
        elif suspicious_count > 0:
            files_score = 80
    
    # Calculate weighted total
    total = (
        (password_score * weights['password']) +
        (typing_score * weights['typing']) +
        (behavioral_score * weights['behavioral']) +
        (usb_score * weights['usb']) +
        (files_score * weights['files'])
    )
    
    total = round(min(100, max(0, total)), 1)
    
    # Determine threat level
    if total >= 80:
        threat_level = 'LOW'
    elif total >= 60:
        threat_level = 'MODERATE'
    elif total >= 40:
        threat_level = 'ELEVATED'
    else:
        threat_level = 'CRITICAL'
    
    return {
        'total': total,
        'threat_level': threat_level,
        'password': round(password_score, 1),
        'typing': round(typing_score, 1),
        'behavioral': round(behavioral_score, 1),
        'usb': round(usb_score, 1),
        'files': round(files_score, 1)
    }

def generate_recommendations(final_score, session_data):
    recommendations = []
    
    # Password recommendations
    password_score = final_score.get('password', 0)
    if password_score < 60:
        recommendations.append({
            'priority': 'HIGH',
            'title': 'Improve Password Security',
            'description': 'Use a longer password with mixed case, numbers, and special characters.'
        })
    elif password_score < 80:
        recommendations.append({
            'priority': 'MEDIUM',
            'title': 'Strengthen Password',
            'description': 'Consider adding more complexity to your password.'
        })
    
    # Typing/Behavior recommendations
    typing_score = final_score.get('typing', 0)
    if typing_score < 50:
        recommendations.append({
            'priority': 'LOW',
            'title': 'Improve Typing Consistency',
            'description': 'Irregular typing patterns may indicate distraction or fatigue.'
        })
    
    # Behavioral recommendations
    behavioral_score = final_score.get('behavioral', 0)
    if behavioral_score < 70:
        recommendations.append({
            'priority': 'HIGH',
            'title': 'Adopt Security Best Practices',
            'description': 'Enable 2FA, avoid password reuse, and use a password manager.'
        })
    
    # USB recommendations
    usb_score = final_score.get('usb', 0)
    if usb_score < 70:
        recommendations.append({
            'priority': 'HIGH',
            'title': 'Review USB Device Content',
            'description': 'Your USB contains executable files or hidden content. Scan with antivirus.'
        })
    
    # Add generic recommendations if needed
    if len(recommendations) < 2:
        recommendations.append({
            'priority': 'MEDIUM',
            'title': 'Regular Security Audits',
            'description': 'Perform monthly security assessments to maintain your digital hygiene.'
        })
    
    return recommendations[:4]