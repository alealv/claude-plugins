# Feature Specification: Voice Dictation Command

**Feature Branch**: `001-voice-dictation`
**Created**: 2026-02-13
**Status**: Draft
**Input**: User description: "Create a command that starts a process or connects to an ASR backend and transcribes everything said to the text input from Claude Code. Inspired by voicemode. No MCP, just direct transcription until Enter is pressed. Support multiple languages and model sizes via configuration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Voice Dictation (Priority: P1)

A developer working in Claude Code wants to dictate a prompt instead of typing it. They execute the `/dictate` command (or a configured hotkey/shortcut), start speaking naturally, and see their words appear as text in real-time. When they are satisfied with the transcription, they press Enter to submit the text as their prompt to Claude Code.

**Why this priority**: This is the core value proposition. Without basic voice-to-text working end-to-end, no other features matter. A developer who can speak a 200-word prompt in 30 seconds instead of typing it for 3 minutes gets immediate productivity gains.

**Independent Test**: Can be fully tested by executing the dictation command, speaking a sentence, and verifying the spoken text appears in the Claude Code input field ready for submission.

**Acceptance Scenarios**:

1. **Given** the user has a working microphone and a running ASR backend, **When** the user executes the dictation command, **Then** the system begins capturing audio from the microphone and transcribing speech in real-time.
2. **Given** the dictation session is active and the user is speaking, **When** the user speaks a sentence, **Then** the transcribed text appears progressively in the Claude Code text input area.
3. **Given** a dictation session is active, **When** the user presses Enter, **Then** the dictation session ends and the accumulated transcription is submitted as the user's prompt.
4. **Given** a dictation session is active, **When** the user presses Escape, **Then** the dictation session is cancelled and no text is submitted.

---

### User Story 2 - Language Selection (Priority: P2)

A multilingual developer wants to dictate prompts in a language other than English (e.g., Spanish, French, German). They configure their preferred language either via the command invocation or a persistent configuration, and the ASR system accurately transcribes speech in that language.

**Why this priority**: Many developers work in non-English contexts or prefer to express complex ideas in their native language. This significantly broadens the feature's audience without adding major complexity (most ASR engines already support multiple languages).

**Independent Test**: Can be tested by configuring the language to a non-English option, speaking a sentence in that language, and verifying correct transcription.

**Acceptance Scenarios**:

1. **Given** the user has configured the dictation language to Spanish, **When** the user speaks in Spanish, **Then** the system transcribes the speech accurately in Spanish.
2. **Given** no language is explicitly configured, **When** the user starts a dictation session, **Then** the system defaults to English or auto-detects the spoken language.
3. **Given** the user wants to change the language mid-session or for a single dictation, **When** they pass a language parameter to the command, **Then** that language is used for that session only.

---

### User Story 3 - Model Size Configuration (Priority: P3)

A developer with limited hardware resources wants to use a smaller, faster ASR model for acceptable accuracy, while another developer with a powerful machine wants the highest accuracy possible from a larger model. Both can configure the model size to fit their needs.

**Why this priority**: Different hardware capabilities and accuracy/latency trade-offs are important but secondary to the core dictation working. The default model should work well for most users; this story addresses optimization and customization.

**Independent Test**: Can be tested by configuring different model sizes, dictating the same phrase, and comparing transcription speed and accuracy.

**Acceptance Scenarios**:

1. **Given** the user has configured a "tiny" model, **When** they dictate a sentence, **Then** transcription completes faster (lower latency) with potentially lower accuracy.
2. **Given** the user has configured a "large" model, **When** they dictate a sentence, **Then** transcription is more accurate with potentially higher latency.
3. **Given** no model size is configured, **When** the user starts a dictation session, **Then** a sensible default model is used (balancing speed and accuracy for typical hardware).

---

### User Story 4 - Persistent Configuration (Priority: P4)

A developer wants to set their preferred language, model size, and other dictation preferences once and have them persist across sessions without needing to reconfigure each time.

**Why this priority**: Quality-of-life improvement that reduces friction for repeat users. Not essential for first-time or occasional use.

**Independent Test**: Can be tested by setting configuration values, restarting the tool, and verifying the configuration persists.

**Acceptance Scenarios**:

1. **Given** the user sets language to "fr" and model to "medium" in their configuration, **When** they start a new dictation session without parameters, **Then** the system uses French language and medium model.
2. **Given** the user has persistent configuration set, **When** they pass explicit parameters to the command, **Then** the command parameters override the persistent configuration for that session.

---

### Edge Cases

