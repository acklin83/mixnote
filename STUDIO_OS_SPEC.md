# Studio OS — Product Specification

> **Zweck dieses Dokuments:** Single Source of Truth für die Entwicklung von Studio OS.
> Dieses Dokument wird im Repository abgelegt und dient als Briefing für Claude Code.
> Letzte Aktualisierung: 2026-02-12

---

## 1. Produktvision

### 1.1 Studio OS

Studio OS ist eine modulare, selbst-hostbare Plattform für Recording-Studios, Mixing/Mastering-Engineers und Produzenten. Ein Login, ein Dashboard, ein System — für den gesamten Studio-Betrieb.

**Module (in Reihenfolge der Entwicklung):**

| Modul | Funktion | Ersetzt | Priorität |
|---|---|---|---|
| **MixNote** | Audio Review & Delivery | Mixup.audio, Dropbox-Workflows | Phase 1 (jetzt) |
| **Studio CRM** | Kontakte & Unified Inbox | Cloze, HubSpot | Phase 2 (~Q3 2026) |
| **Studio Books** | Angebote, Rechnungen, Buchhaltung | Bexio, Wave | Phase 3 (~Q4 2026) |
| **Studio Planner** | Kalender, Session-Planung | Calendly, ClickUp | Phase 4 (~2027) |

Alle Module teilen sich die gleiche Datenbank, das gleiche Auth-System, die gleiche Contact-Tabelle und den gleichen Event-Bus. Ein Kunde existiert einmal im System — egal ob er über MixNote kommentiert, per WhatsApp schreibt oder eine Rechnung bekommt.

### 1.2 MixNote (Modul 1 — dieses Dokument)

MixNote ist das erste Modul und das Produkt, mit dem Studio OS an den Markt geht. Es ist eine webbasierte Audio-Review-Plattform. Kunden erhalten einen Link, hören den Mix, kommentieren direkt auf der Timeline und geben ihr Approval — ohne Account, ohne App-Download, ohne Reibung.

**Positioning:** "Die zuverlässige Mixup.audio-Alternative — gebaut von einem Engineer, der es jeden Tag nutzt."

**Kernversprechen:**
- Für Engineers: Alle Projekte, alle Revisionen, alle Kommentare — ein Dashboard. Nie wieder E-Mail-Chaos.
- Für Kunden: Ein Link. Play. Kommentieren. Approve. Fertig.

### 1.3 Architektur-Prinzip: Modular von Tag 1

Jedes Modul ist über den **Shared Core** verbunden:

```
┌─────────────────────────────────────────────────────────┐
│                      SHARED CORE                        │
│                                                         │
│  Tenant ─── User ─── Contact ─── Event Bus ─── Auth    │
│                                                         │
│  Notification Pipeline ─── File Storage ─── Settings    │
│                                                         │
└──────┬──────────┬──────────────┬──────────────┬─────────┘
       │          │              │              │
   ┌───┴───┐  ┌──┴───┐   ┌─────┴────┐  ┌──────┴─────┐
   │MixNote│  │ CRM  │   │  Books   │  │  Planner   │
   │       │  │      │   │          │  │            │
   │Review │  │Inbox │   │Angebote  │  │Kalender    │
   │Approve│  │Email │   │Rechnungen│  │Sessions    │
   │Deliver│  │WhatsA│   │Zahlungen │  │Ressourcen  │
   └───────┘  └──────┘   └──────────┘  └────────────┘
```

**Regeln:**
- Module kommunizieren NICHT direkt miteinander, sondern über den Event-Bus
- Jedes Modul kann eigenständig funktionieren (graceful degradation)
- Shared Core Entities (Contact, Tenant, User) gehören keinem Modul
- Modul-spezifische Entities (Song, Version, Invoice) gehören ihrem Modul

---

## 2. Zielgruppen

### Primär: Freelance Mixing/Mastering Engineers
- 1-3 Personen
- 5-30 aktive Projekte gleichzeitig
- Frustriert von Dropbox/WeTransfer/E-Mail-Workflows
- Preissensitiv, aber bereit für Tools die Zeit sparen

### Sekundär: Recording Studios
- Kleines Team (2-5)
- Wollen professionell wirken (White Label)
- Brauchen dokumentierte Approvals

### Tertiär: Podcast-Produzenten, Post-Production
- Gleicher Review-Workflow, anderer Content-Typ
- V1 fokussiert auf Musik, aber Architektur soll content-agnostisch sein

---

## 3. Wettbewerbsanalyse

### Mixup.audio (Hauptkonkurrent)
- **Stärken:** DAW-Plugin (AAX/AU/VST), LUFS-Level-Matching, Dolby Atmos, Spotify/YouTube Referenz-Vergleich, grosse Testimonials (SZA, A$AP Ferg)
- **Schwächen:** App crasht ständig (App Store Reviews: "I don't trust using it with my clients"), Notifications unzuverlässig, Support quasi inexistent, Approval erst im $30/mo-Tier, kein Projekt-Dashboard, kein dokumentierter Approval-Workflow
- **Pricing:** Free (30 Tage Limit) / Pro $9.99/mo / Studio $29.99/mo

### Samply.app
- Einfacher Audio-Player mit Share-Links
- Wenig Features, aber funktioniert zuverlässig
- Transparenzprobleme (Pricing schwer zu finden)

### Fidbak
- Empfohlen als Alternative auf Gearspace
- Fokus auf einfaches Feedback

### Filepass
- Enterprise-orientiert, teurer
- Fokus auf Delivery, nicht Review

### MixNote Differenzierung
1. **Reliability > Feature Bloat** — Es funktioniert. Jedes Mal. Auf jedem Gerät.
2. **Projekt-zentrisch** statt Track-zentrisch — ein Auftrag = ein Projekt mit Status
3. **Approval als dokumentierter Workflow** — nicht nur ein Button
4. **Engineer Dashboard** — Überblick über alle laufenden Projekte
5. **Smart Notifications** — die tatsächlich funktionieren
6. **Self-Hostable** — Docker-Image für Studios mit Datenschutz-Anforderungen

---

## 4. Pricing-Modell

| | **Free** | **Pro** | **Studio** |
|---|---|---|---|
| **Preis** | €0/mo | €12/mo (€120/Jahr) | €35/mo (€350/Jahr) |
| **Aktive Projekte** | 3 | Unbegrenzt | Unbegrenzt |
| **Songs total** | 15 | Unbegrenzt | Unbegrenzt |
| **Zeitlimit** | 15 Tage pro Track | Keins | Keins |
| **Approval** | Basic (Button) | ✓ mit E-Mail-Bestätigung | ✓ mit PDF-Export |
| **Branding** | MixNote-Brand | Logo + Farben | Custom Subdomain + White Label |
| **Notifications** | Basis-E-Mail | ✓ + Auto-Nudge | ✓ + Wöchentlicher Digest |
| **Dashboard** | Einfach | Vollständig | Vollständig |
| **Storage** | 2 GB | 50 GB | 200 GB |
| **Users** | 1 | 1 | 3 |
| **REAPER Integration** | ✗ | ✓ | ✓ |
| **API Zugang** | ✗ | ✗ | ✓ |

