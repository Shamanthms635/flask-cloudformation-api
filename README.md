
# Flask + AWS CloudFormation Template Modifier API

This is a Flask-based REST API that interacts with AWS CloudFormation using **Boto3**. It allows you to:

- ✅ Fetch an existing CloudFormation template
- ✏️ Modify a subnet resource (make it private)
- 🚀 Apply the changes safely using a CloudFormation ChangeSet

---

## 📦 Project Structure

```
flask_aws_assignment/
│
├── app.py                      # Main Flask app with 3 API endpoints
├── template_modified.json      # Modified template (generated after PUT)
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── venv/                       # Python virtual environment
```

---

## 🛠 Prerequisites

- Python 3.8+
- AWS account with CloudFormation stack already created
- AWS CLI configured (`aws configure`)
- CloudFormation stack name must match in `app.py`

---

## 🔧 Setup Instructions

### 1. Clone this repository or copy the project files.

### 2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS/Linux
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set up AWS credentials:
```bash
aws configure
```
Provide:
- Access Key ID
- Secret Access Key
- Region: `ap-southeast-2`
- Output: `json` or leave blank

### 5. Start the Flask app:
```bash
python app.py
```

---

## 🌐 API Endpoints

### 1️⃣ `GET /template`

- **Description**: Fetches the current CloudFormation template for the specified stack
- **Response**: JSON of the full template

### 2️⃣ `PUT /template`

- **Description**: Modifies `MySubnet` to set `MapPublicIpOnLaunch: false` (make it private)
- **Effect**: Saves updated template as `template_modified.json`

### 3️⃣ `POST /changeset`

- **Description**: Creates and executes a ChangeSet based on `template_modified.json`
- **Effect**: Updates the AWS stack safely

---

## 🧪 Testing with Postman

### Base URL:
```
http://127.0.0.1:5000
```

| Method | Endpoint       | Description                          |
|--------|----------------|--------------------------------------|
| GET    | `/template`    | View current template from AWS       |
| PUT    | `/template`    | Modify subnet to private             |
| POST   | `/changeset`   | Apply changes via CloudFormation     |

No body or headers needed.

---

## 🔐 Permissions Used

The IAM user for this project should have either:

- `AdministratorAccess` (for development)  
**OR**  
- The following policies:
  - `AmazonEC2FullAccess`
  - `AWSCloudFormationFullAccess`
  - `AmazonVPCFullAccess`

---

## 📌 Notes

- Make sure the stack name (`MyNetworkStack`) matches your actual CloudFormation stack
- Flask app only runs locally (not deployed)
- `template_modified.json` is overwritten with each PUT call

---

## 🧑‍💻 Author

**Shamanth MS**  
---

## 🏁 Future Improvements (Optional)

- Add authentication to the Flask API
- Log CloudFormation change history
- Create a frontend UI to control the updates visually

---

## 📝 License

This project is for educational and job evaluation purposes only.
