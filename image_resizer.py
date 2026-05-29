# image_resizer.py
from PIL import Image
import os
from typing import Optional, Tuple

class ImageResizer:
    """图像分辨率编辑核心类"""
    
    SUPPORTED_READ_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    SUPPORTED_WRITE_FORMATS = {
        'PNG': '.png',
        'JPEG': '.jpg',
        'BMP': '.bmp',
        'GIF': '.gif'
    }
    
    def __init__(self):
        self._image: Optional[Image.Image] = None
        self._file_path: Optional[str] = None
    
    def load_image(self, file_path: str) -> bool:
        """加载图片，成功返回 True，失败返回 False"""
        try:
            img = Image.open(file_path)
            # 转换为 RGB 模式，避免保存 JPEG 时出现模式错误
            if img.mode not in ('RGB', 'RGBA', 'L'):
                img = img.convert('RGB')
            self._image = img
            self._file_path = file_path
            return True
        except Exception as e:
            print(f"加载图片失败: {e}")
            return False
    
    def resize_image(self, width: int, height: int) -> bool:
        """缩放图片到指定分辨率，成功返回 True"""
        if self._image is None:
            return False
        try:
            self._image = self._image.resize((width, height), Image.Resampling.LANCZOS)
            return True
        except Exception as e:
            print(f"缩放图片失败: {e}")
            return False
    
    def save_image(self, save_path: str, format_hint: str = None) -> bool:
        """保存图片，自动根据扩展名或 format_hint 确定格式"""
        if self._image is None:
            return False
        try:
            # 确定保存格式
            ext = os.path.splitext(save_path)[1].lower()
            if format_hint and format_hint in self.SUPPORTED_WRITE_FORMATS:
                fmt = format_hint
            elif ext in self.SUPPORTED_WRITE_FORMATS.values():
                # 根据扩展名查找对应的格式键
                for fmt, suffix in self.SUPPORTED_WRITE_FORMATS.items():
                    if suffix == ext:
                        fmt = fmt
                        break
                else:
                    fmt = 'PNG'  # 默认 PNG
            else:
                fmt = 'PNG'
            
            # 处理 JPEG 保存时的模式问题
            img_to_save = self._image
            if fmt == 'JPEG' and img_to_save.mode == 'RGBA':
                img_to_save = img_to_save.convert('RGB')
            
            img_to_save.save(save_path, format=fmt)
            return True
        except Exception as e:
            print(f"保存图片失败: {e}")
            return False
    
    @property
    def is_image_loaded(self) -> bool:
        return self._image is not None
    
    def get_original_size(self) -> Tuple[int, int]:
        """获取原始图片尺寸 (宽, 高)"""
        if self._image:
            return self._image.size
        return (0, 0)
