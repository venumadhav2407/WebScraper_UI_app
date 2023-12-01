import subprocess


packages = ['requests', 'beautifulsoup4', 'customtkinter', 'regex']


for package in packages:
    try:
        result = subprocess.run(['pip', 'show', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"{package} is already installed.")
    except subprocess.CalledProcessError:
        print(f"{package} is not installed.")
        subprocess.run(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

print("All required packages are now installed!")
