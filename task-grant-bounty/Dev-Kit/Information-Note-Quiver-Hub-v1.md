# Status

`Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: None`

# Project Description

**Subject:** Work completed in fulfilment of Quiver Hub V1 Grant, Milestones M1–M3

Core deliverables for **M1–M3**, covering the **Hub Security Baseline**, **Logs v1 Module**, and **OTA v1 Module** for Quiver Hub V1. This phase was focused on delivering the first operational core of the platform and closing the most immediate gaps needed to make the Hub practically usable.

In this phase, I executed on three priority areas:
-   **M1: Hub Security Baseline**  
    established the initial job-security and artefact-integrity foundations for the Hub.
-   **M2: Logs v1 Module**  
    built the first working log retrieval and handling flow between the flight controller, the companion computer, and the Hub UI.
-   **M3: OTA v1 Module**  
    built the first firmware upload, validation, staging, dispatch, and flashing flow for remote update operations.
    
# Methodology

I used a job-based execution model in which the Hub dashboard dispatches work through the backend, and the Raspberry Pi companion polls, acknowledges, and executes those jobs against the flight controller and related subsystems. This gave me a consistent way to implement both log-handling and OTA workflows while also creating the basis for future security and permission hardening.

The work I completed across M1–M3 included the following:

## 1. Security baseline

A formal job-security analysis was carried out and documented, covering:
-   artefact integrity,
-   job allow-listing,
-   job reliability,
-   and job permissions.
    
From that work, I implemented the most immediately critical security foundations needed for this phase.

A key result was the introduction of **firmware artefact integrity verification**. I made the Hub compute and store a **SHA-256 hash** when firmware is uploaded, pass that hash through the `flash_firmware` job payload, and verify it on the companion before any flashing takes place. If the hash does not match, the flash is aborted and the temporary file is cleaned up.

I also implemented the **job reliability** layer, including retry handling, expiry behaviour, timeout reaping, locking / mutex protections, and cleanup behaviour for stuck or failed work.

Some elements of the job-security pipeline, particularly **job allow-listing** and **job permissions**, were intentionally left as planned follow-on work. This was not because they were overlooked, but because they are more appropriately completed as part of the next stage of platform development alongside the broader **Quiver SDK / quiver-hub integration layer**, rather than being forced prematurely into the M1–M3 delivery window.

## 2. Logs v1

The first complete **FC-to-companion-to-Hub logs pipeline** was built.

On the companion side, I implemented a three-tier strategy for log access:
-   check local cache first,
-   attempt HTTP access to FC logs,
-   and fall back to FTP / MAVFTP-style retrieval where needed.

On the Hub side was built the supporting routes and UI flows needed to make this usable from the dashboard.

In the frontend, I delivered dedicated operational views for:
-   **FC Logs**
-   **OTA Updates**
-   **Diagnostics**
-   **Remote Logs**
    
Within the logs flow, it enables users to:
-   trigger scan jobs,
-   browse discovered logs,
-   request downloads from the FC,
-   store retrieved logs in the Hub,
-   download them via the browser,
-   and forward completed logs into analytics workflows.

This moved the Hub from being a conceptual control surface toward a working operational tool for handling real flight data.

## 3. OTA v1

The first operational **OTA firmware workflow** for Quiver Hub was built.

This included:
-   firmware upload,
-   firmware record creation,
-   SHA-256 hashing,
-   job dispatch for flashing,
-   staged delivery through the companion,
-   and the flash request flow to the FC.
    
The OTA flow was designed around a staged and validated process rather than ad hoc manual update handling. The companion downloads the firmware artefact, verifies its integrity, extracts metadata, temporarily serves the artefact where needed for the FC-side pull flow, and then completes the flash-and-reboot sequence.

I also built the Hub-side management functions needed to support this flow, including listing firmware, uploading it, requesting flash jobs, and clearing failed firmware records.

# Results and Deliverables

Through M1–M3, delivered was the first practical operational core of [Quiver Hub](https://github.com/Pan-Robotics/Arrow-Quiver-Hub) V1.

Specifically delivered was:
-  **Documented and partially implemented security baseline**, with artefact integrity and job reliability in place,
- Working **Logs v1 pipeline** for scan, discovery, retrieval, storage, and analytics forwarding,
- Working **OTA v1 foundation** for firmware upload, hashing, dispatch, and flash execution,
- Frontend operational tooling covering **Logs, OTA, Diagnostics, and Remote Logs**,
- Hub-side job and API scaffolding needed to support those workflows.
    
# Remarks

This phase should be understood as the delivery of the **first operational core** of Quiver Hub V1, not the completion of the entire long-term Hub / SDK architecture.

What was completed in M1–M3 was the most immediately valuable and practical slice of work needed to make the Hub materially functional: security foundations, logs handling, and OTA handling.

Where parts of the security pipeline remain marked as **planned**  that should be understood as a deliberate sequencing decision. I identified those items at this stage, but they are more appropriately completed in the next layer of platform maturation alongside the wider **Quiver SDK / quiver-hub** development path.

Further Development of Quiver Hub could implement Comprehensive Mission Planning, including Autonomous Path Planning and Control (M4), as well as then leading into multiple deployment strategies; A Local
individual system deployment, and hosted scalable Saas platform (M5). Beyond these are continued developer SDK formalisation, encapsulation, and functional expansion, to make payload deployment easier:
[Quiver SDK Repo](https://github.com/Arrow-air/quiver-sdk)

# References

[Quiver Hub Information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-Hub-Software.md)
[Quiver SDK Information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-SDK.md)
[Quiver SDK Test Information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-SDK-Test.md)
[Job Security Analysis](https://github.com/Pan-Robotics/Arrow-Quiver-Hub/blob/main/docs/JOB_SECURITY_ANALYSIS.md)
[Logs OTA Pipeline](https://github.com/Pan-Robotics/Arrow-Quiver-Hub/blob/main/docs/LOGS_OTA_PIPELINE.md)
