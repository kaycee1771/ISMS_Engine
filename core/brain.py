def suggest_remediation(violation):
    if "MFA" in violation:
        return "enable_mfa.sh"
    if "Password" in violation:
        return "enforce_password_policy.sh"
    return "manual_review_needed"

def run():
    print("[Brain] No active learning yet. Placeholder ready.")
