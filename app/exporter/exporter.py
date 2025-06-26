# ...existing code from exporter.py...
def export_results(all_results, output_path):
    import json, csv, os
    from pathlib import Path
    ext = os.path.splitext(output_path)[1].lower()
    if ext == '.json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\nHasil disimpan ke {output_path}")
    elif ext == '.csv':
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username','platform','status','url','message'])
            for username, lines in all_results.items():
                for item in lines:
                    writer.writerow([username, item['platform'], item['status'], item['url'], item['message']])
        print(f"\nHasil disimpan ke {output_path}")
    elif ext == '.txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            for username, lines in all_results.items():
                f.write(f"Hasil untuk {username}:\n")
                for item in lines:
                    f.write(f"[{item['platform']}] {item['status']}\n  URL: {item['url']}\n  {item['message']}\n\n")
        print(f"\nHasil disimpan ke {output_path}")
    elif ext == '.md':
        with open(output_path, 'w', encoding='utf-8') as f:
            for username, entries in all_results.items():
                f.write(f'# Hasil Pencarian Username: {username}\n\n')
                for entry in entries:
                    f.write(f"- **{entry['platform']}**: {entry['status']}  \n  URL: {entry['url']}  \n  {entry['message']}\n")
                f.write('\n')
        print(f"\nHasil disimpan ke {output_path}")
    elif ext == '.html':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('<html><head><meta charset="utf-8"><title>Hasil UsernameHunter</title></head><body>')
            for username, entries in all_results.items():
                f.write(f'<h2>Hasil Pencarian Username: {username}</h2><ul>')
                for entry in entries:
                    f.write(f'<li><b>{entry["platform"]}</b>: {entry["status"]}<br>URL: <a href="{entry["url"]}">{entry["url"]}</a><br>{entry["message"]}</li>')
                f.write('</ul>')
            f.write('</body></html>')
        print(f"\nHasil disimpan ke {output_path}")
    elif ext == '.pdf':
        try:
            from fpdf import FPDF
        except ImportError:
            print('[red]Library fpdf belum terinstall. Jalankan: pip install fpdf[/red]')
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        for username, entries in all_results.items():
            pdf.cell(0, 10, f'Hasil Pencarian Username: {username}', ln=1)
            pdf.set_font('Arial', '', 12)
            for entry in entries:
                pdf.multi_cell(0, 8, f"{entry['platform']}: {entry['status']}\nURL: {entry['url']}\n{entry['message']}\n")
            pdf.ln(4)
        pdf.output(output_path)
        print(f"\nHasil disimpan ke {output_path}")
    else:
        print(f'[yellow]Format file {ext} belum didukung.[/yellow]')
