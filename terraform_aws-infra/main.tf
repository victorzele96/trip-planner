data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

provider "aws" {
  region = var.region
}

# יצירת קבוצת אבטחה (Firewall)
resource "aws_security_group" "trip_planner_sg" {
  name        = "trip-planner-sg"
  description = "Allow SSH, HTTP and Streamlit"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # זה יאפשר ל-test-netconnection לעבור
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# יצירת השרת
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.trip_planner_sg.id]

  # פקודות התקנה שירוצו ברגע שהשרת נדלק
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo usermod -aG docker ubuntu
              EOF

  tags = {
    Name = "TripPlanner-Server"
  }
}

# הצגת ה-IP של השרת בסיום
output "server_public_ip" {
  value = aws_instance.app_server.public_ip
}