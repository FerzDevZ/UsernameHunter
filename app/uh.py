import argparse
from platforms import SOCIAL_PLATFORMS
from proxy.proxy import get_proxy_list
from validation.validation import is_valid_username
from plugins_mod.plugins import load_custom_platforms, load_plugin_platforms
from exporter.exporter import export_results
from search.search import check_username, filter_results, print_history, save_history, get_stats_from_results, print_stats_summary
from tqdm import tqdm
import os
import json
from pathlib import Path
try:
    import yaml
except ImportError:
    yaml = None
import webbrowser
try:
    import pyperclip
except ImportError:
    pyperclip = None

AUTHORS = [
    "Owner: @FerzDevZ",
    "Contributors:",
    "  - @callysta-cloud",
    "  - @ChristianAngelo1",
    "  - @EnnVyy7",
    "  - @HoseajsJ",
    "  - @JusdyParla",
    "  - @KieranYui",
    "  - @rianmmuahamad",
    "  - @Feng Liuz",
    "  - @frrllxs",
]

VERSION = "1.0.0"

HELP_TEXTS = {
    'id': {
        'desc': (
            "Cek username di berbagai sosial media & situs viral (termasuk Indonesia).\n"
            "Contoh penggunaan:\n  python3 uh.py johndoe\n  python3 uh.py johndoe janedoe --only-found\n  python3 uh.py --username-file daftar.txt --output hasil.json\n"
        ),
        'epilog': '''\
Contoh penggunaan:
  python3 uh.py johndoe
  python3 uh.py johndoe janedoe --only-found
  python3 uh.py --username-file daftar.txt --output hasil.json
  python3 uh.py --config config.json --progress --logfile hasil.log
  python3 uh.py --chart
  python3 uh.py --wizard
  python3 uh.py --faq
  python3 uh.py --tips

Tips:
- Gunakan --wizard untuk mode tanya-jawab interaktif.
- Gunakan --logfile dan --loglevel untuk logging otomatis.
- Gunakan --chart untuk summary visual hasil.
- Gunakan --faq dan --tips untuk bantuan dan troubleshooting.

FAQ:
Q: Bagaimana export ke Excel?
A: Gunakan --output hasil.xlsx (fitur akan segera hadir, sementara gunakan .csv).
Q: Bagaimana menambah platform baru?
A: Tambahkan di custom JSON atau folder plugins.
Q: Bagaimana agar hasil hanya ke file, tidak ke layar?
A: Gunakan --silent --logfile hasil.log
Q: Bagaimana monitoring otomatis?
A: Jalankan dengan cron/scheduler dan gunakan --logfile.
''',
        'args': {
            'author': 'Tampilkan informasi author dan kontributor',
            'version': 'Tampilkan versi UsernameHunter',
            'list_platforms': 'Tampilkan semua platform yang didukung',
            'example': 'Tampilkan contoh penggunaan CLI',
            'config': 'File konfigurasi YAML/JSON',
            'username': 'Username yang ingin dicek (bisa lebih dari satu, pisahkan spasi)',
            'username_file': 'File berisi daftar username (satu baris satu username)',
            'output': 'Simpan hasil ke file (format: .json/.txt/.csv/.xlsx)',
            'timeout': 'Timeout per request (detik)',
            'max_workers': 'Jumlah thread paralel',
            'progress': 'Tampilkan progress bar (rich)',
            'proxy_file': 'File daftar proxy (satu baris satu proxy)',
            'custom_platforms': 'File JSON custom platform',
            'plugin_dir': 'Folder plugin platform',
            'silent': 'Nonaktifkan semua output ke layar',
            'logfile': 'Simpan semua output ke file log',
            'history': 'Tampilkan riwayat pencarian username terakhir',
            'stats': 'Tampilkan ringkasan statistik hasil pencarian',
            'faq': 'Tampilkan FAQ dan troubleshooting',
            'tips': 'Tampilkan tips penggunaan',
            'loglevel': 'Level logging detail',
            'wizard': 'Mode interaktif tanya-jawab',
            'chart': 'Tampilkan summary visual (pie/bar chart)',
            'lang': 'Pilih bahasa CLI/output',
            'only_found': 'Hanya tampilkan yang ditemukan',
            'only_not_found': 'Hanya tampilkan yang tidak ditemukan',
            'show_failed': 'Tampilkan juga platform yang gagal diakses/time out',
        }
    },
    'en': {
        'desc': (
            "Check username availability on various social media & viral sites, including Indonesian platforms.\n"
            "Example usage:\n  python3 uh.py johndoe\n  python3 uh.py johndoe janedoe --only-found\n  python3 uh.py --username-file daftar.txt --output hasil.json\n"
        ),
        'epilog': '''\
Example usage:
  python3 uh.py johndoe
  python3 uh.py johndoe janedoe --only-found
  python3 uh.py --username-file daftar.txt --output hasil.json
  python3 uh.py --config config.json --progress --logfile hasil.log
  python3 uh.py --chart
  python3 uh.py --wizard
  python3 uh.py --faq
  python3 uh.py --tips

Tips:
- Use --wizard for interactive Q&A mode.
- Use --logfile and --loglevel for automatic logging.
- Use --chart for visual summary.
- Use --faq and --tips for help and troubleshooting.

FAQ:
Q: How to export to Excel?
A: Use --output hasil.xlsx (feature coming soon, use .csv for now).
Q: How to add a new platform?
A: Add in custom JSON or plugins folder.
Q: How to output only to file, not to screen?
A: Use --silent --logfile hasil.log
Q: How to automate monitoring?
A: Run with cron/scheduler and use --logfile.
''',
        'args': {
            'author': 'Show author and contributor info',
            'version': 'Show tool version',
            'list_platforms': 'List all supported platforms',
            'example': 'Show CLI usage examples',
            'config': 'YAML/JSON config file',
            'username': 'Usernames to check, can be more than one, separated by space',
            'username_file': 'File containing list of usernames, one per line',
            'output': 'Save results to file: .json/.txt/.csv/.xlsx',
            'timeout': 'Timeout per request in seconds',
            'max_workers': 'Number of parallel threads',
            'progress': 'Show progress bar',
            'proxy_file': 'Proxy list file, one per line',
            'custom_platforms': 'Custom platform JSON file',
            'plugin_dir': 'Plugin platform folder',
            'silent': 'Disable all console output',
            'logfile': 'Save all output to log file',
            'history': 'Show username search history',
            'stats': 'Show search statistics summary',
            'faq': 'Show FAQ and troubleshooting',
            'tips': 'Show usage tips',
            'loglevel': 'Logging level',
            'wizard': 'Interactive CLI wizard',
            'chart': 'Show summary visual (pie/bar chart)',
            'lang': 'Choose CLI/output language',
            'only_found': 'Show only found usernames',
            'only_not_found': 'Show only not found usernames',
            'show_failed': 'Show also failed/time out platforms',
        }
    }
}

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    pass

