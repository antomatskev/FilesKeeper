# Files Keeper Vulnerability Report

## Table of Contents
1. Summary
2. Methodology
3. Findings
4. Appendices

## Summary
### Objectives
The goal of this report is to test the Files Keeper application against five ASVS requirements. The result should be a description of how to repeat an attack, its limitations, and prerequisites; a list of risks found vulnerabilities could cause; recommendations on how to fix issues.

### Scope
This report covers the Files Keeper application hosted with replit service. The application's URL is https://fileskeeper.antomatskev.repl.co/ 

### Findings
There are five findings that correspond to OWASP ASVS 1.12.2, 2.1, 3.3.1, 5.2.5, and 12.1.1.

### Recommendations
Overall recommendations are to use some cloud storage for storing files, tweak registration, logging out, and file upload functionality.

### Overall Assessment
As the system is simple and doesn't have different user privileges, some findings don't have the severity they usually could have. Therefore fixing the mentioned issues would make the application much safer and the service more stable.

## Methodology
### Testing Scope
The scope of the testing is only the Files Keeper application with the URL https://fileskeeper.antomatskev.repl.co/
No other systems have been tested.

### Testing Approach
A White Box testing approach has been used. The source code of the application can be found at https://github.com/antomatskev/FilesKeeper . OWASP ASVS has been used to find issues in the application, especially five points: 1.12.2, 2.1, 3.3.1, 5.2.5, and 12.1.1. For analysing web pages content Inspect functionality of Google Chrome has been used.

### Testing Schedule
The testing has been done on the 17th of January, 2023.

### Testing Team
The team consists of Anton Matskevich, pentester, who is responsible for the full life cycle of the test provided.

### Compliance
No compliance requirements have been considered during the test, as the application under the test has been developed by the pentester himself.

## Findings
### Vulnerabilities
1. Secure File Upload Architecture (ASVS 1.12.2). All uploaded files are stored on the same server, instead of using an unrelated cloud file storage bucket. Also, no Content Security Policy was implemented. This can lead to XSS attacks, which has high likelihood;
2. Password Security (ASVS 2.1). Almost all ASVS requirements under section 2.1 aren't implemented, except for 2.1.3, 2.1.4, 2.1.9, 2.1.10. Overall, password standards have been ignored during the development process. Violating this section allows attackers to easily perform password attacks, which have a high likelihood;
3. Session Termination (ASVS 3.3.1). After logging out the session cookie doesn't get invalidated and can be used to resume an authenticated session by attackers. This could have a high impact, as it allows impersonating another user, but the system doesn't have different account privileges, nor user's actions are logged. Therefore, the impact is medium, as the likelihood is high (attackers will need to find a way to get user's cookies, and there is one: see the next point);
4. Sanitization and Sandboxing (ASVS 5.2.5). File name `}<IMG SRC=# onmouseover=&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#120;&#120;&#115;&#39;&#41;>.txt` invokes an alert on hovering a mouse over it right after any file is uploaded. The impact is high allowing attackers to steal user's cookies to impersonate them later. The likelihood is also high;
5. File Upload (ASVS 12.1.1). Uploading large files to fill up the storage makes the files uploading service unavailable. This has a very high impact, because of the Denial of Service possibility. The likelihood is also very high because the server storage is relatively small;

