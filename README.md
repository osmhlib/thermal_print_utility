# thermal_print_utility
Utility for printing images on thermal receipt printer

1. Requirements:

- Installed original printer driver
- Python 3.10+

2. Getting VID and PID:

- Connect the printer to the computer
- Launch USBDeview
- Find the printer and copy VID and PID

3. Replace the driver:

- Download Zadig
- Find the printer
- Select libusbK and click Replace Driver (may not work – try other available drivers)

4. Using the program:

- Run lib_py_install.bat (once, it will install the required libraries)
- Run the xp_print.py script
- Enter VID and PID in the program interface (after the first use, the values will be saved in printer_config.json and will be loaded automatically)
- Select an image
- Adjust contrast and specify the number of copies if needed
- Print

Errors:

- Device not found – incorrect VID and PID
- no backend available – incorrect replaced driver

Note:

- The program was originally developed for use with the Xprinter C58H receipt printer with driver xp-58c; functionality with other models has not been tested

------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Вимоги:

- Встановлений оригінальний драйвер принтера
- Python 3.10+

2. Отримання VID та PID:

- Підключити принтер до комп'ютера
- Запустити USBDeview
- Знайти принтер і скопіювати VID і PID

3. Замінити драйвер:

- Завантажити Zadig
- Знайти принтер
- Обрати libusbK і натиснути Replace Driver (може не запрацювати - спробувати інші доступні драйвери)

4. Використання програми:

- Запустити lib_py_install.bat (одноразово, встановить необхідні бібліотеки)
- Запустити скрипт xp_print.py
- Вказати VID і PID у інтерфейсі програми (після першого використання значення збережуться у `printer_config.json` і будуть підставлятися автоматично)
- Обрати зображення
- За потреби відрегулювати контраст та вказати кількість копій
- Надрукувати

5. Помилки:

- Device not found - неправильні VID і PID
- no backend avaible - не підходить замінений драйвер

Примітка:

- Першочергово програма розроблялася на суміщенні з принтером чеків Xprinter C58H з драйвером xp-58c, робота з іншим моделями не тестувалася
