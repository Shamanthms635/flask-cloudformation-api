from flask import Flask, jsonify
import boto3
import botocore
import json
import time
import uuid

app = Flask(__name__)

# --- CONFIGURATION ---
STACK_NAME = "MyNetworkStack"
REGION = "ap-southeast-2"

cloudformation = boto3.client('cloudformation', region_name=REGION)

# --- HOME ROUTE ---
@app.route('/')
def home():
    return jsonify({"message": "Flask CloudFormation API is running ✅"}), 200

# --- GET /template ---
@app.route('/template', methods=['GET'])
def get_template():
    try:
        response = cloudformation.get_template(StackName=STACK_NAME)
        template_body = response.get('TemplateBody', {})
        return jsonify(template_body), 200
    except botocore.exceptions.ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# --- PUT /template ---
@app.route('/template', methods=['PUT'])
def update_subnet_to_private():
    try:
        response = cloudformation.get_template(StackName=STACK_NAME)
        template_body = response.get('TemplateBody', {})

        resources = template_body.get('Resources', {})
        subnet = resources.get('MySubnet')

        if not subnet:
            return jsonify({"error": "MySubnet not found in template"}), 404

        subnet_props = subnet.get('Properties', {})
        subnet_props['MapPublicIpOnLaunch'] = False
        subnet['Properties'] = subnet_props
        resources['MySubnet'] = subnet
        template_body['Resources'] = resources

        with open('template_modified.json', 'w') as f:
            json.dump(template_body, f, indent=2)

        return jsonify({
            "message": "Template updated successfully. Subnet is now private.",
            "updated_resource": subnet
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- POST /changeset ---
@app.route('/changeset', methods=['POST'])
def create_and_execute_changeset():
    try:
        # Load the modified template
        with open('template_modified.json', 'r') as f:
            modified_template = json.load(f)

        # Create a unique ChangeSet name
        changeset_name = f"ChangeSet-{uuid.uuid4().hex[:8]}"

        # Create ChangeSet
        response = cloudformation.create_change_set(
            StackName=STACK_NAME,
            TemplateBody=json.dumps(modified_template),
            ChangeSetName=changeset_name,
            ChangeSetType='UPDATE',
            Description='Update subnet to private',
        )

        # Wait for ChangeSet to be created
        while True:
            describe = cloudformation.describe_change_set(
                StackName=STACK_NAME,
                ChangeSetName=changeset_name
            )
            status = describe['Status']
            reason = describe.get('StatusReason', '')

            if status in ['CREATE_COMPLETE', 'FAILED']:
                break
            time.sleep(2)

        if status == 'FAILED':
            return jsonify({
                "message": "ChangeSet creation failed",
                "reason": reason
            }), 400

        # Execute ChangeSet
        cloudformation.execute_change_set(
            StackName=STACK_NAME,
            ChangeSetName=changeset_name
        )

        return jsonify({
            "message": "ChangeSet executed successfully",
            "changeset": changeset_name
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- MAIN ---
if __name__ == '__main__':
    app.run(debug=True)
