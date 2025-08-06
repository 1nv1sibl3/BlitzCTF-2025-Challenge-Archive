import os
import asyncio
import discord

from discord.ext import commands
from discord import app_commands, File, Interaction

from lib import payload_utils 
from config import PAYLOADS_DIR, PAYLOADS_VIEW

async def query1_autocomplete(interaction: Interaction, current: str):
    return await payload_utils.autocomplete_payload(interaction, current, PAYLOADS_DIR)

async def type_autocomplete(interaction: Interaction, current: str):
    return await payload_utils.autocomplete_type(interaction, current)

def is_safe_path(base_dir, requested_file):
    """
    Validate that the requested file is within the allowed directory.
    Prevents directory traversal attacks.
    """
    # Remove any path separators and normalize the filename
    safe_filename = os.path.basename(requested_file)
    
    # Check for suspicious patterns
    if '..' in requested_file or '/' in requested_file or '\\' in requested_file:
        return False, None
    
    # Construct the full path
    full_path = os.path.join(base_dir, safe_filename)
    
    # Get the real paths (resolves symlinks and normalizes)
    try:
        real_base = os.path.realpath(base_dir)
        real_full = os.path.realpath(full_path)
        
        # Check if the resolved path is within the base directory
        if not real_full.startswith(real_base + os.sep) and real_full != real_base:
            return False, None
            
        return True, full_path
    except (OSError, ValueError):
        return False, None

