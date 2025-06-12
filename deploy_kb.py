"""
Deploy Knowledge Base Infrastructure

This script sets up the Amazon Bedrock Knowledge Base infrastructure
and populates it with school documents.
"""

import os
import sys
import argparse
from kb_store.kb import KnowledgeBasesForAmazonBedrock, read_yaml_file
import boto3


def deploy_knowledge_base():
    """Deploy the knowledge base infrastructure and populate it with data"""
    print("Starting Knowledge Base deployment...")
    
    try:
        # Get current directory and config path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "kb_store", "prereqs_config.yaml")
        
        # Load configuration
        print(f"Loading configuration from {config_path}")
        config_data = read_yaml_file(config_path)
        
        if not config_data:
            print(f"Error: Could not read configuration from {config_path}")
            return False
        
        print(f"Configuration loaded successfully")
        print(f"   Knowledge Base Name: {config_data['knowledge_base_name']}")
        print(f"   Description: {config_data['knowledge_base_description']}")
        
        # Initialize Knowledge Base manager
        print("🔧 Initializing Knowledge Base manager...")
        kb = KnowledgeBasesForAmazonBedrock()
        
        # Create or retrieve knowledge base
        print("Creating or retrieving Knowledge Base...")
        kb_id, ds_id = kb.create_or_retrieve_knowledge_base(
            config_data["knowledge_base_name"], 
            config_data["knowledge_base_description"]
        )
        
        if not kb_id or not ds_id:
            print("Failed to create or retrieve Knowledge Base")
            return False
            
        print(f"Knowledge Base ready!")
        print(f"   Knowledge Base ID: {kb_id}")
        print(f"   Data Source ID: {ds_id}")
        
        # Upload documents
        documents_path = os.path.join(current_dir, "kb_store", config_data["kb_files_path"])
        print(f"Uploading documents from {documents_path}")
        
        if not os.path.exists(documents_path):
            print(f"Warning: Documents directory not found at {documents_path}")
            print("Knowledge Base created but no documents uploaded.")
            return True
            
        kb.upload_directory(documents_path, kb.get_data_bucket_name())
        print("Documents uploaded successfully")
        
        # Synchronize data
        print("Synchronizing data (this may take a few minutes)...")
        kb.synchronize_data(kb_id, ds_id)
        print("Data synchronization completed")
        
        # Store KB ID in SSM for future reference
        print("Storing Knowledge Base ID in SSM Parameter Store...")
        try:
            ssm_client = boto3.client("ssm", region_name=config_data.get("region_name", "us-east-1"))
            ssm_client.put_parameter(
                Name=f"{config_data['knowledge_base_name']}-kb-id",
                Description=f"{config_data['knowledge_base_name']} kb id",
                Value=kb_id,
                Type="String",
                Overwrite=True,
            )
            print("Knowledge Base ID stored in SSM")
        except Exception as e:
            print(f"Warning: Could not store KB ID in SSM: {str(e)}")
        
        print("\nKnowledge Base deployment completed successfully!")
        print(f"   You can now query the knowledge base using KB ID: {kb_id}")
        print(f"   Try asking questions about academic calendar, rules, graduation, or FAQ topics.")
        
        return True
        
    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        return False


def check_knowledge_base_status():
    """Check the status of the deployed knowledge base"""
    print("Checking Knowledge Base status...")
    
    try:
        # Load configuration
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "kb_store", "prereqs_config.yaml")
        config_data = read_yaml_file(config_path)
        
        if not config_data:
            print(f"Could not read configuration from {config_path}")
            return False
        
        # Initialize KB manager
        kb = KnowledgeBasesForAmazonBedrock()
        
        # Get knowledge base ID
        kb_id = kb.get_kb_id_from_name(config_data["knowledge_base_name"])
        
        if not kb_id:
            print(f"Knowledge Base '{config_data['knowledge_base_name']}' not found")
            return False
        
        # Get knowledge base details
        kb_details = kb.get_kb(kb_id)
        
        if not kb_details:
            print(f"Could not retrieve details for Knowledge Base")
            return False
        
        kb_info = kb_details["knowledgeBase"]
        
        print(f"\nKnowledge Base Status:")
        print(f"   Name: {kb_info['name']}")
        print(f"   ID: {kb_info['knowledgeBaseId']}")
        print(f"   Status: {kb_info['status']}")
        print(f"   Description: {kb_info.get('description', 'No description')}")
        print(f"   Created: {kb_info.get('createdAt', 'Unknown')}")
        print(f"   Updated: {kb_info.get('updatedAt', 'Unknown')}")
        
        # Check if status is ACTIVE
        if kb_info['status'] == 'ACTIVE':
            print("Knowledge Base is ready for queries!")
        else:
            print(f"Knowledge Base status is {kb_info['status']} - it may not be ready for queries yet")
        
        return True
        
    except Exception as e:
        print(f"Error checking status: {str(e)}")
        return False


def delete_knowledge_base():
    """Delete the knowledge base and all associated resources"""
    print("Deleting Knowledge Base and associated resources...")
    
    try:
        # Load configuration
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "kb_store", "prereqs_config.yaml")
        config_data = read_yaml_file(config_path)
        
        if not config_data:
            print(f"Could not read configuration from {config_path}")
            return False
        
        # Confirm deletion
        kb_name = config_data["knowledge_base_name"]
        confirmation = input(f"Are you sure you want to delete Knowledge Base '{kb_name}' and ALL associated resources? (yes/no): ")
        
        if confirmation.lower() != 'yes':
            print("Deletion cancelled")
            return False
        
        # Initialize KB manager
        kb = KnowledgeBasesForAmazonBedrock()
        
        # Delete the knowledge base
        kb.delete_kb(
            kb_name=kb_name,
            delete_s3_bucket=True,
            delete_iam_roles_and_policies=True,
            delete_aoss=True
        )
        
        # Remove SSM parameter
        try:
            ssm_client = boto3.client("ssm", region_name=config_data.get("region_name", "us-east-1"))
            ssm_client.delete_parameter(Name=f"{kb_name}-kb-id")
            print("SSM parameter removed")
        except Exception:
            print("SSM parameter may not have existed")
        
        print(f"Knowledge Base '{kb_name}' and all associated resources deleted successfully!")
        return True
        
    except Exception as e:
        print(f"Error deleting Knowledge Base: {str(e)}")
        return False


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description="Knowledge Base deployment and management")
    parser.add_argument(
        "--action",
        choices=["deploy", "status", "delete"],
        default="deploy",
        help="Action to perform (default: deploy)"
    )
    
    args = parser.parse_args()
    
    print("🎓 Knowledge Base Management Tool")
    print("=" * 50)
    
    if args.action == "deploy":
        success = deploy_knowledge_base()
    elif args.action == "status":
        success = check_knowledge_base_status()
    elif args.action == "delete":
        success = delete_knowledge_base()
    
    if success:
        print("\nOperation completed successfully!")
        sys.exit(0)
    else:
        print("\nOperation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
