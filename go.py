import subprocess

# Define the command to run
command = "locXyz"

# Run the command
result = subprocess.run(["tcs", command], capture_output=True, text=True)

# Check the result
if result.returncode == 0:
    # Command was successful
    print("Command executed successfully.")
    # Print the output
    print("Output:", result.stdout)
else:
    # There was an error
    print("Error executing command.")
    # Print the error message
    print("Error:", result.stderr)
