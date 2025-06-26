from proxy.proxy import get_requests_proxy
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn, TaskProgressColumn
import json
import datetime
from pathlib import Path

console = Console()

def check_single_platform(platform, url_pattern, username, timeout=5, proxies=None, max_retries=3):
    import socket
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
        ])
    }
    url = url_pattern.format(username=username)
    for attempt in range(max_retries):
        try:
            host = url.split('/')[2]
            socket.gethostbyname(host)
            time.sleep(random.uniform(0.2, 0.7))
            proxy = None
            if proxies:
                proxy = get_requests_proxy(random.choice(proxies))
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, proxies=proxy)
            if resp.status_code == 200:
                if any(x in resp.text.lower() for x in ['not found', '404', 'does not exist', 'page not found', 'user not found', 'profile not found']):
                    return platform, {'exists': False, 'url': url, 'status': resp.status_code, 'note': 'Konten error'}
                return platform, {'exists': True, 'url': url}
            elif resp.status_code == 404:
                return platform, {'exists': False, 'url': url}
            elif resp.status_code in (403, 400, 410, 429, 999):
                if any(x in resp.text.lower() for x in ['not found', '404', 'does not exist', 'page not found', 'user not found', 'profile not found']):
                    return platform, {'exists': False, 'url': url, 'status': resp.status_code, 'note': 'Konten error'}
                if 'login' in resp.text.lower() or 'masuk' in resp.text.lower():
                    return platform, {'exists': None, 'url': url, 'status': resp.status_code, 'note': 'Redirect/login/captcha'}
                if proxies and attempt < max_retries-1:
                    continue
                return platform, {'exists': None, 'url': url, 'status': resp.status_code, 'note': 'Cek manual, kemungkinan rate limit/captcha/protected'}
            else:
                return platform, {'exists': None, 'url': url, 'status': resp.status_code}
        except socket.gaierror:
            return platform, {'exists': None, 'url': url, 'error': 'DNS resolution failed'}
        except requests.exceptions.TooManyRedirects:
            return platform, {'exists': None, 'url': url, 'error': 'Terlalu banyak redirect'}
        except requests.exceptions.RequestException as e:
            if proxies and attempt < max_retries-1:
                continue
            return platform, {'exists': None, 'url': url, 'error': str(e)}
    return platform, {'exists': None, 'url': url, 'error': 'All proxy attempts failed'}

def check_username(username, max_workers=20, timeout=5, platforms=None, progress=False, proxies=None, silent=False, progress_obj=None):
    results = {}
    total = len(platforms)
    done = 0
    if progress_obj:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_platform = {
                executor.submit(check_single_platform, platform, url_pattern, username, timeout, proxies): platform
                for platform, url_pattern in platforms.items()
            }
            for future in as_completed(future_to_platform):
                platform, result = future.result()
                results[platform] = result
                progress_obj.advance(1)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_platform = {
                executor.submit(check_single_platform, platform, url_pattern, username, timeout, proxies): platform
                for platform, url_pattern in platforms.items()
            }
            for future in as_completed(future_to_platform):
                platform, result = future.result()
                results[platform] = result
                done += 1
                if progress and not silent:
                    print(f"\rProgress: {done}/{total} sites", end="", flush=True)
    if progress and not silent and not progress_obj:
        print()
    return results

def filter_results(results, only_found=False, only_not_found=False, only_failed=False):
    filtered = {}
    for platform, info in results.items():
        if only_found and info['exists'] is True:
            filtered[platform] = info
        elif only_not_found and info['exists'] is False:
            filtered[platform] = info
        elif only_failed and info['exists'] is None:
            filtered[platform] = info
        elif not (only_found or only_not_found or only_failed):
            filtered[platform] = info
    return filtered

def check_username_multi(usernames, progress=False, **kwargs):
    all_results = {}
    if progress and not kwargs.get('silent', False):
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress_bar:
            username_tasks = {}
            for username in usernames:
                username_tasks[username] = progress_bar.add_task(f"[white]Cek [cyan]{username}", total=len(kwargs['platforms']))
            for username in usernames:
                def progress_obj():
                    return progress_bar
                all_results[username] = check_username(
                    username,
                    progress=True,
                    progress_obj=progress_bar,
                    **kwargs,
                )
                progress_bar.update(username_tasks[username], completed=len(kwargs['platforms']))
    else:
        for username in usernames:
            all_results[username] = check_username(username, **kwargs)
    return all_results

def print_result_colored(platform, info, username, console=console, silent=False, logfile=None):
    status = info.get('exists')
    url = info.get('url')
    msg = info.get('error') or info.get('note') or info.get('status') or 'Tidak diketahui'
    output = ""
    if status is True:
        output = f"[bold green][{platform}] TERDAFTAR[/bold green] [cyan]{url}[/cyan]"
    elif status is False:
        output = f"[bold yellow][{platform}] TIDAK TERDAFTAR[/bold yellow] [cyan]{url}[/cyan]"
    elif status is None:
        output = f"[bold red][{platform}] ERROR[/bold red] [cyan]{url}[/cyan] [red]{msg}[/red]"
    else:
        output = f"[{platform}] [cyan]{url}[/cyan]"
    if not silent and not logfile:
        console.print(output, highlight=False)
    if logfile:
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(f"{platform}\t{status}\t{url}\t{msg}\n")


def print_stats_summary(stats, console=console, silent=False, logfile=None):
    lines = [
        "\n[bold]Ringkasan Statistik:[/bold]",
        f"[green]Tersedia/Registered:[/green] {stats['found']}",
        f"[yellow]Tidak Terdaftar:[/yellow] {stats['not_found']}",
        f"[red]Error/Unknown:[/red] {stats['error']}",
        f"[white]Total Dicek:[/white] {stats['total']}"
    ]
    if not silent and not logfile:
        for line in lines:
            console.print(line)
    if logfile:
        with open(logfile, 'a', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')


def save_history(results, history_path='history.jsonl'):
    """Simpan hasil pencarian ke file riwayat (JSONL, satu baris per pencarian)"""
    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'results': results
    }
    with open(history_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def print_history(history_path='history.jsonl', limit=10, console=console):
    """Tampilkan riwayat pencarian terakhir (default 10)"""
    path = Path(history_path)
    if not path.exists():
        console.print('[yellow]Belum ada riwayat pencarian.[/yellow]')
        return
    with open(history_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[-limit:]
        for i, line in enumerate(lines, 1):
            entry = json.loads(line)
            ts = entry.get('timestamp', '-')
            res = entry.get('results', {})
            console.print(f"[bold]{i}. {ts}[/bold]")
            stats = get_stats_from_results(res)
            print_stats_summary(stats, console=console)

def get_stats_from_results(results):
    """
    Ambil statistik dari hasil pencarian username (bisa dict hasil check_username atau check_username_multi)
    """
    stats = {'found': 0, 'not_found': 0, 'error': 0, 'total': 0}
    if not results:
        return stats
    if isinstance(next(iter(results.values())), dict):
        sample = next(iter(results.values()))
        if isinstance(next(iter(sample.values())), dict):
            for username, platforms in results.items():
                for info in platforms.values():
                    stats['total'] += 1
                    if info.get('exists') is True:
                        stats['found'] += 1
                    elif info.get('exists') is False:
                        stats['not_found'] += 1
                    else:
                        stats['error'] += 1
        else:
            for info in results.values():
                stats['total'] += 1
                if info.get('exists') is True:
                    stats['found'] += 1
                elif info.get('exists') is False:
                    stats['not_found'] += 1
                else:
                    stats['error'] += 1
    return stats
