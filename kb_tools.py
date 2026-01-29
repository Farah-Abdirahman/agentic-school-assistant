"""
Knowledge Base Tools Module

This module provides specialized tools for integrating Amazon Bedrock Knowledge Base
functionality into any Strands agent system.
"""

import os
import boto3
from strands import tool
from kb_store.kb import KnowledgeBasesForAmazonBedrock, read_yaml_file


@tool
def search_knowledge_base(query: str, knowledge_base_name: str = "schoolassistant") -> str:
    """
    Search any Amazon Bedrock Knowledge Base for information.
    
    This is a general-purpose tool that can query any knowledge base by name.
    It's particularly useful for searching academic information, documentation,
    or any other content that has been ingested into a Bedrock Knowledge Base.
    
    Args:
        query: The search query or question
        knowledge_base_name: Name of the knowledge base to search (default: schoolassistant)
        
    Returns:
        Relevant information from the knowledge base
    """
    try:
        # Initialize KB manager
        kb_manager = KnowledgeBasesForAmazonBedrock()
        
        # Get knowledge base ID from name
        kb_id = kb_manager.get_kb_id_from_name(knowledge_base_name)
        
        if not kb_id:
            available_kbs = []
            try:
                kbs_response = kb_manager.bedrock_agent_client.list_knowledge_bases(maxResults=100)
                available_kbs = [kb['name'] for kb in kbs_response.get("knowledgeBaseSummaries", [])]
            except:
                pass
            
            if available_kbs:
                return f"Knowledge base '{knowledge_base_name}' not found. Available knowledge bases: {', '.join(available_kbs)}"
            else:
                return f"Knowledge base '{knowledge_base_name}' not found and no knowledge bases are available."
        
        # Query the knowledge base
        response = kb_manager.query_knowledge_base(
            kb_id=kb_id,
            query=query,
            model_id="amazon.nova-lite-v1:0",
            max_results=5
        )
        
        return response
        
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"


@tool
def intelligent_search(query: str) -> str:
    """
    Intelligent search that automatically determines the best knowledge source.
    
    This tool analyzes the query and decides whether to search:
    - School knowledge base for academic information
    - AWS documentation for technical information
    - Or provide general assistance
    
    Args:
        query: The user's question or search query
        
    Returns:
        Comprehensive answer from the most appropriate knowledge source
    """
    try:
        # Initialize KB manager
        kb_manager = KnowledgeBasesForAmazonBedrock()
        
        # Keywords that suggest school-related queries
        school_keywords = [
            "trimester", "semester", "academic", "calendar", "graduation", "fees", 
            "university", "campus", "student", "registration", "exam", "attendance",
            "virtual campus", "add/drop", "clearance", "gown", "rules", "regulations",
            "KCAU", "KCA", "school", "class", "course", "degree", "bachelor", 
            "postgraduate", "doctoral", "faq", "distance learning"
        ]
        
        # Keywords that suggest AWS-related queries
        aws_keywords = [
            "aws", "amazon", "ec2", "s3", "lambda", "cloudformation", "vpc", "rds",
            "dynamodb", "iam", "cloudwatch", "sns", "sqs", "api gateway", "bedrock",
            "cloud", "serverless", "kubernetes", "container", "docker", "devops"
        ]
        
        query_lower = query.lower()
        
        # Check if query contains school-related keywords
        has_school_keywords = any(keyword in query_lower for keyword in school_keywords)
        has_aws_keywords = any(keyword in query_lower for keyword in aws_keywords)
        
        if has_school_keywords and not has_aws_keywords:
            # Query school knowledge base
            kb_id = kb_manager.get_kb_id_from_name("schoolassistant")
            if kb_id:
                response = kb_manager.query_knowledge_base(
                    kb_id=kb_id,
                    query=query,
                    model_id="amazon.nova-lite-v1:0",
                    max_results=5
                )
                return f"📚 **School Knowledge Base Response:**\n\n{response}"
            else:
                return "School knowledge base is not available. Please create it first using the create_school_knowledge_base tool."
        
        elif has_aws_keywords and not has_school_keywords:
            # This would require AWS documentation research - return guidance
            return "🔧 **AWS Query Detected:** This appears to be an AWS-related question. For comprehensive AWS documentation research, please use the aws_documentation_researcher tool or ask the main agent directly."
        
        else:
            # Mixed or general query - try school KB first, then provide general guidance
            kb_id = kb_manager.get_kb_id_from_name("schoolassistant")
            if kb_id:
                try:
                    response = kb_manager.query_knowledge_base(
                        kb_id=kb_id,
                        query=query,
                        model_id="amazon.nova-lite-v1:0",
                        max_results=3
                    )
                    # If the response seems relevant (contains actual information)
                    if len(response) > 50 and "error" not in response.lower():
                        return f"📚 **Knowledge Base Response:**\n\n{response}"
                except:
                    pass
            
            return "❓ **General Query:** I can help with school-related questions (academic calendar, rules, graduation) or AWS technical questions. Please be more specific about what you're looking for, or use the appropriate specialized tools."
            
    except Exception as e:
        return f"Error in intelligent search: {str(e)}"


