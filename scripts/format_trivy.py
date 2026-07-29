#!/usr/bin/env python3
import json
import sys
import re
import os

def parse_trivy_json(json_path):
    if not os.path.exists(json_path):
        return None
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        return None

def format_report(data):
    if not data:
        return "### 🛡️ Trivy Güvenlik Taraması Raporu\n\n*Tarama sonucu bulunamadı veya okunamadı.*"

    artifact_name = data.get("ArtifactName", "Docker Image")
    results = data.get("Results", [])

    os_summary = []
    python_pkgs_count = 0
    python_vuln_count = 0
    vulnerability_list = []

    for result in results:
        target = result.get("Target", "")
        result_type = result.get("Type", "")
        vulnerabilities = result.get("Vulnerabilities", []) or []

        vuln_count = len(vulnerabilities)

        if result_type in ["alpine", "debian", "ubuntu", "centos", "amazon"]:
            os_match = re.search(r'\(([^)]+)\)', target)
            os_name = os_match.group(1) if os_match else target
            os_summary.append({
                "name": f"🐧 OS ({os_name})",
                "type": result_type,
                "count": vuln_count
            })
        elif result_type == "python-pkg" or "site-packages" in target:
            python_pkgs_count += 1
            python_vuln_count += vuln_count

        for vuln in vulnerabilities:
            pkg_name = vuln.get("PkgName", "")
            installed_ver = vuln.get("InstalledVersion", "")
            fixed_ver = vuln.get("FixedVersion", "N/A")
            severity = vuln.get("Severity", "UNKNOWN")
            vuln_id = vuln.get("VulnerabilityID", "")

            vulnerability_list.append({
                "pkg": pkg_name,
                "installed": installed_ver,
                "fixed": fixed_ver,
                "severity": severity,
                "id": vuln_id
            })

    lines = []
    lines.append("### 🛡️ Trivy Güvenlik Taraması Raporu")
    lines.append(f"**İmaj:** `{artifact_name}`\n")
    lines.append("#### 📊 Özet")
    lines.append("| Hedef / Kategori | Tür | Zafiyet Sayısı | Durum |")
    lines.append("|---|---|:---:|:---:|")

    for os_item in os_summary:
        status = "✅ Temiz" if os_item["count"] == 0 else f"⚠️ {os_item['count']} Zafiyet"
        lines.append(f"| {os_item['name']} | `{os_item['type']}` | {os_item['count']} | {status} |")

    if python_pkgs_count > 0:
        py_status = "✅ Temiz" if python_vuln_count == 0 else f"⚠️ {python_vuln_count} Zafiyet"
        lines.append(f"| 🐍 Python Paketleri ({python_pkgs_count} paket taranmıştır) | `python-pkg` | {python_vuln_count} | {py_status} |")

    lines.append("\n#### ⚠️ Zafiyet Detayları")
    if not vulnerability_list:
        lines.append("*Yüksek (HIGH) veya Kritik (CRITICAL) seviyesinde güvenlik açığı bulunamadı. ✅*\n")
    else:
        lines.append("| Paket | Yüklü Sürüm | Çözüm Sürümü | Seviye | Zafiyet ID |")
        lines.append("|---|---|---|:---:|---|")
        for v in vulnerability_list:
            sev_badge = f"🔴 **{v['severity']}**" if v['severity'] in ["CRITICAL", "HIGH"] else f"🟡 {v['severity']}"
            lines.append(f"| `{v['pkg']}` | `{v['installed']}` | `{v['fixed']}` | {sev_badge} | `{v['id']}` |")

    return "\n".join(lines)

def main():
    json_file = sys.argv[1] if len(sys.argv) > 1 else "trivy-results.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "trivy-comment.md"

    data = parse_trivy_json(json_file)
    markdown_content = format_report(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    main()
