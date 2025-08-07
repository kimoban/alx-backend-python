# Docker Setup Instructions for Windows

## Install Docker Desktop for Windows

1. **Download Docker Desktop:**

   - Go to [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Download Docker Desktop for Windows

2. **Install Docker Desktop:**
   - Run the installer
   - Follow the installation wizard
   - Restart your computer when prompted

3. **Verify Installation:**

   ```powershell
   docker --version
   docker-compose --version
   ```

## Build and Run the Messaging App

1. **Open PowerShell as Administrator**

2. **Navigate to the project directory:**

   ```powershell
   cd "C:\Users\Isaiah Kimoban\Desktop\alx_prodev\prodevbe\alx-backend-python\messaging_app"
   ```

3. **Build the Docker image:**

   ```powershell
   docker build -t messaging-app -f .\messaging_app\Dockerfile .
   ```

4. **Run the container:**

   ```powershell
   docker run -p 8000:8000 -e DEBUG=True -e SECRET_KEY=django-insecure-docker-development-key -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 messaging-app
   ```

   Or use Docker Compose:

   ```powershell
   docker-compose up --build
   ```

5. **Access the application:**
   - Open your browser and go to http://localhost:8000

## Troubleshooting Windows Issues

### WSL2 Backend Issues

If you encounter WSL2 issues:

1. Enable WSL2 feature in Windows
2. Install a Linux distribution from Microsoft Store
3. Set WSL2 as default: `wsl --set-default-version 2`

### Hyper-V Issues

If you have Hyper-V conflicts:

1. Disable Hyper-V: `bcdedit /set hypervisorlaunchtype off`
2. Restart your computer
3. Try Docker Desktop again

### File Sharing Issues

If you get file sharing errors:

1. Go to Docker Desktop Settings
2. Resources → File Sharing
3. Add the project directory path
4. Apply & Restart
