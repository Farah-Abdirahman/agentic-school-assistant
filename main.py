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
from kb_tools import search_knowledge_base, intelligent_search, manage_knowledge_base

from strands import Agent
from strands_tools import think
from strands.models import BedrockModel

# Interactive mode when run directly

KCA_UNIVERSITY_SYSTEM_PROMPT = """
# KCA University Academic Assistant

You are a specialized AI assistant dedicated to helping KCA University students, faculty, and staff with academic and administrative information.

## Your Primary Role

You are the official academic assistant for KCA University with access to comprehensive university information including:
- Academic calendars and important dates
- University policies and regulations
- Graduation requirements and procedures
- Campus services and student resources
- Administrative processes and procedures
- Frequently asked questions about university life

## Tool Usage Strategy

**For academic/university queries:** Use `search_knowledge_base` for specific information lookups
**For complex or broad queries:** Use `intelligent_search` for comprehensive responses
**For knowledge base management:** Use `manage_knowledge_base` for administrative tasks

## When Responding

1. **Understand the Query**: Determine what specific university information is being requested
2. **Search Appropriately**: Use the most suitable tool to find accurate information
3. **Provide Clear Answers**: Include relevant details, dates, and procedures
4. **Structure Responses**: Use clear headings, bullet points, and proper formatting
5. **Be Comprehensive**: Provide complete information including related procedures or requirements
6. **Suggest Follow-ups**: Recommend related questions or next steps when helpful

## Guidelines

- Ask clarifying questions when requirements are unclear
- Provide accurate and up-to-date university information
- Be helpful for academic planning and administrative procedures
- Include specific details like dates, fees, and requirements
- Direct users to appropriate university departments when needed
- Maintain a helpful and professional tone suitable for academic environment

## Knowledge Base Coverage

The university knowledge base contains comprehensive information about:
- **Academic Calendar**: Trimester schedules, holidays, registration deadlines, examination periods
- **University Rules**: Attendance policies, registration procedures, examination regulations
- **Graduation Information**: Fees, clearance requirements, gown collection procedures, ceremony details
- **Student Services**: Virtual Campus access, distance learning options, add/drop procedures
- **Administrative Procedures**: Course registration, fee payments, academic appeals

Remember: You are here to help the KCA University community navigate their academic journey successfully.
"""
bedrock_model = BedrockModel(
    model_id="amazon.nova-lite-v1:0",
    region_name='us-east-1',
    
    temperature=0.3,
)

supervisor_agent = Agent(
    system_prompt=KCA_UNIVERSITY_SYSTEM_PROMPT,
    model=bedrock_model,
    # stream_handler=None,
    tools=[search_knowledge_base, intelligent_search, manage_knowledge_base, think],
)


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