@tool 
def manage_knowledge_base(action: str, kb_name: str = "schoolassistant") -> str:
    """
    Manage knowledge base operations including create, delete, status, and list.
    
    Args:
        action: The action to perform (create, delete, status, list)
        kb_name: Name of the knowledge base (default: schoolassistant)
        
    Returns:
        Result of the management operation
    """
    try:
        kb_manager = KnowledgeBasesForAmazonBedrock()
        
        if action.lower() == "create":
            # Load configuration
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "kb_store", "prereqs_config.yaml")
            config_data = read_yaml_file(config_path)
            
            if not config_data:
                return f"Could not load configuration from {config_path}"
            
            # Create knowledge base
            kb_id, ds_id = kb_manager.create_or_retrieve_knowledge_base(
                kb_name=config_data["knowledge_base_name"],
                kb_description=config_data["knowledge_base_description"]
            )
            
            if kb_id and ds_id:
                # Upload documents
                documents_path = os.path.join(current_dir, "kb_store", config_data["kb_files_path"])
                if os.path.exists(documents_path):
                    kb_manager.upload_directory(documents_path, kb_manager.get_data_bucket_name())
                    kb_manager.synchronize_data(kb_id, ds_id)
                    return f"✅ Successfully created and populated knowledge base '{config_data['knowledge_base_name']}' with ID: {kb_id}"
                else:
                    return f"⚠️ Knowledge base created but documents directory not found: {documents_path}"
            else:
                return "❌ Failed to create knowledge base"
                
        elif action.lower() == "delete":
            kb_manager.delete_kb(kb_name)
            return f"✅ Successfully deleted knowledge base '{kb_name}' and all associated resources"
            
        elif action.lower() == "status":
            kb_id = kb_manager.get_kb_id_from_name(kb_name)
            if not kb_id:
                return f"❌ Knowledge base '{kb_name}' not found"
            
            kb_details = kb_manager.get_kb(kb_id)
            if kb_details:
                kb_info = kb_details["knowledgeBase"]
                return f"""📊 **Knowledge Base Status for '{kb_name}':**
                
**ID:** {kb_info['knowledgeBaseId']}
**Name:** {kb_info['name']}
**Status:** {kb_info['status']}
**Description:** {kb_info.get('description', 'No description')}
**Created:** {kb_info.get('createdAt', 'Unknown')}
**Updated:** {kb_info.get('updatedAt', 'Unknown')}"""
            else:
                return f"❌ Could not retrieve details for knowledge base '{kb_name}'"
                
        elif action.lower() == "list":
            kbs_response = kb_manager.bedrock_agent_client.list_knowledge_bases(maxResults=100)
            
            if not kbs_response.get("knowledgeBaseSummaries"):
                return "📭 No knowledge bases found in your AWS account"
            
            result = "📋 **Available Knowledge Bases:**\n\n"
            for kb in kbs_response["knowledgeBaseSummaries"]:
                result += f"• **{kb['name']}** (ID: {kb['knowledgeBaseId']}) - Status: {kb['status']}\n"
            
            return result
            
        else:
            return f"❌ Unknown action '{action}'. Supported actions: create, delete, status, list"
            
    except Exception as e:
        return f"❌ Error managing knowledge base: {str(e)}"
