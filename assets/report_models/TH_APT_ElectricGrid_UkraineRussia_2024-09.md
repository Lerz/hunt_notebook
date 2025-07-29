### **1. Executive Summary**
**Objective**: The purpose of this threat hunt is to assess the cybersecurity posture, given the current geopolitical conflict between **Ukraine and Russia**. The report focuses on detecting **state-sponsored attacks** targeting critical infrastructure, including electric grids and power generation facilities, in line with recent trends observed in cyber warfare.

**Key Findings**:
- Increased **reconnaissance activity** was detected, suggesting potential pre-attack mapping of critical electric grid systems.
- Several suspicious attempts to access OT systems were observed, possibly indicating efforts to disrupt or sabotage electricity production.
- No immediate signs of a successful compromise, but heightened risk due to **Advanced Persistent Threats (APT)** linked to **Russian state-sponsored groups**, such as **Sandworm** and **Berserk Bear**.

**Recommendations**:
- Strengthen **network segmentation** between IT and OT systems to mitigate the risk of lateral movement in case of a breach.
- Enhance real-time monitoring and logging of all activities across critical OT systems.
- Proactively block known IP addresses associated with Russian APT groups and monitor for Indicators of Compromise (IOCs) related to **Industroyer/CrashOverride** malware.

---

### **2. Scope & Methodology**
**Timeframe**: Focused on recent network activity from **February 2022 to September 2024**, with a focus on critical energy infrastructure.
  
**Data Sources**:
- **SIEM logs** from IT and OT systems.
- Threat intelligence feeds reporting on **Russian state-sponsored cyber activity**.
- Historical data from recent attacks on European energy producers, particularly during periods of escalation in the Ukraine/Russia conflict.

### **3. Hypotheses/Queries**
- Are there indicators of **APT activity** or **reconnaissance** related to Russia-linked groups like **Sandworm** targeting critical OT infrastructure?
- Are there any signs of **malware** or tools related to **Industroyer**, which was used in previous attacks on Ukraine’s power grid, being deployed against European electric production facilities?

### **4. Findings**
**Techniques Detected**:
- **T1595 - Active Scanning**: Multiple instances of unauthorized scanning were detected on critical OT systems, indicating reconnaissance efforts to map vulnerabilities within the electric grid’s control systems.
- **T1566 - Phishing**: Employees in administrative positions received phishing emails with malicious attachments, attempting to gain entry to IT systems, which could allow pivoting into OT networks.

**Indicators of Compromise (IOCs)**:
- IP addresses linked to **Berserk Bear (APT28)** were flagged for attempting to access corporate networks.

**MITRE ATT&CK Mapping**:
- **T0832 - Inhibit Response Function**: Analysis of detected activities suggests efforts to disable critical response functions in OT environments, which could result in significant power disruptions or damage to equipment.
- **T1195 - Supply Chain Compromise**: There were signs of attempts to compromise third-party vendors, whose services could provide indirect access to OT systems.

### **5. Mitigation & Response**
**Actions Taken**:
- **Real-time blocking** of known malicious IP addresses linked to Russian APT activity.
- **Incident response teams** were activated to monitor ongoing suspicious activity and respond to any potential breaches in real time.

**Further Recommendations**:
- **Conduct penetration testing** to simulate potential cyberattacks on electric production facilities and identify vulnerabilities before attackers exploit them.
- Deploy **multi-factor authentication (MFA)** across all access points, particularly for employees working on critical infrastructure.
- Regularly update **patch management systems** to close any vulnerabilities
- **Staff Training**: Conduct regular **cybersecurity awareness training** focused on phishing and spear-phishing campaigns, which remain one of the primary vectors of compromise.
- **Real-time OT Monitoring**: Integrate **OT systems** into the Security Operations Center (SOC) for continuous monitoring and rapid response in case of attack.

### **6. Conclusion**
The current geopolitical environment has led to increased cyber threats targeting critical infrastructure, particularly **electric production and energy facilities**. While no direct breaches have been detected, the ongoing reconnaissance and phishing activity by **Russian APT groups** suggest the need for continuous vigilance.