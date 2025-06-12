# Agentic School Assistant

**Stop wasting time hunting for university information.** I built this because I was tired of digging through endless PDFs and emails just to find out when the trimester starts or what my graduation fees are.

This is a smart assistant that knows everything about KCA University - academic calendars, policies, graduation requirements, fees, and more. Just ask it questions naturally, like you would ask a friend who works in the academic office.

## Demo

[![Watch the demo video](https://img.youtube.com/vi/q19k_QpWpJ4/0.jpg)](https://www.youtube.com/watch?v=q19k_QpWpJ4)

*Watch how easy it is to get instant answers about university information*

---

## Why I Built This

As a KCA University student, I noticed I was spending way too much time on simple questions:
- Searching through 20-page academic calendars for one date
- Hunting through multiple websites for graduation fees  
- Emailing the academic office for basic policy questions
- Missing deadlines because information was scattered everywhere

So I built an AI assistant trained on all our university documents. Now I get instant, accurate answers without the hassle.

## What It Does

Ask questions like a normal person:
- "When does the January trimester start?"
- "How much will graduation cost me?"
- "Can I still add units if I'm late to register?"
- "What's the Virtual Campus login process?"

Get immediate answers from official university documents. No more email chains or endless scrolling.

---

## Setup Guide

### Prerequisites

You'll need:
- Python 3.8 or higher
- An AWS account (free tier works fine)
- 10-15 minutes for setup

### Step 1: Get the Code

```powershell
git clone https://github.com/yourusername/kca-university-assistant
cd kca-university-assistant
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Configure AWS

If you haven't used AWS before, don't worry - here's what you need:

1. **Create an AWS account** at [aws.amazon.com](https://aws.amazon.com)
2. **Get your credentials** from the AWS Console:
   - Go to IAM → Users → Create User
   - Attach policies: `AmazonBedrockFullAccess`, `AmazonS3FullAccess`, `AmazonOpenSearchServerlessFullAccess`
   - Save your Access Key ID and Secret Access Key

3. **Configure on your computer:**
```powershell
aws configure
```
Enter your keys when prompted, use `us-east-1` as the region.

> **Don't have AWS CLI?** Download it [here](https://aws.amazon.com/cli/) first.

### Step 4: Deploy the Knowledge Base

This creates your university database in the cloud:

```powershell
python deploy_kb.py --action deploy
```

You'll see output like this:
```
Creating S3 bucket for documents...
Setting up OpenSearch collection...
Building knowledge base...
Uploading KCA University documents...
✓ Knowledge base ready!
```

**This takes about 5-10 minutes** and costs roughly $10-15/month to run.

### Step 5: Start the Assistant

```powershell
python main.py
```

You should see:
```
🎓 KCA University Assistant Ready!
Ask me about academic calendars, graduation, fees, or university policies.

Student: 
```

That's it! Start asking questions.

---

## How to Use It

### Basic Questions

Just type naturally:

```
Student: when does january trimester start
Assistant: The January trimester starts on January 2nd, 2025. Orientation for new students is on January 6th.

Student: graduation fees bachelor degree
Assistant: Bachelor's degree graduation fee is 8,000 KES. You'll also need to complete academic, financial, and library clearances by June 21st, 2024.

Student: can i add units late
Assistant: Yes, you can add units within the add/drop period (first two weeks of each trimester). For January 2025, the deadline is January 20th, 2025.
```

### Getting Help

Type `help` to see what the assistant knows about:
- Academic calendars and important dates
- University rules and regulations  
- Graduation requirements and fees
- FAQ about distance learning and Virtual Campus
- Registration and add/drop procedures

### Exiting

Type `exit`, `quit`, or `bye` to close the assistant.

---

## What's Inside

The assistant knows about:

**📅 Academic Calendar**
- Trimester start/end dates for 2025
- Important deadlines (add/drop, exams)
- Holidays and university closure days
- Orientation schedules

**📚 University Policies**  
- Registration requirements
- Attendance policies (5-minute lateness rule)
- Examination rules and procedures
- Academic standards and requirements

**🎓 Graduation Information**
- Fees by degree level (Bachelor: 8,000, Postgrad: 8,500, Doctoral: 10,000)
- Clearance requirements and deadlines
- Gown collection procedures and dates

**❓ Common Questions**
- Distance learning guidance
- Virtual Campus access instructions
- Course registration help
- Academic support services

---

## Management Commands

### Check if everything is working:
```powershell
python deploy_kb.py --action status
```

### Update documents (after adding new university files):
```powershell
python deploy_kb.py --action sync
```

### Remove everything (to stop AWS costs):
```powershell
python deploy_kb.py --action delete
```

---

## Troubleshooting

**"Knowledge base not found" error?**
Run the deploy command again:
```powershell
python deploy_kb.py --action deploy
```

**AWS permission errors?**
Make sure your AWS user has the required policies attached (see Step 3 above).

**"Module not found" errors?**
Install dependencies:
```powershell
pip install -r requirements.txt
```

**Assistant giving weird answers?**
Check that your documents uploaded properly:
```powershell
python deploy_kb.py --action status
```

**Still stuck?** Create an issue on GitHub with your error message.

---

## Project Structure

```
kca-university-assistant/
├── main.py                    # The main assistant program
├── deploy_kb.py              # Sets up the knowledge base
├── kb_tools.py               # Core functionality
├── requirements.txt          # Python packages needed
├── README.md                 # This file
└── kb_store/
    ├── kb.py                 # Knowledge base management
    ├── prereqs_config.yaml   # Configuration settings
    └── kb_files/             # University documents
        ├── academic_calendar.json
        ├── FAQ.json
        ├── Graduation.json
        └── rules.json
```

---

## Adding Your Own Documents

Want to add more university information? Easy:

1. **Create a JSON file** in `kb_store/kb_files/` with your content
2. **Update the knowledge base:**
   ```powershell
   python deploy_kb.py --action sync
   ```
3. **Test it** by asking questions about your new content

### Example new file format:
```json
{
  "title": "Library Services",
  "services": [
    {"name": "Book Checkout", "duration": "2 weeks"},
    {"name": "Study Rooms", "booking": "Online reservation required"}
  ]
}
```

---

## For Other Universities

This system works for any university! Here's how to adapt it:

1. **Replace the files** in `kb_store/kb_files/` with your university's documents
2. **Update the config** in `kb_store/prereqs_config.yaml`:
   ```yaml
   knowledge_base_name: 'your-university-assistant'
   knowledge_base_description: 'Your University academic information assistant'
   ```
3. **Deploy:** `python deploy_kb.py --action deploy`

The assistant will now answer questions about your university instead.

---
