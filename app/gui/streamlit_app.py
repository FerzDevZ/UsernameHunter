import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import json
from pathlib import Path
from search.search import check_username, filter_results, get_stats_from_results
from platforms import SOCIAL_PLATFORMS
from validation.validation import is_valid_username
from exporter.exporter import export_results
import time
from io import BytesIO
import random
import string

st.set_page_config(page_title="UsernameHunter GUI", layout="wide")

# Sidebar: Language, About, Tips, FAQ
lang = st.sidebar.selectbox("Language / Bahasa", ["id", "en"], index=0)
if lang == "en":
    st.sidebar.title("About UsernameHunter")
    st.sidebar.info("""
    Powerful username checker for 200+ social media & viral sites.\
    - Multi-platform, multi-username, export, stats, chart, plugins, proxy, and more!\
    - For advanced features, use CLI.
    """)
    st.sidebar.markdown("**Tips:** Use config, proxy, and plugins for automation.")
    st.sidebar.markdown("**FAQ:** See README.md for more.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Source:** [FerzDevZ on GitHub](https://github.com/FerzDevZ/UsernameHunter)")
    st.sidebar.markdown("**Community:** [ferztap Community](https://github.com/ferztap)")
else:
    st.sidebar.title("Tentang UsernameHunter")
    st.sidebar.info("""
    Tools cek username di ratusan platform sosial media & viral.\
    - Multi-platform, multi-username, export, statistik, chart, plugin, proxy, dan banyak lagi!\
    - Untuk fitur lanjutan, gunakan CLI.
    """)
    st.sidebar.markdown("**Tips:** Gunakan config, proxy, dan plugin untuk otomasi.")
    st.sidebar.markdown("**FAQ:** Lihat README.md untuk info lebih lanjut.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Sumber:** [FerzDevZ di GitHub](https://github.com/FerzDevZ/UsernameHunter)")
    st.sidebar.markdown("**Komunitas:** [ferztap Community](https://github.com/ferztap)")

st.title("🔎 UsernameHunter - Social Media Username Checker (GUI)")

# Username generator function
def generate_usernames(n=5, length=8):
    return [
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        for _ in range(n)
    ]

# Tabs for Results, History, Stats, FAQ/Tips
main_tabs = st.tabs([
    "🔍 Hasil/Results", "🕑 Riwayat/History", "📊 Statistik/Stats", "❓ FAQ/Tips"
])