**Revenue-Ziel:**
- 100 Pro + 30 Studio = €2'250 MRR (Milestone 1)
- 200 Pro + 80 Studio = €5'200 MRR (Milestone 2, ~12 Monate nach Launch)

---

## 5. Architektur

### 5.1 Tech Stack

| Komponente | Technologie | Begründung |
|---|---|---|
| **Backend** | Python / FastAPI | Existiert bereits im MVP, async, schnell, gut für API |
| **Datenbank** | PostgreSQL | Multi-Tenant, Full-Text-Search, robust. Migration von SQLite. |
| **Frontend** | Vanilla JS + TailwindCSS | Existiert im MVP. Kein Framework-Overhead. |
| **Audio Player** | Wavesurfer.js | Existiert im MVP. Waveform-Rendering, Timeline-Kommentare. |
| **File Storage** | S3-kompatibel (Backblaze B2) | $6/TB/mo, egress über Cloudflare kostenlos |
| **Hosting** | Hetzner Cloud VPS (Nürnberg) | Nah an Schweiz, günstig, zuverlässig |
| **Reverse Proxy** | Caddy | Automatisches SSL, einfache Konfiguration |
| **DNS/CDN** | Cloudflare | Wildcard SSL, DDoS-Schutz, Caching |
| **E-Mail** | Postmark | Transactional E-Mails (Notifications, Approvals) |
| **Billing** | Stripe | Subscriptions, Webhooks |
| **Containerisierung** | Docker + Docker Compose | Deployment + Self-Hosted Option |
| **REAPER Integration** | Lua / ReaImGui | Existiert im MVP |

### 5.2 Multi-Tenancy

**Ansatz:** Shared Database mit Tenant-ID (nicht separate DBs pro Tenant).

```
Routing:
  studio-name.mixnote.io → Caddy → FastAPI (tenant_id aus Subdomain)
  mixnote.io/s/{share_uuid} → Öffentlicher Share-Link (tenant-agnostisch)
```

**Begründung:** Einfacher zu warten, einfacher zu migrieren, Queries über alle Tenants möglich (Admin-Analytics). Tenant-Isolation über konsequente WHERE-Clauses und Middleware.

### 5.3 Infrastruktur-Skalierung

| Phase | Kunden | Server | Kosten |
|---|---|---|---|
| 0-20 | MVP | CX22 (2 vCPU, 4 GB) | ~€7/mo |
| 20-50 | Wachstum | CX32 (4 vCPU, 8 GB) | ~€12/mo |
| 50-100 | Etabliert | CX42 (8 vCPU, 16 GB) | ~€23/mo |
| 100+ | Scale | Multi-Server + LB | Nach Bedarf |

### 5.4 Private Instanz

Frank's DiskStation (Störsender Studio) läuft separat:
- URL: mix.stoersender.ch
- Eigene Docker-Instanz mit SQLite (Single-Tenant)
- 10GbE internes Netzwerk
- Dient als Dogfooding- und Test-Instanz

---

## 6. Datenmodell

### 6.1 Shared Core Entities

Diese Entities gehören keinem Modul. Sie sind die Basis für alle Module.

```
Tenant
├── id: UUID
├── name: String
├── slug: String (Subdomain)
├── plan: Enum (free, pro, studio)
├── stripe_customer_id: String?
├── branding_logo_url: String?
├── branding_primary_color: String?
├── branding_accent_color: String?
├── custom_domain: String? (Studio-Plan)
├── storage_used_bytes: BigInt
├── created_at: DateTime
└── updated_at: DateTime

User (Engineer/Studio-Besitzer — der zahlende Nutzer)
├── id: UUID
├── tenant_id: FK → Tenant
├── email: String (unique)
├── password_hash: String
├── name: String
├── role: Enum (owner, member)
├── created_at: DateTime
└── last_login_at: DateTime

Contact (Shared: Kunden, Bandmitglieder, Labels, etc.)
├── id: UUID
├── tenant_id: FK → Tenant
├── name: String
├── company: String? (Band, Label, Agentur)
├── emails: JSON (Array von E-Mail-Adressen, erste = primär)
├── phones: JSON (Array von Telefonnummern)
├── notes: Text? (Freitext-Notizen)
├── tags: JSON (Array von Strings, z.B. ["band", "label", "mastering"])
├── source: Enum (manual, website_form, mixnote_share, crm_import)
├── last_activity_at: DateTime? (letzter Kontaktpunkt, egal welches Modul)
├── created_at: DateTime
└── updated_at: DateTime
```

**Contact-Regeln:**
- Ein Contact wird automatisch erstellt, wenn ein Projekt mit neuer E-Mail angelegt wird
- Wenn eine E-Mail bereits existiert (im selben Tenant), wird der bestehende Contact verknüpft
- Contacts sind modul-übergreifend: MixNote, CRM, Books, Planner referenzieren alle den gleichen Record
- Contact-Matching: Primär über E-Mail, sekundär über Telefonnummer

```
Event (Event-Bus — Shared Communication Layer)
├── id: UUID
├── tenant_id: FK → Tenant
├── type: String (dotted notation: "mixnote.comment.created", "mixnote.approval.completed")
├── source_module: String ("mixnote", "crm", "books", "planner", "core")
├── actor_type: Enum (user, client, system)
├── actor_id: UUID? (User.id oder Contact.id)
├── entity_type: String ("project", "song", "comment", "contact", "invoice")
├── entity_id: UUID
├── contact_id: FK → Contact? (wenn Event einen Kunden betrifft)
├── project_id: FK → Project? (wenn Event ein Projekt betrifft)
├── payload: JSON (Event-spezifische Daten)
├── created_at: DateTime
└── processed_by: JSON (Array von Modul-Namen die dieses Event verarbeitet haben)
```

**Event-Typen (MixNote V1):**
- `mixnote.project.created` — Neues Projekt angelegt
- `mixnote.version.uploaded` — Neue Version hochgeladen
- `mixnote.comment.created` — Neuer Kommentar (Engineer oder Client)
- `mixnote.comment.resolved` — Kommentar als gelöst markiert
- `mixnote.approval.completed` — Song vom Client approved
- `mixnote.share.accessed` — Client hat Share-Link geöffnet
- `mixnote.nudge.sent` — Auto-Reminder an Client gesendet

