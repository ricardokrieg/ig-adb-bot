output "private_ip" {
  value = aws_instance.genymotion.*.private_ip
}

output "id" {
  value = aws_instance.genymotion.*.id
}