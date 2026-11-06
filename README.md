# Claude Code status line

แถบสถานะใต้ช่องพิมพ์ของ Claude Code แสดง 2 บรรทัด:

```
common · main* · Opus 5.5 (high) · fast
ctx ▓▓▓▓░░░░░░ 43% (85k/200k) · 5h 84% ↻ 14:33 (2h 13m 05s) · 7d 41% ↻ Sat 31 (2d 04h 13m 05s) · $1.23 · 1h15m · +156/-23
```

- บรรทัด 1: โฟลเดอร์ · git branch (`*` = มีไฟล์ที่ยังไม่ commit) · model (effort) · fast mode · ชื่อ agent · vim mode
- บรรทัด 2: context ที่ใช้ (เขียว < 50% · เหลือง < 80% · แดง) · โควตา 5 ชั่วโมง / 7 วัน + เวลารีเซ็ต (เวลาที่เหลือ วัน/ชั่วโมง/นาที/วินาที) · ค่าใช้จ่าย · เวลา · บรรทัดที่แก้
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
3. ใส่ `statusLine` (พร้อม `refreshInterval: 1` ให้นับถอยหลังทุกวินาที) ลงใน `~/.claude/settings.json` โดย **เก็บการตั้งค่าอื่นไว้ครบ** และสำรองไฟล์เดิมเป็น `settings.json.bak`

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
     "command": "python3 ~/.claude/statusline.py",
     "refreshInterval": 1
   }
   ```

   **Windows** (ใช้ `/` ไม่ใช้ `\` — Claude Code รันคำสั่งผ่าน Git Bash ซึ่งจะกิน backslash)
   ```json
   "statusLine": {
     "type": "command",
     "command": "python ~/.claude/statusline.py",
     "refreshInterval": 1
   }
   ```
   ถ้าไม่ขึ้น ให้ใส่ path เต็มของ Python แทน เช่น `C:/Python315/python.exe C:/Users/<user>/.claude/statusline.py` (หา path ด้วย `where python` แล้วเลือกตัวที่ **ไม่ใช่** `...\WindowsApps\python.exe` ซึ่งเป็นตัวปลอมของ Microsoft Store)

   `refreshInterval` = รันซ้ำทุกกี่วินาที (ต่ำสุด 1) ทำให้เวลาที่เหลือนับถอยหลังแม้ไม่ได้พิมพ์อะไร · ไม่ใส่ก็ได้ แต่ตัวเลขจะขยับเฉพาะตอนมี event (ส่งข้อความ / Claude ตอบ)

3. ระวัง comma: `statusLine` ต้องคั่นกับ key อื่นด้วย `,` — ตรวจว่า JSON ถูกด้วย `python -m json.tool ~/.claude/settings.json`

## ถอนออก

ใน Claude Code พิมพ์ `/statusline delete` หรือลบ `statusLine` ออกจาก `~/.claude/settings.json` แล้วลบ `~/.claude/statusline.py`

## ทำงานยังไง

ไม่ใช่ plugin ที่ฝังใน Claude Code — เป็น **โปรแกรมธรรมดาที่ Claude Code สั่งรัน แล้วเอาสิ่งที่มัน print ออกมาไปแสดงใต้ช่องพิมพ์**

### มาอยู่ตรงนั้นได้ยังไง

ตัวติดตั้งทำ 2 อย่าง:

1. คัดลอก `statusline.py` ไปที่ `~/.claude/statusline.py`
2. ใส่ใน `~/.claude/settings.json`:
   ```json
   "statusLine": {
     "type": "command",
     "command": "<python> ~/.claude/statusline.py",
     "refreshInterval": 1
   }
   ```

Claude Code อ่าน `settings.json` ตอนเปิด → เห็น `statusLine` → รู้ว่าต้องรันคำสั่งนี้แล้วเอาผลมาแสดง (ลบ `statusLine` ออก = แถบหาย แม้ไฟล์ `.py` ยังอยู่)

### วงจรการทำงาน (ทุกครั้งที่อัปเดต)

```
 Claude Code                                  statusline.py
 ───────────                                  ─────────────
 เกิด event / ครบ 1 วินาที
   │
   ├─ รวบรวมข้อมูล session เป็น JSON
   │
   ├─ รัน command ─── stdin: JSON ──────────▶ อ่าน JSON
   │   (Windows: ผ่าน Git Bash)               ├─ หยิบ field ที่ต้องใช้
   │                                          ├─ รัน git เองเพื่อดู branch
   │                                          ├─ คำนวณเวลาที่เหลือจากนาฬิกาเครื่อง
   │                                          └─ print 2 บรรทัด (มีรหัสสี ANSI)
   │
   ◀────────────── stdout: ข้อความ ──────────┘
   │
   └─ วาดใต้ช่องพิมพ์ (แทนของเดิม)
