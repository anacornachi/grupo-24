import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

class AWSSNSService:
    """
    Serviço para enviar alertas via AWS SNS (Simple Notification Service).
    """
    
    def __init__(self):
        """
        Inicializa o cliente SNS com credenciais do .env
        """
        self.enabled = False
        self.client = None
        self.topic_arn = None
        
        try:
            # Ler configurações do ambiente
            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_region = os.getenv("AWS_REGION", "us-east-1")
            # Aceitar tanto AWS_SNS_TOPIC_ARN quanto SNS_TOPIC_ARN
            self.topic_arn = os.getenv("AWS_SNS_TOPIC_ARN") or os.getenv("SNS_TOPIC_ARN")
            
            # Validar se as credenciais estão configuradas
            if not aws_access_key or not aws_secret_key or not self.topic_arn:
                print("⚠️ AWS SNS não configurado. Alertas desabilitados.")
                print("   Configure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY e SNS_TOPIC_ARN no .env")
                return
            
            # Criar cliente SNS
            self.client = boto3.client(
                'sns',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            
            self.enabled = True
            print(f"✅ AWS SNS configurado. Região: {aws_region}")
            
        except Exception as e:
            print(f"❌ Erro ao configurar AWS SNS: {e}")
            self.enabled = False
    
    def send_alert(self, subject: str, message: str) -> bool:
        """
        Envia um alerta via SNS.
        
        Args:
            subject: Assunto do alerta (até 100 caracteres)
            message: Corpo da mensagem
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        if not self.enabled:
            print(f"⚠️ SNS desabilitado. Alerta não enviado: {subject}")
            return False
        
        try:
            # Truncar subject se necessário (limite SNS)
            subject = subject[:100]
            
            response = self.client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message
            )
            
            print(f"✅ Alerta SNS enviado: {subject}")
            print(f"   MessageID: {response.get('MessageId', 'N/A')}")
            return True
            
        except NoCredentialsError:
            print("❌ Credenciais AWS inválidas ou não encontradas")
            return False
        except ClientError as e:
            print(f"❌ Erro do cliente AWS SNS: {e}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado ao enviar alerta SNS: {e}")
            return False
    
    def send_pest_alert(self, detected_animals: list) -> bool:
        """
        Envia alerta específico para detecção de pragas.
        
        Args:
            detected_animals: Lista de dicionários com 'class' e 'confidence'
        """
        if not detected_animals:
            return False
        
        subject = "🚨 ALERTA: Pragas Detectadas!"
        
        animal_list = "\n".join([
            f"  • {animal['class'].upper()} (confiança: {animal['confidence']:.1%})"
            for animal in detected_animals
        ])
        
        message = f"""
ALERTA FARMTECH SOLUTIONS - VISÃO COMPUTACIONAL

Foram detectados ANIMAIS na área de cultivo:

{animal_list}

Ação recomendada: Verificar o local imediatamente para evitar danos à safra.

---
Sistema de Monitoramento FarmTech
        """.strip()
        
        return self.send_alert(subject, message)
    
    def send_sensor_alert(self, alert_type: str, sensor_data: dict) -> bool:
        """
        Envia alerta específico para problemas nos sensores.
        
        Args:
            alert_type: Tipo do alerta (ex: 'pH Crítico', 'Seca Severa')
            sensor_data: Dados do sensor que causaram o alerta
        """
        subject = f"🚨 ALERTA: {alert_type}"
        
        # Mapear mensagens específicas
        messages = {
            "pH Crítico": f"""
Solo com pH CRÍTICO detectado!

Valor atual: {sensor_data.get('soil_ph', 'N/A')}
Faixa ideal: 5.5 - 7.0

Ação: Ajuste imediato do pH com corretivos (calcário para acidez, enxofre para alcalinidade).
            """,
            "Seca Severa": f"""
SECA SEVERA detectada!

Umidade do solo: {sensor_data.get('soil_moisture', 'N/A')}%
Nível crítico: Abaixo de 20%

Ação: Ativar irrigação URGENTE para evitar perda da safra.
            """,
            "Encharcamento": f"""
Solo ENCHARCADO detectado!

Umidade do solo: {sensor_data.get('soil_moisture', 'N/A')}%
Nível crítico: Acima de 80%

Ação: Verificar drenagem. Risco de fungos e apodrecimento.
            """,
            "Deficiência Nutricional": f"""
DEFICIÊNCIA NUTRICIONAL crítica!

Fósforo (P): {'Ausente' if not sensor_data.get('phosphorus_present') else 'Presente'}
Potássio (K): {'Ausente' if not sensor_data.get('potassium_present') else 'Presente'}

Ação: Aplicar fertilizantes ricos em P e K imediatamente.
            """,
            "Falha na Irrigação": f"""
FALHA no Sistema de Irrigação!

Umidade do solo: {sensor_data.get('soil_moisture', 'N/A')}%
Status irrigação: {sensor_data.get('irrigation_status', 'N/A')}

Ação: Verificar sistema de irrigação. Solo crítico mas irrigação desligada.
            """
        }
        
        message = f"""
ALERTA FARMTECH SOLUTIONS - MONITORAMENTO IoT

{messages.get(alert_type, f"Alerta: {alert_type}")}

Timestamp: {sensor_data.get('timestamp', 'N/A')}

---
Sistema de Monitoramento FarmTech
        """.strip()
        
        return self.send_alert(subject, message)


# Instância global (singleton)
_sns_service = None

def get_sns_service() -> AWSSNSService:
    """
    Retorna a instância singleton do serviço SNS.
    """
    global _sns_service
    if _sns_service is None:
        _sns_service = AWSSNSService()
    return _sns_service