**Reservierte Event-Typen (für spätere Module):**
- `crm.email.received`, `crm.whatsapp.received` — CRM Modul
- `books.invoice.sent`, `books.payment.received` — Books Modul
- `planner.session.booked`, `planner.session.completed` — Planner Modul

```
Notification (Shared — generiert aus Events)
├── id: UUID
├── tenant_id: FK → Tenant
├── user_id: FK → User (Empfänger)
├── event_id: FK → Event (das auslösende Event)
├── type: Enum (new_comment, approval, nudge_reminder, weekly_digest)
├── project_id: FK → Project?
├── song_id: FK → Song?
├── title: String
├── body: Text
├── is_read: Boolean
├── email_sent: Boolean
├── email_sent_at: DateTime?
├── created_at: DateTime
└── read_at: DateTime?
```

### 6.2 MixNote Entities

Diese Entities gehören zum MixNote-Modul.

```
Project
├── id: UUID
├── tenant_id: FK → Tenant
├── contact_id: FK → Contact (der Kunde)
├── title: String
├── status: Enum (active, waiting_feedback, approved, archived)
├── created_at: DateTime
├── updated_at: DateTime
└── archived_at: DateTime?

Song
├── id: UUID
├── project_id: FK → Project
├── title: String
├── order: Int (Reihenfolge im Projekt)
├── status: Enum (in_progress, waiting_feedback, revision_requested, approved)
├── approved_at: DateTime?
├── approved_by_contact_id: FK → Contact?
├── approved_version_id: FK → Version?
├── created_at: DateTime
└── updated_at: DateTime

Version
├── id: UUID
├── song_id: FK → Song
├── version_number: Int (auto-increment per song)
├── file_path: String (S3 key)
├── file_size_bytes: BigInt
├── duration_seconds: Float
├── sample_rate: Int?
├── bit_depth: Int?
├── waveform_data: JSON (pre-computed peaks für Wavesurfer)
├── notes: Text? (Engineer-Notizen zur Version)
├── created_at: DateTime
└── is_current: Boolean

Comment
├── id: UUID
├── version_id: FK → Version
├── parent_id: FK → Comment? (für Replies)
├── author_contact_id: FK → Contact? (wenn Client)
├── author_user_id: FK → User? (wenn Engineer)
├── author_type: Enum (engineer, client)
├── timestamp_seconds: Float? (null = General Comment)
├── body: Text
├── is_resolved: Boolean (default false)
├── resolved_at: DateTime?
├── created_at: DateTime
└── updated_at: DateTime

ShareLink
├── id: UUID
├── project_id: FK → Project
├── token: String (short UUID, URL-safe)
├── password_hash: String? (optional Passwortschutz)
├── expires_at: DateTime?
├── is_active: Boolean
├── last_accessed_at: DateTime?
├── access_count: Int
├── created_at: DateTime
└── updated_at: DateTime

ApprovalRecord
├── id: UUID
├── song_id: FK → Song
├── version_id: FK → Version
├── contact_id: FK → Contact
├── approved_at: DateTime
├── ip_address: String?
├── user_agent: String?
├── notes: Text? (optionaler Kommentar bei Approval)
└── pdf_path: String? (generiertes Approval-Dokument, Pro/Studio)
```

### 6.3 Indexes

```sql
-- Shared Core
CREATE INDEX idx_contact_tenant ON contact(tenant_id);
CREATE INDEX idx_contact_emails ON contact USING GIN (emails);
CREATE INDEX idx_event_tenant_type ON event(tenant_id, type, created_at DESC);
CREATE INDEX idx_event_contact ON event(contact_id, created_at DESC) WHERE contact_id IS NOT NULL;
CREATE INDEX idx_event_project ON event(project_id, created_at DESC) WHERE project_id IS NOT NULL;

-- MixNote
CREATE INDEX idx_project_tenant_status ON project(tenant_id, status);
CREATE INDEX idx_project_contact ON project(contact_id);
CREATE INDEX idx_song_project ON song(project_id, "order");
CREATE INDEX idx_version_song ON version(song_id, version_number DESC);
CREATE INDEX idx_comment_version ON comment(version_id, created_at);
CREATE INDEX idx_sharelink_token ON sharelink(token) WHERE is_active = true;
CREATE INDEX idx_notification_user_unread ON notification(user_id, created_at DESC) WHERE is_read = false;
```

### 6.4 Event-Bus Implementation

Kein Kafka, kein RabbitMQ. PostgreSQL-nativ:

```
Schreiben: Jede relevante Aktion → INSERT in Event-Tabelle
Verarbeiten: Background Worker polled neue Events (oder LISTEN/NOTIFY)
Konsumenten: Jedes Modul registriert Handler für relevante Event-Typen

Aktuell (MixNote only):
  Event → Notification Worker → In-App + E-Mail

Später (mit CRM):
  Event → Notification Worker → In-App + E-Mail
  Event → CRM Worker → Contact Activity Timeline updaten
  Event → Books Worker → Projekt-Stunden für Rechnung tracken
```

**Worker-Architektur:**
```python
# event_handlers.py — Registry Pattern

handlers = {
    "mixnote.comment.created": [
        notification_handler,      # → Notification + E-Mail
        contact_activity_handler,  # → Contact.last_activity_at updaten
    ],
    "mixnote.approval.completed": [
        notification_handler,
        contact_activity_handler,
        # Später: books_handler → "Projekt abgeschlossen, Rechnung erstellen?"
    ],
}
```

---

## 7. API-Spezifikation

### 7.1 Authentifizierung

**Engineer/Admin:** JWT-Token (Login via E-Mail + Passwort)
- Access Token: 15 Minuten Gültigkeit
- Refresh Token: 7 Tage, HttpOnly Cookie
- Alle `/api/`-Routen erfordern gültigen JWT
- Tenant-Isolation: JWT enthält `tenant_id`, Middleware prüft gegen Subdomain

**Client (Share-Link):** Token-basiert
- `/s/{share_token}` → kein Login nötig
- Optional: Passwort-Abfrage (wenn auf ShareLink gesetzt)
- Client-Name wird beim ersten Kommentar gesetzt (Cookie für Wiedererkennung)

### 7.2 Endpoints

#### Auth
```
POST   /api/auth/register          → Account + Tenant erstellen
POST   /api/auth/login             → JWT erhalten
POST   /api/auth/refresh           → Token erneuern
POST   /api/auth/forgot-password   → Reset-Link senden
POST   /api/auth/reset-password    → Passwort setzen
```