def print_authors():
    print("\033[1;36m" + "\n".join(AUTHORS) + "\033[0m\n")

def print_version():
    print(f"UsernameHunter v{VERSION}")

EXAMPLES = """
Contoh penggunaan / Example usage:
  python3 uh.py johndoe
  python3 uh.py johndoe janedoe --only-found
  python3 uh.py --username-file daftar.txt --output hasil.json
  python3 uh.py --list-platforms
  python3 uh.py --config config.yaml
"""

def print_examples():
    print(EXAMPLES)

def print_platforms(platforms):
    print("\nDaftar platform yang didukung / Supported platforms:")
    for p in sorted(platforms.keys()):
        print(f"- {p}")
    print(f"\nTotal: {len(platforms)} platform.")

def load_config(config_file):
    import sys
    default_config = {
        "usernames": ["johndoe", "janedoe"],
        "output": "hasil.json",
        "progress": True,
        "only_found": False
    }
    if not config_file:
        return {}
    config_path = Path(config_file)
    if not config_path.is_file():
        # Buat file config default jika belum ada
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        print(f"[yellow]File konfigurasi '{config_file}' tidak ditemukan. File default telah dibuat![/yellow]")
        print(f"Silakan edit file '{config_file}' sesuai kebutuhan, lalu jalankan ulang perintah Anda.")
        sys.exit(0)
    if config_file.endswith('.json'):
        with open(config_file) as f:
            return json.load(f)
    elif config_file.endswith(('.yaml', '.yml')) and yaml:
        with open(config_file) as f:
            return yaml.safe_load(f)
    else:
        print("[red]Config file must be .json or .yaml/.yml[/red]")
        sys.exit(1)

