# OPERATION PHANTOM - COAL Project Integration

## Assembly Module (password_checker.asm)

The password strength analysis logic is implemented in x86 Assembly language using emu8086.

### Assembly Algorithm:
1. Reads password from input
2. Analyzes each character for:
   - Uppercase letters (A-Z)
   - Lowercase letters (a-z)
   - Digits (0-9)
   - Special characters (!@#$%^&* etc.)
3. Calculates strength score based on:
   - Length (30% weight)
   - Character variety (70% weight)
4. Outputs: SCORE|CRACK_TIME|WEAKNESSES

### Testing Assembly Separately:
1. Open emu8086
2. Load password_checker.asm
3. Run the emulator
4. Enter a password (e.g., Abcd1234..!!)
5. Assembly will output the analysis result

### Python Integration:
The Python backend implements the SAME logic for real-time web display.
The algorithm is consistent between both implementations, demonstrating
how high-level and low-level languages can solve the same problem.