# 1. Import required packages
import os
import boto3
import json

# 2. Search for .txt files under the 'parameters' folder
def find_txt_files(directory):
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

# 3. Interact with the Bedrock Claude 3 Sonnet model
runtime_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

claude3_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

def claude3(prompt):
    body = json.dumps(
        {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": f"{prompt}"}]}
            ],
            "max_tokens": 1000,
            "temperature": 0.5,
            "top_k": 250,
            "top_p": 0.7,
            "anthropic_version": "bedrock-2023-05-31",
        }
    )

    response = runtime_client.invoke_model(body=body, modelId=claude3_model_id)

    response_body = json.loads(response.get("body").read())
    output_text = "".join([content["text"] for content in response_body.get("content", [])])
    return output_text

def generate_sam_yaml(text_file):
    # Read the text file content
    with open(text_file, 'r') as f:
        text_content = f.read()

    # Prepare the prompt for the Sonnet model
    prompt = f"You are an AI assistant specializing in generating AWS SAM (Serverless Application Model) YAML files based on natural language descriptions. Your task is to read the provided text and understand the requirements for the serverless application. Then, you will generate a corresponding AWS SAM YAML file that defines the necessary resources and configurations for the application.\n\nText:\n{text_content}"

    # Call the Sonnet model using claude3 function
    sam_yaml_content = claude3(prompt)

    return sam_yaml_content

def main():
    # Set up AWS credentials (if not already configured)
    # boto3.setup_default_session(profile_name='your_profile_name')

    # Find all .txt files in the 'parameters' folder
    txt_files = find_txt_files('parameters')

    # Get the current working directory
    current_dir = os.getcwd()

    # Iterate over the .txt files and generate SAM YAML files
    for txt_file in txt_files:
        try:
            sam_yaml_content = generate_sam_yaml(txt_file)
            sam_yaml_filename = os.path.join(current_dir, os.path.splitext(os.path.basename(txt_file))[0] + '.yaml')
            with open(sam_yaml_filename, 'w') as f:
                f.write(sam_yaml_content)
            print(f"Generated {sam_yaml_filename} from {txt_file}")
        except Exception as e:
            print(f"Error generating SAM YAML for {txt_file}: {e}")

if __name__ == "__main__":
    main()