#### Contacts (Shared Core)
```
GET    /api/contacts                → Liste aller Kontakte (Filter: search, tags)
POST   /api/contacts               → Neuen Kontakt erstellen
GET    /api/contacts/{id}           → Kontakt-Detail
PATCH  /api/contacts/{id}           → Kontakt updaten
DELETE /api/contacts/{id}           → Kontakt löschen (Soft Delete)
GET    /api/contacts/{id}/activity  → Activity Timeline (Events aller Module für diesen Kontakt)
GET    /api/contacts/{id}/projects  → Alle MixNote-Projekte dieses Kontakts
```

#### Projects
```
GET    /api/projects                → Liste aller Projekte (mit Filter: status, contact_id, search)
POST   /api/projects               → Neues Projekt erstellen (mit contact_id ODER client_name/email → auto-Contact)
GET    /api/projects/{id}           → Projekt-Detail (inkl. Songs, aktuelle Versionen, Contact)
PATCH  /api/projects/{id}           → Projekt updaten (Titel, Contact, Status)
DELETE /api/projects/{id}           → Projekt archivieren (Soft Delete)
GET    /api/projects/{id}/activity  → Activity Feed (alle Events dieses Projekts)
```

#### Songs
```
GET    /api/projects/{id}/songs              → Songs eines Projekts
POST   /api/projects/{id}/songs              → Song hinzufügen
PATCH  /api/projects/{id}/songs/{song_id}    → Song updaten (Titel, Reihenfolge)
DELETE /api/projects/{id}/songs/{song_id}    → Song entfernen
```

#### Versions
```
GET    /api/songs/{song_id}/versions                     → Alle Versionen eines Songs
POST   /api/songs/{song_id}/versions                     → Neue Version hochladen (multipart)
GET    /api/songs/{song_id}/versions/{version_id}/stream  → Audio-Stream (Range-Support)
DELETE /api/songs/{song_id}/versions/{version_id}         → Version löschen
```

#### Comments
```
GET    /api/versions/{version_id}/comments               → Kommentare einer Version
POST   /api/versions/{version_id}/comments               → Kommentar erstellen
PATCH  /api/comments/{comment_id}                        → Kommentar bearbeiten
PATCH  /api/comments/{comment_id}/resolve                → Als gelöst markieren
DELETE /api/comments/{comment_id}                        → Kommentar löschen
```

#### Share Links
```
GET    /api/projects/{id}/share                → Aktive Share-Links
POST   /api/projects/{id}/share                → Neuen Share-Link erstellen
PATCH  /api/share/{share_id}                   → Link updaten (Passwort, Ablauf)
DELETE /api/share/{share_id}                   → Link deaktivieren
```

#### Public (Client-Facing, kein JWT)
```
GET    /s/{token}                              → Projekt-Ansicht für Kunden
GET    /s/{token}/songs/{song_id}/stream       → Audio-Stream
POST   /s/{token}/songs/{song_id}/comments     → Kommentar als Client
POST   /s/{token}/songs/{song_id}/approve      → Approval abgeben
```

#### Approval
```
GET    /api/songs/{song_id}/approval           → Approval-Status und -Record
POST   /api/songs/{song_id}/approval/pdf       → PDF-Export generieren (Pro/Studio)
```

#### Notifications
```
GET    /api/notifications                      → Ungelesene Notifications
PATCH  /api/notifications/{id}/read            → Als gelesen markieren
PATCH  /api/notifications/read-all             → Alle als gelesen markieren
```

#### Dashboard
```
GET    /api/dashboard                          → Aggregierte Daten:
                                                  - Projekte nach Status
                                                  - Ungelesene Kommentare
                                                  - Überfällige Reviews (kein Feedback seit X Tagen)
                                                  - Storage-Verbrauch
```

#### Account & Billing
```
GET    /api/account                            → Account-Details
PATCH  /api/account                            → Account updaten
GET    /api/account/billing                    → Stripe Customer Portal Link
POST   /api/account/billing/checkout           → Stripe Checkout Session erstellen
POST   /api/webhooks/stripe                    → Stripe Webhooks empfangen
```

---

## 8. User Flows

### 8.1 Engineer: Neues Projekt erstellen

```
1. Login → Dashboard
2. "+ Neues Projekt"
3. Formular: Titel, Client-Name, Client-E-Mail (optional)
4. → Projekt erstellt, Weiterleitung zu Projekt-Ansicht
5. "Song hinzufügen" → Titel eingeben
6. "Version hochladen" → Drag & Drop oder File Picker
7. Upload startet, Waveform wird generiert
8. "Share-Link erstellen" → Link kopieren, optional mit Passwort
9. Link per E-Mail/WhatsApp an Kunden senden
   ODER: E-Mail direkt aus MixNote (wenn Client-E-Mail hinterlegt)
```

### 8.2 Client: Mix reviewen und kommentieren

```
1. Klick auf Share-Link → Browser öffnet MixNote Client-View
2. Kein Login, kein Account, kein Download
3. Projekt-Titel und Studio-Branding sichtbar
4. Song-Liste mit aktuellem Status
5. Play drücken → Audio-Stream startet, Waveform läuft
6. An gewünschter Stelle auf Waveform klicken → Kommentar-Input erscheint
7. Kommentar tippen → Absenden
8. Kommentar erscheint als Marker auf der Waveform
9. Weitere Songs durchgehen
10. Wenn alles passt: "Approve" Button pro Song
11. Approval-Bestätigung: "Du gibst Version 3 von 'Songtitel' frei. Bist du sicher?"
12. Bestätigung → Song-Status wechselt zu "Approved"
13. Engineer bekommt Notification
```

### 8.3 Engineer: Feedback verarbeiten

```
1. Dashboard zeigt: "Projekt X: 5 neue Kommentare"
2. Klick → Projekt-Ansicht
3. Kommentare sichtbar auf Waveform + als Liste
4. Klick auf Kommentar → Audio springt zu Timestamp
5. Kommentar bearbeiten in DAW
6. Neue Version hochladen
7. Kommentar als "Resolved" markieren
8. Kunde bekommt automatisch Notification: "Neue Version verfügbar"
```

### 8.4 Engineer: REAPER-Integration (Pro/Studio)

```
1. REAPER Script installieren (Lua/ReaImGui)
2. Script öffnen → MixNote-URL eingeben + API-Token
3. Projekte laden → Song auswählen
4. Kommentare erscheinen im REAPER-Fenster
5. Klick auf Kommentar → REAPER-Playhead springt zu Position
6. "Resolve" direkt aus REAPER
7. "Neue Version hochladen" → Render + Upload in einem Schritt
```

### 8.5 Approval-Workflow (Detail)