def print_welcome(lang='id'):
    # Contoh penggunaan multi-bahasa pada output
    if lang == 'en':
        WELCOME = "Welcome to UsernameHunter! Check username availability on hundreds of global & Indonesian platforms. Use --help to see all CLI options."
        TIPS = "Tip: Try --list-platforms to see all supported platforms!"
    else:
        WELCOME = "Selamat datang di UsernameHunter! Cek ketersediaan username di ratusan platform global & Indonesia. Gunakan --help untuk melihat semua opsi CLI."
        TIPS = "Tips: Coba perintah --list-platforms untuk melihat semua platform yang didukung!"
    print("\033[1;32m==============================\033[0m")
    print(f"\033[1;36m{WELCOME}\033[0m")
    print("\033[1;32m==============================\033[0m")
    print(TIPS)
    print()

def print_feature_suggestions():
    print("\n\033[1;35mSaran fitur lanjutan yang bisa Anda tambahkan:\033[0m")
    print("- Export ke Excel (.xlsx) atau Google Sheets")
    print("- Notifikasi Telegram/Discord/email jika username tersedia")
    print("- Monitoring username secara berkala (scheduler)")
    print("- Integrasi headless browser (Selenium/Playwright) untuk bypass captcha")
    print("- Integrasi database (SQLite/MySQL/PostgreSQL)")
    print("- Auto-update daftar platform dari repo/URL")
    print("- Output warna lebih kaya (pakai rich/colorama)")
    print("- Mode silent/log only untuk automation")
    print("- Fitur validasi username per platform lebih detail")
    print("- Proxy pool & auto-rotate proxy dari API")
    print("- Plugin system: support plugin eksternal (pip installable)")
    print()