```

**รันเมื่อไหร่** ([docs](https://code.claude.com/docs/en/statusline)):
- มี event: ส่งข้อความ, Claude ตอบเสร็จ, เปลี่ยน model / mode ฯลฯ
- ครบ `refreshInterval` (ตั้งไว้ 1 วินาที) — แม้นั่งเฉยๆ
- ถึงเวลา `resets_at` ของโควตา
- หลาย event ติดกัน → รอ 300ms ให้เงียบก่อนค่อยรันครั้งเดียว (debounce)
- รอบใหม่มาตอนรอบเก่ายังไม่เสร็จ → ยกเลิกรอบเก่า

แต่ละรอบคือ process ใหม่ (เปิด Python → รัน → ปิด) ไม่มีอะไรค้างอยู่เบื้องหลัง ใช้ประมาณ 0.1 วินาทีต่อรอบ

### ข้อมูลมาจากไหน (3 แหล่ง)

**ก. JSON จาก Claude Code ทาง stdin** (แหล่งหลัก) — ตัวอย่างบางส่วน:

```json
{
  "workspace": { "current_dir": "/home/me/project" },
  "model":     { "display_name": "Opus 5.5" },
  "effort":    { "level": "high" },
  "fast_mode": false,
  "context_window": {
    "used_percentage": 43,
    "total_input_tokens": 80000, "total_output_tokens": 5000,
    "context_window_size": 200000
  },
  "rate_limits": {
    "five_hour": { "used_percentage": 84, "resets_at": 1793990000 },
    "seven_day": { "used_percentage": 41, "resets_at": 1794170000 }
  },
  "cost": {
    "total_cost_usd": 1.23, "total_duration_ms": 4500000,
    "total_lines_added": 156, "total_lines_removed": 23
  }
}
```

| ที่แสดง | field | Claude Code ได้มาจาก |
|---|---|---|
| ชื่อโฟลเดอร์ | `workspace.current_dir` | โฟลเดอร์ที่เปิด session |
| `Opus 5.5 (high)` | `model.display_name`, `effort.level` | ค่าที่เลือกใน session |
| `ctx ▓▓▓▓░░ 43%` | `context_window.*` | นับ token ของบทสนทนาเทียบขนาด context ของ model |
| `5h 84%` / `7d 41%` | `rate_limits.*.used_percentage` | **API ของ Anthropic ส่งกลับมากับทุก response** → ขึ้นหลัง Claude ตอบครั้งแรก, เฉพาะแพ็กเกจ Pro / Max / Ultra |
| `↻ 20:11` | `rate_limits.*.resets_at` | มากับ API เช่นกัน เป็น Unix epoch (วินาทีนับจาก 1970) |
| `$1.23 · 1h15m · +156/-23` | `cost.*` | Claude Code นับเองตลอด session |

ใน script:

```python
data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig").strip() or "{}")
model = get(data, "model", "display_name")
```

`get()` เดินเข้าไปใน dict ทีละชั้น ถ้า field ไหนไม่มีคืน `None` แล้วข้ามไป แถบจึงไม่พังตอนข้อมูลยังมาไม่ครบ (เช่น `rate_limits` ก่อน Claude ตอบครั้งแรก)

**ข. script ไปถามเอง: git branch** — `main*` ไม่ได้มาจาก Claude Code แต่ script รัน git เองในโฟลเดอร์ `current_dir`:

```
git -C <cwd> branch --show-current                     → main
git -C <cwd> status --porcelain --untracked-files=no   → มีผลลัพธ์ = มีไฟล์ยังไม่ commit → เติม *
```

ตั้ง timeout 1 วินาที — ไม่ใช่ git repo หรือ git ช้า ก็แค่ไม่แสดงส่วนนี้

**ค. คำนวณเอง: เวลาที่เหลือ**

```python
left = countdown(resets - time.time())   # resets_at − เวลาปัจจุบันของเครื่อง = วินาทีที่เหลือ
```

`countdown()` ใช้ `divmod` แตกเป็นวัน (86400) → ชั่วโมง (3600) → นาที (60) → วินาที ได้ `2d 04h 13m 05s` · `resets_at` คงที่ แต่ `time.time()` เปลี่ยน + `refreshInterval: 1` ให้คำนวณใหม่ทุกวินาที จึงนับถอยหลังได้ · `time.localtime()` แปลง epoch เป็นเวลาตาม timezone ของเครื่อง (`20:11`, `Sun 08`)

### สีและ 2 บรรทัด

- สี = รหัส ANSI ในข้อความ เช่น `\033[32m` (เขียว) … `\033[0m` (รีเซ็ต) Claude Code แปลเป็นสีให้ · `color_for()` เลือกสีตาม %: < 50 เขียว, < 80 เหลือง, ที่เหลือแดง
- 2 บรรทัด = `print()` 2 ครั้ง Claude Code แสดงทุกบรรทัดจาก stdout

### ลองรันเองนอก Claude Code

เพราะมันแค่ "รับ JSON เข้า → print ออก" ทดสอบได้ไม่ต้องเปิด Claude Code:

```bash
echo '{"model":{"display_name":"Test"},"context_window":{"used_percentage":70}}' | python ~/.claude/statusline.py
```

```
 · Test
ctx ▓▓▓▓▓▓▓░░░ 70%
```

อยากเห็น JSON จริงที่ Claude Code ส่งมา → เพิ่มบรรทัดนี้ใต้ `data = ...` ชั่วคราว แล้วเปิดดู `~/.claude/statusline-last.json` (ดูเสร็จลบออก ไม่งั้นมันเขียนไฟล์ทุกวินาที):

```python
open(os.path.expanduser("~/.claude/statusline-last.json"), "w").write(json.dumps(data, indent=2))
```

## ไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| `statusline.py` | ตัว status line (อ่าน JSON ของ session จาก stdin — [schema](https://code.claude.com/docs/en/statusline)) |
| `merge_settings.py` | ใส่ `statusLine` ลง settings.json อย่างปลอดภัย |
| `install.sh` / `install.ps1` | ตัวติดตั้ง Linux-macOS / Windows |