with main_tabs[0]:
    # Input username manual atau upload file
    usernames = st.text_area(
        "Masukkan username (satu per baris):" if lang=="id" else "Enter usernames (one per line):", height=120)
    usernames = [u.strip() for u in usernames.splitlines() if u.strip()]

    # Username generator
    if st.button("Generate Random Usernames" if lang=="en" else "Buat Username Acak"):
        gen_names = generate_usernames()
        st.write(", ".join(gen_names))
        if st.button("Add to Input"):
            usernames += gen_names
            usernames = list(set(usernames))

    uploaded_file = st.file_uploader("Atau upload file username (.txt):" if lang=="id" else "Or upload username file (.txt):", type=["txt"])
    if uploaded_file:
        file_usernames = [u.strip() for u in uploaded_file.read().decode("utf-8").splitlines() if u.strip()]
        usernames += file_usernames
        usernames = list(set(usernames))

    # Pilih platform
    platforms = list(SOCIAL_PLATFORMS.keys())
    selected_platforms = st.multiselect(
        "Pilih platform (kosongkan untuk semua):" if lang=="id" else "Select platforms (empty for all):",
        platforms, default=platforms[:10])

    # Advanced options
    with st.expander("Advanced Options"):
        timeout = st.number_input("Timeout (detik):" if lang=="id" else "Timeout (seconds):", min_value=1, max_value=60, value=5)
        max_workers = st.number_input("Jumlah thread paralel:" if lang=="id" else "Number of parallel threads:", min_value=1, max_value=100, value=20)
        filter_mode = st.radio("Filter hasil:" if lang=="id" else "Result filter:", ["all", "only_found", "only_not_found", "show_failed"], index=0)
        output_format = st.selectbox("Format export hasil:", ["json", "csv", "txt", "md", "html", "pdf"], index=0)
        # Proxy, custom platforms, plugin dir (upload path/file)
        proxy_file = st.file_uploader("Proxy file (.txt):", type=["txt"])
        custom_platforms = st.file_uploader("Custom platforms (.json):", type=["json"])
        # Plugin dir: input path (manual)
        plugin_dir = st.text_input("Plugin directory (optional):", "")

    # Jalankan pencarian
    if st.button("Cek Username" if lang=="id" else "Check Username") and usernames:
        start_time = time.time()
        st.info("Memulai pencarian... Mohon tunggu." if lang=="id" else "Searching... Please wait.")
        # Simpan proxy/temp file jika diupload
        proxy_path = None
        if proxy_file:
            proxy_path = "proxy_gui.txt"
            with open(proxy_path, "w", encoding="utf-8") as f:
                f.write(proxy_file.read().decode("utf-8"))
        custom_path = None
        if custom_platforms:
            custom_path = "custom_gui.json"
            with open(custom_path, "w", encoding="utf-8") as f:
                f.write(custom_platforms.read().decode("utf-8"))
        # Build platform dict
        from platforms import SOCIAL_PLATFORMS
        platforms_dict = SOCIAL_PLATFORMS.copy()
        if custom_path:
            from plugins_mod.plugins import load_custom_platforms
            platforms_dict.update(load_custom_platforms(custom_path))
        if plugin_dir:
            from plugins_mod.plugins import load_plugin_platforms
            platforms_dict.update(load_plugin_platforms(plugin_dir))
        if selected_platforms:
            platforms_dict = {k: v for k, v in platforms_dict.items() if k in selected_platforms}
        # Run search
        results_all = {}
        for username in usernames:
            valid, reason = is_valid_username(username)
            if not valid:
                st.warning(f"Username '{username}' tidak valid: {reason}" if lang=="id" else f"Username '{username}' is invalid: {reason}")
                continue
            results = check_username(
                username,
                max_workers=max_workers,
                timeout=timeout,
                progress=False,
                proxies=proxy_path,
                platforms=platforms_dict
            )
            filtered = filter_results(
                results,
                only_found=(filter_mode=="only_found"),
                only_not_found=(filter_mode=="only_not_found"),
                only_failed=(filter_mode=="show_failed")
            )
            results_all[username] = filtered
            st.subheader(f"Hasil untuk: {username}" if lang=="id" else f"Results for: {username}")
            for platform, info in filtered.items():
                status = ("Terdaftar" if info['exists'] else ("Tidak Terdaftar" if info['exists'] is False else "Tidak Diketahui")) if lang=="id" else ("Found" if info['exists'] else ("Not Found" if info['exists'] is False else "Unknown"))
                color = "green" if info['exists'] else ("red" if info['exists'] is False else "orange")
                badge = f"<span style='background-color:{color};color:white;padding:2px 8px;border-radius:8px;font-size:90%'>{status}</span>"
                st.markdown(f"**[{platform}]** {badge}  ", unsafe_allow_html=True)
                st.markdown(f"[🔗 {info['url']}]({info['url']})", unsafe_allow_html=True)
                if 'error' in info:
                    st.error(f"Error: {info['error']}")
        if results_all:
            st.success("Pencarian selesai!" if lang=="id" else "Search finished!")
            exec_time = time.time() - start_time
            st.info(f"Waktu eksekusi: {exec_time:.2f} detik" if lang=="id" else f"Execution time: {exec_time:.2f} seconds")
            # Export hasil
            out_path = f"hasil_gui.{output_format}"
            export_results(results_all, out_path)
            with open(out_path, "rb") as f:
                st.download_button(f"Download hasil_gui.{output_format}", f, file_name=f"hasil_gui.{output_format}")
            # Preview hasil export (JSON/CSV/TXT/MD/HTML)
            if output_format in ["json", "txt", "md", "html"]:
                with open(out_path, "r", encoding="utf-8") as f:
                    st.code(f.read(), language=output_format)
            # Statistik
            stats = get_stats_from_results({u: r for u, r in results_all.items()})
            st.write("## Statistik Ringkasan" if lang=="id" else "## Stats Summary")
            st.json(stats)
            # Chart Pie & Bar
            try:
                import matplotlib.pyplot as plt
                import matplotlib
                matplotlib.use('Agg')
                labels = [k for k in stats.keys() if isinstance(stats[k], int)]
                values = [stats[k] for k in labels]
                fig, ax = plt.subplots(1,2,figsize=(10,4))
                ax[0].pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
                ax[0].set_title('Pie')
                ax[1].bar(labels, values, color=['#4caf50','#ffeb3b','#f44336'])
                ax[1].set_title('Bar')
                st.pyplot(fig)
                buf = BytesIO()
                fig.savefig(buf, format="png")
                st.download_button("Download Chart PNG", buf.getvalue(), file_name="hasil_chart.png", mime="image/png")
            except Exception as e:
                st.warning(f"Chart error: {e}")
            st.balloons()
    else:
        st.info("Masukkan username dan klik 'Cek Username'." if lang=="id" else "Enter username(s) and click 'Check Username'.")

