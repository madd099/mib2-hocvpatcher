# MIB STD2 HMIOFFCLOCKVIEW (Hocv) PATCHER

**Скрывает баг «дата из будущего» под часами** на PQ-юнитах с HMI от ZR-прошивок (SEAT / SKODA / VW) · v1.2

## 🇷🇺 Описание

Как известно, один из багов, которые мы получаем после прошивки HMI от ZR в PQ юнит — неверная дата под часами в режиме ожидания.
Патч работает с файлами `Hocv*.jxe` из ZR-прошивки: в заданном коридоре адресов ищет сигнатуры и меняет один байт, после чего виджет даты становится невидимым. 

### Что делает патчер

- Ищет в файлах `Hocv*.jxe` сигнатуры SEAT Navi/Non Navi и SKODA-VW Navi/Non Navi в области `0x5B00–0x6000`
- В каждой найденной сигнатуре меняет байт `0x04` → `0x03`

### Как применить

Делаем дамп скинов через Toolbox или вытаскиваем из скачанной прошивки.
В папке со скином, который мы хотим поправить (советую выбрать какой-нибудь 4 или 5, чтобы в случае проблем, вернуться на свой прошлый через длинное кодирование), есть файл viewhandler.zip. Открываем и извлекаем файлы
- Hocv_08DA85708EEB9B2F_CA54.jxe
- Hocv_08DA85708EEB9B2F_DA1F.jxe
  
Выбираем их в программе, запускаем - готово. Дальше остается только закинуть исправленные файлы обратно в viewhandler.zip.
На наше счастье, контрольные суммы не сверяются.
Кладем всю папку со скином на SD карту с тулбоксом в custom\skins\replace и заменяем скин при помощи customization/skins/ -> Copy images.mcf and ambienceColorMap.res from /custom/skins

### Скачать

Готовые сборки — в [Releases](../../releases):
- `MST2HocvPatcher_v1.2-windows.exe` — Windows 10/11 x64
- `MST2HocvPatcher_v1.2-linux` — Linux x64
- Также данный патчер включен в состав [конвертера](https://github.com/madd099/mib2-metainfoconverter)

### Запуск из исходников

```bash
pip install PySide6
python MST2HocvPatcher.py
```

###  Полезные ссылки
- [Патч даты из будущего — статья на Drive2](https://www.drive2.ru/l/712453299302827334)

---

## 🇬🇧 English

**Hides the "date from the future" bug below the clock** on PQ units running HMI from ZR firmware (SEAT / SKODA / VW) · v1.2

### Description

As you may know, one of the bugs we get after flashing a ZR HMI onto a PQ unit is an incorrect date below the clock in standby mode.
The patcher works with `Hocv*.jxe` files from the ZR firmware: within a defined address window it searches for signatures and changes a single byte, after which the date widget becomes invisible.

### What the patcher does

- Searches `Hocv*.jxe` files for the SEAT Navi/Non Navi and SKODA-VW Navi/Non Navi signatures within the `0x5B00–0x6000` area
- In each found signature it changes the byte `0x04` → `0x03`

### How to apply

Dump the skins using Toolbox or extract them from the downloaded firmware.
In the folder of the skin you want to fix (I recommend picking skin 4 or 5, so that in case of problems you can switch back to your previous one via long coding), there is a viewhandler.zip file. Open it and extract the files:
- Hocv_08DA85708EEB9B2F_CA54.jxe
- Hocv_08DA85708EEB9B2F_DA1F.jxe
  
Select them in the program and press Run — done. All that is left is to put the fixed files back into viewhandler.zip.
Luckily for us, no checksums are verified.
Put the whole skin folder on the SD Card with Toolbox into custom\skins\replace and replace the skin using customization/skins/ -> Copy images.mcf and ambienceColorMap.res from /custom/skins

### Download

Ready-made builds are available in [Releases](../../releases):
- `MST2HocvPatcher_v1.2-windows.exe` — Windows 10/11 x64
- `MST2HocvPatcher_v1.2-linux` — Linux x64
- This patcher is also included in the [converter](https://github.com/madd099/mib2-metainfoconverter)

### Run from sources

```bash
pip install PySide6
python MST2HocvPatcher.py
```
### Links
- [About this patch on Drive2](https://www.drive2.ru/l/712453299302827334)
