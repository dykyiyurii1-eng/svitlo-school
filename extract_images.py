import base64
import re
import os

HTML_FILE = 'index.html'      
IMAGES_DIR = 'images'        


def main():
    # Перевіряємо, чи існує HTML-файл
    if not os.path.exists(HTML_FILE):
        print(f"❌ Помилка: файл '{HTML_FILE}' не знайдено!")
        print(f"   Переконайся, що скрипт лежить у тій самій папці, що й HTML.")
        return

    # Створюємо папку для фото
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"📁 Папка '{IMAGES_DIR}' готова")

    # Читаємо HTML
    print(f"📖 Читаю '{HTML_FILE}'...")
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    original_size = len(html.encode('utf-8'))
    print(f"   Початковий розмір: {original_size / 1024 / 1024:.2f} МБ")

    # Знаходимо всі base64-зображення в полі "photo:"
    # Формат: photo:'data:image/jpeg;base64,XXXXX' або photo:'data:image/png;base64,XXXXX'
    pattern = r"photo:'data:image/(jpeg|jpg|png|webp);base64,([^']+)'"
    matches = re.findall(pattern, html)

    if not matches:
        print("⚠️  Не знайдено жодного base64-зображення в полі 'photo:'")
        print("   Можливо, файл вже оптимізований або формат інший.")
        return

    print(f"🖼️  Знайдено зображень: {len(matches)}")

    # Обробляємо кожне зображення
    counter = 0
    for ext, data in matches:
        # Нормалізуємо розширення
        if ext == 'jpg':
            ext = 'jpeg'
        file_ext = 'jpg' if ext == 'jpeg' else ext

        counter += 1
        filename = f"teacher-{counter:02d}.{file_ext}"
        filepath = os.path.join(IMAGES_DIR, filename)

        # Декодуємо base64 і зберігаємо
        try:
            image_bytes = base64.b64decode(data)
            with open(filepath, 'wb') as img_file:
                img_file.write(image_bytes)

            size_kb = len(image_bytes) / 1024
            print(f"   ✅ {filename} ({size_kb:.1f} КБ)")

            # Замінюємо в HTML base64 на шлях до файлу
            old_value = f"data:image/{ext};base64,{data}"
            new_value = f"{IMAGES_DIR}/{filename}"
            html = html.replace(old_value, new_value)

        except Exception as e:
            print(f"   ❌ Помилка з {filename}: {e}")

    # Записуємо оновлений HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    new_size = len(html.encode('utf-8'))
    print()
    print("=" * 50)
    print(f"🎉 Готово! Витягнуто {counter} зображень у папку '{IMAGES_DIR}'")
    print(f"📉 Розмір HTML: {original_size / 1024 / 1024:.2f} МБ → {new_size / 1024:.1f} КБ")
    print(f"   Зменшено у {original_size / new_size:.1f} разів!")
    print("=" * 50)
    print()
    print("Наступні кроки:")
    print("  1. Відкрий index.html у браузері — перевір, що все працює")
    print("  2. git add . && git commit -m 'Optimize images' && git push")


if __name__ == '__main__':
    main()