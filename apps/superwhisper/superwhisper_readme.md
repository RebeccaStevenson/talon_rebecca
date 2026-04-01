# SuperWhisper Talon Integration (Legacy)

This file is kept for historical context. See `superwhisper_talon_integration.md` in this folder for the current setup.

This integration allows you to trigger SuperWhisper using a voice command in Talon.

## Setup Instructions

1. **Create and configure the shell script**:

   - Create a directory for your scripts if you don't have one:
     ```bash
     mkdir -p ~/scripts
     ```
   
   - Copy the template to create your shell script:
     ```bash
     cp trigger_superwhisper.sh.template ~/scripts/trigger_superwhisper.sh
     ```
   
   - Edit the script to add your SuperWhisper key:
     ```bash
     nano ~/scripts/trigger_superwhisper.sh
     ```
   
   - Make the script executable:
     ```bash
     chmod +x ~/scripts/trigger_superwhisper.sh
     ```

2. **Verify the Talon files**:
   - Make sure `apps/superwhisper/superwhisper_trigger.py` and `apps/superwhisper/superwhisper.talon` are in your Talon user directory.

3. **Restart Talon** to load the new files.

## Usage

Say one of the following voice commands to trigger SuperWhisper:
- "trigger super whisper"
- "run super whisper"

## Troubleshooting

- If the command doesn't work, check that the helper scripts are present in `apps/superwhisper/scripts/`.
- Ensure SuperWhisper is installed on your system.
- Check that your SuperWhisper key is correctly set in the shell script. 
