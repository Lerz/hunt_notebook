### **1. Executive Summary**
**Objective**: This threat hunting activity was initiated in response to a **previous ransomware attack** onboard one of our transport ships. The incident occurred when a crew member inserted an **infected USB key** into the IT station of the **crew mess**, which resulted in both **IT and OT systems** being compromised.

**Key Findings**:
- No direct signs of ransomware infection were detected during this hunt, but **network traffic anomalies** were observed, particularly around remote access ports.
- Signs of **port scanning** and **unauthorized access attempts** were detected, which could indicate pre-attack reconnaissance similar to the methods used in the previous ransomware incident.

**Recommendations**:
- Further tighten **USB access controls** by enforcing restrictions on removable media.
- Implement **more rigorous segmentation** between onboard IT and OT systems to prevent lateral movement in case of future incidents.
- Integrate **Marlink’s SOC alerts** into our SIEM for early detection of network anomalies.
- Use USB white station onboard.
---

### **2. Scope & Methodology**
**Timeframe**: Focused on a two-week period, reviewing real-time monitoring logs and historical data from the onboard **White Station** and security tools. Special attention was given to vulnerabilities exposed by the **previous ransomware incident**.

**Data Sources**:
- **Marlink’s onboard security suite**, including network traffic logs, firewall data, and event logs from both IT and OT systems.
- **Incident report** from the **previous ransomware attack** on the "Messe des marins" IT station.

### **3. Hypotheses/Queries**
- Are there **residual vulnerabilities** from the previous ransomware incident related to removable media and USB drives?
- Is there evidence of **network abnormalities** or signs of **ransomware propagation** similar to the earlier attack that affected both IT and OT operations?

### **4. Findings**
**Previous Incident Overview**:
In the earlier incident, a crew member inserted an **infected USB key** into the **IT station** at the "crew mess," which led to a **ransomware infection** that spread to both onboard **IT and OT systems**. The malware encrypted critical files, disrupted cargo management systems until onboard intervention to restore backups.

**Current Techniques Detected**:
- **T1078 - Valid Accounts**: Detected abnormal login attempts at the IT station, possibly indicating repeated attack vectors from unauthorized accounts.
- **T1071 - Application Layer Protocol**: Network traffic analysis showed suspicious outbound connections from onboard IT systems, possibly signaling attempts to communicate with external C2 servers.

**Indicators of Compromise (IOCs)**:
- **Unauthorized access attempts** to IT systems similar to those seen in the prior ransomware incident.
- **Unusual network activity** on ports associated with remote access, including **port 3389 (RDP)**, which was exploited in the earlier attack.

### **5. Mitigation & Response**
**Actions Taken**:
- **USB restrictions** have been recommended to renforce fleet-wide to prevent unauthorized devices from being connected to onboard systems. Any detected attempts are now logged and flagged in real time.
- **Immediate blocking** of external IPs attempting unauthorized access to onboard systems with satelit link as been tested.
- **Regular scans** were conducted to ensure no remnants of the previous ransomware attack remain.

**Further Recommendations**:
- **Upgrade to USB control software** that logs and enforces policies for removable media usage across the fleet.
- Continue leveraging **Marlink’s detection** to enhance monitoring of IT and OT systems for network anomalies.
- Implement **network segmentation** between IT and OT systems, ensuring isolated operation in case of future attacks.

### **6. Lessons from the Previous Incident & Ongoing Security**
The ransomware attack that originated from the "crew mess" IT station was a clear reminder of the dangers posed by **inadequate USB controls** and **unsegmented networks**. Since the incident, USB restrictions and **incident response protocols** was handled in a specific project, but this threat hunt has identified **potential attack vectors** that still exist in network configurations.

**Next Steps**:
- **Proactive Threat Hunting**: Continue using Marlink’s onboard security tools for **real-time anomaly detection**.
- **Training and Awareness**: Implement crew awareness training to prevent the use of unauthorized USB devices onboard.
- **Incident Response Drills**: Conduct regular **tabletop exercises** to prepare the crew for responding to ransomware or network anomalies impacting both IT and OT systems.