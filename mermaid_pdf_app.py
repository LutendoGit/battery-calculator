from __future__ import annotations

import os
import tempfile
from io import BytesIO
from pathlib import Path

from flask import Flask, flash, render_template, request, send_file

from scripts.generate_system_pdf import build_pdf, parse_mermaid


standalone_app = Flask(__name__)
standalone_app.config["SECRET_KEY"] = os.environ.get("MERMAID_PDF_SECRET_KEY", "dev")


def _safe_pdf_download_name(raw_name: str | None) -> str:
    name = (raw_name or "mermaid_diagram").strip()
    name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in name)
    name = name.strip("._") or "mermaid_diagram"
    return f"{name}.pdf"


@standalone_app.route("/", methods=["GET", "POST"])
def mermaid_home():
    if request.method == "POST":
        mermaid_text = (request.form.get("mermaid_text") or "").strip()
        title = (request.form.get("title") or "Mermaid Diagram").strip()
        output_name_raw = request.form.get("output_name") or "mermaid_diagram"
        output_name = _safe_pdf_download_name(output_name_raw)

        if not mermaid_text:
            flash("Please paste Mermaid graph text before generating the PDF.", "danger")
            return render_template(
                "mermaid_pdf_standalone.html",
                mermaid_text=mermaid_text,
                title=title,
                output_name=output_name_raw,
            )

        tmp_path = ""
        try:
            diagram = parse_mermaid(mermaid_text)
            tmp = tempfile.NamedTemporaryFile(prefix="mermaid_pdf_", suffix=".pdf", delete=False)
            tmp_path = tmp.name
            tmp.close()

            pdf_path = build_pdf(diagram, Path(tmp_path), title)
            with open(pdf_path, "rb") as handle:
                pdf_bytes = handle.read()
        except Exception as exc:
            flash(f"Unable to generate Mermaid PDF: {exc}", "danger")
            return render_template(
                "mermaid_pdf_standalone.html",
                mermaid_text=mermaid_text,
                title=title,
                output_name=output_name_raw,
            )
        finally:
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass

        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=output_name,
        )

    return render_template(
        "mermaid_pdf_standalone.html",
        mermaid_text="",
        title="Mermaid Diagram",
        output_name="mermaid_diagram",
    )


if __name__ == "__main__":
    host = os.environ.get("MERMAID_PDF_HOST", "127.0.0.1")
    port = int(os.environ.get("MERMAID_PDF_PORT", "5001"))
    debug = os.environ.get("MERMAID_PDF_DEBUG", "1") == "1"
    standalone_app.run(host=host, port=port, debug=debug)