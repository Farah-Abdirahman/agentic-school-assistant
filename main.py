"""
# 🎓 KCA University Academic Assistant

A specialized AI assistant for KCA University students, faculty, and staff.

## What This Assistant Provides

This assistant offers comprehensive support for:
- Academic calendar information (trimester schedules, holidays, deadlines)
- University policies and regulations (attendance, registration, examination rules)
- Graduation requirements and procedures (fees, clearance, gown collection)
- Campus services and resources (Virtual Campus access, student support)
- Administrative procedures (add/drop courses, distance learning options)
- Frequently asked questions about university life

Example queries:
```
When does the January trimester start?
What are the graduation fees?
How do I access the Virtual Campus?
What are the attendance requirements?
```
"""
from assistant import create_agent

# Interactive mode when run directly
supervisor_agent = create_agent()


# Example usage
if __name__ == "__main__":
    print("\n🎓 KCA University Academic Assistant\n")
    print("Ask questions about KCA University academic and administrative information.\n")
    
    print("Example queries:")
    print("📅 Academic Calendar: 'When does the January trimester start?'")
    print("💰 Fees & Graduation: 'What are the graduation fees?'")
    print("🌐 Campus Services: 'How do I access the Virtual Campus?'")
    print("📋 Policies: 'What are the attendance requirements?'")
    print("📚 Registration: 'How do I add or drop a course?'")
    print("🎓 Graduation: 'What are the clearance requirements for graduation?'")
    print("⚙️  Management: 'Create the university knowledge base'")
    print("📊 Status: 'Check knowledge base status'")
    

    # Interactive loop
    while True:
        try:
            user_input = input("\n🎓 KCA University > ")
            if user_input.lower() == "exit":
                print("\nThank you for using KCA University Academic Assistant! Goodbye!")
                break

            response = supervisor_agent(
                user_input,
            )

            # Extract and print only the relevant content from the agent's response
            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Thank you for using KCA University Academic Assistant!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question about KCA University.")
