# Status

`Valid`

# Project Description

The **Flight Log Analyser** is a web-based application designed to facilitate the upload, processing, and visualization of Ardupilot flight logs (`.BIN`,`.log` files), along with associated flight test documentation (Markdown `.md` files) and videos. Built using Flask, the application offers an intuitive interface for drone enthusiasts and engineers to analyze flight performance metrics such as attitude, rate, altitude, Electronic Speed Controller (ESC) data, and battery status. It supports GitHub OAuth for secure user authentication and utilizes a SQLite database to store session data.
[Github Repo](https://github.com/Pan-Robotics/Flight-Log-Analyser/)

# Methodology

The application is developed in Python using the Flask framework for web development. It incorporates Bootstrap for responsive UI design. The system allows users to:

- Authenticate securely via GitHub OAuth.
- Upload Ardupilot `.BIN` or `.log` log files for flight data analysis.
- Upload Markdown (`.md`) files to document flight test processes.
- Upload multiple video files to associate with flight logs.

The uploaded data is processed and visualized to provide insights into various flight parameters. Session data and user information are managed using a SQLite database.

# Results and Deliverables

The primary deliverable is a functional web application that enables users to:

- Securely log in using GitHub credentials.
- Upload and manage flight logs, documentation, and videos.
- Visualize flight performance metrics, including attitude, rate, altitude, ESC data, and battery status.

The application enhances the ability of users to analyze and document drone flight tests comprehensively.

# Remarks

The project is currently hosted on GitHub and is open for contributions. It is particularly useful for drone developers and testers who utilize Ardupilot systems and seek an integrated platform for analyzing and documenting flight data. Future enhancements could include support for additional log file formats, more advanced data analysis features, and deployment to eternal servers.

--- 
