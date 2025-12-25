from secret_santa import assign_names

def main():
    participants = [
        "Albert Einstein",
        "Ada Lovelace",
        "Marie Curie",
        "Leonardo da Vinci",
        "Isaac Newton"
    ]
    
    assignments = assign_names(participants)
    
    print("Secret Santa Assignments:")
    for giver, receiver in assignments.items():
        print(f"{giver} is giving a gift to {receiver}")

if __name__ == "__main__":
    main()
