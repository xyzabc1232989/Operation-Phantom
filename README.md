OPERATION PHANTOM — Project Description
What It Is

Operation Phantom is a multi-module digital security assessment platform built as a university course project. It presents itself as professional analyst-grade software rather than a student demo, combining three technology layers into one cohesive pipeline:

The Three Layers
1. Frontend — Analyst Dashboard

A single-page HTML/CSS/JS application with a clean, dark intelligence aesthetic. It walks the user through five assessment steps — registration, password analysis, typing biometrics, behavioral questionnaire, and USB scanning — then renders a final scored profile. Everything updates in real time as the user types or interacts.

2. Python Flask Backend — Analysis Engine

Six real processing modules running server-side:

Password Intelligence — computes entropy, character pool size, estimated crack time (upgrades to zxcvbn if installed)
Typing Biometrics — processes raw keystroke timestamps to extract WPM, accuracy, inter-key consistency, hesitation patterns, and backspace rate
Behavior Engine — scores weighted answers to seven security hygiene questions
USB Detection — uses psutil to find removable drives in real time
File System Scan — walks the USB, counts files by category, flags suspicious extensions (.exe, .bat, .vbs, .ps1, etc.), and detects hidden files
Report Generator — computes a weighted final score and calls the EMU8086 engine
3. EMU8086 — Low-Level Security Engine

A fully functional x86 assembly program that satisfies the course requirement for low-level programming. It reads five scores from an input.dat file, computes the weighted overall score using 32-bit arithmetic to avoid overflow, classifies the threat level using CMP/JA branching, and prints a formatted report with module-by-module pass/review/fail verdicts. The Python backend calls it via subprocess and falls back gracefully if the emulator isn't installed.

How the Score Is Calculated
Module	Weight
Password Security	30%
Typing Consistency	25%
Behavioral Stability	30%
USB Safety	15%

The final score maps to four threat classifications: Minimal, Moderate, Elevated, or Critical.

Design Philosophy

The UI deliberately avoids every cliché of student security projects — no green terminals, no matrix rain, no skulls. The color palette (
#0B0F14 background, 
#60A5FA accent) and typography (Syne + IBM Plex Mono) are modeled after tools like CrowdStrike, Cloudflare, and Linear, so it reads as production software during a presentation.

Files Delivered
File	Purpose
templates/index.html	Complete frontend — all steps, dashboard, live analysis
app.py	Flask backend — all 6 analysis modules
emu8086/phantom_engine.asm	EMU8086 assembly — security engine with full arithmetic and classification
