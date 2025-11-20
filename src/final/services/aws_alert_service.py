import boto3
from botocore.exceptions import ClientError, BotoCoreError

from src.final.config.settings import AWS_SNS_TOPIC_ARN, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

sns_client = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def send_alert(message: str, subject: str):
    if not AWS_SNS_TOPIC_ARN:
        return {"ok": False, "error": "AWS_SNS_TOPIC_ARN não configurado."}

    try:
        response = sns_client.publish(
            TopicArn=AWS_SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        return {"ok": True, "message_id": response.get("MessageId")}
    except (ClientError, BotoCoreError) as e:
        return {"ok": False, "error": str(e)}
