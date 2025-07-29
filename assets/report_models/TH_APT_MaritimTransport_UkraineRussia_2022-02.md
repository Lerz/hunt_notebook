### **1. Executive Summary**
**Objective**: This threat hunt focused on identifying and mitigating potential cyber threats from **Russian state-sponsored actors** targeting the transportation sector, specifically in the context of the Russia-Ukraine conflict, which escalated eralier this year.

**Key Findings**:
- **No direct cyberattacks** on the transportation industry were reported at the beginning of the conflict, but **spillover risks** from critical infrastructure attacks were high.
- Russian-affiliated cybercrime groups increased activity, targeting sectors including logistics and critical transportation nodes.
- **DDoS and ransomware attacks** were the most common tactics used, aimed at disrupting operations in Ukraine and Western-aligned countries.

**Recommendations**:
- Enhance **network monitoring** and adopt proactive threat hunting techniques.
- Patch known vulnerabilities, especially those in **logistics management software** and **critical infrastructure control systems**.
- Implement **multi-factor authentication (MFA)** and review remote access policies to mitigate risk.

### **2. Scope & Methodology**
**Timeframe**: Focused on activity from February 2022 to March 2022.  
**Data Sources**: Network traffic logs, endpoint detection and response (EDR) systems, and intelligence from government agencies such as **CISA**, **FBI**,**NSA**,**ANSSI** and **MCAD**.  
**Hunt Focus**: The threat hunt concentrated on detecting activity linked to **ransomware** (e.g., **Conti**), **DDoS attacks**, and **phishing campaigns** targeting the transportation sector.

### **3. Hypotheses/Queries**
- Are there indicators of **phishing** or **malware** related to Russian-backed groups targeting transportation systems?
- Are there any signs of **network reconnaissance** or **DDoS activity** targeting transportation infrastructure?

### **4. Findings**
**Techniques Detected**:
- **DDoS Attacks**: DDoS campaigns were launched by Russian-aligned against Ukrainian organizations, with potential spillover effects on transportation services.
- **Ransomware**: The **Conti ransomware** group, aligned with Russian state interests, threatened critical infrastructure sectors in Western countries, including transportation and logistics.
  
**Indicators of Compromise (IOCs)**:
- **Malicious IPs**: IP addresses used in **DDoS attacks** were linked to Russian hacktivist groups.
- **Phishing Emails**: Multiple phishing campaigns were observed targeting logistics companies involved in humanitarian efforts.

**MITRE ATT&CK Mapping**:
- **T1190** - Exploitation of Public-Facing Applications: Used by Russian actors for initial access through vulnerable web-facing applications.
- **T1071** - Application Layer Protocol: Identified in DDoS attacks, where network protocols were used to flood services【69†source】.

### **5. Mitigation & Response**
**Actions Taken**:
- Enhanced monitoring and implemented additional **firewall rules** to block identified malicious IPs.
- Increased **incident response readiness** in the event of ransomware or DDoS attacks.

**Further Recommendations**:
- Regularly update transportation-related software and implement **network segmentation** to prevent lateral movement in case of breach.
- Conduct **tabletop exercises** simulating ransomware and DDoS scenarios to enhance response capabilities.

### **6. Conclusion**
This threat hunt confirmed increased cyber activity by Russian-backed actors in sectors adjacent to transportation. While no direct attacks were observed initially, the risk of spillover from DDoS attacks and ransomware targeting critical infrastructure remains high. Especially with transport organization taking action to help in humanitary context Ukraine. Continuous monitoring and proactive defense measures are critical.
We recommand conducing a geopolitical **strategical CTI** with CERT Team.