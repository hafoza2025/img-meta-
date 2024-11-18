from flask import Flask, request, send_file, render_template
import requests
from io import BytesIO
from mimetypes import guess_type

app = Flask(__name__)

@app.route('/')
def index():
    # عرض صفحة HTML عند زيارة الموقع
    return render_template('index.html')

@app.route('/download')
def download_image():
    # الحصول على رابط الصورة من معلمات الطلب
    url = request.args.get('url')
    
    if not url:
        return "لم يتم توفير رابط الصورة.", 400

    # إعداد رأس "User-Agent" لمحاكاة متصفح فعلي
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # إرسال الطلب إلى الرابط مع السماح بإعادة التوجيه
        response = requests.get(url, stream=True, headers=headers, allow_redirects=True)
        
        # التحقق من نجاح الطلب
        response.raise_for_status()
        
        # تحديد نوع المحتوى من رأس الاستجابة
        content_type = response.headers.get('Content-Type')
        
        # إذا كان نوع المحتوى يحتوي على صورة (image)، نكمل العمل
        if content_type.startswith('image'):
            # تحديد امتداد الصورة بناءً على نوع المحتوى (مثل jpg أو png)
            extension = guess_type(url)[1] or 'jpg'  # في حالة عدم التعرف على الامتداد نستخدم "jpg" كافتراضي
            
            # تخزين الصورة مؤقتًا في الذاكرة
            img_data = BytesIO(response.content)
            
            # إرسال الصورة للمتصفح كملف لتحميله
            return send_file(img_data, mimetype=content_type, as_attachment=True, download_name=f"downloaded_image.{extension}")
        else:
            return "الرابط لا يحتوي على صورة.", 400
        
    except requests.exceptions.RequestException as e:
        return f"خطأ في تنزيل الصورة: {e}", 400

if __name__ == "__main__":
    app.run(debug=True)
