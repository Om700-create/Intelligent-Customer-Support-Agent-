import os
from pathlib import Path

def create_file(path, content=""):
    """Create a file with the given content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_project_structure():
    """Create the complete project structure"""
    
    # Define the project structure
    project_structure = {
        "backend/app/__init__.py": "",
        "backend/app/main.py": "",
        "backend/app/core/__init__.py": "",
        "backend/app/core/config.py": "",
        "backend/app/core/security.py": "",
        "backend/app/core/database.py": "",
        "backend/app/core/deps.py": "",
        "backend/app/models/__init__.py": "",
        "backend/app/models/user.py": "",
        "backend/app/models/conversation.py": "",
        "backend/app/models/message.py": "",
        "backend/app/schemas/__init__.py": "",
        "backend/app/schemas/auth.py": "",
        "backend/app/schemas/user.py": "",
        "backend/app/schemas/chat.py": "",
        "backend/app/schemas/admin.py": "",
        "backend/app/services/__init__.py": "",
        "backend/app/services/huggingface_textgen.py": "",
        "backend/app/services/huggingface_classifier.py": "",
        "backend/app/services/conversation_service.py": "",
        "backend/app/prompts/__init__.py": "",
        "backend/app/prompts/system_prompt.txt": "",
        "backend/app/prompts/system_prompt_loader.py": "",
        "backend/app/prompts/classification_labels.json": "",
        "backend/app/routers/__init__.py": "",
        "backend/app/routers/auth.py": "",
        "backend/app/routers/chat.py": "",
        "backend/app/routers/admin.py": "",
        "backend/app/alembic/__init__.py": "",
        "backend/app/alembic/env.py": "",
        "backend/app/alembic/script.py.mako": "",
        "backend/app/alembic/versions/__init__.py": "",
        "backend/app/alembic/versions/2025_01_01_000001_init.py": "",
        "backend/requirements.txt": "",
        "backend/Dockerfile": "",
        "backend/alembic.ini": "",
        
        "frontend/__init__.py": "",
        "frontend/index.html": "",
        "frontend/package.json": "",
        "frontend/tsconfig.json": "",
        "frontend/vite.config.ts": "",
        "frontend/Dockerfile": "",
        "frontend/src/__init__.py": "",
        "frontend/src/main.tsx": "",
        "frontend/src/App.tsx": "",
        "frontend/src/styles.css": "",
        "frontend/src/api/__init__.py": "",
        "frontend/src/api/client.ts": "",
        "frontend/src/api/auth.ts": "",
        "frontend/src/api/chat.ts": "",
        "frontend/src/api/admin.ts": "",
        "frontend/src/store/__init__.py": "",
        "frontend/src/store/auth.tsx": "",
        "frontend/src/components/__init__.py": "",
        "frontend/src/components/LoginForm.tsx": "",
        "frontend/src/components/Navbar.tsx": "",
        "frontend/src/components/ConversationList.tsx": "",
        "frontend/src/components/ConversationDetail.tsx": "",
        "frontend/src/pages/__init__.py": "",
        "frontend/src/pages/LoginPage.tsx": "",
        "frontend/src/pages/DashboardPage.tsx": "",
        "frontend/src/pages/ConversationPage.tsx": "",
        
        "infra/docker-compose.yml": "",
        "infra/nginx.conf": "",
        "infra/init.sql": "",
        
        ".github/workflows/ci.yml": "",
        
        ".env.example": "",
        ".gitignore": "",
        "README.md": "",
    }
    
    # Create all files
    for file_path, content in project_structure.items():
        create_file(file_path, content)
    
    print("✅ Project structure created successfully!")
    print("📁 intelligent-support-agent/")
    print("├── backend/")
    print("├── frontend/") 
    print("├── infra/")
    print("├── .github/")
    print("└── configuration files")

if __name__ == "__main__":
    create_project_structure()