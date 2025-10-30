# 🔐 A Novel Framework for Lab Exam Integrity Using Netbooting

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Tech Stack](https://img.shields.io/badge/TechStack-LTSP%2C%20PXE%2C%20Flask%2C%20Epoptes-informational)

## 📘 Overview

This project proposes a secure, scalable, and centralized framework for conducting lab-based examinations using **network booting** (Netbooting) via the **Linux Terminal Server Project (LTSP)**.

By booting all lab systems from a centralized, tamper-proof image, we eliminate inconsistencies, local vulnerabilities, and manual setup overhead. A custom-built **Flask web app** and **Epoptes** classroom monitoring tool enable full visibility and control throughout the exam lifecycle.

---

## 🚀 Features

- 🖥️ Diskless boot via **PXE/iPXE** for consistent, non-persistent environments
- 🔐 Secure, fresh OS instance for every exam session
- 📊 Real-time student monitoring with **Epoptes**
- 🧑‍🏫 Web-based teacher panel (built with Flask) for:
  - Exam creation and management
  - Live monitoring of submissions
  - Session timing and login control
- ⚡ Fast setup for large-scale deployments
- 💬 Supports teacher-student interaction via broadcast

---

## 🧰 Tech Stack

| Component       | Technology                      |
|----------------|----------------------------------|
| OS Deployment  | PXE Booting, iPXE, LTSP         |
| Backend        | Python, Flask                   |
| Monitoring     | Epoptes                         |
| Network Mgmt   | dnsmasq, DHCP, TFTP             |
| Server OS      | Fedora 43 with KDE Plasma             |

---

## 📸 Screenshots

### 👨‍🏫 Teacher Dashboard
<img width="1548" height="1198" alt="image" src="https://github.com/user-attachments/assets/7ed5d78e-0b6a-4db7-84c1-4510f2f035c9" />

### 👩‍🎓 Student Exam Interface
<img width="1572" height="651" alt="image" src="https://github.com/user-attachments/assets/09a59185-944e-4ebf-b6bf-1ecd8bcffce6" />



---

## 🛠️ Installation

### 📌 Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Debian-based OS (for LTSP server setup)
- PXE-compatible client systems
- VirtualBox (for building custom client images)

### 🚀 Quick Start with Docker

1. **Clone the repository**
    ```bash
    git clone https://github.com/mfscpayload-690/ExamNetShield.git
    cd ExamNetShield
    ```

2. **Configure environment**
    ```bash
    cp .env.example .env
    # Edit .env and set your SECRET_KEY and other configurations
    ```

3. **Run with Docker Compose**
    ```bash
    docker-compose up -d
    ```

4. **Create admin user**
    ```bash
    docker-compose exec web python create_user.py
    ```

5. **Access the application**
    - Open your browser and navigate to `http://localhost:5000`
    - Default credentials: username: `sharon`, password: `sharon` (change after first login)

### 🐍 Manual Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/mfscpayload-690/ExamNetShield.git
    cd ExamNetShield
    ```

2. **Create virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment**
    ```bash
    cp .env.example .env
    # Edit .env and set your SECRET_KEY and other configurations
    ```

5. **Initialize database and create admin user**
    ```bash
    python create_user.py
    ```

6. **Run the application**
    ```bash
    python app.py
    ```

7. **Access the application**
    - Open your browser and navigate to `http://localhost:5000`

### 🖥️ LTSP Server Setup

1. **Install LTSP**
    ```bash
    sudo apt install ltsp dnsmasq
    ```

2. **Build Client Image**
    - Create a custom Debian VM
    - Export and squash the filesystem

3. **Configure Boot Menu**
    ```bash
    ltsp image /opt/ltsp/client
    ```

4. **Start Monitoring with Epoptes**
    ```bash
    sudo epoptes
    ```

---

## 🧪 Testing

Run the test suite:
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

## 🔒 Security

This project implements several security measures:
- Session management with secure cookies
- Password hashing using Werkzeug
- File upload validation and sanitization
- Path traversal protection
- Input validation on all forms
- Logging for audit trails


## 🛣️ Roadmap

- [ ] Add multi-language support
- [ ] Implement real-time proctoring features
- [ ] Add automated grading system
- [ ] Support for multiple question types (MCQ, essay, coding)
- [ ] Export exam results to CSV/PDF
- [ ] Email notifications for exam events
- [ ] Two-factor authentication
- [ ] Mobile-responsive student interface

---

## 🎯 Use Case

This framework is designed for **colleges and schools** that need to conduct **lab-based exams** in a controlled and scalable environment. It guarantees uniformity, secures academic integrity, and streamlines IT management.


---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
