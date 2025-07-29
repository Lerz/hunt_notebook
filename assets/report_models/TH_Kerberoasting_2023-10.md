### **1. Executive Summary**
**Objective**: The hunt aimed to identify and mitigate potential **Kerberoasting attacks** targeting Active Directory (AD) environments, which exploit service tickets to obtain valid credentials. A recent [crowdstrike report](xxxx) shown the increase of this threat. 
  
**Key Findings**:
- **583% increase** in Kerberoasting attacks since last year.
- Attackers were primarily leveraging misconfigurations in AD service accounts.
  
**Recommendations**:
- Enforce **multi-factor authentication (MFA)** on privileged accounts.
- Strengthen AD account policies and monitor for ticket requests.

### **2. Scope & Methodology**
- **Timeframe**: January 2023 to June 2023
- **Tools Used**: SIEM, AD Audit logs, Hanzo
- **Data Sources**: Active Directory service tickets, network traffic logs, and endpoint detection

### **3. Hypotheses/Queries**
- Are there unusual **service ticket requests** from non-privileged accounts?
- Is there any sign of **credential dumps** using tools like Mimikatz?
- Is MITRE ATT&CK framework **T1558** is exploited ?

### **4. Findings**
**Techniques Detected**:
- **T1558.003 - Kerberoasting**: Detected multiple requests for service tickets, which were abused with tentative to perform lateral movement
- **T1078 - Valid Accounts**: 62% of intrusions involved the use of valid credentials

**Indicators of Compromise (IOCs)**:
- Service ticket requests from unknown accounts.
- Detection of Kerberos-related PowerShell scripts.

### **5. Mitigation & Response**
**Actions Taken**:
- Asked to block suspicious service ticket requests and reset compromised AD accounts (ITSM INC0029574).
- Asking to enable strict auditing for service ticket usage (ITSM REQ0019228).
- Elaborating analytic based on finding.

```spl
index=windows sourcetype=WinEventLog:Security EventCode=4769
| lookup kerberoasting_whitelist.csv src_user OUTPUT src_user as is_whitelisted
| lookup thresholds.csv src_user OUTPUT threshold
| where isnull(is_whitelisted) AND count > threshold AND src_user!="krbtgt"
| stats count by src_user, dest_user, service_name
| where count > threshold
| table _time, src_user, dest_user, service_name, count
```

**Further Recommendations**:
- Accelerate tiering on EUWINSERV2012XX which was involved in incident

### **6. Conclusion**
This investigation revealed Kerberoasting attacks and highlighted the need for robust monitoring of AD service tickets. A part of server are not collected in SOC. While no major breaches were detected, the environment remains at risk without enhanced defenses.