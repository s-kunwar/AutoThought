# AutoThought

A real-time two-agent debate desktop application (`CONVICTION ENGINE: ASYNC INTERRUPT`) built with Python, Tkinter, and a local Ollama LLM. Two distinct personas—**ELIAS** and **MAYA**—continuously debate a shared prompt while an asynchronous GUI renders procedural 2D stick-figure animations and streams each response word-by-word.

## How the Asynchronous Debate & Interruption Engine Works

`debate.py` separates rendering from LLM generation and text streaming across two threads inside `RealtimeCollisionGUI`:

1. **Main Tkinter Thread (`root.mainloop()` & `animate_loop`)**
   - Schedules `animate_loop()` every `30 ms` (~33 FPS) via `self.root.after(30, self.animate_loop)`.
   - On each tick, clears the `tk.Canvas` and calls `draw_human()` for both `elias` (`x=400`) and `maya` (`x=1000`, `flipped=True`).

2. **Background Director Thread (`self.director`)**
   - Started as a daemon `threading.Thread(target=self.director, daemon=True)` in `__init__`.
   - Runs an infinite turn loop:
     1. Selects the next speaker randomly (`random.random() > 0.5` chooses `ELIAS`, otherwise `MAYA`).
     2. Clears `self.interrupt_event` (`threading.Event()`).
     3. Sets the active speaker's `"mood"` to `"talking"` and the opponent's `"mood"` to `"neutral"`.
     4. Calls `ollama.chat(model=MODEL, messages=...)` with the speaker's system persona (`"ACT AS {persona} Max 12 words. Be blunt."`) and `self.current_context` as the user message.
     5. Updates `self.current_context` to the newly generated response string so the next turn replies directly to it.
     6. Calls `stream_text(speaker_ui, speaker_state, text)` to append the response word-by-word (`random.uniform(0.08, 0.2)` seconds per word) into the speaker's `tk.Text` pane.
     7. Resets the speaker's `"mood"` to `"neutral"` and sleeps `random.uniform(1, 2)` seconds before the next turn.

3. **Interruption Mechanics (`interrupt_event`)**
   - Before appending each word in `stream_text()`, the loop checks `if self.interrupt_event.is_set():`.
   - When set, it appends `"... [CUT OFF]"` (tagged `"meta"`), sets `agent_state["mood"] = "stunned"`, and breaks out of the word stream immediately.
   - *Current state in `debate.py`:* `self.interrupt_event` and `self.active_speaker` are initialized and checked in `stream_text()`, and `"stunned"` visuals are implemented in `draw_human()`, though no trigger currently calls `self.interrupt_event.set()`.

## Key Components (`debate.py`)

- **`RealtimeCollisionGUI`**
  - **`__init__(self, root)`**: Configures the `1400x900` dark window (`#050505`), initializes shared debate state (`current_context`, `interrupt_event`, `active_speaker`) and agent state dictionaries (`elias`, `maya`), builds the UI, starts `animate_loop()`, and spawns the `director` daemon thread.
  - **`setup_ui(self)` & `create_box(self, parent, name, color, side)`**: Creates the top `tk.Canvas` (`height=300`, `#0a0a0a`) and the bottom two-column `tk.Frame` containing labeled, read-only `tk.Text` widgets (`Consolas` 12pt) for `ELIAS` (left) and `MAYA` (right).
  - **`draw_human(self, x, state, color, flipped=False)`**: Procedurally draws each character using `time.time()` and trigonometric offsets:
    - **Breathing & sway:** Vertical bob `math.sin(t * 2) * 2` and horizontal sway `math.cos(t * 1.5) * 3`.
    - **Mouth animation:** Oscillating oval (`abs(math.sin(t * 18)) * 10`) when `mood == "talking"`, a small `"o"` oval when `mood == "stunned"`, and a flat line when `"neutral"`.
    - **Arm kinematics:** Sets arm angle (`math.radians(...)`) to `140°` (`"talking"`), `40°` (`"stunned"`), or `0°` (`"neutral"`).
  - **`animate_loop(self)`**: Refreshes the canvas every `30 ms`.
  - **`stream_text(self, agent_ui, agent_state, text)`**: Streams words into the target `tk.Text` widget with per-word timing jitter and `interrupt_event` checks.
  - **`director(self)`**: Drives the continuous Ollama conversation loop.

## Configuration & Parameters

All configuration is defined in `debate.py` (no CLI arguments are used):

| Parameter | Value | Description |
| --- | --- | --- |
| `MODEL` | `"smollm2:1.7b"` | Local Ollama model used in `ollama.chat()` |
| `current_context` | `"The universe is a cold, mathematical accident."` | Initial seed prompt for the debate |
| `ELIAS` persona | `"Grumpy surgeon, materialist, short sentences."` | System persona (`pos`: `400`, `color`: `#3498db`, initial `hr`: `72`, `anger`: `10`) |
| `MAYA` persona | `"Spiritual mother, sharp, uses 'u' and 'rly'."` | System persona (`pos`: `1000`, `color`: `#e74c3c`, initial `hr`: `70`, `anger`: `10`) |
| System prompt constraint | `"Max 12 words. Be blunt."` | Appended to each agent's system prompt |
| `animate_loop` interval | `30 ms` | Canvas redraw period (~33 FPS) |
| Word streaming delay | `0.08–0.2 s` | `random.uniform(0.08, 0.2)` per word |
| Inter-turn pause | `1–2 s` | `random.uniform(1, 2)` after each turn |

*(Note: `hr` and `anger` values are initialized in `self.elias` and `self.maya`, though they are not dynamically updated or rendered in the current `debate.py`.)*

## Installation & Running

### Prerequisites
- Python 3 with `tkinter`
- Ollama installed and running locally

### Setup & Launch
```bash
git clone https://github.com/s-kunwar/AutoThought
cd AutoThought
pip install -r requirements.txt
ollama pull smollm2:1.7b
python debate.py
```

*(Note: `requirements.txt` includes `ollama` as well as additional packages—`chromadb`, `pdfplumber`, `langchain`, `langchain-core`, `langchain-ollama`, `langchain-community`, `langchain_text_splitters`, `unstructured`, `unstructured[all-docs]`, `fastembed`, `pikepdf`, `sentence-transformers`, `elevenlabs`—though `debate.py` currently imports only `tkinter`, `ollama`, `threading`, `time`, `random`, and `math`.)*

## Project Structure

```text
AutoThought/
├── debate.py          # Tkinter GUI, procedural stick-figure animation, Ollama director thread, and word streamer
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```