### Supporting Evidence
1. As it is White Box testing, the pentester has access to the system and sees the file-storing implementation in the source code:
`file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))`
Also, there is `uploads` directory in the replit, which contains all the stored files;
2. This issue is seen also from the source code: `password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])` and from the prompt visible during the registration process: ![poc 2](https://raw.githubusercontent.com/antomatskev/FilesKeeper/main/report/poc-2.png)
3. This will be described in the next section;
4. On the screenshot the alert with the text "xss" can be seen, which appears after hovering the cursor over the uploaded file with the name `}<IMG SRC=# onmouseover=&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#120;&#120;&#115;&#39;&#41;>.txt`: ![poc 4](https://raw.githubusercontent.com/antomatskev/FilesKeeper/main/report/poc-4.png)
5. After the storage gets filled the application itself doesn't indicate any issues, but the logs have an exception:
```
172.31.128.1 - - [18/Jan/2023 10:48:00] "POST /upload HTTP/1.1" 200 -
172.31.128.1 - - [18/Jan/2023 10:48:00] "GET / HTTP/1.1" 200 -
[2023-01-18 10:52:59,466] ERROR in app: Exception on /upload [POST]
Traceback (most recent call last):
  File "/home/runner/FilesKeeper/venv/lib/python3.8/site-packages/flask/app.py", line 2525, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/runner/FilesKeeper/venv/lib/python3.8/site-packages/flask/app.py", line 1822, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/runner/FilesKeeper/venv/lib/python3.8/site-packages/flask/app.py", line 1820, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/runner/FilesKeeper/venv/lib/python3.8/site-packages/flask/app.py", line 1796, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "main.py", line 98, in upload
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  File "/home/runner/FilesKeeper/venv/lib/python3.8/site-packages/werkzeug/datastructures.py", line 3006, in save
    copyfileobj(self.stream, dst, buffer_size)
  File "/nix/store/2vm88xw7513h9pyjyafw32cps51b0ia1-python3-3.8.12/lib/python3.8/shutil.py", line 208, in copyfileobj
    fdst_write(buf)
OSError: [Errno 122] Disk quota exceeded
172.31.128.1 - - [18/Jan/2023 10:52:59] "POST /upload HTTP/1.1" 500 -
```

### Proof-of-concepts
1. No PoC available;
2. To make sure there are 8-symbol passwords available (ASVS 2.1.1):
   1. Go to https://fileskeeper.antomatskev.repl.co/register
   2. Create a new user with some username (i.e. pwd-test)
   3. As a password enter 8 symbols (i.e. 12345678)
   4. Click on the `Sign Up` button and make sure you get to the page with the string `The new user has been registered. Log in!` shown
   5. Make sure you are able to log in with the registered username and password
3. To make sure cookie doesn't get invalidated, you'll need two accounts (i.e. pwd-test from the previous test and cookie-test):
   1. Log in to the Files Keeper using some account (i.e. pwd-test)
   2. Using built-in browser tools find the account's session cookie and copy it (in Google Chrome right-click on the web page, choose `Inspect`, then click `Application`, then under `Storage` section choose `Cookies`)
   3. Log out from the application by clicking on `Log out` on the third line of the web page
   4. Log in to the Files Keeper using the other account (i.e. cookie-test)
   5. Using built-in browser tools change the session cookie to the copied from the previous account
   6. Refresh the page and make sure the second line now welcomes the first user (i.e. `Welcome, pwd-test`)
4. To test XSS via file name:
   1. Log in to the File Keeper with some account (i.e. pwd-test)
   2. Create the file on your machine with the name `}<IMG SRC=# onmouseover=&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#120;&#120;&#115;&#39;&#41;>.txt`
   3. Upload this file to the File Keeper
   4. Right after the upload finishes, make sure the table gets updated with the newly added file, but it is rendered as a not found image
   5. Hover the cursor over this image
   6. Make sure an alert window appears with the text `xss` inside
5. To test the application's disk space overloading:
   1. Log in to the File Keeper with some account (i.e. pwd-test)
   2. Upload some file(s), which size will extend 1024 MB
   3. Make sure after that no new files can be uploaded to the website

### Severity
1. Severity of this issue itself is Medium, but it causes another issue;
2. Severity of this issue is High allowing attackers to perform successful passwords attacks;
3. Severity of this issue is Low, as impersonating another account in the current system doesn't give anything;
4. Severity of this issue is High allowing to steal cookies from another user;
5. Severity of this issue is High allowing to perform DoS;

### CVSS
1. No CVSS;
2. 7.5;
3. 6.5;
4. 7.5;
5. 7.5;

### Recommendations
1. Use some cloud storage for storing uploaded files (i.e. AWS bucket);
2. Set up a password policy and change the source code accordingly;
3. Tweak logging out functionality to invalidate a user's cookie;
4. Tweak main.js code, so it won't clear the table and build it again on its own, but use the flask template rendering for that;
5. Tweak file uploading functionality so it will check the size of uploaded files, also add exceptions handling, so users would be notified if file upload fails;

## Appendices
1. OWASP ASVS Latest Stable Version - https://github.com/OWASP/ASVS/tree/v4.0.3#latest-stable-version---403
2. XSS Filter Evasion - https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html
3. Files Keeper - https://fileskeeper.antomatskev.repl.co/
4. CVSS Calculator - https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator