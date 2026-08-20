def analyze(responses):
    # Risk factor weights
    risk_factors = []
    score = 100
    
    # Question 1: Password reuse
    if responses.get('reuse_passwords') == 'yes':
        score -= 20
        risk_factors.append('Password Reuse')
    
    # Question 2: 2FA usage
    if responses.get('uses_2fa') == 'no':
        score -= 25
        risk_factors.append('No Two-Factor Authentication')
    
    # Question 3: Public WiFi
    if responses.get('uses_public_wifi') == 'yes':
        score -= 20
        risk_factors.append('Public WiFi Usage')
    
    # Question 4: Link verification
    if responses.get('verifies_links') == 'no':
        score -= 20
        risk_factors.append('Does not verify links')
    
    # Question 5: Password manager
    if responses.get('uses_password_manager') == 'no':
        score -= 15
        risk_factors.append('No password manager')
    
    # Additional factors from free text
    additional = responses.get('additional_risks', '')
    if 'share' in additional.lower() or 'shared' in additional.lower():
        score -= 10
        risk_factors.append('Password sharing')
    
    score = max(0, min(100, score))
    
    # Determine stability level
    if score >= 80:
        stability = 'High'
    elif score >= 50:
        stability = 'Moderate'
    else:
        stability = 'Low'
    
    return {
        'score': round(score, 1),
        'stability': stability,
        'risk_factors': risk_factors[:5]
    }