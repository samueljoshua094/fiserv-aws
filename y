version = 0.1
[y]
[y.deploy]
[y.deploy.parameters]
stack_name = "fiserv-aws"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-ekqj8qah5uqa"
s3_prefix = "fiserv-aws"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
disable_rollback = true
image_repositories = []

[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "fiserv-aws"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-ekqj8qah5uqa"
s3_prefix = "fiserv-aws"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
disable_rollback = true
image_repositories = []
