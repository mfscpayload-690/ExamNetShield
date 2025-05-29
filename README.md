# 🔐 A Novel Framework for Lab Exam Integrity Using Netbooting

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Tech Stack](https://img.shields.io/badge/TechStack-LTSP%2C%20PXE%2C%20Flask%2C%20Epoptes-informational)

## 📘 Overview

This project proposes a secure, scalable, and centralized framework for conducting lab-based examinations using **network booting** (Netbooting) via the **Linux Terminal Server Project (LTSP)**.

By booting all lab systems from a centralized, tamper-proof image, we eliminate inconsistencies, local vulnerabilities, and manual setup overhead. A custom-built **Flask web app** and **Epoptes** classroom monitoring tool enable full visibility and control throughout the exam lifecycle.

> 🎓 Mini project submitted to **APJ Abdul Kalam Technological University**, 2025.

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
| Server OS      | Debian 12 with XFCE             |

---

## 📸 Screenshots

### 👨‍🏫 Teacher Dashboard
![Teacher Dashboard](assets/teacher-dashboard.png)

### 👩‍🎓 Student Exam Interface
![Student Interface](assets/student-interface.png)



---

## 🛠️ Installation

### 📌 Prerequisites
- Debian-based OS
- PXE-compatible client systems
- VirtualBox (for building custom client images)

### 🧱 Setup Steps

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

4. **Run Flask Web App**
    ```bash
    cd flask-app
    python app.py
    ```

5. **Start Monitoring with Epoptes**
    ```bash
    sudo epoptes
    ```

> Detailed setup instructions available in the [project report](./Major.pdf).

---

## 🎯 Use Case

This framework is designed for **colleges and schools** that need to conduct **lab-based exams** in a controlled and scalable environment. It guarantees uniformity, secures academic integrity, and streamlines IT management.



---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

**Sharon Aliyas Johnson**  
📫 [LinkedIn](https://www.linkedin.com/in/sharonaliyas/)  
🌐 [Portfolio](https://portfolio-8u1t.vercel.app)

---

> “Integrity is doing the right thing, even when no one is watching.” — C.S. Lewis
