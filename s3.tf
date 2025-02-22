resource "aws_s3_bucket" "artifact_bucket" {
  bucket = "${var.system_identifier}-artifact-bucket"
}