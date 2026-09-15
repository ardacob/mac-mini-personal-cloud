# Contributing

This guide grew out of a real-world setup and troubleshooting process. Contributions are very welcome.

- Clearly describe any hardware, macOS, Docker, File Browser, Tailscale, or NAStool differences that may affect the result.
- Do not submit passwords, API keys, real Tailscale IP addresses, private network details, or personal screenshots containing sensitive information.
- For troubleshooting contributions, prefer the format: **symptom → test → finding → solution**.
- For HEIC-related issues, include the File Browser version, FFmpeg version, and the HTTP status returned by the preview endpoint whenever possible.
- Keep fixes reproducible: include the exact command, configuration change, or log line that confirmed the solution.
- Avoid destructive steps unless they are clearly marked and include a backup or rollback note.
- Submit major behavior changes as a separate pull request so they can be reviewed independently.

## Pull requests

Before opening a pull request:

1. Make sure no secrets, personal files, or private addresses are included.
2. Keep the change focused on one problem or improvement.
3. Update the relevant documentation if the setup steps or expected behavior change.
4. Test commands and configuration examples when possible.
5. Explain what was changed, why it was changed, and how it was verified.

Thanks for helping make the guide more accurate and useful for other Mac mini and self-hosting users.
