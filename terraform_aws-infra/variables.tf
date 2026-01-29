variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "The name of the key pair you created in AWS"
  default     = "trip-planner-key"
}