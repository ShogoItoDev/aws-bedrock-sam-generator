# はじめに

- 本レポジトリは作成者が個人的に考案・作成したものであり、所属組織等を代表するものではありません。
- 本レポジトリは検証目的であり、利用による損害等の発生には対応致しかねます。

# 本レポジトリの目的

本レポジトリでは、AWSのサーバーレスアプリケーション開発を効率化するため、自然言語による指示からAWS SAM (Serverless Application Model) YAMLファイルを自動生成するCI/CDパイプラインの構築を目的とします。

具体的には、開発者が実現したいサーバーレスアプリケーションの概要を自然言語（日本語）で記述したテキストファイルを配置するだけで、AWS CodePipelineが自動的にAWS SAM YAMLファイルを生成し、指定のS3バケットにアップロードする仕組みを提供します。

これにより、以下のようなメリットが期待できます。

- AWS SAM YAMLファイルの記述にかかる時間と労力の削減
- サーバーレスアプリケーションの初期開発の迅速化
- 自然言語による記述を介した、非エンジニアとの連携の容易化 (将来的な展望)

# 利用技術と構成

本レポジトリでは、以下のAWSサービスおよび技術を利用しています。

- **AWS CodeCommit**: ソースコードリポジトリとして利用します。
- **AWS CodeBuild**: ビルドプロジェクトを実行し、Pythonスクリプト(`SamGenerator.py`)を介してAmazon Bedrock Claude 3 Sonnetモデルを呼び出します。
- **AWS CodePipeline**: CI/CDパイプラインを構築し、CodeCommitへのプッシュをトリガーとして、CodeBuildプロジェクトを実行します。
- **Amazon Bedrock (Claude 3 Sonnet)**: 自然言語処理(NLP)モデルとして利用し、自然言語の記述からAWS SAM YAMLファイルを生成します。
- **Amazon S3**: 生成されたAWS SAM YAMLファイルの出力先として利用します。
- **Terraform**: AWSリソースのプロビジョニングと管理をコード化(IaC)するために利用します。

## 処理フロー

![diagram](https://github.com/user-attachments/assets/44e0a7ea-ed4d-4169-adad-9e9b77db8037)


1. **ユーザー: 自然言語テキストを配置**
   - ユーザーは、`parameters` フォルダ内に、実現したいサーバーレスアプリケーションの概要を自然言語で記述したテキストファイルを配置します。

2. **CodeCommitへのプッシュ**
   - `parameters` フォルダへの変更を含むソースコードがCodeCommitリポジトリにプッシュされます。

3. **CodePipelineのトリガー**
   - CodeCommitリポジトリへのプッシュをトリガーとして、CodePipelineが自動的に起動します。

4. **CodeBuildプロジェクトの実行**
   - CodePipelineは、定義されたCodeBuildプロジェクトを実行します。

5. **SamGenerator.pyの実行**
   - CodeBuildプロジェクトは、`SamGenerator.py` スクリプトを実行します。このスクリプトは、以下の処理を行います。
     - `parameters` フォルダ内のテキストファイルを読み込みます。
     - Amazon BedrockのClaude 3 Sonnetモデルを呼び出し、テキストファイルの内容を基にAWS SAM YAMLファイルを生成するよう指示します。
     - 生成されたAWS SAM YAMLファイルを指定のS3バケットにアップロードします。

6. **S3へのアップロード**
   - 生成されたAWS SAM YAMLファイルは、指定されたS3バケットにアップロードされ、後続のデプロイプロセスで利用できるようになります。


### 自然言語テキストの配置
ユーザーは、`parameters` フォルダ内に、実現したいサーバーレスアプリケーションの概要を自然言語で記述したテキストファイルを配置します。

### CodeCommitへのプッシュ
`parameters` フォルダへの変更を含むソースコードがCodeCommitリポジトリにプッシュされます。

### CodePipelineのトリガー
CodeCommitリポジトリへのプッシュをトリガーとして、CodePipelineが自動的に起動します。

### CodeBuildプロジェクトの実行
CodePipelineは、定義されたCodeBuildプロジェクトを実行します。

### SamGenerator.pyの実行
CodeBuildプロジェクトは、`SamGenerator.py` スクリプトを実行します。このスクリプトは、以下の処理を行います。

- `parameters` フォルダ内のテキストファイルを読み込みます。
- Amazon BedrockのClaude 3 Sonnetモデルを呼び出し、テキストファイルの内容を基にAWS SAM YAMLファイルを生成するよう指示します。
- 生成されたAWS SAM YAMLファイルを指定のS3バケットにアップロードします。

### S3へのアップロード
生成されたAWS SAM YAMLファイルは、指定されたS3バケットにアップロードされ、後続のデプロイプロセスで利用できるようになります。

# 利用方法

## リポジトリのクローン

本レポジトリをローカル環境にクローンします。

```bash
git clone <本レポジトリのURL>
cd <クローンしたディレクトリ>
```


## Terraformの初期化

Terraformを利用してAWSリソースをプロビジョニングするために、初期化を行います。
```bash
terraform init
```


## Terraformの適用

`main.tf` ファイル内の `system_identifier` （S3バケット名の一意性を確保するためのプレフィックス）を適切な値に変更し、Terraformを適用してAWSリソースを作成します。
```bash
terraform apply
```

> **Note**: `system_identifier` は、S3バケット名がAWS全体で一意になるように設定してください。

## 自然言語テキストの配置

`parameters` フォルダ内に、実現したいサーバーレスアプリケーションの概要を自然言語で記述したテキストファイルを作成・配置します。

## CodeCommitへのプッシュ

変更をCodeCommitリポジトリにプッシュします。

```bash
git add . git commit -m "Add natural language description" 
git push origin main
```


## SAM YAMLの確認

CodePipelineの実行が完了すると、指定したS3バケットにAWS SAM YAMLファイルが生成・アップロードされます。


