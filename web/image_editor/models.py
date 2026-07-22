import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageFilter
from django.core.files.base import ContentFile
import io
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', verbose_name="Пользователь")
    original_image = models.ImageField(upload_to='editor/originals/', verbose_name="Исходное изображение")
    processed_image = models.ImageField(upload_to='editor/processed/', blank=True, null=True, verbose_name="Обработанное изображение")
    filter_used = models.CharField(max_length=50, blank=True, verbose_name="Применённый фильтр")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return f"Изображение {self.id} пользователя {self.user.username}"

    def apply_filter(self, filter_name):
        """
        Применяет указанный фильтр к оригинальному изображению,
        сохраняет результат в processed_image и возвращает URL или None при ошибке.
        """
        # Проверка существования оригинального файла
        if not self.original_image or not os.path.exists(self.original_image.path):
            return None
        try:
            # Открываем оригинал
            img = Image.open(self.original_image.path)
            # Применяем фильтр
            if filter_name == 'grayscale':
                img = img.convert('L')
            elif filter_name == 'sepia':
                img = img.convert('L').convert('RGB')
                width, height = img.size
                pixels = img.load()
                for x in range(width):
                    for y in range(height):
                        r, g, b = pixels[x, y]
                        tr = int(r * 0.393 + g * 0.769 + b * 0.189)
                        tg = int(r * 0.349 + g * 0.686 + b * 0.168)
                        tb = int(r * 0.272 + g * 0.534 + b * 0.131)
                        pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
            elif filter_name == 'blur':
                img = img.filter(ImageFilter.BLUR)
            elif filter_name == 'contour':
                img = img.filter(ImageFilter.CONTOUR)
            elif filter_name == 'square_crop':
                width, height = img.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                img = img.crop((left, top, left + size, top + size))
            elif filter_name == 'rotate_90':
                img = img.rotate(90, expand=True)
            elif filter_name == 'rotate_180':
                img = img.rotate(180, expand=True)
            elif filter_name == 'rotate_270':
                img = img.rotate(270, expand=True)
            else:
                return None  # неизвестный фильтр
            # Подготавливаем имя файла
            name, ext = os.path.splitext(os.path.basename(self.original_image.name))
            new_filename = f"{name}_{filter_name}{ext}"
            # Сохраняем в байтовый поток
            img_io = io.BytesIO()
            img_format = ext[1:].upper() if ext else 'JPEG'
            if img_format == 'JPG':
                img_format = 'JPEG'
            img.save(img_io, format=img_format)
            # Сохраняем в поле processed_image
            self.processed_image.save(new_filename, ContentFile(img_io.getvalue()), save=False)
            self.filter_used = filter_name
            self.save()
            return self.processed_image.url
        except Exception as e:
            print(f"Ошибка при применении фильтра: {e}")
            return None