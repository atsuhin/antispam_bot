import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import asyncio
from text_preprocessor import TextPreprocessor
import os

class ProfanityDetector:
    def __init__(self, model_path='model', device=None):
        """
        Инициализация детектора нецензурной лексики
        
        Args:
            model_path (str): Путь к сохраненной модели
            device (str): Устройство для вычислений ('cuda' или 'cpu')
        """
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
            
        try:
            # Загружаем базовую модель и токенизатор
            self.tokenizer = AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
            self.model = AutoModelForSequenceClassification.from_pretrained('DeepPavlov/rubert-base-cased', num_labels=2)
            
            # Загружаем веса обученной модели
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_file = os.path.join(script_dir, model_path, 'best_model.pt')
            state_dict = torch.load(model_file, map_location=self.device)
            self.model.load_state_dict(state_dict)
            
            self.model.to(self.device)
            self.model.eval()
        except Exception as e:
            raise e
        
        self.preprocessor = TextPreprocessor()
        # Создаем пул потоков для выполнения тяжелых операций
        self.loop = asyncio.get_event_loop()
        self.thread_pool = asyncio.get_event_loop().run_in_executor
    
    async def predict(self, text):
        """
        Асинхронно проверяет текст на наличие нецензурной лексики
        
        Args:
            text (str): Текст для проверки
            
        Returns:
            dict: Словарь с результатами:
                - has_profanity (bool): Есть ли нецензурная лексика
                - confidence (float): Уверенность модели (от 0 до 1)
        """
        try:
            # Предобработка текста
            cleaned_text = self.preprocessor.clean_text(text)
            
            # Токенизация
            inputs = self.tokenizer(
                cleaned_text,
                add_special_tokens=True,
                max_length=256,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            # Перенос на нужное устройство
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            def run_inference():
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    probabilities = torch.softmax(outputs.logits, dim=1)
                    prediction = torch.argmax(probabilities, dim=1)
                    confidence = probabilities[0][prediction].item()
                return prediction.item(), confidence
            
            # Запускаем тяжелые вычисления в отдельном потоке
            prediction, confidence = await self.thread_pool(None, run_inference)
            
            return {
                'has_profanity': bool(prediction),
                'confidence': confidence
            }
            
        except Exception as e:
            raise e

async def check_text(text, model_path='model'):
    """
    Асинхронная функция для быстрой проверки текста
    
    Args:
        text (str): Текст для проверки
        model_path (str): Путь к модели
        
    Returns:
        dict: Результаты проверки
    """
    detector = ProfanityDetector(model_path)
    return await detector.predict(text)

async def main():
    test_text = "Привет?"
    test_text1 = "Пизда"

    results = await asyncio.gather(
        check_text(test_text),
        check_text(test_text1)
    )
    
    print(f"Текст: {test_text}")
    print(f"Результат: {results[0]}")
    print(f"Текст: {test_text1}")
    print(f"Результат: {results[1]}")

if __name__ == "__main__":
    asyncio.run(main()) 