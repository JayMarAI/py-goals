#ADD TRY TO INPUTS

#modules
import os
import json
import sys
import tkinter as tk
root = tk.Tk()
root.title('nigger')
root.geometry('300x200')


def load_data():
    with open("data.json","r") as file:
        global data 
        data = json.load(file)

def save():
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


def decision(act, func, g=None):
    os.system('clear')
    if act:
        
        global all_goals
        all_goals = []
        if g is not None:
            act(g)    
        else:
            act()
    else:
        print("Invalid Choice")
        func()

#sections

#goal viewing
def view_goals():
    all_goals = []
    goals = len(data['goals'])
    if(goals <= 0):
        print("You currently have no goals.")
        print("")
        print("")
        print("Please select an option:)")
        print("")
        print("1. Add a new goal")
        print("2. Return to main menu")
        view_nogoal_choice = input("Enter your choice (1-2): ")
        action = view_nogoal_choices.get(view_nogoal_choice)

        decision(action, view_goals)
    else:
        if(goals == 1):
            print(f"You currently have {goals} goal.")
        else:
            print(f"You currently have {goals} goals.")
        print("")
        print("Select the one you'd like to check.")
        print("")

        for goal_list in data['goals'].values():
            all_goals.extend(goal_list)

        for index, goal in enumerate(all_goals, start=1):       
                print(f"{index}. {goal['goal']}                      {'Completed' if goal['completed'] == True else 'In Progress'}")

        view_goal_choice = input(f"Enter your choice (1-{goals}, 0 to return): ")
        
        num = int(view_goal_choice)
        if 1 <= num <= goals:
            selected = all_goals[num - 1]
            view_goal(selected)
        elif num == 0:
            os.system('clear')
            main_menu()
        else:
            os.system('clear')
            print("Invalid Choice")
            view_goals() 

def view_goal(s):
    print(f"              - {s['goal']} -            ")
    print(f"Planned Hours: {s['hours_planned']}")
    print(f"Logged Hours: {s['hours_logged']}")
    print(f"Status: {'Completed' if s['completed'] == True else 'In Progress'}\n\n\n")
    print("1. Edit\n2. Log Hours\n3. Mark as Complete\n4. Delete\n5. Return\n6. Main Menu")

    viewed_goal_choice = input("Enter your choice (1-6): ")
    action = viewed_goal_choices.get(viewed_goal_choice)
    
    decision(action, lambda: view_goal(s), s if viewed_goal_choice in ('1','2','3','4') else None)

def edit_goal(g):
    print("What will be changed?\n\n")
    print("1. Goal\n2. Planned Hours\n3. Return\n4. Main Menu")
    edit_goal_choice = input("Enter your choice (1-4): ")
    action = edit_goal_choices.get(edit_goal_choice)
    decision(action, lambda: view_goal(g), g if edit_goal_choice in ('1','2') else None)

def edit_goal_name(g):
    rename = input(f"What would you like to rename \"{g['goal']}\" to? ")
    rename_confirm = input(f"Change \"{g['goal']}\" to \"{rename}\"? (y/n)")
    if rename_confirm == "y":
        g['goal'] = rename
        save()

        os.system('clear')
        print(f"Goal successfuly changed to \"{g['goal']}\".")
        input("Press any key to return... ")
        os.system('clear')
    
        view_goals()
    elif rename_confirm == "n":
        os.system('clear')
        edit_goal(g)
    else:
        os.system('clear')
        print('Invalid Input. Try Again.')
        edit_goal_name(g)
        
def edit_planned_hours(g):
    while True:
        try:
            updated_phours = int(input(f"What would you like to change the planned hours too? Current planned hours is {g['hours_planned']} hours. "))
            break
        except ValueError:
            print("Please enter a valid number.")
            input("Press any key to try again...")
            os.system('clear')

    phours_confirm = input(f"Change planned hours of {g['goal']} from {g['hours_planned']} to {updated_phours}? (y/n)")
    if phours_confirm == "y":
        g['hours_planned'] = int(updated_phours)
        save()

        os.system('clear')
        print(f"Planned Hours successfuly changed to {g['hours_planned']}.")
        input("Press any key to return... ")
        os.system('clear')
    
        view_goals()
    elif phours_confirm == "n":
        os.system('clear')
        edit_goal(g)
    else:
        os.system('clear')
        print('Invalid Input. Try Again.')
        edit_goal_name(g)