# Tombol reset
if st.button("Reset Form" if lang=="id" else "Reset Form"):
    st.experimental_rerun()

with main_tabs[1]:
    # History (riwayat)
    history_path = Path("history.jsonl")
    if history_path.exists():
        lines = history_path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines[-10:]):
            entry = json.loads(line)
            st.write(f"{i+1}. {entry.get('results', {})}")
        st.download_button("Download history.jsonl", history_path.read_bytes(), file_name="history.jsonl")
    else:
        st.info("Belum ada riwayat." if lang=="id" else "No history yet.")

with main_tabs[2]:
    st.info("Statistik akan muncul setelah pencarian." if lang=="id" else "Stats will appear after search.")

with main_tabs[3]:
    st.markdown("""
    **FAQ & Tips**
    - Gunakan proxy untuk menghindari limit.
    - Gunakan plugin untuk platform custom.
    - Export hasil ke berbagai format.
    - Gunakan CLI untuk fitur lanjutan.
    - Lihat README.md untuk info lengkap.
    """ if lang=="id" else """
    **FAQ & Tips**
    - Use proxy to avoid rate limits.
    - Use plugins for custom platforms.
    - Export results to various formats.
    - Use CLI for advanced features.
    - See README.md for full info.
    """)

# Add dark mode toggle in sidebar
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False
if st.sidebar.checkbox('🌙 Dark Mode', value=st.session_state['dark_mode']):
    st.session_state['dark_mode'] = True
    st.markdown(
        '<style>body { background-color: #222; color: #eee; } .stApp { background-color: #222; }</style>',
        unsafe_allow_html=True)
else:
    st.session_state['dark_mode'] = False

# Monitor/auto-refresh option
monitor = st.sidebar.checkbox('🔄 Monitor/Auto-refresh', value=False)
interval = st.sidebar.number_input('Interval (detik)', min_value=5, max_value=3600, value=30) if monitor else None

if monitor and usernames:
    import time
    st.info('Monitoring aktif. Pencarian akan di-refresh otomatis.')
    while True:
        # ...existing code for search and display...
        st.info(f'Refresh dalam {interval} detik...')
        time.sleep(interval)
        st.experimental_rerun()

st.caption("UsernameHunter GUI - Powered by Streamlit | For full features, use CLI mode.")
