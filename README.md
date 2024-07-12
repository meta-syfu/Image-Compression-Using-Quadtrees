# Image-Compression-Using-Quadtrees

## سینا بهرامی `9900442201`

# عملکرد برنامه فشرده‌سازی تصویر با استفاده از Quadtrees

فشرده‌سازی تصویر با استفاده از درخت‌های چهارتایی (Quadtrees) یک تکنیک مؤثر برای کاهش حجم داده‌های تصویری است. این روش به خصوص برای تصاویری که دارای نواحی بزرگ و همگن از رنگ یا شدت روشنایی مشابه هستند، کاربرد دارد. در زیر، نحوه عملکرد این نوع فشرده‌سازی توضیح داده شده است:

### مفهوم درخت‌های چهارتایی

درخت‌های چهارتایی ساختارهای داده‌ای هستند که هر گره در آن به چهار زیرگره تقسیم می‌شود. این تقسیم‌بندی به صورت بازگشتی انجام می‌شود تا جایی که هر بخش از تصویر یکپارچه و همگن شود.

### مراحل فشرده‌سازی تصویر با درخت‌های چهارتایی

1. **تقسیم تصویر به چهار بخش**: در ابتدا، کل تصویر به چهار قسمت مساوی تقسیم می‌شود. هر قسمت به صورت یک مربع کوچک‌تر از تصویر اصلی است.

2. **تحلیل هر بخش**: هر یک از این چهار بخش بررسی می‌شود تا مشخص شود که آیا همه پیکسل‌های آن مشابه هستند یا نه. اگر پیکسل‌های آن بخش همگن باشند (یعنی تفاوت کمی در رنگ یا شدت روشنایی داشته باشند)، آن بخش به عنوان یک برگ در درخت چهارتایی ذخیره می‌شود.

3. **تقسیم بازگشتی بخش‌های ناهمگن**: اگر یک بخش ناهمگن باشد (یعنی تنوع زیادی در رنگ یا شدت روشنایی داشته باشد)، آن بخش دوباره به چهار قسمت مساوی تقسیم می‌شود و این فرآیند به صورت بازگشتی ادامه می‌یابد تا زمانی که همه بخش‌ها همگن شوند یا به حداقل اندازه ممکن برسند.

4. **ذخیره‌سازی اطلاعات درخت چهارتایی**: ساختار درخت چهارتایی به همراه مقادیر پیکسل‌های برگ‌ها (بخش‌های همگن) ذخیره می‌شود. این ساختار به دلیل تعداد کمتر گره‌ها نسبت به پیکسل‌های اصلی تصویر، باعث کاهش حجم داده‌ها می‌شود.

### مزایا و معایب فشرده‌سازی با درخت‌های چهارتایی

#### مزایا:
- **کارایی بالا در تصاویری با نواحی بزرگ همگن**: این روش به خوبی برای تصاویری که دارای نواحی وسیع با رنگ‌های مشابه هستند، کار می‌کند.
- **کاهش قابل توجه حجم داده‌ها**: به دلیل ذخیره‌سازی فشرده بخش‌های همگن، حجم داده‌ها کاهش می‌یابد.

#### معایب:
- **پیچیدگی محاسباتی**: فرآیند تقسیم‌بندی و تحلیل بازگشتی ممکن است به لحاظ محاسباتی پیچیده و زمان‌بر باشد.
- **کارایی پایین در تصاویری با جزئیات بالا**: در تصاویری که دارای جزئیات زیاد و نواحی همگن کم هستند، این روش ممکن است به خوبی عمل نکند و حجم داده‌ها به طور قابل توجهی کاهش نیابد.

در مجموع، فشرده‌سازی تصویر با استفاده از درخت‌های چهارتایی یک روش مؤثر برای کاهش حجم تصاویر با نواحی همگن بزرگ است، اما ممکن است برای تمامی انواع تصاویر مناسب نباشد.


این برنامه به منظور فشرده‌سازی تصاویر با استفاده از تکنیک Quadtrees طراحی شده است. در ادامه، هر بخش از کد به تفصیل توضیح داده شده است.

## وارد کردن کتابخانه‌ها

در این بخش، کتابخانه‌های مورد نیاز برای اجرای برنامه وارد می‌شوند.

```python
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
```

- `tkinter` برای ایجاد رابط کاربری گرافیکی استفاده می‌شود.
- `filedialog` برای باز کردن دیالوگ‌های انتخاب و ذخیره فایل استفاده می‌شود.
- `PIL` (Python Imaging Library) برای پردازش تصاویر استفاده می‌شود.
- `numpy` برای عملیات عددی روی آرایه‌ها استفاده می‌شود.

## کلاس `Node`

این کلاس نماینده یک گره در Quadtree است.

```python
class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_leaf = True
        self.color = None
        self.children = []
```

- `x` و `y` مختصات بالا-چپ گره را مشخص می‌کنند.
- `width` و `height` عرض و ارتفاع ناحیه را تعیین می‌کنند.
- `is_leaf` نشان می‌دهد که آیا این گره یک برگ است یا نه.
- `color` رنگ ناحیه را ذخیره می‌کند.
- `children` لیستی از فرزندان گره را نگه می‌دارد.

## فشرده‌سازی تصویر با استفاده از Quadtree

