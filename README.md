# 🧠 Neural Friction: AI Conviction & Kinetic Debate Engine

A real-time simulation of ideological conflict. This engine pairs **Large Language Models (LLMs)** with a **High-DOF Kinematic System** to visualize the physical toll of a heated debate. 

Unlike standard "helpful" AI assistants, these agents are programmed with **unshakeable convictions**, leading to genuine "Friction"—interruptions, physical agitation, and emotional volatility.



## 🚀 The Vision
The "Neural Friction" engine explores how abstract ideas manifest as physical stress.
* **Asynchronous Interaction:** Agents do not wait for "turns." They stream text word-by-word and can interrupt each other based on aggression thresholds.
* **Biometric Animation:** Stick figures utilize 12+ degrees of freedom (Neck, Shoulders, Elbows, Hips, Knees) to express arrogance, defensiveness, or agitation.
* **Persistent Memory:** Agents track "Grudges"—specific phrases said by the opponent—and bring them back up to mock or counter-argue.

---

## 🛠️ Requirements

* **Python 3.8+**
* **Tkinter** (Standard UI Library)
* **Ollama** (Required for the "Neural" logic. Suggested model: `smollm2:1.7b` for speed)

---

## 🕹️ Biological Degrees of Freedom (DOF)

The physical agents react in real-time to the sentiment of the conversation:

| Variable | Physical Manifestation | Trigger |
| :--- | :--- | :--- |
| **Ego / Neck** | Head Tilt | High confidence or dismissive tone. |
| **Anger / Arms** | Gesturing / Pointing | Use of exclamation marks or "Grudge" keywords. |
| **Stress / Jitter** | Procedural Sway | High Heart Rate (HR) or being interrupted. |
| **Speech / Mouth** | Mouth Oscillation | Tied directly to the word-by-word text stream. |



---

## 🛣️ The Roadmap (Next Path)

We are moving toward a more "Human" simulation by refining the following:

* **[ ] Interruption Logic:** Refilling the "Patience Meter." When it hits zero, the listener stops the speaker mid-sentence.
* **[ ] Voice Stress Visualizer:** Adding jagged waveform lines that react to the "Volume" or "Sharpness" of the text.
* **[ ] Environmental Tension:** Shaking the UI or dimming the lights as the "Global Tension" variable increases.
* **[ ] Spatial Awareness:** Having the figures physically lean in or turn away based on the level of agreement.

---

## 🤝 Contribution

If you want to help make these AI agents even more "difficult" to talk to:

1. Fork the Project.
2. Add a new **Physical Action** (e.g., `FACEPALM` or `CROSSED_ARMS`).
3. Map that action to a specific **NLP Sentiment**.
4. Open a Pull Request.

---

## 🏃 How to Run
1. Ensure **Ollama** is running with `ollama run smollm2:1.7b`.
2. Run the main script:
   ```bash
   python debate_engine.py
