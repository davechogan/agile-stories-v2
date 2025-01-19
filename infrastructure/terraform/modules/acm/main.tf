# ACM Certificate (in us-east-1 for CloudFront)
resource "aws_acm_certificate" "cert" {
  provider = aws.us-east-1

  domain_name       = var.domain_name
  validation_method = "DNS"

  subject_alternative_names = ["*.${var.domain_name}"]

  lifecycle {
    create_before_destroy = true
  }
}

# DNS Validation records
resource "aws_route53_record" "cert_validation" {
  provider = aws.us-east-1

  allow_overwrite = true
  name            = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_name
  records         = [tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_value]
  type            = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_type
  zone_id         = var.route53_zone_id
  ttl             = 60
}

# Certificate validation
resource "aws_acm_certificate_validation" "cert" {
  provider = aws.us-east-1

  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [aws_route53_record.cert_validation.fqdn]
}

output "certificate_arn" {
  value = aws_acm_certificate.cert.arn
} 