#!/usr/bin/env python3
"""
Windows Button Simulator Pro - Quick Start Guide

This script provides interactive setup and testing.
"""

import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import customtkinter
        import pynput
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install required packages."""
    print("Installing dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "-r", "requirements.txt"
    ])
    print("✓ Dependencies installed successfully!")


def run_app():
    """Run the main application."""
    print("\nStarting Windows Button Simulator Pro...")
    print("Press F8 to toggle simulation (or your configured key)")
    print("Press ESC for emergency stop\n")
    
    import main
    app = main.WindowsButtonSimulatorApp()
    app.run()


def show_menu():
    """Display main menu."""
    print("\n" + "="*50)
    print("  Windows Button Simulator Pro - Setup")
    print("="*50)
    print("\n1. Install/Update Dependencies")
    print("2. Run Application")
    print("3. View Documentation")
    print("4. Check Module Structure")
    print("5. Exit")
    print("\nEnter your choice (1-5): ", end="")


def show_structure():
    """Display project structure."""
    structure = """
Project Structure:
  UIS/
  ├── main.py           - Application entry point
  ├── ui.py             - UI components
  ├── simulator.py      - Simulation engine
  ├── controllers.py    - Input controllers
  ├── config.py         - Configuration & constants
  ├── requirements.txt  - Python dependencies
  ├── README.md         - Full documentation
  ├── ARCHITECTURE.md   - Detailed architecture
  └── setup.py          - This file

Modules:
  • config.py       - All settings and colors in one place
  • controllers.py  - Mouse/keyboard input handling
  • simulator.py    - Core simulation logic
  • ui.py           - All UI components
  • main.py         - Application orchestration
    """
    print(structure)


def main():
    """Main setup script."""
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_app()
        return
    
    while True:
        show_menu()
        
        try:
            choice = input().strip()
            
            if choice == "1":
                install_dependencies()
                
            elif choice == "2":
                if check_dependencies():
                    run_app()
                else:
                    print("\n⚠ Dependencies not installed.")
                    print("Install now? (y/n): ", end="")
                    if input().strip().lower() == "y":
                        install_dependencies()
                        print("\nNow running application...")
                        run_app()
                    else:
                        print("Please run: pip install -r requirements.txt")
                break
                
            elif choice == "3":
                print("\nRefer to:")
                print("  • README.md - Main documentation")
                print("  • ARCHITECTURE.md - Technical details")
                
            elif choice == "4":
                show_structure()
                
            elif choice == "5":
                print("\nExiting...")
                sys.exit(0)
                
            else:
                print("\n✗ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
