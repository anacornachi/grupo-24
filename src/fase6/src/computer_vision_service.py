"""
Serviço de Visão Computacional para detecção de objetos usando YOLO.
"""
import io
import numpy as np
from PIL import Image


class ComputerVisionService:
    """
    Serviço para análise de imagens usando YOLOv8 (Ultralytics).
    """
    
    def __init__(self, model_path=None):
        """
        Inicializa o serviço com o modelo YOLO.
        
        Args:
            model_path: Caminho para o modelo YOLO customizado (opcional)
        """
        self.model = None
        self.model_path = model_path or 'yolov8l.pt'  # Modelo padrão
        
    def _load_model(self):
        """Carrega o modelo YOLO (lazy loading)"""
        if self.model is None:
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.model_path)
                print(f"✅ Modelo YOLO carregado: {self.model_path}")
            except Exception as e:
                print(f"❌ Erro ao carregar modelo YOLO: {e}")
                raise
    
    def analyze_image(self, image_bytes):
        """
        Analisa uma imagem e retorna objetos detectados.
        
        Args:
            image_bytes: Bytes da imagem (de um file upload, por exemplo)
            
        Returns:
            tuple: (imagem_anotada_array, lista_de_deteccoes)
        """
        try:
            # Importações tardias para evitar erro se libs não estiverem instaladas
            import cv2
            from ultralytics import YOLO
            
            # Carregar modelo se necessário
            self._load_model()
            
            # Converter bytes para imagem PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # Converter PIL para numpy array (formato que o YOLO aceita)
            image_np = np.array(image)
            
            # Executar detecção COM THRESHOLD de confiança
            # conf=0.7 significa "só aceitar detecções com 70%+ de confiança"
            # Isso reduz falsos positivos (ex: rato detectado como cachorro)
            results = self.model(image_np, conf=0.7)
            
            # Obter imagem anotada
            annotated_frame = results[0].plot()
            
            # Extrair detecções
            detections = []
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = results[0].names[class_id]
                
                detections.append({
                    'class': class_name,
                    'confidence': confidence,
                    'class_id': class_id
                })
            
            # Retornar sucesso (True como flag) + imagem + detecções
            return True, annotated_frame, detections
            
        except ImportError as e:
            print(f"❌ Biblioteca não encontrada: {e}")
            print("   Instale com: pip install opencv-python ultralytics")
            return False, None, []
        except Exception as e:
            print(f"❌ Erro ao analisar imagem: {e}")
            return False, None, []