این تابع تصویر را فشرده می‌کند.

```python
def compress(image, node, threshold):
    region = image[node.y:node.y+node.height, node.x:node.x+node.width]
    mean_color = np.mean(region, axis=(0, 1))
    diff = np.max(np.abs(region - mean_color))
    
    if diff < threshold or node.width <= 1 or node.height <= 1:
        node.color = mean_color
        return [node]
    
    node.is_leaf = False
    half_width = node.width // 2
    half_height = node.height // 2
    
    nodes = [
        Node(node.x, node.y, half_width, half_height),
        Node(node.x + half_width, node.y, half_width, half_height),
        Node(node.x, node.y + half_height, half_width, half_height),
        Node(node.x + half_width, node.y + half_height, half_width, half_height),
    ]
    
    compressed_nodes = []
    for n in nodes:
        compressed_nodes.extend(compress(image, n, threshold))
    
    node.children = nodes
    return compressed_nodes
```

- `region` ناحیه‌ای از تصویر را که گره نمایندگی می‌کند، می‌گیرد.
- `mean_color` میانگین رنگ ناحیه را محاسبه می‌کند.
- `diff` بیشترین اختلاف رنگ بین پیکسل‌ها و میانگین رنگ را محاسبه می‌کند.
- اگر `diff` کمتر از `threshold` باشد، یا اندازه ناحیه به 1 پیکسل رسیده باشد، گره به عنوان برگ تنظیم می‌شود و رنگ میانگین به آن اختصاص داده می‌شود.
- در غیر این صورت، ناحیه به چهار قسمت تقسیم می‌شود و برای هر قسمت یک گره جدید ایجاد می‌شود.
- سپس برای هر گره فرزند تابع `compress` دوباره فراخوانی می‌شود.

## بازسازی تصویر از Quadtree

این تابع تصویر فشرده شده را بازسازی می‌کند.

```python
def reconstruct(image, node):
    if node.is_leaf:
        image[node.y:node.y+node.height, node.x:node.x+node.width] = node.color
        return
    
    for child in node.children:
        reconstruct(image, child)
```

- اگر گره یک برگ باشد، رنگ ناحیه را با رنگ گره پر می‌کند.
- در غیر این صورت، برای هر گره فرزند تابع `reconstruct` دوباره فراخوانی می‌شود.

## رابط کاربری گرافیکی (GUI)

این بخش رابط کاربری گرافیکی برنامه را ایجاد می‌کند.

```python
class QuadtreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compression Using Quadtrees")
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.canvas = tk.Canvas(self.frame, width=600, height=400)
        self.canvas.pack()
        
        self.select_button = tk.Button(self.frame, text="Select Image", command=self.select_image)
        self.select_button.pack()
        
        self.threshold_label = tk.Label(self.frame, text="Compression Threshold")
        self.threshold_label.pack()
        
        self.threshold = tk.IntVar(value=20)
        self.threshold_slider = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.threshold)
        self.threshold_slider.pack()
        
        self.compress_button = tk.Button(self.frame, text="Compress Image", command=self.compress_image)
        self.compress_button.pack()
        
        self.save_button = tk.Button(self.frame, text="Save Image", command=self.save_image)
        self.save_button.pack()
        
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.pack()
        
        self.image = None
        self.compressed_image = None
        self.nodes = []
    
    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert('RGB')
            self.display_image(self.image)
    
    def display_image(self, img):
        img.thumbnail((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(300, 200, image=self.img_tk)
    
    def compress_image(self):
        if self.image:
            img_array = np.array(self.image)
            root_node = Node(0, 0, img_array.shape[1], img_array.shape[0])
            self.nodes = compress(img_array, root_node, self.threshold.get())
            self.compressed_image = np.zeros_like(img_array)
            reconstruct(self.compressed_image, root_node)
            self.display_image(Image.fromarray(np.uint8(self.compressed_image)))
    
    def reset(self):
        self.canvas.delete("all")
        self.image = None
        self.compressed_image = None
        self.nodes = []
    
    def save_image(self):
        if self.compressed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                Image.fromarray(np.uint8(self.compressed_image)).save(file_path)
```

- در اینجا رابط کاربری گرافیکی شامل بوم (canvas) برای نمایش تصویر، دکمه‌هایی برای انتخاب تصویر، فشرده‌سازی تصویر، ذخیره تصویر و تنظیمات آستانه فشرده‌سازی است.
- `select_image` تصویر را از کاربر می‌گیرد.
- `display_image` تصویر را در بوم نمایش می‌دهد.
- `compress_image` تصویر را فشرده کرده و نمایش می‌دهد.
- `reset` تنظیمات برنامه را به حالت اولیه برمی‌گرداند.
- `save_image` تصویر فشرده شده را ذخیره می‌کند.

## اجرای برنامه

این بخش برنامه را اجرا می‌کند.

```python
root = tk.Tk()
app = QuadtreeApp(root)
root.mainloop()
```

- یک پنجره اصلی ایجاد می‌شود و برنامه اجرا می‌شود.

## پیش‌نیازها

- Python 3.x
- کتابخانه‌های `tkinter`, `PIL`, و `numpy`

## نصب پیش‌نیازها

```bash
pip install pillow numpy tk
```

## اجرا

```bash
python main.py
```