```
Client klickt "Approve" auf Song
  → Confirmation Dialog: "Version 3 von 'Songtitel' freigeben?"
  → Optional: Kommentar hinzufügen ("Sounds great!")
  → Bestätigen

System erstellt ApprovalRecord:
  - Timestamp
  - Client-Name
  - IP-Adresse
  - User Agent
  - Version-Referenz
  - Optionaler Kommentar

Song-Status → "Approved"
Notification an Engineer
E-Mail-Bestätigung an Client (mit Zusammenfassung)

Pro/Studio: PDF-Approval-Dokument generieren
  - Projekt-Titel, Song-Titel
  - Freigegebene Version (Nr. + Timestamp des Uploads)
  - Datum und Uhrzeit der Freigabe
  - Name des Freigebenden
  - Revisionshistorie (alle Versionen + Kommentare)
```

---

## 9. Seiten & Views

### 9.1 Marketing / Public

```
mixnote.io/                → Landing Page (Pitch, Features, Pricing, CTA)
mixnote.io/pricing         → Pricing-Vergleich
mixnote.io/login           → Login-Formular
mixnote.io/register        → Registrierung
mixnote.io/s/{token}       → Client Share-View (öffentlich)
```

### 9.2 Engineer App (nach Login)

```
app.mixnote.io/                     → Dashboard (Projektübersicht, Notifications)
app.mixnote.io/projects             → Alle Projekte (Filter, Suche)
app.mixnote.io/projects/new         → Neues Projekt erstellen
app.mixnote.io/projects/{id}        → Projekt-Detail (Songs, Versionen, Kommentare)
app.mixnote.io/projects/{id}/share  → Share-Links verwalten
app.mixnote.io/settings             → Account-Einstellungen
app.mixnote.io/settings/branding    → Logo, Farben, Subdomain (Pro/Studio)
app.mixnote.io/settings/billing     → Plan, Stripe Portal
```

### 9.3 Client Share-View (kein Login)

```
mixnote.io/s/{token}                → Projekt mit allen Songs
  ├── Song-Liste (Titel, Status, letzte Version)
  ├── Audio-Player mit Waveform
  ├── Versions-Switcher (Dropdown)
  ├── Kommentar-Markers auf Waveform
  ├── Kommentar-Liste (chronologisch)
  ├── Kommentar-Input (Klick auf Waveform oder "General Comment")
  └── Approve-Button pro Song
```

---

## 10. UI/UX-Prinzipien

### Design-Philosophie
- **Dunkel, professionell, ruhig.** Kein buntes SaaS-Design. Audio-Profis arbeiten in dunklen Räumen.
- **Information Density.** Dashboard zeigt alles Relevante ohne Scrollen.
- **Zero Learning Curve für Clients.** Wenn ein Client eine Erklärung braucht, haben wir versagt.
- **Responsive, nicht Mobile-First.** Engineers arbeiten am Desktop. Clients reviewen oft am Handy.

### Client-View Regeln
- Kein sichtbares MixNote-Branding im Studio-Plan
- Maximale Schriftgrösse für Kommentar-Input
- Play-Button muss das grösste Element sein
- Waveform-Kommentare: farbliche Unterscheidung Engineer vs. Client
- Approved-Songs: grüner Haken, nicht mehr kommentierbar

### Dashboard Regeln
- Projekte sortiert nach: Ungelesene Kommentare → Wartet auf Feedback → Aktiv → Approved → Archiviert
- Badge-Counter für ungelesene Kommentare
- "Überfällig"-Markierung wenn Client seit >7 Tagen nicht reagiert hat
- Quick Actions: "Remind Client", "Upload New Version", "Archive"

---

## 11. E-Mail-Templates

### Transaktionale E-Mails (via Postmark)

1. **Welcome** — Nach Registrierung
2. **New Version Available** — An Client wenn Engineer neue Version hochlädt
3. **New Comment** — An Engineer wenn Client kommentiert
4. **Approval Confirmation** — An Client + Engineer nach Approval
5. **Nudge Reminder** — An Client: "Dein Feedback zu [Projekt] steht noch aus"
6. **Weekly Digest** (Studio-Plan) — An Engineer: Zusammenfassung der Woche

### E-Mail-Design
- Einfach, Text-lastig, kein Marketing-Look
- Studio-Branding (Logo + Farben) im Pro/Studio-Plan
- Direkter Link zum relevanten Projekt/Song
- Unsubscribe-Link

---

## 12. File Handling

### Upload-Prozess

```
Client (Browser)
  → Multipart POST an /api/songs/{id}/versions
  → Backend validiert:
     - Dateityp: WAV, FLAC, MP3, AAC, AIFF (kein Video, kein ZIP)
     - Dateigrösse: Max 500 MB pro File
     - Storage-Limit des Tenants prüfen
  → Datei wird nach S3/Backblaze gestreamt (nicht im RAM halten)
  → Waveform-Peaks werden berechnet (Background Job)
  → Audio-Metadaten extrahiert (Duration, Sample Rate, Bit Depth)
  → Version-Record in DB erstellt
  → Notification an Client (wenn Share-Link aktiv)
```

### Audio-Streaming

```
GET /s/{token}/songs/{song_id}/stream
  → Range-Header Support (Seeking)
  → Streaming direkt von S3 (Proxy oder Signed URL)
  → Optional: On-the-fly Transcoding zu MP3/AAC für Bandbreite
     (V1: nur Original-Format streamen, Transcoding in V2)
```

### Waveform-Generierung

```
Background Job nach Upload:
  → audiowaveform oder ffmpeg → JSON Peaks
  → Gespeichert in Version.waveform_data
  → Frontend nutzt Wavesurfer.js mit pre-computed Peaks
  → Kein Client-seitiges Decoding nötig → schneller Load
```

---

## 13. Notification-System

### Trigger-Events

| Event | Empfänger | Kanal | Timing |
|---|---|---|---|
| Neuer Kommentar (Client) | Engineer | In-App + E-Mail | Sofort |
| Neuer Kommentar (Engineer) | Client (wenn E-Mail bekannt) | E-Mail | Sofort |
| Neue Version hochgeladen | Client (wenn E-Mail bekannt) | E-Mail | Sofort |
| Song approved | Engineer | In-App + E-Mail | Sofort |
| Kein Feedback seit 7 Tagen | Engineer | In-App | Täglich um 09:00 |
| Auto-Nudge an Client | Client | E-Mail | Nach 7 Tagen ohne Feedback (einmalig) |
| Wöchentlicher Digest | Engineer (Studio-Plan) | E-Mail | Montag 09:00 |

### Implementation

- **In-App:** Notification-Tabelle + Polling (alle 30s) oder SSE
- **E-Mail:** Postmark API, Background Job Queue
- **Rate Limiting:** Max 1 E-Mail pro Projekt pro Stunde an Client (Batching)

