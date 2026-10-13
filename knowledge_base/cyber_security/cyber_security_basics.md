# Cyber Security — Fundamentals

## 1. Introduction

Cyber security is the practice of protecting computers, networks, applications, systems, and data from unauthorized access, attacks, damage, or disruption.

Common security objectives are represented by the CIA Triad:

```text
Confidentiality
      +
Integrity
      +
Availability
```

## 2. CIA Triad

### Confidentiality

Ensures that information is accessible only to authorized users.

Techniques include:

- Encryption
- Access control
- Authentication

### Integrity

Ensures that data is not modified without authorization.

Techniques include:

- Hashing
- Digital signatures
- Checksums

### Availability

Ensures that systems and information are available when required.

Techniques include:

- Backups
- Redundancy
- Disaster recovery

## 3. Authentication

Authentication verifies the identity of a user or system.

Examples:

- Password
- OTP
- Biometrics
- Security keys

## 4. Authorization

Authorization determines what an authenticated user is allowed to access.

Example:

```text
User → Login → Authentication → Authorization → Resource
```

## 5. Encryption

Encryption converts readable data into an unreadable form using an encryption algorithm and key.

Decryption converts the encrypted data back into readable form.

### Symmetric Encryption

Uses the same key for encryption and decryption.

Example:

- AES

### Asymmetric Encryption

Uses a public key and a private key.

Example:

- RSA

## 6. Hashing

Hashing converts data into a fixed-length value.

A cryptographic hash is designed to make it computationally difficult to recover the original input.

Examples:

- SHA-256
- SHA-3

Passwords should generally be stored using secure password-hashing methods rather than plain text.

## 7. Common Cyber Attacks

### Phishing

Attempts to trick users into revealing sensitive information.

### Malware

Malicious software designed to damage systems, steal information, or perform unauthorized actions.

Types include:

- Virus
- Worm
- Trojan
- Ransomware
- Spyware

### Denial of Service

Attempts to make a service unavailable by overwhelming it with requests or traffic.

### SQL Injection

An attack where malicious input is used to manipulate database queries.

Prevention includes:

- Parameterized queries
- Input validation
- Least privilege

### Cross-Site Scripting

XSS occurs when malicious scripts are injected into web pages and executed in a user's browser.

Prevention includes:

- Output encoding
- Input validation
- Content Security Policy

## 8. Firewall

A firewall controls network traffic according to predefined security rules.

It can be implemented as:

- Network firewall
- Host-based firewall
- Cloud firewall

## 9. VPN

A Virtual Private Network creates an encrypted connection between a device and a network or service.

VPNs can improve privacy and provide secure remote access.

## 10. Digital Signature

A digital signature provides mechanisms for:

- Authentication
- Integrity
- Non-repudiation

It is based on asymmetric cryptography.

## 11. Access Control

Access control determines who can access a resource and what actions they can perform.

Common principles:

- Least privilege
- Role-based access control
- Strong authentication
- Separation of duties

## 12. Zero Trust

Zero Trust is a security approach based on the principle that access should not automatically be trusted simply because a user or device is inside a network.

Important concepts include:

- Verify explicitly
- Least privilege
- Continuous monitoring

## 13. Secure Software Development

Security should be considered throughout the software development lifecycle.

Important practices:

- Secure coding
- Dependency management
- Input validation
- Authentication
- Authorization
- Logging
- Security testing
- Vulnerability scanning

## 14. Cyber Security Best Practices

- Use strong passwords
- Enable multi-factor authentication
- Keep software updated
- Avoid suspicious links
- Encrypt sensitive data
- Maintain backups
- Apply least privilege
- Monitor systems
- Use secure network connections

## 15. Important Questions

1. What is cyber security?
2. Explain the CIA Triad.
3. Differentiate authentication and authorization.
4. What is encryption?
5. Compare symmetric and asymmetric encryption.
6. What is hashing?
7. What is phishing?
8. What is malware?
9. Explain SQL injection.
10. What is XSS?
11. What is a firewall?
12. What is a VPN?
13. What is a digital signature?
14. Explain Zero Trust.
15. What is least privilege?

## Quick Revision

```text
Cyber Security
├── CIA Triad
│   ├── Confidentiality
│   ├── Integrity
│   └── Availability
├── Authentication
├── Authorization
├── Encryption
│   ├── Symmetric
│   └── Asymmetric
├── Hashing
├── Malware
├── Phishing
├── SQL Injection
├── XSS
├── Firewall
├── VPN
├── Digital Signature
└── Zero Trust
```