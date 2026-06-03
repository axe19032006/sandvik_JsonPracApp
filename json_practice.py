import json  # Python's built-in tool for converting between dicts and JSON

# 1. Build a Python dictionary of fake project details.
#    This is the same shape your Streamlit form will collect.
project = {
    "project_name": "North Mine Expansion",
    "duration_weeks": "26",        # a number (no quotes) so we can do math on it
    "budget_usd": "480000",        # also a number
    "location" : "Japan",
    "start_state" : "exploratory drilling complete",
    "end_state": "production-ready shaft",
    "requirements": ["site survey", "drilling", "safety audit"],  # a list
    "is_priority": True          # a yes/no value (a boolean)
}

# 2. Confirm what we have: a Python dictionary living in memory.
print("STEP 1 - what type is it in Python?")
print(type(project))             # <class 'dict'>
print("One field:", project["project_name"])  # read a value by its label
print()

# 3. Convert the dictionary INTO JSON text (what gets sent over an API).
#    indent=2 just makes it pretty and readable.
project_as_json = json.dumps(project, indent=2)

print("STEP 2 - the same data as JSON text:")
print(project_as_json)
print()
print("Its type is now a string (plain text), not a dict:")
print(type(project_as_json))     # <class 'str'>
print()

# 4. Convert the JSON text BACK into a Python dictionary
#    (what you do with a response you receive).
back_to_dict = json.loads(project_as_json)

print("STEP 3 - converted back into a Python dict:")
print(type(back_to_dict))        # <class 'dict'>
print("Budget doubled:", back_to_dict["budget_usd"] * 2)  # math works: it's a number