---

## 14. Sicherheit

### Authentifizierung
- Passwort-Hashing: bcrypt (cost factor 12)
- JWT mit RS256 (asymmetrisch)
- CSRF-Schutz auf allen State-changing Endpoints
- Rate Limiting: 5 Login-Versuche pro Minute

### Share-Links
- Token: 12-Zeichen URL-safe Base64 (72 Bit Entropie)
- Optionaler Passwort-Schutz (bcrypt)
- Deaktivierbar und mit Ablaufdatum
- Kein Zugriff auf andere Projekte des Tenants

### Audio-Schutz
- Kein direkter Download-Link (Streaming only, ausser Engineer aktiviert Download)
- Signed URLs für S3 mit kurzer Gültigkeit (15 Minuten)
- Kein Rechtsklick-Download im Player (kein DRM, aber Hürde)

### Datenschutz
- EU-Hosting (Hetzner Nürnberg)
- Keine Tracking-Cookies für Clients
- Keine Weitergabe an Dritte
- GDPR-konform: Löschung auf Anfrage
- Self-Hosted Option für maximale Kontrolle

---

## 15. REAPER-Integration (Pro/Studio)

### Funktionsumfang V1

```lua
-- ReaImGui-basiertes Script
-- Kommuniziert mit MixNote API

Features:
1. Login mit API-Token
2. Projekt-Liste laden
3. Song auswählen → Kommentare laden
4. Kommentar-Liste mit Timestamps
5. Klick auf Kommentar → reaper.SetEditCurPos() + optional Play
6. Reply auf Kommentar direkt aus REAPER
7. Kommentar als "Resolved" markieren
8. Neue Version hochladen (Render-Dialog → Upload)
```

### API-Token
- Generiert in MixNote Settings
- Long-lived Token (kein JWT-Refresh nötig)
- Scope: Read/Write auf eigene Projekte
- Widerrufbar in Settings

---

## 16. Entwicklungs-Phasen

### Phase 0: Migration & Shared Core (Woche 1-2)

**Ziel:** Bestehenden MVP-Code auf produktionsreife Basis migrieren. Shared Core aufbauen.

- [ ] PostgreSQL aufsetzen, SQLite-Daten migrieren
- [ ] Shared Core Entities implementieren: Tenant, User, Contact, Event, Notification
- [ ] MixNote Entities implementieren: Project (mit contact_id FK), Song, Version, Comment, ShareLink, ApprovalRecord
- [ ] Alembic für DB-Migrations einrichten
- [ ] Event-Bus: Event-Tabelle + Worker-Registry + Basis-Handler (notification_handler, contact_activity_handler)
- [ ] Contact Auto-Creation: Bei neuem Projekt mit E-Mail → Contact lookup oder erstellen
- [ ] Docker Compose für Production (PostgreSQL, Redis, Caddy, FastAPI)
- [ ] Backblaze B2 Bucket einrichten, S3-kompatiblen Upload implementieren
- [ ] CI: Linting + Tests (pytest)
- [ ] Environment-Konfiguration (.env) für Dev/Staging/Prod
- [ ] Ordnerstruktur modular anlegen (siehe Anhang D)

### Phase 1: MixNote Core (Woche 3-6)

**Ziel:** Funktionierendes Produkt, das ein Engineer mit seinen Kunden nutzen kann.

- [ ] Auth-System (Register, Login, JWT, Password Reset)
- [ ] Contact CRUD (erstellen, suchen, Tags, Notizen)
- [ ] Projekt CRUD mit Contact-Verknüpfung und Status-Management
- [ ] Song CRUD mit Drag & Drop Reorder
- [ ] Version Upload mit Waveform-Generierung (Background Job)
- [ ] Audio-Streaming mit Range-Support
- [ ] Timestamped Comments (Engineer + Client)
- [ ] Comment Replies und Resolved-Status
- [ ] Share-Link erstellen/verwalten (mit optionalem Passwort)
- [ ] Client Share-View (komplett neues Frontend, zero-friction)
- [ ] Basic Approval (Button + Record + Event)
- [ ] Engineer Dashboard (Projektliste mit Status + Badges)
- [ ] Contact-Detail-Seite (Projekte + Activity Timeline aus Events)
- [ ] Event-Schreibung bei jeder relevanten Aktion (siehe Event-Typen in 6.4)
- [ ] In-App Notifications (generiert aus Events, Polling)
- [ ] E-Mail Notifications (Neuer Kommentar, Neue Version, Approval)

### Phase 2: SaaS Features (Woche 7-10)

**Ziel:** Zahlende Kunden onboarden.

- [ ] Multi-Tenant Middleware (Subdomain-Routing)
- [ ] Stripe Integration (Checkout, Webhooks, Customer Portal)
- [ ] Plan-Enforcement (Limits für Free/Pro/Studio)
- [ ] Branding-System (Logo-Upload, Farben, Subdomain)
- [ ] Approval PDF-Export (Pro/Studio)
- [ ] Auto-Nudge Notifications (7 Tage ohne Feedback)
- [ ] Weekly Digest E-Mail (Studio)
- [ ] Landing Page (mixnote.io)
- [ ] Onboarding-Flow (nach Registration)
- [ ] Settings-Seiten (Account, Branding, Billing)

### Phase 3: Differenzierung (Woche 11-14)

**Ziel:** Features die Mixup nicht hat.

- [ ] REAPER Script aktualisieren für neue API
- [ ] Version A/B-Vergleich im Client-View (Switch zwischen Versionen an gleicher Position)
- [ ] Activity Feed pro Projekt (Timeline aller Events)
- [ ] Projekt-Archivierung mit Retention
- [ ] API-Dokumentation (Studio-Plan)
- [ ] Self-Hosted Docker-Image publizieren
- [ ] Referenz-Upload (Client kann Referenz-Song hochladen)

### Phase 4: Launch & Growth (Woche 15+)

- [ ] Public Beta Launch
- [ ] Gearspace / Reddit / REAPER Forum Posts
- [ ] Feedback-Loop mit ersten Nutzern
- [ ] Performance-Optimierung basierend auf realer Nutzung
- [ ] SEO für Landing Page
- [ ] Dokumentation / Help Center

---

## 17. Was MixNote V1 bewusst NICHT kann

Diese Features sind explizit ausgeschlossen, um Scope Creep zu vermeiden:

