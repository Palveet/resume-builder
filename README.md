
## How to Run the Project

### Prerequisites
1. **Download the Source Code**  
   Clone or download the source code to your local machine.

2. **Install Python**  
   Ensure Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

---

### Installation
1. **Install Dependencies**  
   Navigate to the project directory in your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Database Migrations**  
   Generate and apply the necessary database migrations by running:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start the Development Server**  
   Launch the server using the command:
   ```bash
   python manage.py runserver
   ```
   Your project will start on `localhost` at port `8000`.  
   Access it at: [http://localhost:8000/](http://localhost:8000/)

-

### Frontend Integration
To connect to the backend, use the associated frontend repository:  
[Frontend Repository](https://github.com/Palveet/resume_builder_react)
