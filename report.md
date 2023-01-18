# Files Keeper Vulnerability Report

## Table of Contents
1. Summary
2. Methodology
3. Findings
4. Appendices

## Summary
### Objectives
The goal of this report is to test Files Keeper application against five ASVS requirements. The result should be a description of how to repeat an attack, its limitations and prerequisities; list of risks found vulnerabilities could cause; recommendations on how to fix issues.

### Scope
This report covers Files Keeper application hosted with replit service. The application's URL is https://fileskeeper.antomatskev.repl.co/ 

### Findings
**TODO**

### Recommendations
**TODO**

### Overall Assessment
**TODO**

## Methodology
### Testing Scope
The scope of the testing is only Files Keeper application with URL https://fileskeeper.antomatskev.repl.co/
No other systems have been tested.

### Testing Approach
A White Box testing approach has been used. The source code of the application can be found at https://github.com/antomatskev/FilesKeeper . OWASP ASVS has been used to find issues in the application, especially five points: 1.12.2, 2.1, 3.3.1, 5.2.5, and 12.1.1. For analysing web pages content Inspect functionality of Google Chrome has been used.

### Testing Schedule
The testing has been done during the 17th of January, 2023.

### Testing Team
The team consists on Anton Matskevich, pentester, who is responsible for the full life cycle of the test provided.

### Compliance
No compliance requirements have been considered during the test, as the application under the test has been developed by the pentester himself.

## Findings
### Vulnerabilities
1. Secure File Upload Architecture (ASVS 1.12.2). All uploaded files are stored on the same server, instead of using an unrelated cloud file storage bucket. Also, no Content Security Policy implemented. This can lead to XSS attacks, which has high likelihood;
2. Password Security (ASVS 2.1). Almost all ASVS requirements under section 2.1 aren't implemented, except from 2.1.3, 2.1.9, 2.1.10. Overall, password standards have been ignored during the development process. Violating this section allows attackers to easily perform password attacks, which has high likelihood;
3. Session Termination (ASVS 3.3.1). After logging out the session cookie doesn't get invalidated and can be used to resume an authenticated session by attackers. This could have high impact, as it allows to impersonate another users, but the system doesn't have different account privileges, nor users actions are logged. Therefore, the impact is moderate, as the likelihood is high (attackers will need to find a way to get users cookies, and there is one: see the next point);
4. Sanitization and Sandboxing (ASVS 5.2.5). File name `}<IMG SRC=# onmouseover=&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#120;&#120;&#115;&#39;&#41;>.txt` invokes an alert on hovering a mouse over it right after any file is uploaded. The impact is high allowing attackers to steal users cookies to impersonate them later. The likelihood is also high;
5. File Upload (ASVS 12.1.1). Uploading large files to fill up the storage makes the files uploading service unavailable. This has very high impact, because of Denial of Service possibility. The likelihood is also very high, because the server storage is relatively small;

### Supporting Evidence

### Proof-of-concepts

### Severity

### CVSS

### Recommendations


## Appendices
1. OWASP ASVS Latest Stable Version - https://github.com/OWASP/ASVS/tree/v4.0.3#latest-stable-version---403
2. XSS Filter Evasion - https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html
3. 