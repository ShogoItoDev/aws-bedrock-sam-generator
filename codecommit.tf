resource "aws_codecommit_repository" "default" {
  repository_name = "${var.system_identifier}-repo"
  description     = "CodeCommit repository for ${var.system_identifier} system"
}