 
## AWS Account Plans

<details> <summary>✨ Free Plan (6 Months)</summary>

- **Purpose**: Learn, experiment, and build prototypes.
    
- **Credits**: Up to USD $200.

    - $100 on sign-up.
        
    - Additional $100 by completing activities (e.g., creating a budget alert).
        
- **Included Usage**: Free monthly limits for select AWS services.
    
- **Scaling**: Workloads can scale beyond credit thresholds.
    
- **Access**:
    
    - Access to all AWS services and features.
        
    - Limited access to certain services and AWS Marketplace.
        
- **Expiration**:
    
    - Account closes after 6 months or when credits are used up.
        
    - Can upgrade to paid plan to continue.
        

</details> <details> <summary>💼 Paid Plan</summary>

- **Purpose**: Develop production-ready workloads.
    
- **Credits**: Up to USD $200.
    
    - $100 on sign-up.
        
    - Additional $100 by completing activities.
        
- **Included Usage**: Free monthly limits for select AWS services.
    
- **Scaling**: Workloads can scale beyond credit thresholds.
    
- **Access**:
    
    - Full access to **all** AWS services and features.
        
    - No expiration or service interruption.
        
- **Pricing**: Standard AWS pricing applies after credits are exhausted.
    

</details> <details> <summary>📌 Additional Notes</summary>

- **Shared Benefits**:
    
    - Both plans include free monthly usage for select services.
        
    - Both receive $100 base credits + $100 via activity completion.
        
- **Credit Usage**:
    
    - Credits apply to eligible AWS services.
        
    - Example activity: Setting up a budget alert to monitor usage.
        
- **Resources**:
    
    - [AWS Privacy Policy](https://aws.amazon.com/privacy/)
        
    - [AWS Terms of Use](https://aws.amazon.com/terms/)
        
    - [Free Tier Details](https://aws.amazon.com/free)
        
    - [Free Tier Plans Documentation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html)
        

</details>


# AWS Marketplace Seller Account Setup

<details>
<summary>AWS Account Types</summary>

- **Root User**  
  - Created by default for every AWS account.
  - Has unrestricted access to all resources and billing.
  - Use only for account/admin-level tasks, not for daily operations.
  - Enable Multi-Factor Authentication (MFA) for security.
- **IAM (Identity and Access Management) User**  
  - Create multiple users with specific permissions.
  - Assign roles such as seller admin, product publisher, billing.
  - Best practice: Do not use root user for marketplace operations—use IAM users instead.

</details>

<details>
<summary>Registering as a Seller on AWS Marketplace</summary>

- **Prerequisites**
  - AWS account (preferably separate from other workloads).
  - Prepared company information, banking, and tax details (for paid listings).
- **Steps**
  1. Sign in to AWS Marketplace Management Portal with your AWS account.
  2. Review and accept the seller terms and conditions.
  3. Provide seller details:  
     - Company display name and legal name  
     - Company website  
     - Public contact email and description  
     - Company logo
  4. Enter and verify tax details (W-9, W-8, VAT/GST depending on location).
  5. Link and verify the bank account (required for paid products, US bank/virtual allowed).
  6. Submit registration for review.
- **Approval**
  - AWS reviews submitted details; follow up if extra info is needed.
  - You'll receive confirmation when ready to publish.

</details>

<details>
<summary>Creating Your Public Profile</summary>

- Display name (your AWS Marketplace name).
- Company description, logo, and website.
- Contact information for customer and AWS communication.
- This information is visible to AWS customers on the Marketplace listing.

</details>

<details>
<summary>Marketplace Management and Listing Products</summary>
  
- Access the AWS Marketplace Management Portal after approval.
- Manage product listings, update pricing, and access customer reports.
- Use IAM for granular team roles:  
  - Product publishing  
  - Billing and payment management  
  - Support and customer queries
- For software, follow the [SaaS/Product listing guides](https://docs.aws.amazon.com/marketplace/latest/userguide/create-public-profile.html).

</details>

<details>
<summary>Security & Best Practices</summary>

- Always use IAM users for daily management.
- Limit root user access; enable MFA on all sensitive users.
- Assign permissions based on roles (least privilege approach).
- Regularly audit users, roles, and billing activity.
- Read more on [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

</details>

<details>
<summary>Additional Resources</summary>

- [AWS Marketplace Seller User Guide](https://docs.aws.amazon.com/marketplace/latest/userguide/user-guide-for-sellers.html)
- [Public Profile Creation](https://docs.aws.amazon.com/marketplace/latest/userguide/create-public-profile.html)
- [Seller Account Types](https://docs.aws.amazon.com/signin/latest/userguide/user-types-list.html)
- [Root vs IAM User Comparison](https://arshsharma.com/posts/2024-11-02-root-vs-iam-user/)

</details>


## **User Guide**

<details> <summary>🛡️ Root User vs IAM User: Key Differences</summary>

- **Root User**
    
    - Created when the AWS account is set up (uses the account email).
        
    - Has unrestricted access to all AWS resources and billing.
        
    - Only one root user per account.
        
    - Should only be used for critical tasks (e.g., closing account, changing billing info, enabling MFA).
        
    - Cannot be restricted by IAM policies.
        
- **IAM User**
    
    - Created by the root user or an IAM admin.
        
    - Can have custom permissions (least privilege principle).
        
    - Multiple IAM users can exist per account.
        
    - Used for daily operations and team access.
        
    - Permissions can be changed or revoked at any time.
        
- **Best Practice**: Use the root user only for tasks that require it, and use IAM users for everything else. Always enable MFA for the root user and admin IAM users.
    

</details> <details> <summary>📝 Tasks Only the Root User Can Perform</summary>

- Change account settings and contact information.
    
- Close the AWS account.
    
- Change or cancel AWS support plans.
    
- Restore IAM user access to the billing console.
    
- Enable or disable MFA on the root account.
    
- Manage some advanced security and payment settings.
    

</details> <details> <summary>🔑 Security Essentials for Beginners</summary>

- Enable Multi-Factor Authentication (MFA) for all users, especially root.
    
- Never share root credentials.
    
- Regularly review IAM users and permissions.
    
- Use strong, unique passwords for all AWS accounts.
    
- Set up billing alerts to avoid unexpected charges.
    
- Rotate access keys and passwords regularly.
    

</details> <details> <summary>📦 Product Listing Types on AWS Marketplace</summary>

- **AMI (Amazon Machine Image)**: Pre-configured virtual machine images.
    
- **SaaS (Software as a Service)**: Cloud-based software products.
    
- **Container Products**: Docker images for ECS/EKS.
    
- **Data Products**: Datasets for analytics and ML.
    
- **Professional Services**: Consulting, support, and implementation services.
    
- Each type has specific listing and integration requirements.
    

</details> <details> <summary>📊 Monitoring & Billing Basics</summary>

- Use AWS Cost Explorer and billing dashboard to track usage.
    
- Set up budget alerts and cost anomaly detection.
    
- Download detailed usage and billing reports.
    
- Understand how credits are applied and when charges begin.
    

</details> <details> <summary>📚 Learning & Support Resources</summary>

- [AWS Marketplace Seller Guide](https://docs.aws.amazon.com/marketplace/latest/userguide/user-guide-for-sellers.html)
    
- [AWS Free Tier Details](https://aws.amazon.com/free)
    
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
    
- [AWS Support Center](https://aws.amazon.com/support)
    
- [AWS Training and Certification](https://aws.amazon.com/training)
    

</details>
