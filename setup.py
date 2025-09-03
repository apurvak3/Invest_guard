import os

# Directory structure
structure = {
    "investorguard": {
        "backend": {
            "models": {"__init__.py": "", "fraud_model.py": "# ML model placeholder\n"},
            "blueprints": {
                "__init__.py": "",
                "fraud_detection.py": "# Fraud detection blueprint\n",
                "education.py": "# Education blueprint\n",
                "blockchain.py": "# Blockchain mock\n",
            },
            "utils": {
                "__init__.py": "",
                "encryption.py": "# Encryption utils\n",
                "scraping.py": "# Scraping utils\n",
            },
            "__init__.py": "",
            "app.py": "# Flask app entry\n",
            "config.py": "# Config file\n",
            "database.py": "# DB connection\n",
        },
        "frontend": {
            "app.py": "# Frontend entry\n",
        },
        "README.md": "# InvestorGuard Project\n",
        "requirements.txt": "flask\nsqlalchemy\npandas\nnumpy\nscikit-learn\nrequests\nbeautifulsoup4\ncryptography\n",
        "run.sh": "#!/bin/bash\npython backend/app.py\n",
    }
}


def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ InvestorGuard project structure created successfully!")
