variable "route53_zone_id" {
  description = "Route53 zone ID for the domain"
  type        = string
}

variable "domain_name" {
  description = "Primary domain name"
  type        = string
}

variable "domain_aliases" {
  description = "List of domain aliases for CloudFront"
  type        = list(string)
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
}

variable "certificate_arn" {
  description = "ARN of the ACM certificate for CloudFront distribution"
  type        = string
} 