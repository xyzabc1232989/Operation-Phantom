# Operation Phantom

**A Multi-Module Digital Security Assessment Platform**

Operation Phantom is a multi-module digital security assessment platform developed as a university course project. It combines a professional analyst dashboard, a Python Flask analysis engine, and a low-level x86 assembly security engine into a single assessment pipeline.

The platform evaluates multiple aspects of a user's security profile—including password strength, typing behavior, security hygiene, and removable-drive safety—and produces a weighted overall security assessment.

---

## Architecture

Operation Phantom is built around three integrated layers:

### 1. Frontend — Analyst Dashboard

The frontend is a single-page HTML/CSS/JavaScript application designed with a dark, analyst-oriented interface.

The assessment guides the user through five stages:

1. User registration
2. Password analysis
3. Typing biometrics
4. Behavioral security questionnaire
5. USB security scanning

Results are updated dynamically as the user interacts with the system, culminating in a final security profile and threat classification.

---

### 2. Python Flask Backend — Analysis Engine

The Flask backend acts as the main processing layer and integrates six analysis modules.

#### Password Intelligence

Analyzes password characteristics including:

* Entropy estimation
* Character pool size
* Password length
* Estimated cracking time
* Optional `zxcvbn` integration when available

#### Typing Biometrics

Processes raw keystroke timing data to extract behavioral characteristics such as:

* Words per minute (WPM)
* Typing accuracy
* Inter-key timing consistency
* Hesitation patterns
* Backspace rate

#### Behavior Engine

Evaluates responses to seven security-hygiene questions using weighted scoring to estimate the user's security behavior.

#### USB Detection

Uses `psutil` to identify removable storage devices connected to the system.

#### File System Scanner

When a removable drive is detected, the scanner can:

* Traverse the drive's file system
* Count files by category
* Detect hidden files
* Flag potentially suspicious extensions

Examples of monitored extensions include:

```text
.exe
.bat
.vbs
.ps1
```

#### Report Generator

Combines the individual module scores into a weighted overall security score and passes the results to the EMU8086 security engine.

If the assembly engine or emulator is unavailable, the backend provides a graceful fallback rather than terminating the assessment.

---

## 3. EMU8086 — Low-Level Security Engine

Operation Phantom also includes a functional x86 assembly component implemented for the course's low-level programming requirement.

The assembly engine:

1. Reads five assessment scores from `input.dat`
2. Performs weighted score calculations
3. Uses 32-bit arithmetic to prevent intermediate overflow
4. Classifies the overall security level using `CMP` and conditional branching
5. Produces module-level pass/review/fail verdicts
6. Generates a formatted security report

The Python backend invokes the assembly engine through a subprocess, connecting the high-level Flask application with the low-level x86 component.

---

## Security Scoring

The final assessment uses four weighted security dimensions:

| Module               | Weight |
| -------------------- | -----: |
| Password Security    |    30% |
| Typing Consistency   |    25% |
| Behavioral Stability |    30% |
| USB Safety           |    15% |

The weighted scores are combined to produce the final security assessment.

### Threat Classification

The final score is mapped to four threat levels:

* **Minimal**
* **Moderate**
* **Elevated**
* **Critical**

The final dashboard presents both the overall classification and the individual module results.

---

## Design Philosophy

Operation Phantom was intentionally designed to avoid the typical visual style associated with student cybersecurity projects.

Instead of using:

* Green terminal interfaces
* Matrix-style animations
* Skull graphics
* Overly dramatic hacker imagery

the interface uses a restrained intelligence-dashboard aesthetic inspired by modern security and developer platforms.

### Visual System

**Background**

```text
#0B0F14
```

**Primary Accent**

```text
#60A5FA
```

**Typography**

* Syne
* IBM Plex Mono

The goal is to make the application feel like an analyst-facing security tool rather than a conventional classroom demonstration.

---

## Project Structure

```text
operation_phantom/
│
├── app.py
│
├── templates/
│   └── index.html
│
└── emu8086/
    └── phantom_engine.asm
```

### File Overview

| File                         | Purpose                                                          |
| ---------------------------- | ---------------------------------------------------------------- |
| `app.py`                     | Flask backend and six analysis modules                           |
| `templates/index.html`       | Complete frontend, assessment flow, dashboard, and live analysis |
| `emu8086/phantom_engine.asm` | x86 assembly security engine                                     |
| `input.dat`                  | Score input passed to the assembly engine                        |

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* `psutil`
* `zxcvbn` *(optional)*

### Low-Level Engine

* x86 Assembly
* EMU8086
* 32-bit arithmetic
* Conditional branching

---

## Assessment Pipeline

```text
User
  │
  ▼
Analyst Dashboard
  │
  ├── Password Analysis
  ├── Typing Biometrics
  ├── Behavioral Assessment
  └── USB/File System Analysis
          │
          ▼
   Flask Analysis Engine
          │
          ▼
   Weighted Score Generation
          │
          ▼
      input.dat
          │
          ▼
   EMU8086 Security Engine
          │
          ▼
 Threat Classification
          │
          ▼
 Final Security Profile
```

---

## Project Objective

The primary objective of Operation Phantom is to demonstrate how multiple computing concepts can be integrated into one practical security assessment system.

The project brings together:

* Web application development
* Backend programming
* Security-oriented data analysis
* Behavioral analysis
* File-system inspection
* Hardware/removable-device detection
* Low-level x86 programming
* Inter-process communication
* Weighted decision systems

Rather than treating these technologies as isolated course components, Operation Phantom integrates them into a single end-to-end application.

---

## Disclaimer

Operation Phantom is a **university course project and security assessment prototype**. It is intended for educational and controlled testing environments.

The security scores and threat classifications are assessment indicators, not professional cybersecurity certifications or definitive measurements of an individual's security posture.
