#Variables are names attached to a value to use later.
project_name = "North Mine Expansion"
budget = 480000

print(project_name)
print(budget)
#Function is a named block of instructions you can run over and over. 
# You feed it inputs (called parameters), it does something, and it hands back a result with return.
def add_tax(amount):
    return amount * 1.25
print(add_tax(budget) )
print(add_tax(1000))
#Dictionaries
project = {"name": "North Mine", "budget": 480000}

print(project["name"])        # read a value by its label

project["budget"] = 500000    # change an existing value
project["location"] = "Sweden"  # add a brand-new label

print(project)

#To make a function that takes inputs and returns a dictionary 
def build_proj(name, duration_weeks, budget, start_state, end_state ):
    proj ={"Project_name": name, 
           "duration_weeks": duration_weeks,
           "budget_usd": budget,
            "start_state": start_state,
        "end_state": end_state
    }
    return proj
# Call it with fake details, like a user filling the form:
p = build_proj(
    "North Mine Expansion",
    26,
    550000,
    "exploratory drilling complete",
    "production-ready shaft",
)

print(p)

#TO see how read/write work
##SINCE WHEN SCRIPT ENDS, DICTIONARY VANISHES, SO TO SAVE WE NEED TO SAVE IT UNTO A JSON FILE
import json

# WRITE the dictionary to a file as JSON
with open("proj.json", "w") as f:
    json.dump(p, f, indent=2)

print("Saved to proj.json")

# READ it back from the file
with open("proj.json", "r") as f:
    loaded = json.load(f)

print("Loaded back:", loaded["Project_name"])