def delete_goal(g):
    delete_goal_decision = input(f"Are you sure you'd like to delete \"{g['goal']}\"? ")
    if delete_goal_decision == "y":
        for key, goal_list in data["goals"].items():
            for goal in goal_list:
                if goal == g:
                    goal_list.remove(goal)
    else:
        view_goals()

    data['goals'] = {k: v for k, v in data['goals'].items() if v}

    save()

    os.system('clear')
    print("Goal deleted successfully")
    input("Press any key to return... ")
    os.system('clear')
    
    view_goals()



def add_goal():
    ngoal_name = input('Enter your goal: ')
    while True:
        try:   
            nplanned_hours = int(input('How many hours do you plan on this goal taking? '))
            break
        except ValueError:
            print("Please enter a valid number.")
            input("Press any key to try again...")
            os.system('clear')

    new_goal = {
        "goal": ngoal_name,
        "hours_planned": int(nplanned_hours),
        "hours_logged": 0,
        "completed": False
    }

    os.system('clear')
    print(f"Goal Name: {ngoal_name}\n Planned Hours: {nplanned_hours}")
    confirm = input('Confirm Goal Creation (y/n): ')

    if confirm == "y":
        
        existing_goals = data.get("goals", {})
        next_index = len(existing_goals) + 1

        while f"goal{next_index}" in existing_goals:
            next_index += 1

        data["goals"][f"goal{next_index}"] = [new_goal]

        save()

        os.system('clear')
        print(f"Goal \"{ngoal_name}\" created.")
        input("Press any key to return... ")
        os.system('clear')
    
        main_menu()
    elif confirm == "n":
        os.system('clear')
        main_menu()
    else:
        os.system('clear')
        print('Invalid Input. Try Again.')
        main_menu()

def mark_goal(g):
    if g["completed"] == False:
        confirm = input("Mark goal as complete?")
        if confirm == "y":
            g["completed"] = True
            save()
            os.system('clear')
            print(f"Goal marked as Complete. Good work.")
            input("Press any key to return... ")
            os.system('clear')
            view_goal(g)   
        elif confirm == "n":
            os.system('clear')
            view_goal(g)
        else:
            os.system('clear')
            print('Invalid Input. Try Again.')
            mark_goal(g)
    else:
        confirm = input("Mark goal as incomplete?")
        if confirm == "y":
            g["completed"] = False
            save()
            os.system('clear')
            print(f"Goal marked as Incomplete.")
            input("Press any key to return... ")
            os.system('clear')
            view_goal(g)   
        elif confirm == "n":
            os.system('clear')
            view_goal(g)
        else:
            os.system('clear')
            print('Invalid Input. Try Again.')
            mark_goal(g)

    


def log_time(g):
    try:
        ulogged_hours = int(input(f"What would you like to update your logged hours to? The current hours logged is {g['hours_logged']}. " ))
    except ValueError:
        print("Please enter a valid number.")
        input("Press any key to try again...")
        os.system('clear')
        return log_time(g)
        
    confirm = input(f"Update logged hours to {ulogged_hours}? (y/n) ")
    if confirm == "y":
            g["hours_logged"] = int(ulogged_hours)
            save()
            os.system('clear')
            print(f"Logged Hours for {g['goal']} updated to {g['hours_logged']}. Keep it up.")
            input("Press any key to return... ")
            os.system('clear')
            view_goal(g)   
    elif confirm == "n":
            os.system('clear')
            view_goal(g)
    else:
            os.system('clear')
            print('Invalid Input. Try Again.')
            log_time(g)

def goodbye():
    print("See you soon")
    sys.exit()

def main_menu():
    print("")
    print("Welcome to Your Learning Dashboard!")
    print("Please select an option:")
    print("")
    print("1. View goals")
    print("2. Add a new goal")
    print("3. Exit")

    main_choice = input("Enter your choice (1-3): ")

    action = main_choices.get(main_choice)

    decision(action, main_menu)

#choices
main_choices = {
    "1": view_goals,
    "2": add_goal,
    "3": goodbye
}

view_nogoal_choices = {
    "1": add_goal,
    "2": main_menu
}

viewed_goal_choices = {
    "1": edit_goal,
    "2": log_time,
    "3": mark_goal,
    "4": delete_goal,
    "5": view_goals,
    "6": main_menu
}

edit_goal_choices = {
    "1": edit_goal_name,
    "2": edit_planned_hours,
    "3": view_goals,
    "4": main_menu
}

#start
load_data()
main_menu()
root.mainloop()