- What happens when no microphone is detected or accessible? The system should display a clear error message explaining the issue and how to fix it (e.g., check permissions, connect a microphone).
- What happens when the ASR backend is not running or unreachable? The system should display a clear error message with instructions on how to start the backend.
- What happens when the user speaks but there is too much background noise? The system should transcribe as best as possible; silence detection should still function to avoid hanging indefinitely.
- What happens when the user starts dictation but says nothing for an extended period? The system should remain in listening mode until the user explicitly ends the session (Enter or Escape), with no automatic timeout that could lose context.
- What happens when the user's audio hardware changes during a session (e.g., Bluetooth headset disconnects)? The system should handle audio device changes gracefully, either continuing with the new default device or notifying the user.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST capture audio from the user's default microphone when a dictation session starts.
- **FR-002**: The system MUST send captured audio to a local ASR backend for transcription (no cloud services required for basic functionality).
- **FR-003**: The system MUST display transcribed text progressively in the Claude Code input area as speech is recognized.
- **FR-004**: The system MUST end the dictation session and submit the transcribed text when the user presses Enter.
- **FR-005**: The system MUST cancel the dictation session and discard transcribed text when the user presses Escape.
- **FR-006**: The system MUST support configuring the transcription language, with English as the default.
- **FR-007**: The system MUST support configuring the ASR model size (e.g., tiny, base, small, medium, large).
- **FR-008**: The system MUST work without any MCP server integration, operating as a direct command.
- **FR-009**: The system MUST provide clear error messages when the microphone is unavailable or the ASR backend is unreachable.
- **FR-010**: The system MUST allow configuration to persist across sessions via a configuration file.
- **FR-011**: The system MUST allow command-line parameters to override persistent configuration for a single session.
- **FR-012**: The system MUST connect to an existing local ASR backend (e.g., a Whisper-compatible server) rather than bundling its own model inference. The user is responsible for running the ASR backend separately.

### Key Entities

- **Dictation Session**: A single voice input episode from start (command execution) to end (Enter/Escape). Attributes: start time, accumulated transcription text, language, model, status (active/completed/cancelled).
- **ASR Backend Connection**: The connection to the speech recognition service. Attributes: endpoint address, model identifier, language setting, connection status.
- **Dictation Configuration**: User preferences for dictation behavior. Attributes: default language, default model size, ASR backend address, audio input device.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete a voice dictation session (start speaking, see transcription, submit) in a single uninterrupted flow without needing to switch windows or applications.
- **SC-002**: Transcribed text appears within 2 seconds of the user finishing a spoken phrase, providing near-real-time feedback.
- **SC-003**: Users can dictate a 100-word prompt at least 2x faster than typing the same prompt, measured by time from command execution to text submission.
- **SC-004**: The system correctly transcribes at least 9 out of 10 common English sentences spoken clearly in a quiet environment.
- **SC-005**: Users can switch between at least 5 languages without restarting or reinstalling the tool.
- **SC-006**: First-time setup (from command execution to first successful transcription) takes less than 5 minutes, including any required ASR backend configuration.

## Assumptions

- The user has a working microphone connected to their machine with appropriate OS-level permissions granted.
- A local ASR backend (such as a Whisper-compatible server) is available or can be started by the user. The dictation command connects to this service rather than embedding model inference directly.
- The user's machine has sufficient resources to run the chosen ASR model (smaller models for resource-constrained machines).
- The command operates within the Claude Code CLI environment and injects text into the active input field.
- Audio processing and transcription happen locally on the user's machine; no audio data is sent to external cloud services.
- The voicemode installation at `~/.voicemode` provides a reference architecture for audio capture and ASR backend communication patterns.

## Prior Art & Inspiration

- **VoiceMode** (`~/.voicemode`): Existing MCP-based voice integration for Claude Code. Uses local Whisper STT via OpenAI-compatible `/v1/audio/transcriptions` endpoint. Handles audio capture, VAD (Voice Activity Detection), and transcription. This feature takes inspiration from its architecture but operates as a direct command without MCP.
- **Claude STT** (`jarrodwatts/claude-stt`): Plugin that uses Moonshine ONNX model locally (~400ms transcription). Supports toggle and push-to-talk modes. Injects text via keyboard simulation or clipboard. Cross-platform (macOS, Linux, Windows).
- **listen-claude-code** (`gmoqa/listen-claude-code`): MCP server wrapping a `listen` CLI tool with Whisper. Supports 9 languages. Uses Ctrl+C to stop recording.
- **stt-mcp-server-linux**: Push-to-talk using Right Ctrl key. Injects transcribed text via tmux `send-keys`. Docker-based. Whisper tiny model default.
- **whisper.cpp `stream`**: Native C++ real-time streaming transcription tool. Samples audio every half second. Supports all Whisper model sizes. Can be used as a backend.
- **Superwhisper / MacWhisper**: macOS native dictation apps using Whisper locally. System-level dictation that works across all apps including terminals. Demonstrate that local Whisper-based dictation is viable and performant on consumer hardware.
