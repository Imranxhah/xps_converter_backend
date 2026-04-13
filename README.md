<h1 align="center">XPS Converter Backend 📄</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Framework-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

## 📖 Overview
A robust file-processing backend engine developed using **Python & Django**. This API serves as the core processor for uploading `.xps` documents, analyzing their buffer content, and securely transforming them into versatile accessible formats dynamically.

## ✨ Features
- **File I/O Parsing**: Handles document streams cleanly, avoiding large memory overheads.
- **RESTful Endpoints**: Dedicated upload and download streaming capabilities linked natively to the Flutter frontend application.
- **Secure Processing**: Sandbox-isolated conversion methods ensuring data integrity and safety.

## 🛠️ Getting Started
```bash
git clone https://github.com/Imranxhah/xps_converter_backend.git
cd xps_converter_backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

---
*Created by [Imranxhah](https://github.com/Imranxhah)*