- **Kein DAW-Plugin (AAX/AU/VST).** Zu komplex, zu fragil. REAPER-Script reicht.
- **Kein LUFS-Level-Matching.** Nice-to-have für V2.
- **Kein Dolby Atmos / Spatial Audio.** Nischenfeature.
- **Keine Mobile App.** Responsive Web reicht.
- **Kein Real-Time Collaboration.** Asynchrones Review ist der Use Case.
- **Kein Stem-Upload / Multitrack.** V1 = Stereo-Mixe.
- **Kein integrierter Messenger / Chat.** Kommentare pro Version reichen. → CRM-Modul (Phase 2)
- **Keine Rechnungsstellung / Invoicing.** → Books-Modul (Phase 3)
- **Kein Kalender / Session-Planung.** → Planner-Modul (Phase 4)
- **Keine Unified Inbox (E-Mail/WhatsApp).** → CRM-Modul (Phase 2)
- **Keine AI-Features.** Kein Auto-Transcribe, keine AI-Kommentar-Zusammenfassung. Vielleicht V2.
- **Kein OAuth / Social Login.** E-Mail + Passwort. Einfach. (V2: Google OAuth)

**Aber: Die Shared Core Architektur (Contact, Event-Bus) ist von Tag 1 bereit, diese Module aufzunehmen.**

---

## 18. Erfolgs-Metriken

### Product-Market Fit Indikatoren
- **Activation Rate:** >40% der Registrierungen erstellen mindestens 1 Projekt mit Share-Link
- **Retention:** >60% der Pro/Studio-Kunden nach 3 Monaten aktiv
- **NPS:** >50 (gemessen nach 30 Tagen Nutzung)

### Business-Metriken
- **MRR Milestone 1:** €1'000 (innerhalb 6 Monate nach Launch)
- **MRR Milestone 2:** €3'000 (innerhalb 12 Monate)
- **MRR Milestone 3:** €5'000 (innerhalb 18 Monate)
- **Churn Rate:** <5% monatlich
- **CAC:** <€50 (primär organisch/Community)

### Technical Health
- **Uptime:** >99.5%
- **Page Load (Client View):** <2 Sekunden
- **Audio Start (Time to First Byte):** <500ms
- **Upload-Fehlerrate:** <1%

---

## 19. Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|---|---|---|---|
| Mixup verbessert App/Support drastisch | Mittel | Hoch | Speed — vor ihnen launchen, Community aufbauen |
| Geringe Adoption (kein PMF) | Mittel | Hoch | Eigene Nutzung als Validation, frühe Beta-Tester |
| Storage-Kosten explodieren | Niedrig | Mittel | Backblaze B2 ist billig, Limits pro Plan |
| Sicherheitsvorfall (Datenleck) | Niedrig | Sehr Hoch | Security-First Architektur, Penetration Testing vor Launch |
| Token-Kosten für Claude Code zu hoch | Mittel | Mittel | Spec-First Ansatz (dieses Dokument), gezieltes Coden |
| Ein-Mann-Projekt = Single Point of Failure | Hoch | Mittel | Einfache Architektur, gute Dokumentation, Docker-basiert |

---

## 20. Glossar

| Begriff | Definition |
|---|---|
| **Tenant** | Ein registrierter Account (Studio/Engineer) mit eigenem Subdomain |
| **Project** | Ein Auftrag / Job mit einem oder mehreren Songs |
| **Song** | Ein einzelner Track innerhalb eines Projekts |
| **Version** | Eine spezifische Iteration eines Songs (V1, V2, V3...) |
| **Share-Link** | Öffentlicher URL der Kunden Zugang zum Projekt gibt |
| **Approval** | Formelle Freigabe einer Song-Version durch den Kunden |
| **Engineer** | Der Studio-Betreiber / MixNote-Nutzer (bezahlt) |
| **Client** | Der Kunde des Engineers (nutzt MixNote kostenlos via Share-Link) |
| **Nudge** | Automatische Erinnerung an Client bei ausstehendem Feedback |

---

## Anhang A: Umgebungsvariablen

```env
# App
APP_ENV=production
APP_SECRET_KEY=<random-64-char>
APP_BASE_URL=https://mixnote.io
APP_ALLOWED_ORIGINS=https://mixnote.io,https://*.mixnote.io

# Database
DATABASE_URL=postgresql://mixnote:password@db:5432/mixnote

# Redis (Background Jobs, Caching)
REDIS_URL=redis://redis:6379/0

# Storage (S3-kompatibel)
S3_ENDPOINT=https://s3.eu-central-003.backblazeb2.com
S3_BUCKET=mixnote-audio
S3_ACCESS_KEY=<key>
S3_SECRET_KEY=<secret>
S3_REGION=eu-central-003

# E-Mail
POSTMARK_API_TOKEN=<token>
EMAIL_FROM=notifications@mixnote.io

# Stripe
STRIPE_SECRET_KEY=<key>
STRIPE_WEBHOOK_SECRET=<secret>
STRIPE_PRICE_PRO_MONTHLY=price_xxx
STRIPE_PRICE_PRO_YEARLY=price_xxx
STRIPE_PRICE_STUDIO_MONTHLY=price_xxx
STRIPE_PRICE_STUDIO_YEARLY=price_xxx

# JWT
JWT_PRIVATE_KEY_PATH=/etc/mixnote/jwt_private.pem
JWT_PUBLIC_KEY_PATH=/etc/mixnote/jwt_public.pem
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Waveform Generation
AUDIOWAVEFORM_BIN=/usr/bin/audiowaveform

# Limits
MAX_UPLOAD_SIZE_MB=500
FREE_STORAGE_LIMIT_GB=2
PRO_STORAGE_LIMIT_GB=50
STUDIO_STORAGE_LIMIT_GB=200
FREE_MAX_ACTIVE_PROJECTS=3
FREE_MAX_SONGS=15
FREE_TRACK_EXPIRY_DAYS=15
```

---

## Anhang B: Docker Compose (Production)

```yaml
version: "3.8"

services:
  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: mixnote
      POSTGRES_USER: mixnote
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mixnote"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

  app:
    build: .
    restart: always
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    env_file: .env
    volumes:
      - uploads:/app/uploads  # Temporär, vor S3-Upload
    expose:
      - "8000"

  worker:
    build: .
    restart: always
    command: celery -A app.worker worker --loglevel=info
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    env_file: .env
    volumes:
      - uploads:/app/uploads

  beat:
    build: .
    restart: always
    command: celery -A app.worker beat --loglevel=info
    depends_on:
      redis:
        condition: service_started
    env_file: .env

  caddy:
    image: caddy:2-alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config

volumes:
  postgres_data:
  redis_data:
  uploads:
  caddy_data:
  caddy_config:
```

---

## Anhang C: Caddyfile

