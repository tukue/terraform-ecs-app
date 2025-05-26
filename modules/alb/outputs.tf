output "alb_hostname" {
  description = "Hostname of the ALB"
  value       = aws_lb.main.dns_name
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = aws_lb_target_group.app.id
}

output "lb_listener_arn" {
  description = "ARN of the load balancer listener"
  value       = aws_lb_listener.front_end.arn
}