def main(lang, desc, epilog, args_help):
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=CustomFormatter,
        epilog=epilog
    )
    # args_help sudah diterima sebagai argumen
    parser.add_argument('--author', action='store_true', help=args_help['author'])
    parser.add_argument('--version', action='store_true', help=args_help['version'])
    parser.add_argument('--list-platforms', action='store_true', help=args_help['list_platforms'])
    parser.add_argument('--example', action='store_true', help=args_help['example'])
    parser.add_argument('--config', help=args_help['config'])
    parser.add_argument('username', nargs='*', help=args_help['username'])
    parser.add_argument('--username-file', help=args_help['username_file'])
    parser.add_argument('--output', '-o', help=args_help['output'])
    parser.add_argument('--timeout', type=int, default=5, help=args_help['timeout'])
    parser.add_argument('--max-workers', type=int, default=20, help=args_help['max_workers'])
    parser.add_argument('--progress', action='store_true', help=args_help['progress'])
    parser.add_argument('--proxy-file', help=args_help['proxy_file'])
    parser.add_argument('--custom-platforms', help=args_help['custom_platforms'])
    parser.add_argument('--plugin-dir', help=args_help['plugin_dir'])
    parser.add_argument('--silent', action='store_true', help=args_help['silent'])
    parser.add_argument('--logfile', help=args_help['logfile'])
    parser.add_argument('--history', action='store_true', help=args_help['history'])
    parser.add_argument('--stats', action='store_true', help=args_help['stats'])
    parser.add_argument('--faq', action='store_true', help=args_help['faq'])
    parser.add_argument('--tips', action='store_true', help=args_help['tips'])
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error'], help=args_help['loglevel'])
    parser.add_argument('--wizard', action='store_true', help=args_help['wizard'])
    parser.add_argument('--chart', action='store_true', help=args_help['chart'])
    parser.add_argument('--lang', default=lang, choices=['id', 'en'], help=args_help['lang'])
    parser.add_argument('--gui', action='store_true', help='Jalankan GUI (Streamlit atau Tkinter)')
    filter_group = parser.add_mutually_exclusive_group()
    filter_group.add_argument('--only-found', action='store_true', help=args_help['only_found'])
    filter_group.add_argument('--only-not-found', action='store_true', help=args_help['only_not_found'])
    filter_group.add_argument('--show-failed', action='store_true', help=args_help['show_failed'])
    args = parser.parse_args()
    lang = args.lang

    # Jalankan GUI jika diminta
    if getattr(args, 'gui', False):
        try:
            import streamlit
            import subprocess
            subprocess.run(["streamlit", "run", "gui/streamlit_app.py"])
        except ImportError:
            try:
                import tkinter
                import sys
                import os
                os.system(f"python3 gui/tkinter_app.py")
            except ImportError:
                print("[red]streamlit dan tkinter tidak tersedia. Install salah satu untuk GUI.[/red]")
        return

    # Jalankan fitur yang tidak butuh username lebih dulu
    if args.history:
        print_history()
        return
    if args.stats and not (args.username or args.username_file or (config.get('usernames') or config.get('username_file'))):
        # Tampilkan statistik dari riwayat terakhir
        path = Path('history.jsonl')
        if not path.exists():
            print('[yellow]Belum ada riwayat pencarian.[/yellow]')
            return
        with open('history.jsonl', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                print('[yellow]Belum ada riwayat pencarian.[/yellow]')
                return
            entry = json.loads(lines[-1])
            stats = get_stats_from_results(entry.get('results', {}))
            print_stats_summary(stats, silent=args.silent, logfile=args.logfile)
        return

    # Load config if provided
    config = load_config(args.config) if args.config else {}

    # Merge config with CLI args (CLI args take precedence)
    usernames = args.username or config.get('usernames', [])
    if args.username_file or config.get('username_file'):
        username_file = args.username_file or config.get('username_file')
        with open(username_file) as f:
            usernames += [u.strip() for u in f if u.strip()]

    # Load platforms
    platforms = SOCIAL_PLATFORMS.copy()
    if args.custom_platforms or config.get('custom_platforms'):
        platforms.update(load_custom_platforms(args.custom_platforms or config.get('custom_platforms')))
    if args.plugin_dir or config.get('plugin_dir'):
        platforms.update(load_plugin_platforms(args.plugin_dir or config.get('plugin_dir')))

    if args.list_platforms:
        print_platforms(platforms)
        print_feature_suggestions()
        return

    if not usernames:
        parser.error('the following arguments are required: username')

    proxies = get_proxy_list(args.proxy_file or config.get('proxy_file'))
    all_results = {}
    for username in tqdm(usernames, desc='Username', disable=not (args.progress or config.get('progress', False))):
        valid, reason = is_valid_username(username)
        if not valid:
            print(f"[WARNING] Username '{username}' tidak valid: {reason}")
            continue
        results = check_username(
            username,
            max_workers=args.max_workers if args.max_workers else config.get('max_workers', 20),
            timeout=args.timeout if args.timeout else config.get('timeout', 5),
            progress=args.progress if 'progress' in args else config.get('progress', False),
            proxies=proxies,
            platforms=platforms
        )
        filtered = filter_results(
            results,
            only_found=args.only_found or config.get('only_found', False),
            only_not_found=args.only_not_found or config.get('only_not_found', False),
            only_failed=args.show_failed or config.get('show_failed', False)
        )
        print(f"\nHasil pencarian untuk username: {username}\n")
        output_lines = []
        for platform, info in filtered.items():
            valid, reason = is_valid_username(username, platform)
            if not valid:
                message = f"[WARNING] Username tidak valid untuk {platform}: {reason}"
                status = 'Tidak Valid'
            elif info['exists'] is True:
                status = 'Terdaftar'
                message = f"Username ditemukan di {platform}"
            elif info['exists'] is False:
                status = 'Tidak Terdaftar'
                message = f"Username tidak ditemukan di {platform}"
            else:
                status = 'Tidak Diketahui'
                if 'error' in info:
                    message = f"Gagal cek {platform}: {info['error']}"
                elif 'status' in info:
                    message = f"Status HTTP: {info['status']}"
                else:
                    message = f"Tidak dapat menentukan status di {platform}"
            line = f"[{platform}] {status}\n  URL: {info['url']}\n  {message}\n"
            print(line)
            # Copy-to-clipboard and open-link buttons (CLI)
            if pyperclip:
                print(f"  [C] Copy URL to clipboard")
            print(f"  [O] Open URL in browser")
            user_action = input("  Action (C/O/Enter=skip): ").strip().lower()
            if user_action == 'c' and pyperclip:
                pyperclip.copy(info['url'])
                print("    [Copied to clipboard]")
            elif user_action == 'o':
                webbrowser.open(info['url'])
                print("    [Opened in browser]")
            output_lines.append({
                'platform': platform,
                'status': status,
                'url': info['url'],
                'message': message
            })
        all_results[username] = output_lines
        # Simpan riwayat
        save_history(filtered)
        # Tampilkan statistik jika diminta
        if args.stats:
            stats = get_stats_from_results(filtered)
            print_stats_summary(stats, silent=args.silent, logfile=args.logfile)
    # Export hasil jika diminta
    if args.output or config.get('output'):
        export_results(all_results, args.output or config.get('output'))

    import logging
    logging.basicConfig(
        level=getattr(logging, args.loglevel.upper(), logging.INFO),
        format='[%(levelname)s] %(message)s'
    )
    if args.faq:
        print("\n[bold cyan]FAQ & Troubleshooting:[/bold cyan]\n")
        print("- Bagaimana export ke Excel? Gunakan --output hasil.xlsx (fitur segera hadir, sementara gunakan .csv)")
        print("- Bagaimana menambah platform baru? Tambahkan di custom JSON atau folder plugins.")
        print("- Bagaimana agar hasil hanya ke file, tidak ke layar? Gunakan --silent --logfile hasil.log")
        print("- Bagaimana monitoring otomatis? Jalankan dengan cron/scheduler dan gunakan --logfile.")
        return
    if args.tips:
        print("\n[bold green]Tips Penggunaan UsernameHunter:[/bold green]\n")
        print("- Gunakan --progress untuk progress bar modern.")
        print("- Gunakan --plugin-dir untuk menambah platform custom.")
        print("- Gunakan --chart untuk summary visual.")
        print("- Gunakan --wizard untuk mode interaktif.")
        return
    if args.wizard:
        print("[bold magenta]Mode Wizard Interaktif belum diimplementasikan penuh. Akan hadir di update berikutnya![/bold magenta]")
        # TODO: Implementasi wizard interaktif
        return
    if args.chart:
        try:
            import matplotlib.pyplot as plt
            import warnings
        except ImportError:
            print("[red]matplotlib belum terinstall. Jalankan: pip install matplotlib[/red]")
            return
        # Ambil statistik dari riwayat terakhir
        path = Path('history.jsonl')
        if not path.exists():
            print('[yellow]Belum ada riwayat pencarian untuk chart.[/yellow]')
            return
        with open('history.jsonl', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                print('[yellow]Belum ada riwayat pencarian untuk chart.[/yellow]')
                return
            entry = json.loads(lines[-1])
            stats = get_stats_from_results(entry.get('results', {}))
        labels = ['Terdaftar', 'Tidak Terdaftar', 'Error']
        values = [stats['found'], stats['not_found'], stats['error']]
        colors = ['#4caf50', '#ffeb3b', '#f44336']
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Ringkasan Hasil Pencarian Username')
        plt.axis('equal')
        out_path = 'hasil_chart.png'
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
                plt.show()
        except Exception as e:
            print(f"[yellow]Chart tidak bisa ditampilkan interaktif. Chart disimpan ke: {out_path}[/yellow]")
            print(f"[INFO] Error: {e}")
        finally:
            plt.savefig(out_path)
            print(f"[green]Chart juga disimpan ke: {out_path}[/green]")
        return

if __name__ == '__main__':
    import sys
    lang = 'id'
    if '--lang' in sys.argv:
        try:
            idx = sys.argv.index('--lang')
            if idx + 1 < len(sys.argv):
                lang_candidate = sys.argv[idx + 1].lower()
                if lang_candidate in HELP_TEXTS:
                    lang = lang_candidate
        except Exception:
            lang = 'id'

    desc = HELP_TEXTS[lang]['desc']
    epilog = HELP_TEXTS[lang]['epilog']
    args_help = HELP_TEXTS[lang]['args']

    main(lang, desc, epilog, args_help)