```caddyfile
# Main site
mixnote.io {
    reverse_proxy app:8000
}

# App subdomain
app.mixnote.io {
    reverse_proxy app:8000
}

# Wildcard für Tenant-Subdomains (Studio-Plan)
*.mixnote.io {
    reverse_proxy app:8000
}
```

---

*Ende der Spezifikation. Dieses Dokument wird im Repository unter `/docs/STUDIO_OS_SPEC.md` abgelegt und bei Bedarf aktualisiert.*

---

## Anhang D: Modulare Ordnerstruktur

```
studio-os/
├── docs/
│   └── STUDIO_OS_SPEC.md          ← dieses Dokument
│
├── core/                           ← Shared Core (gehört keinem Modul)
│   ├── models/
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   ├── event.py
│   │   └── notification.py
│   ├── auth/
│   │   ├── jwt.py
│   │   ├── middleware.py
│   │   └── routes.py
│   ├── events/
│   │   ├── bus.py                  ← Event-Schreibung + Registry
│   │   ├── handlers.py            ← Shared Handler (notification, contact_activity)
│   │   └── worker.py              ← Background Worker
│   ├── contacts/
│   │   ├── routes.py
│   │   ├── service.py             ← Matching-Logik, Auto-Creation
│   │   └── schemas.py
│   └── notifications/
│       ├── routes.py
│       ├── service.py
│       └── email.py               ← Postmark Integration
│
├── modules/
│   ├── mixnote/                    ← MixNote Modul
│   │   ├── models/
│   │   │   ├── project.py
│   │   │   ├── song.py
│   │   │   ├── version.py
│   │   │   ├── comment.py
│   │   │   ├── share_link.py
│   │   │   └── approval.py
│   │   ├── routes/
│   │   │   ├── projects.py
│   │   │   ├── songs.py
│   │   │   ├── versions.py
│   │   │   ├── comments.py
│   │   │   ├── share.py
│   │   │   └── public.py          ← Client Share-View API
│   │   ├── services/
│   │   │   ├── upload.py           ← S3 Upload + Waveform
│   │   │   ├── streaming.py       ← Audio-Streaming
│   │   │   ├── approval.py        ← Approval-Logik + PDF
│   │   │   └── dashboard.py       ← Dashboard-Aggregation
│   │   ├── events.py              ← MixNote-spezifische Event-Handler
│   │   └── schemas.py             ← Pydantic Models
│   │
│   ├── crm/                       ← CRM Modul (Phase 2 — Platzhalter)
│   │   └── README.md
│   │
│   ├── books/                     ← Books Modul (Phase 3 — Platzhalter)
│   │   └── README.md
│   │
│   └── planner/                   ← Planner Modul (Phase 4 — Platzhalter)
│       └── README.md
│
├── frontend/
│   ├── public/                    ← Client Share-View (vanilla JS)
│   ├── app/                       ← Engineer Dashboard (vanilla JS + Tailwind)
│   └── landing/                   ← Marketing Landing Page
│
├── reaper/
│   └── mixnote_comments.lua      ← REAPER Integration Script
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── Dockerfile
├── Caddyfile
├── alembic/                       ← DB Migrations
├── tests/
│   ├── core/
│   └── modules/
│       └── mixnote/
├── .env.example
└── README.md
```

**Regeln für die Ordnerstruktur:**
- `core/` importiert NIEMALS aus `modules/`
- `modules/mixnote/` importiert aus `core/`, niemals aus `modules/crm/` etc.
- Module kommunizieren ausschliesslich über Events
- Neue Module = neuer Ordner unter `modules/`, neue Event-Handler registrieren, fertig

---

## Anhang E: Zukünftige Module — Grob-Outline

> Diese Outlines dienen der Planung und beeinflussen das Shared Core Design.
> Detaillierte Specs werden erstellt wenn das jeweilige Modul in Entwicklung geht.

### E.1 Studio CRM (Phase 2 — ~Q3 2026)

**Zweck:** Alle Kommunikation mit Kunden an einem Ort.

**Kern-Features:**
- Unified Inbox: E-Mail (IMAP/SMTP), WhatsApp (whatsmeow), Signal, Telegram
- Nachrichten → automatisch dem Contact zugeordnet
- Contact-Profil: komplette Kommunikationshistorie über alle Kanäle
- Pipeline-View: Lead → Angebot → Buchung → Produktion → Abgeschlossen
- Follow-up Reminders basierend auf Inaktivität
- Website-Kontaktformular → direkt als Contact + Lead

**Shared Core Nutzung:**
- Contact-Tabelle: Ergänzt um Kommunikationskanal-Details
- Event-Bus: Schreibt `crm.email.received`, `crm.whatsapp.received` etc.
- Konsumiert MixNote-Events für Contact Activity Timeline

**Neue Entities (CRM-spezifisch):**
- Message (Kanal, Richtung, Content, Attachments)
- Channel (E-Mail-Account, WhatsApp-Session, etc.)
- Pipeline / PipelineStage
- Reminder

### E.2 Studio Books (Phase 3 — ~Q4 2026)

**Zweck:** Angebote, Rechnungen, Zahlungstracking. Schweizer KMU-tauglich.

**Kern-Features:**
- Angebots-Templates (pro Service-Typ: Recording, Mixing, Mastering)
- Angebot → Rechnung Konvertierung
- PDF-Export (Schweizer QR-Rechnung)
- Zahlungstracking (manuell, später TWINT/Stripe)
- Einfache Buchhaltung (Einnahmen/Ausgaben)
- Optional: Bitcoin-denominierte Ansicht (Kaufkraft-Tracking)

**Shared Core Nutzung:**
- Contact-Tabelle: Rechnungsadresse, Zahlungskonditionen
- Event-Bus: `books.invoice.sent`, `books.payment.received`
- Konsumiert MixNote-Events: "Projekt approved → Rechnung fällig?"

**Neue Entities (Books-spezifisch):**
- Quote (Angebot)
- Invoice (Rechnung)
- LineItem
- Payment
- Expense (für einfache Buchhaltung)

### E.3 Studio Planner (Phase 4 — ~2027)

**Zweck:** Session-Kalender, Raum-/Equipment-Planung, Kundenbuchung.

**Kern-Features:**
- Kalender-View (Tag/Woche/Monat)
- Session-Buchung mit Raum + Equipment
- Booking-Link für Kunden (Calendly-Alternative)
- Automatische Session-Prep Checkliste
- Erinnerungen an Kunden und Team

**Shared Core Nutzung:**
- Contact-Tabelle: Buchungshistorie
- Event-Bus: `planner.session.booked`, `planner.session.completed`
- Konsumiert CRM-Events: "Neuer Lead → Session-Vorschlag?"

**Neue Entities (Planner-spezifisch):**
- Session
- Room / Resource
- BookingLink
- Availability
