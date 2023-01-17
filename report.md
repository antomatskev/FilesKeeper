# Files Keeper Vulnerability Report

## Table of Contents
1. Summary
2. Methodology
3. Findings
4. Recommendations
5. Appendices

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
For testing five requirements from OWASP ASVS are used:
1. Sanitization and Sandboxing: 5.2.5 Verify that the application protects against template injection attacks by ensuring that any user input being included is sanitized or sandboxed. File name `}<IMG SRC=# onmouseover=&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#120;&#120;&#115;&#39;&#41;>.txt` invokes an alert on hovering a mouse over it right after any file is uploaded;
2. File Execution: 12.3 **TODO**
3. Password Security: 2.1 **TODO**
4. Session Termination: 3.3.1: After logging out the session cookie doesn't get invalidated and can be used to resume an authenticated session. **TODO**
5. **TODO**
Options: 1.2.3, 1.12.2, 

## Findings
**TODO**

## Recommendations
**TODO**

## Appendices
1. OWASP ASVS Latest Stable Version - https://github.com/OWASP/ASVS/tree/v4.0.3#latest-stable-version---403
2. XSS Filter Evasion - https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html
3. 