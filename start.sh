#!/bin/bash

# Check if the .venv folder exists
if [ -d ".venv" ]; then
    goto_activate_venv
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."
    goto_activate_venv
fi

goto_activate_venv() {
    echo "Activating virtual environment..."
    source .venv/bin/activate

    # Run the Python script
    sudo python noone_pause.py

    # Deactivate the virtual environment
    deactivate

    echo "Task completed."
}
