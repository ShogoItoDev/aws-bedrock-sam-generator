resource "aws_iam_role" "codebuild_role" {
  name = "${var.system_identifier}-codebuild-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "codebuild_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"
  role       = aws_iam_role.codebuild_role.name
}

resource "aws_codebuild_project" "default" {
  name         = "${var.system_identifier}-project"
  description  = "CodeBuild project for ${var.system_identifier} system"
  service_role = aws_iam_role.codebuild_role.arn

  source {
    type            = "CODECOMMIT"
    location        = aws_codecommit_repository.default.clone_url_http
    git_clone_depth = 1
    buildspec       = "buildspec.yaml"
  }

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
  }
}