# Cloud Computing — Fundamentals

## 1. Introduction

Cloud computing is the delivery of computing resources such as servers, storage, databases, networking, software, and processing power over the internet.

Instead of purchasing and maintaining physical infrastructure, users can access computing resources on demand.

Examples of cloud providers include:

- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud Platform (GCP)

## 2. Characteristics of Cloud Computing

Important characteristics include:

- On-demand self-service
- Broad network access
- Resource pooling
- Rapid elasticity
- Measured service
- Scalability
- High availability

## 3. Benefits

- Reduced infrastructure cost
- Flexible resource usage
- Easy scalability
- Global accessibility
- Faster deployment
- Backup and disaster recovery
- High availability

## 4. Challenges

- Internet dependency
- Security concerns
- Privacy concerns
- Vendor lock-in
- Compliance requirements
- Cost management
- Service outages

## 5. Cloud Service Models

### IaaS — Infrastructure as a Service

Provides virtualized infrastructure such as:

- Virtual machines
- Storage
- Networks
- Firewalls

Example: Amazon EC2.

### PaaS — Platform as a Service

Provides a platform for developing and deploying applications without managing the underlying infrastructure.

Examples include managed application platforms and database services.

### SaaS — Software as a Service

Provides complete software applications through the internet.

Examples include web-based email, online office applications, and collaboration platforms.

### Comparison

| Model | User Mainly Manages |
|---|---|
| IaaS | OS, applications, data |
| PaaS | Applications and data |
| SaaS | Application usage and data |

## 6. Cloud Deployment Models

### Public Cloud

Infrastructure is provided by a cloud provider and shared among customers.

### Private Cloud

Cloud infrastructure is dedicated to a particular organization.

### Hybrid Cloud

Combines public and private cloud environments.

### Community Cloud

Infrastructure is shared by organizations with common requirements.

## 7. Virtualization

Virtualization creates virtual versions of computing resources.

A physical server can run multiple virtual machines.

```text
Physical Server
      |
   Hypervisor
  /    |     \
 VM1   VM2    VM3
```

## 8. Hypervisors

A hypervisor manages virtual machines.

### Type 1 Hypervisor

Runs directly on physical hardware.

### Type 2 Hypervisor

Runs on top of a host operating system.

## 9. Containers

Containers package an application with its dependencies so that it can run consistently across environments.

Docker is a popular container technology.

Containers are generally lighter than full virtual machines because they share the host operating system kernel.

## 10. Kubernetes

Kubernetes is an open-source platform used to manage containerized applications.

Common capabilities include:

- Container orchestration
- Scaling
- Service discovery
- Load balancing
- Self-healing

## 11. AWS Fundamentals

AWS provides cloud services for:

- Compute
- Storage
- Databases
- Networking
- Security
- Monitoring
- Machine learning

Important AWS services include:

| Service | Purpose |
|---|---|
| EC2 | Virtual servers |
| S3 | Object storage |
| RDS | Managed relational databases |
| Lambda | Serverless computing |
| VPC | Virtual networking |
| IAM | Identity and access management |
| CloudWatch | Monitoring |

## 12. Serverless Computing

Serverless computing allows developers to run code without directly managing servers.

AWS Lambda is an example.

The cloud provider manages the underlying infrastructure and automatically allocates resources according to demand.

## 13. Cloud Security

Important cloud security practices include:

- Identity and access management
- Encryption
- Network security
- Authentication
- Authorization
- Logging
- Monitoring
- Backup

## 14. Important Questions

1. What is cloud computing?
2. Explain characteristics of cloud computing.
3. What are IaaS, PaaS and SaaS?
4. Compare public and private cloud.
5. What is virtualization?
6. Explain Type 1 and Type 2 hypervisors.
7. What is Docker?
8. What is Kubernetes?
9. What is serverless computing?
10. Explain important AWS services.

## Quick Revision

```text
Cloud Computing
├── Characteristics
├── Benefits
├── Challenges
├── Deployment Models
│   ├── Public
│   ├── Private
│   ├── Hybrid
│   └── Community
├── Service Models
│   ├── IaaS
│   ├── PaaS
│   └── SaaS
├── Virtualization
├── Containers
├── Kubernetes
├── Serverless
└── Cloud Security
```