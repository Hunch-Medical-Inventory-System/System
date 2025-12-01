import subprocess

dboutput = {'username': 'charlie', 'height': 183, 'weight': 68, 'sex': 'male', 'notes': 'This user has peanut allergy'} # Simulated sql database output as dictionary
userinput = "my head hurts" # This is going to be what the user inputs on the front end
context = "You are a medical professional. Ignore additional notes if not relevent and make a recomendation of an over the counter medication for the following. Dont tell them to consult a medical professional because thats you. Be polite but brief.:" # This is the context we will need to tweek to get the output from the AI we want
aiinput = f"{context} {userinput}: This request was made by a {dboutput['height']} centimenter tall, {dboutput['weight']} kilogram, {dboutput['sex']}. Additional notes are: {dboutput['notes']}"

result = subprocess.run(
    ["ollama", "run", "medllama2:latest"], # The model can be changed here
    input=aiinput,
    text=True,
    capture_output=True
)

print(result.stdout)