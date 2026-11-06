# Claude Code status line

แถบสถานะใต้ช่องพิมพ์ของ Claude Code แสดง 2 บรรทัด:

```
common · main* · Opus 5.5 (high) · fast
ctx ▓▓▓▓░░░░░░ 43% (85k/200k) · 5h 84% ↻ 14:33 · 7d 41% ↻ Sat 31 · $1.23 · 1h15m · +156/-23
```

- บรรทัด 1: โฟลเดอร์ · git branch (`*` = มีไฟล์ที่ยังไม่ commit) · model (effort) · fast mode · ชื่อ agent · vim mode
- บรรทัด 2: context ที่ใช้ (เขียว < 50% · เหลือง < 80% · แดง) · โควตา 5 ชั่วโมง / 7 วัน + เวลารีเซ็ต · ค่าใช้จ่าย · เวลา · บรรทัดที่แก้
- โควตา 5h/7d ขึ้นเฉพาะแพ็กเกจ Pro / Max / Ultra และหลัง Claude ตอบครั้งแรกใน session

## ติดตั้งบนเครื่องใหม่

ต้องมี Python 3.8+ (ไม่ต้องลง package เพิ่ม) · คัดลอกทั้งโฟลเดอร์นี้ไปที่เครื่องนั้น (git / USB / zip) แล้ว:

**Linux / macOS (เช่น Arch)**
```bash
bash install.sh
```

**Windows**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

ตัวติดตั้งจะ:
1. หา Python ของเครื่องนั้น (บน Windows ข้าม python stub ของ Microsoft Store)
2. คัดลอก `statusline.py` ไปที่ `~/.claude/`
3. ใส่ `statusLine` ลงใน `~/.claude/settings.json` โดย **เก็บการตั้งค่าอื่นไว้ครบ** และสำรองไฟล์เดิมเป็น `settings.json.bak`

รันซ้ำได้ (ใช้ตอนอัปเดต script ด้วย) · status line ขึ้นเมื่อ Claude Code รีเฟรชหน้าจอครั้งถัดไป หรือเปิดใหม่

## แบบคัดลอกไฟล์ไปวางเอง (ไม่ใช้ตัวติดตั้ง)

1. คัดลอก `statusline.py` ไปไว้ที่ `~/.claude/statusline.py`
   - Linux/macOS: `/home/<user>/.claude/statusline.py`
   - Windows: `C:\Users\<user>\.claude\statusline.py`
2. เปิด `~/.claude/settings.json` แล้วเพิ่ม `statusLine` (ถ้ายังไม่มีไฟล์ ให้สร้างโดยมีแค่ `{ ... }` ข้างล่าง):

   **Linux / macOS**
   ```json
   "statusLine": {
     "type": "command",
     "command": "python3 ~/.claude/statusline.py"
   }
   ```

   **Windows** (ใช้ `/` ไม่ใช้ `\` — Claude Code รันคำสั่งผ่าน Git Bash ซึ่งจะกิน backslash)
   ```json
   "statusLine": {
     "type": "command",
     "command": "python ~/.claude/statusline.py"
   }
   ```
   ถ้าไม่ขึ้น ให้ใส่ path เต็มของ Python แทน เช่น `C:/Python315/python.exe C:/Users/<user>/.claude/statusline.py` (หา path ด้วย `where python` แล้วเลือกตัวที่ **ไม่ใช่** `...\WindowsApps\python.exe` ซึ่งเป็นตัวปลอมของ Microsoft Store)

3. ระวัง comma: `statusLine` ต้องคั่นกับ key อื่นด้วย `,` — ตรวจว่า JSON ถูกด้วย `python -m json.tool ~/.claude/settings.json`

## ถอนออก

ใน Claude Code พิมพ์ `/statusline delete` หรือลบ `statusLine` ออกจาก `~/.claude/settings.json` แล้วลบ `~/.claude/statusline.py`

## ไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| `statusline.py` | ตัว status line (อ่าน JSON ของ session จาก stdin — [schema](https://code.claude.com/docs/en/statusline)) |
| `merge_settings.py` | ใส่ `statusLine` ลง settings.json อย่างปลอดภัย |
| `install.sh` / `install.ps1` | ตัวติดตั้ง Linux-macOS / Windows |
