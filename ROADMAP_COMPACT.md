# Mixnote - Development Roadmap

---

## Task 1: REAPER Waveform-Player mit Mixnote-Audio (PRIORITY)

**Goal:** Waveform des aktuell geladenen Mixnote-Songs direkt im Lua Script anzeigen — mit Playhead-Steuerung und Kommentar-Markern.

**Ansatz:** Peak-Daten werden serverseitig vorberechnet und als JSON-Endpoint bereitgestellt. Das Lua Script lädt die Peaks und rendert sie mit ImGui Draw-Primitives.

**Backend:**
- Beim Upload: Peak-Daten generieren (normalisierte Amplituden-Array, ~500–1000 Samples)
- Neuer Endpoint: `GET /api/versions/{id}/peaks` → JSON-Array `[0.12, 0.45, 0.87, ...]`
- Peaks als JSON-Datei neben der Audiodatei speichern (Cache)

**Lua Script (ImGui):**
1. Peaks vom Backend laden (einmalig pro Version-Wechsel)
2. Waveform zeichnen via `ImGui_DrawList_AddLine()` / `AddRectFilled()`
3. Kommentar-Marker als farbige vertikale Linien auf der Waveform
4. Klick auf Waveform → Timecode berechnen (mit Calibration-Offset) → `reaper.SetEditCurPos()`
5. Playhead-Linie: Echtzeit-Position als vertikale Linie über der Waveform
6. Zoom/Scroll der Waveform (optional, Phase 2)

**Abhängigkeiten:**
- Calibration-Offset (bereits vorhanden im Script)
- Versions-Auswahl (bereits vorhanden)
- Kommentar-Timecodes (bereits vorhanden)

**Files:**
- Backend: `routers/projects.py` oder `routers/comments.py` (neuer Endpoint), `utils/audio.py` (Peak-Berechnung)
- Lua: `reaper/mixnote_v2.lua` (Waveform-Rendering + Interaktion)

---

## Task 2: Marker Display

**Goal:** Eingebettete REAPER-Marker im Waveform anzeigen (Web-Frontend + Lua Script)

**How it works:**
1. User exportiert aus REAPER mit "Embed markers"
2. Backend extrahiert Marker aus WAV/MP3/FLAC beim Upload
3. Frontend zeigt vertikale Linien mit Labels auf der Waveform
4. Klick auf Marker = Jump to Position

**Visual:**
```
    Intro    Verse    Chorus    Bridge
      |        |         |         |
  > [=|========|=========|=========|====]
```

**Backend:**
- Marker aus Audio-Dateien extrahieren (BWF cue points, ID3 tags)
- Neues `Marker` DB-Model
- `GET /api/versions/{id}/markers` Endpoint

**Frontend:**
- Vertikale Linien an Marker-Positionen rendern
- Marker-Namen als Labels
- Click-Handler zum Timecode springen

**Database:**
```sql
CREATE TABLE markers (
    id INTEGER PRIMARY KEY,
    version_id INTEGER REFERENCES versions(id),
    timecode FLOAT NOT NULL,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) DEFAULT '#f59e0b',
    created_at TIMESTAMP
);
```

**Files:**
- Backend: `models.py`, `utils/audio.py`, `routers/projects.py`
- Frontend: `app.js`, `styles.css`

---

## Completed / Cancelled (Archive)

| Task | Status | Notes |
|------|--------|-------|
| Lua/ImGui Beautification | DONE | Dark theme, styled cards, accent colors |
| Client Comment Edit/Delete | DONE | PUT/DELETE endpoints, client UI |
| REAPER Upload from Script | CANCELLED | Kein File-Browser in ImGui |
| WebView Script | CANCELLED | Kein Built-in Browser in REAPER |