class Payload(app_commands.Command):
    def __init__(self):
        @app_commands.describe(
            query1="Main topic (e.g. SQL, XSS, SSTI)",
            query2="Optional keyword (e.g. SELECT, alert)",
            type="payload (default), file, or intruder"
        )
        @app_commands.autocomplete(
            query1=query1_autocomplete,
            type=type_autocomplete
        )
        async def callback(
            interaction: Interaction,
            query1: str,
            query2: str = "",
            type: str = "payload"
        ):
            # Check if query contains "flag" - if so, defer ephemerally and use DMs
            use_dm = "flag" in query1.lower() or "flag" in query2.lower()
            
            if use_dm:
                await interaction.response.defer(ephemeral=True)
            else:
                await interaction.response.defer()

            matched_dirs = []
            for root, _, files in os.walk(PAYLOADS_DIR):
                for file in files:
                    if file.endswith(".md") and query1.lower() in root.lower():
                        matched_dirs.append(os.path.dirname(os.path.join(root, file)))
                        break

            if not matched_dirs:
                if use_dm:
                    try:
                        dm_channel = await interaction.user.create_dm()
                        await dm_channel.send(f"❌ No topic found matching `{query1}`.")
                        await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                    except Exception:
                        await interaction.followup.send(f"❌ No topic found matching `{query1}`. (Failed to send DM)", ephemeral=True)
                else:
                    await interaction.followup.send(f"❌ No topic found matching `{query1}`.")
                return

            base_dir = matched_dirs[0]

            if type.lower() == "file":
                files_dir = os.path.join(base_dir, "Files")
                if not os.path.isdir(files_dir):
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("❌ No `Files` directory found for this topic.")
                            await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ No `Files` directory found for this topic. (Failed to send DM)", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ No `Files` directory found for this topic.")
                    return

                all_files = os.listdir(files_dir)
                if query2:
                    all_files = [f for f in all_files if query2.lower() in f.lower()]
                if not all_files:
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("❌ No matching files found.")
                            await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ No matching files found. (Failed to send DM)", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ No matching files found.")
                    return

                header = f"🔍 Available Files in `{query1}` Insecure Files"
                
                file_list = []
                for f in all_files:
                    if f.endswith(('.jpg', '.png', '.gif', '.jpeg')):
                        icon = "🖼️"
                    elif f.endswith(('.py', '.pyc', '.pyw', '.pyx')):
                        icon = "📄"
                    elif f.endswith(('.html', '.htm')):
                        icon = "📄"
                    elif f.endswith(('.php', '.php3', '.php5')):
                        icon = "📄"
                    elif f.endswith('.zip'):
                        icon = "📦"
                    elif f == ".htaccess":
                        icon = "⚙️"
                    else:
                        icon = "📄"
                    
                    file_list.append(f"{icon} `{f}`")
                
                chunks = []
                current_chunk = [header]
                current_length = len(header)
                
                for file_entry in file_list:
                    if current_length + len(file_entry) + 2 > 1900: 
                        chunks.append("\n".join(current_chunk))
                        current_chunk = [f"🔍 Available Files in `{query1}` (continued)"]
                        current_length = len(current_chunk[0])
                    
                    current_chunk.append(file_entry)
                    current_length += len(file_entry) + 1 
                
                if current_chunk:
                    chunks.append("\n".join(current_chunk))

                for i, chunk in enumerate(chunks):
                    if i == len(chunks) - 1:
                        chunk += "\n\n📩 Reply with the filename to receive the file."
                    
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send(chunk)
                            if i == 0:  # Only send this message once
                                await interaction.followup.send("📩 Check your DMs for the file list.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ Failed to send DM. File list sent here instead:")
                            await interaction.followup.send(chunk)
                    else:
                        await interaction.followup.send(chunk)

                def check(m):
                    if use_dm:
                        return m.author.id == interaction.user.id and isinstance(m.channel, discord.DMChannel)
                    else:
                        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    response = await interaction.client.wait_for("message", timeout=60, check=check)
                    requested_file = response.content.strip()
                    
                    # SECURITY FIX: Validate the file path
                    is_safe, safe_file_path = is_safe_path(files_dir, requested_file)
                    
                    if not is_safe:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ Invalid file path. Only files within the current directory are allowed.")
                            except Exception:
                                await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.")
                        return
                    
                    # Additional check: ensure the file exists in the allowed list
                    if requested_file not in all_files:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ File not found in the available files list.")
                            except Exception:
                                await interaction.followup.send("❌ File not found in the available files list.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ File not found in the available files list.")
                        return
                    
                    if requested_file == "flag" or use_dm:
                        open_dm = await interaction.user.create_dm()
                        await open_dm.send(f"Here is your file `{requested_file}`:", file=File(safe_file_path))
                    elif os.path.isfile(safe_file_path):
                        await interaction.followup.send(f"Here is your file `{requested_file}`:", file=File(safe_file_path))
                    else:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ File not found.")
                            except Exception:
                                await interaction.followup.send("❌ File not found.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ File not found.")
                except asyncio.TimeoutError:
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("⌛ Timeout. You didn't reply in time.")
                        except Exception:
                            await interaction.followup.send("⌛ Timeout. You didn't reply in time.", ephemeral=True)
                    else:
                        await interaction.followup.send("⌛ Timeout. You didn't reply in time.")
                return

            if type.lower() == "intruder":
                intruder_dir = os.path.join(base_dir, "Intruders")
                if not os.path.isdir(intruder_dir):
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("❌ No `Intruder` directory found.")
                            await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ No `Intruder` directory found. (Failed to send DM)", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ No `Intruder` directory found.")
                    return

                if query2:
                    matched_files = await payload_utils.search_intruder_content(intruder_dir, query2)
                    if not matched_files:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ No matching intruder content found.")
                                await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                            except Exception:
                                await interaction.followup.send("❌ No matching intruder content found. (Failed to send DM)", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ No matching intruder content found.")
                        return
                    
                    intruder_list = "\n".join(f"🎯 `{f}`" for f in matched_files)
                    message_content = f"**Intruder Payloads in `{query1}` with `{query2}` text in it:**\n{intruder_list}\n\n📩 Reply with the filename to get it."
                    
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send(message_content)
                            await interaction.followup.send("📩 Check your DMs for the intruder list.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ Failed to send DM. Intruder list sent here instead:")
                            await interaction.followup.send(message_content)
                    else:
                        await interaction.followup.send(message_content)
                    def check(m):
                        if use_dm:
                            return m.author.id == interaction.user.id and isinstance(m.channel, discord.DMChannel)
                        else:
                            return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                    try:
                        response = await interaction.client.wait_for("message", timeout=60, check=check)
                        requested_file = response.content.strip()
                        
                        # SECURITY FIX: Validate the file path
                        is_safe, safe_file_path = is_safe_path(intruder_dir, requested_file)
                        
                        if not is_safe:
                            if use_dm:
                                try:
                                    dm_channel = await interaction.user.create_dm()
                                    await dm_channel.send("❌ Invalid file path. Only files within the current directory are allowed.")
                                except Exception:
                                    await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.", ephemeral=True)
                            else:
                                await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.")
                            return
                        
                        # Additional check: ensure the file exists in the matched files list
                        if requested_file not in matched_files:
                            if use_dm:
                                try:
                                    dm_channel = await interaction.user.create_dm()
                                    await dm_channel.send("❌ File not found in the available files list.")
                                except Exception:
                                    await interaction.followup.send("❌ File not found in the available files list.", ephemeral=True)
                            else:
                                await interaction.followup.send("❌ File not found in the available files list.")
                            return
                        
                        if os.path.isfile(safe_file_path):
                            if use_dm:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send(f"Here's your intruder file `{requested_file}`:", file=File(safe_file_path))
                            else:
                                await interaction.followup.send(f"Here's your intruder file `{requested_file}`:", file=File(safe_file_path))
                        else:
                            if use_dm:
                                try:
                                    dm_channel = await interaction.user.create_dm()
                                    await dm_channel.send("❌ File not found.")
                                except Exception:
                                    await interaction.followup.send("❌ File not found.", ephemeral=True)
                            else:
                                await interaction.followup.send("❌ File not found.")
                    except asyncio.TimeoutError:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("⌛ Timeout. You didn't reply in time.")
                            except Exception:
                                await interaction.followup.send("⌛ Timeout. You didn't reply in time.", ephemeral=True)
                        else:
                            await interaction.followup.send("⌛ Timeout. You didn't reply in time.")
                    return                    

                intruder_files = os.listdir(intruder_dir)
                if not intruder_files:
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("❌ No intruder files found.")
                            await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                        except Exception:
                            await interaction.followup.send("❌ No intruder files found. (Failed to send DM)", ephemeral=True)
                    else:
                        await interaction.followup.send("❌ No intruder files found.")
                    return

                intruder_list = "\n".join(f"🎯 `{f}`" for f in intruder_files)
                message_content = f"**Intruder Payloads in `{query1}`**\n{intruder_list}\n\n📩 Reply with the filename to get it."
                
                if use_dm:
                    try:
                        dm_channel = await interaction.user.create_dm()
                        msg = await dm_channel.send(message_content)
                        await interaction.followup.send("📩 Check your DMs for the intruder list.", ephemeral=True)
                    except Exception:
                        await interaction.followup.send("❌ Failed to send DM. Intruder list sent here instead:")
                        msg = await interaction.followup.send(message_content)
                else:
                    msg = await interaction.followup.send(message_content)

                def check(m):
                    if use_dm:
                        return m.author.id == interaction.user.id and isinstance(m.channel, discord.DMChannel)
                    else:
                        return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    response = await interaction.client.wait_for("message", timeout=60, check=check)
                    requested_file = response.content.strip()
                    
                    # SECURITY FIX: Validate the file path
                    is_safe, safe_file_path = is_safe_path(intruder_dir, requested_file)
                    
                    if not is_safe:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ Invalid file path. Only files within the current directory are allowed.")
                            except Exception:
                                await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ Invalid file path. Only files within the current directory are allowed.")
                        return
                    
                    # Additional check: ensure the file exists in the intruder files list
                    if requested_file not in intruder_files:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ File not found in the available files list.")
                            except Exception:
                                await interaction.followup.send("❌ File not found in the available files list.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ File not found in the available files list.")
                        return
                    
                    if os.path.isfile(safe_file_path):
                        if use_dm:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send(f"Here's your intruder file `{requested_file}`:", file=File(safe_file_path))
                        else:
                            await interaction.followup.send(f"Here's your intruder file `{requested_file}`:", file=File(safe_file_path))
                    else:
                        if use_dm:
                            try:
                                dm_channel = await interaction.user.create_dm()
                                await dm_channel.send("❌ File not found.")
                            except Exception:
                                await interaction.followup.send("❌ File not found.", ephemeral=True)
                        else:
                            await interaction.followup.send("❌ File not found.")
                except asyncio.TimeoutError:
                    if use_dm:
                        try:
                            dm_channel = await interaction.user.create_dm()
                            await dm_channel.send("⌛ Timeout. You didn't reply in time.")
                        except Exception:
                            await interaction.followup.send("⌛ Timeout. You didn't reply in time.", ephemeral=True)
                    else:
                        await interaction.followup.send("⌛ Timeout. You didn't reply in time.")
                return

            # Default: payload
            all_payloads = []
            for root, _, files in os.walk(base_dir):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        payloads = await payload_utils.extract_payloads_from_file(file_path)
                        if query2:
                            payloads = [p for p in payloads if query2.lower() in p.lower()]
                        all_payloads.extend(payloads)

            if not all_payloads:
                if use_dm:
                    try:
                        dm_channel = await interaction.user.create_dm()
                        await dm_channel.send("❌ No matching payloads found.")
                        await interaction.followup.send("📩 Check your DMs for the response.", ephemeral=True)
                    except Exception:
                        await interaction.followup.send("❌ No matching payloads found. (Failed to send DM)", ephemeral=True)
                else:
                    await interaction.followup.send("❌ No matching payloads found.")
                return

            full_payload = "\n\n".join(all_payloads)

            if use_dm:
                try:
                    dm_channel = await interaction.user.create_dm()
                    await interaction.followup.send("📩 Check your DMs for the payload results.", ephemeral=True)
                    
                    # Send payload results via DM using the same view modes
                    if PAYLOADS_VIEW == "page":
                        await payload_utils.send_paginated_dm(dm_channel, full_payload)
                    elif PAYLOADS_VIEW == "msg":
                        await payload_utils.send_long_message_dm(dm_channel, full_payload)
                    elif PAYLOADS_VIEW == "txt":
                        await payload_utils.send_as_txt_file_dm(dm_channel, full_payload)
                    else:
                        await payload_utils.ask_user_view_mode_dm(dm_channel, full_payload)
                except Exception:
                    await interaction.followup.send("❌ Failed to send DM. Payload results sent here instead:", ephemeral=True)
                    # Fallback to normal channel
                    if PAYLOADS_VIEW == "page":
                        await payload_utils.send_paginated(interaction, full_payload)
                    elif PAYLOADS_VIEW == "msg":
                        await payload_utils.send_long_message(interaction.followup, full_payload)
                    elif PAYLOADS_VIEW == "txt":
                        await payload_utils.send_as_txt_file(interaction, full_payload)
                    else:
                        await payload_utils.ask_user_view_mode(interaction, full_payload)
            else:
                if PAYLOADS_VIEW == "page":
                    await payload_utils.send_paginated(interaction, full_payload)
                elif PAYLOADS_VIEW == "msg":
                    await payload_utils.send_long_message(interaction.followup, full_payload)
                elif PAYLOADS_VIEW == "txt":
                    await payload_utils.send_as_txt_file(interaction, full_payload)
                else:
                    await payload_utils.ask_user_view_mode(interaction, full_payload)

        super().__init__(
            name="payload",
            description="Search payloads, files, or intruder wordlists from PayloadsAllTheThings.",
            callback=callback,
        )